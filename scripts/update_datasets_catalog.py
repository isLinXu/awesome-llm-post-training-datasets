#!/usr/bin/env python3
"""Refresh dataset metadata, classify discoveries, and render catalog views.

The curated datasets-list.yaml remains canonical. Discovered repositories are
always quarantined as pending_review and are never promoted to training assets.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate_datasets_list import validate  # noqa: E402

CATALOG = ROOT / "datasets-list.yaml"
CONFIG = ROOT / "config" / "dataset-taxonomy.yaml"
STATE = ROOT / "data" / "dataset-catalog-state.json"
CANDIDATES = ROOT / "datasets-candidates.yaml"
CATALOG_MD = ROOT / "datasets-catalog.md"
REPORT_MD = ROOT / "datasets-update-report.md"
HF_API = "https://huggingface.co"
TRACKED_FIELDS = ("last_modified", "sha", "license", "gated", "downloads", "likes")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_if_changed(path: Path, text: str, dry_run: bool = False) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return True


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def request_json(url: str, config: dict[str, Any]) -> Any:
    automation = config["automation"]
    timeout = float(automation.get("request_timeout_seconds", 20))
    retries = int(automation.get("max_retries", 3))
    headers = {"Accept": "application/json", "User-Agent": "base-llm-dataset-catalog/1.0"}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['HF_TOKEN']}"
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urlopen(Request(url, headers=headers), timeout=timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            last_error = exc
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt + 1 >= retries:
                break
            retry_after = exc.headers.get("Retry-After")
            try:
                delay = min(float(retry_after), 60.0) if retry_after else 2.0 ** attempt
            except ValueError:
                delay = 2.0 ** attempt
            time.sleep(delay)
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(2.0 ** attempt)
    raise RuntimeError(f"请求失败 {url}: {last_error}")


def license_from(payload: dict[str, Any]) -> Any:
    card = payload.get("cardData") if isinstance(payload.get("cardData"), dict) else {}
    value = card.get("license")
    if value is not None:
        return value
    licenses = [tag.split(":", 1)[1] for tag in payload.get("tags", []) if tag.startswith("license:")]
    return licenses[0] if len(licenses) == 1 else licenses or None


def normalize_hf(payload: dict[str, Any], repo_id: str | None = None) -> dict[str, Any]:
    card = payload.get("cardData") if isinstance(payload.get("cardData"), dict) else {}
    card_keys = (
        "language", "license", "task_categories", "size_categories", "pretty_name",
        "annotations_creators", "language_creators", "source_datasets",
    )
    return {
        "repo_id": repo_id or payload.get("id"),
        "url": f"https://huggingface.co/datasets/{repo_id or payload.get('id')}",
        "last_modified": payload.get("lastModified"),
        "sha": payload.get("sha"),
        "downloads": payload.get("downloads"),
        "likes": payload.get("likes"),
        "gated": payload.get("gated"),
        "private": payload.get("private", False),
        "disabled": payload.get("disabled", False),
        "license": license_from(payload),
        "tags": sorted(payload.get("tags") or []),
        "siblings_count": len(payload.get("siblings") or []),
        "card_data": {key: card[key] for key in card_keys if key in card},
    }


def metadata_changes(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    if not previous:
        return {}
    return {
        field: {"old": previous.get(field), "new": current.get(field)}
        for field in TRACKED_FIELDS
        if previous.get(field) != current.get(field)
    }


def merge_metadata(
    record: dict[str, Any] | None,
    current: dict[str, Any],
    dataset_ids: list[str],
    observed_at: str,
    history_keep: int = 30,
) -> tuple[dict[str, Any], dict[str, Any]]:
    record = dict(record or {})
    previous = record.get("current")
    changes = metadata_changes(previous, current)
    history = list(record.get("history") or [])
    if previous and changes:
        history.append({"observed_at": observed_at, "changes": changes, "previous": previous})
    record.update({
        "repo_id": current["repo_id"],
        "dataset_ids": sorted(set(record.get("dataset_ids", [])) | set(dataset_ids)),
        "first_seen_at": record.get("first_seen_at", observed_at),
        "last_checked_at": observed_at,
        "last_success_at": observed_at,
        "status": "ok",
        "error": None,
        "current": current,
        "history": history[-history_keep:],
    })
    return record, changes


def discovery_text(payload: dict[str, Any]) -> tuple[str, str]:
    card = payload.get("cardData") if isinstance(payload.get("cardData"), dict) else {}
    title = " ".join(str(x) for x in (payload.get("id"), card.get("pretty_name")) if x)
    body_parts = [
        str(payload.get("description") or ""),
        str(card.get("description") or ""),
        " ".join(payload.get("tags") or []),
        json.dumps(card, ensure_ascii=False),
    ]
    def normalize_text(value: str) -> str:
        return " ".join(value.lower().replace("-", " ").replace("_", " ").split())

    return normalize_text(title), normalize_text(" ".join(body_parts))


def classify_hf(payload: dict[str, Any], config: dict[str, Any]) -> dict[str, Any] | None:
    title, body = discovery_text(payload)
    combined = title + " " + body
    def normalize_negative(value: str) -> str:
        return " ".join(value.lower().replace("-", " ").replace("_", " ").split())

    negatives = [word for word in config.get("negative", []) if normalize_negative(word) in combined]
    if negatives:
        return {"accepted": False, "reason": "negative_keywords", "matched": negatives}
    weights = config["automation"]["weights"]
    min_score = float(config["automation"].get("min_score", 6.0))
    require_strong = bool(config["automation"].get("require_strong", True))
    results = []
    for category, rule in config["categories"].items():
        score = 0.0
        matched: list[dict[str, str]] = []
        strong_found = False
        for strength in ("strong", "medium", "weak"):
            for keyword in rule.get("keywords", {}).get(strength, []):
                needle = keyword.lower()
                location = "title" if needle in title else ("body" if needle in body else None)
                if not location:
                    continue
                score += float(weights[strength][location])
                matched.append({"keyword": keyword, "strength": strength, "location": location})
                strong_found |= strength == "strong"
        if score >= min_score and (strong_found or not require_strong):
            results.append({"category": category, "score": round(score, 2), "matched": matched})
    results.sort(key=lambda item: (-item["score"], item["category"]))
    return {"accepted": bool(results), "categories": results}


def known_repositories(doc: dict[str, Any]) -> dict[str, list[str]]:
    known: dict[str, list[str]] = defaultdict(list)
    for item in doc["datasets"]:
        source = item.get("source", {})
        if source.get("provider") == "huggingface" and source.get("repo_id"):
            known[source["repo_id"]].append(item["id"])
    return dict(known)


def reconcile_candidates(
    state: dict[str, Any], known: dict[str, list[str]], blocklist: set[str],
) -> None:
    """Reflect human curation decisions without auto-promoting discoveries."""
    for repo_id, candidate in state.get("candidates", {}).items():
        if repo_id in known:
            candidate["status"] = "accepted"
            candidate["canonical_dataset_ids"] = known[repo_id]
        elif repo_id in blocklist:
            candidate["status"] = "rejected"
            candidate["rejection_reason"] = "configured_blocklist"


def citation(url: str) -> str:
    """GitHub 可直接打开的普通 Markdown 来源链接。"""
    return f"[来源]({url})"


def md(value: Any) -> str:
    return str(value if value not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def render_catalog(doc: dict[str, Any], state: dict[str, Any], config: dict[str, Any], generated_at: str) -> str:
    datasets = doc["datasets"]
    tiers = Counter(item["usage_tier"] for item in datasets)
    stages = Counter(stage for item in datasets for stage in item["stages"])
    modalities = Counter(modality for item in datasets for modality in item["modalities"])
    repositories = state.get("repositories", {})
    candidates = state.get("candidates", {})
    pending = sum(item.get("status") == "pending_review" for item in candidates.values())
    lines = [
        "# Base 与多模态模型后训练数据自动目录",
        "",
        f"> 自动更新：{generated_at}；canonical 输入：`datasets-list.yaml`。本文件只生成视图，不改写人工许可和训练分层。",
        f"> 共 {len(datasets)} 项已收录资产；待审核候选 {pending} 项。候选数据不会自动进入训练配方。",
        "",
        "## 分层、模态与阶段索引",
        "",
        "| 维度 | 值 | 数量 |",
        "|---|---|---:|",
    ]
    lines += [f"| usage_tier | `{key}` | {value} |" for key, value in sorted(tiers.items())]
    lines += [f"| modality | `{key}` | {value} |" for key, value in sorted(modalities.items())]
    lines += [f"| stage | `{key}` | {value} |" for key, value in sorted(stages.items())]
    lines += ["", "## 能力覆盖", "", "| 能力 | 训练候选 | 独立评测 |", "|---|---|---|"]
    for capability, rule in doc.get("coverage_requirements", {}).items():
        train = ", ".join(f"`{item}`" for item in rule.get("training_candidates", []))
        evals = ", ".join(f"`{item}`" for item in rule.get("eval_ids", []))
        lines.append(f"| `{capability}` | {train} | {evals} |")
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in datasets:
        by_category[item["category"]].append(item)
    lines += ["", "## 分类目录", ""]
    for category in sorted(by_category):
        name = config.get("categories", {}).get(category, {}).get("name", category)
        lines += [
            f"### {name}（`{category}`）",
            "",
            "| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for item in sorted(by_category[category], key=lambda row: row["id"]):
            source = item["source"]
            record = repositories.get(source.get("repo_id"), {}) if source.get("repo_id") else {}
            current = record.get("current") or {}
            status = record.get("status", "not_tracked")
            lines.append(
                f"| {item['name']}<br>`{item['id']}` | {', '.join(item['modalities'])} | {', '.join(item['stages'])} | {item['usage_tier']} | "
                f"{item['license']['commercial_status']} | {status} | {md(current.get('last_modified'))} | "
                f"{citation(source['url']) if source['url'].startswith('https://') else '内部登记项'} |"
            )
        lines.append("")
    lines += [
        "## 自动化边界",
        "",
        "- 分类、模态、规模、许可和 `usage_tier` 以人工维护的 canonical 总表为准。",
        "- API 返回的许可仅用于变更提醒，不会自动把 `review_required` 改成可商用。",
        "- 新发现数据只进入 `datasets-candidates.yaml`，必须人工审核后才能加入 canonical 总表。",
        "- 多模态资产不会自动进入现有 ERNIE 文本配方；`eval_only` 与私有／时间外评测始终禁止训练。",
        "",
    ]
    return "\n".join(lines)


def render_candidates(state: dict[str, Any], generated_at: str) -> str:
    candidates = sorted(
        state.get("candidates", {}).values(),
        key=lambda item: (item.get("status") != "pending_review", item.get("repo_id", "")),
    )
    doc = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "policy": {
            "default_status": "pending_review",
            "auto_training_allowed": False,
            "promotion_requires": [
                "人工确认 text/image/video/audio 模态与训练阶段", "固定 revision、config 和 split", "许可、上游媒体与教师条款审查",
                "去重去污和样本级抽检", "加入 datasets-list.yaml 后通过完整性校验",
            ],
        },
        "candidates": candidates,
    }
    return yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120)


def render_report(run: dict[str, Any], state: dict[str, Any]) -> str:
    lines = [
        "# 数据目录更新报告",
        "",
        f"> 运行时间：{run['generated_at']}；模式：{run['mode']}。",
        "",
        "## 本次概览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| canonical 资产 | {run['assets']} |",
        f"| 已跟踪 Hugging Face 仓库 | {run['tracked_total']} |",
        f"| 本次成功刷新 | {run['refreshed_ok']} |",
        f"| 刷新失败 | {len(run['errors'])} |",
        f"| 元数据变化 | {len(run['changes'])} |",
        f"| 本次新候选 | {len(run['new_candidates'])} |",
        f"| 累计待审核候选 | {run['pending_candidates']} |",
        f"| 执行发现查询 | {run['queries_run']} |",
        "",
        "## 元数据变化",
        "",
    ]
    if not run["changes"]:
        lines += ["_本次没有已跟踪仓库的元数据变化。_", ""]
    else:
        lines += ["| 仓库 | 关联资产 | 变化字段 |", "|---|---|---|"]
        for change in run["changes"]:
            fields = ", ".join(f"`{key}`" for key in change["changes"])
            repo = change["repo_id"]
            dataset_ids = ", ".join(f"`{dataset_id}`" for dataset_id in change["dataset_ids"])
            lines.append(f"| [`{repo}`]({HF_API}/datasets/{repo}) | {dataset_ids} | {fields or '首次纳入跟踪'} |")
        lines.append("")
    lines += ["## 新发现候选（仅待审核）", ""]
    if not run["new_candidates"]:
        lines += ["_本次没有新增候选。_", ""]
    else:
        lines += ["| 仓库 | 建议分类 | 分数 | 状态 |", "|---|---|---:|---|"]
        for item in run["new_candidates"]:
            repo = item["repo_id"]
            lines.append(f"| [`{repo}`]({HF_API}/datasets/{repo}) | `{item['suggested_category']}` | {item['score']} | pending_review |")
        lines.append("")
    lines += ["## 错误与限制", ""]
    if not run["errors"]:
        lines += ["_本次没有刷新错误。_", ""]
    else:
        lines += [f"- `{item['repo_id']}`：{md(item['error'])}" for item in run["errors"]] + [""]
    lines += [
        "- 外部 API 元数据不等于数据内容审计；许可变化、revision 固定和样本级验证仍需人工完成。",
        "- 自动分类分数表示关键词相关度，不代表数据质量或训练适用性。",
        "- 更新器不会修改原有 42 项保留关系，也不会把候选资产自动写入训练清单。",
        "",
    ]
    return "\n".join(lines)


def empty_state() -> dict[str, Any]:
    return {"schema_version": "1.0", "repositories": {}, "candidates": {}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="不访问网络，只从 canonical 和历史状态重建视图")
    parser.add_argument("--discover", action="store_true", help="通过 Hugging Face 搜索发现待审核候选")
    parser.add_argument("--dry-run", action="store_true", help="打印结果但不写文件")
    parser.add_argument("--strict", action="store_true", help="任一已知仓库刷新失败时返回非零状态")
    parser.add_argument("--limit", type=int, default=None, help="限制本次刷新的已知仓库数，用于调试")
    parser.add_argument("--discovery-limit", type=int, default=None, help="覆盖每条发现查询的返回上限")
    parser.add_argument("--max-queries", type=int, default=None, help="限制发现查询数，用于调试")
    parser.add_argument("--now", default=None, help="固定 ISO 时间，便于可复现测试")
    args = parser.parse_args()

    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    doc = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    errors, warnings, summary = validate(CATALOG)
    if errors:
        print(json.dumps({"valid": False, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 1

    generated_at = args.now or now_utc()
    state = read_json(STATE, empty_state())
    state.setdefault("repositories", {})
    state.setdefault("candidates", {})
    known = known_repositories(doc)
    pause = float(config["automation"].get("request_pause_seconds", 0.1))
    run: dict[str, Any] = {
        "generated_at": generated_at,
        "mode": "offline" if args.offline else ("metadata+discovery" if args.discover else "metadata"),
        "assets": len(doc["datasets"]),
        "tracked_total": len(known),
        "refreshed_ok": 0,
        "changes": [],
        "new_candidates": [],
        "errors": [],
        "queries_run": 0,
        "pending_candidates": 0,
    }

    if not args.offline:
        for index, (repo_id, dataset_ids) in enumerate(sorted(known.items())):
            if args.limit is not None and index >= args.limit:
                break
            key = repo_id
            try:
                payload = request_json(f"{HF_API}/api/datasets/{quote(repo_id, safe='/')}", config)
                current = normalize_hf(payload, repo_id)
                record, changes = merge_metadata(
                    state["repositories"].get(key), current, dataset_ids, generated_at,
                    int(config["automation"].get("history_keep", 30)),
                )
                state["repositories"][key] = record
                run["refreshed_ok"] += 1
                if changes:
                    run["changes"].append({"repo_id": repo_id, "dataset_ids": dataset_ids, "changes": changes})
            except Exception as exc:  # keep prior snapshot and continue other repositories
                record = dict(state["repositories"].get(key) or {})
                record.update({
                    "repo_id": repo_id, "dataset_ids": dataset_ids,
                    "first_seen_at": record.get("first_seen_at", generated_at),
                    "last_checked_at": generated_at, "status": "error", "error": str(exc),
                })
                state["repositories"][key] = record
                run["errors"].append({"repo_id": repo_id, "error": str(exc)})
            time.sleep(pause)

    if args.discover and not args.offline:
        queries = config.get("queries", [])
        if args.max_queries is not None:
            queries = queries[:args.max_queries]
        limit = args.discovery_limit or int(config["automation"].get("discovery_limit_per_query", 20))
        blocklist = set(config.get("blocklist", []))
        for query in queries:
            params = urlencode({
                "search": query["search"], "limit": limit, "full": "true",
                "sort": "lastModified", "direction": "-1",
            })
            try:
                payload = request_json(f"{HF_API}/api/datasets?{params}", config)
                run["queries_run"] += 1
            except Exception as exc:
                run["errors"].append({"repo_id": f"search:{query['search']}", "error": str(exc)})
                time.sleep(pause)
                continue
            for item in payload if isinstance(payload, list) else []:
                repo_id = item.get("id")
                if not repo_id or repo_id in known or repo_id in blocklist:
                    continue
                classified = classify_hf(item, config)
                if not classified or not classified.get("accepted"):
                    continue
                categories = classified["categories"]
                primary = categories[0]
                existing = state["candidates"].get(repo_id)
                is_new = existing is None
                candidate = dict(existing or {})
                candidate.update({
                    "repo_id": repo_id,
                    "url": f"https://huggingface.co/datasets/{repo_id}",
                    "status": candidate.get("status", "pending_review"),
                    "first_seen_at": candidate.get("first_seen_at", generated_at),
                    "last_seen_at": generated_at,
                    "suggested_category": primary["category"],
                    "score": primary["score"],
                    "suggested_categories": categories[:3],
                    "queries": sorted(set(candidate.get("queries", [])) | {query["search"]}),
                    "metadata": normalize_hf(item, repo_id),
                    "review": {
                        "text_modality_confirmed": False,
                        "license_approved": False,
                        "revision_pinned": False,
                        "decontaminated": False,
                        "sample_inspected": False,
                    },
                })
                if candidate.get("last_counted_run") != generated_at:
                    candidate["seen_count"] = int(candidate.get("seen_count", 0)) + 1
                    candidate["last_counted_run"] = generated_at
                state["candidates"][repo_id] = candidate
                if is_new:
                    run["new_candidates"].append({
                        "repo_id": repo_id, "suggested_category": primary["category"], "score": primary["score"],
                    })
            time.sleep(pause)

    reconcile_candidates(state, known, set(config.get("blocklist", [])))
    run["pending_candidates"] = sum(
        item.get("status", "pending_review") == "pending_review" for item in state["candidates"].values()
    )
    state.update({
        "generated_at": generated_at,
        "source_catalog": {"path": CATALOG.name, "sha256": sha256(CATALOG)},
        "last_run": run,
    })
    from dataset_markdown_links import link_dataset_table_entries
    assets = {item["id"]: item for item in doc["datasets"]}
    outputs = {
        STATE: json_text(state),
        CANDIDATES: render_candidates(state, generated_at),
        CATALOG_MD: link_dataset_table_entries(render_catalog(doc, state, config, generated_at), assets),
        REPORT_MD: link_dataset_table_entries(render_report(run, state), assets),
    }
    changed = [path.name for path, text in outputs.items() if write_if_changed(path, text, args.dry_run)]
    result = {
        "valid": True,
        "dry_run": args.dry_run,
        "changed_files": changed,
        "summary": summary,
        "update": run,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.strict and run["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
