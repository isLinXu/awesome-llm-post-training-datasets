#!/usr/bin/env python3
"""Validate the canonical Base LLM post-training asset catalogue."""
from collections import Counter
from pathlib import Path
import argparse
import json
import sys
import yaml

STAGES = {"sft", "preference", "reward_model", "rlvr", "prm", "agent_sft", "agent_rl", "evaluation"}
TIERS = {"core", "optional", "research_only", "eval_only", "local_required"}
COMMERCIAL = {"allowed_with_obligations", "noncommercial", "review_required", "internal_review_required", "eval_only"}
VERIFICATION = {"official_checked", "official_checked_previous", "partial_official_reference", "local_definition_required"}
RELATIONS = {"overlap", "derived_from", "contains", "decontaminated_from"}
MODALITIES = {"text", "image", "video", "audio"}
EXPECTED_SCOPE_MODALITIES = ["text", "image", "video", "audio"]
SHA40 = __import__("re").compile(r"[0-9a-f]{40}")


def validate(path: Path):
    errors, warnings = [], []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"YAML 读取失败：{exc}"], warnings, {}
    if not isinstance(doc, dict):
        return ["顶层必须是 mapping"], warnings, {}
    if doc.get("schema_version") != "1.0":
        errors.append("schema_version 必须为 1.0")
    scope = doc.get("scope", {})
    if scope.get("modalities") != EXPECTED_SCOPE_MODALITIES:
        errors.append("scope.modalities 必须依次为 text/image/video/audio")
    if not scope.get("recipe_boundary") or "文本专用" not in scope["recipe_boundary"]:
        errors.append("缺少现有 ERNIE 文本配方与多模态资产的边界声明")
    if not scope.get("completeness_definition"):
        errors.append("缺少 completeness_definition")
    datasets = doc.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        return ["datasets 必须是非空列表"], warnings, {}

    by_id = {}
    for i, item in enumerate(datasets):
        loc = f"datasets[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{loc} 必须是 mapping")
            continue
        did = item.get("id")
        if not isinstance(did, str) or not did or did.lower() != did:
            errors.append(f"{loc}.id 缺失或不是小写规范 ID")
            continue
        loc = f"datasets[{did}]"
        if did in by_id:
            errors.append(f"重复 ID：{did}")
        by_id[did] = item
        for field in ("name", "category", "stages", "usage_tier", "modalities", "scale", "source", "data_format", "capabilities", "license", "access", "risks", "recommendation", "verification"):
            if field not in item:
                errors.append(f"{loc} 缺少 {field}")
        stages = item.get("stages", [])
        tier = item.get("usage_tier")
        if not isinstance(stages, list) or not stages or not set(stages) <= STAGES:
            errors.append(f"{loc}.stages 含非法值：{stages}")
        if tier not in TIERS:
            errors.append(f"{loc}.usage_tier 非法：{tier}")
        modalities = item.get("modalities")
        if not isinstance(modalities, list) or not modalities or len(modalities) != len(set(modalities)) or not set(modalities) <= MODALITIES:
            errors.append(f"{loc}.modalities 必须是非空、无重复的 text/image/video/audio 子集")
        if not isinstance(item.get("capabilities"), list) or not item.get("capabilities"):
            errors.append(f"{loc}.capabilities 必须非空")
        scale = item.get("scale", {})
        if not isinstance(scale, dict) or not scale.get("unit") or not scale.get("note"):
            errors.append(f"{loc}.scale 必须含 unit 和 note")
        else:
            value = scale.get("value")
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value <= 0):
                errors.append(f"{loc}.scale.value 必须是正整数或 null")
        source = item.get("source", {})
        if not isinstance(source, dict) or not source.get("provider") or not source.get("url") or not source.get("revision_policy"):
            errors.append(f"{loc}.source 必须含 provider、url、revision_policy")
        elif tier != "local_required" and not str(source["url"]).startswith("https://"):
            errors.append(f"{loc}.source.url 必须是 HTTPS 官方来源")
        observed_revision = source.get("observed_revision") if isinstance(source, dict) else None
        if observed_revision is not None and not SHA40.fullmatch(str(observed_revision)):
            errors.append(f"{loc}.source.observed_revision 必须是 40 位 SHA")
        license_info = item.get("license", {})
        commercial = license_info.get("commercial_status") if isinstance(license_info, dict) else None
        if not license_info.get("id") or commercial not in COMMERCIAL:
            errors.append(f"{loc}.license 缺少 id 或 commercial_status 非法")
        if tier == "core" and commercial == "noncommercial":
            errors.append(f"{loc} 非商用数据不得标为 core")
        if tier == "research_only" and commercial not in {"noncommercial", "review_required"}:
            warnings.append(f"{loc} research_only 但 commercial_status={commercial}，请确认分层理由")
        if tier == "eval_only":
            if stages != ["evaluation"] or commercial != "eval_only":
                errors.append(f"{loc} eval_only 必须仅含 evaluation 阶段且 commercial_status=eval_only")
            if item.get("train_prohibited") is not True or item.get("eval_isolation_required") is not True:
                errors.append(f"{loc} eval_only 必须 train_prohibited 且 eval_isolation_required 为 true")
        elif stages == ["evaluation"] and tier != "local_required":
            errors.append(f"{loc} 纯公共评测必须标为 eval_only")
        if tier == "local_required":
            if commercial != "internal_review_required" or source.get("provider") != "local" or item.get("access") != "local":
                errors.append(f"{loc} 本地物料必须 internal/local 分层")
        verification = item.get("verification", {})
        if verification.get("status") not in VERIFICATION or not verification.get("checked_at"):
            errors.append(f"{loc}.verification 状态或日期非法")
        for relation in item.get("relations", []):
            if relation.get("type") not in RELATIONS or not relation.get("target") or not relation.get("action"):
                errors.append(f"{loc} 含非法 relation：{relation}")

    for did, item in by_id.items():
        for relation in item.get("relations", []):
            target = relation.get("target")
            if target not in by_id:
                errors.append(f"{did} relation 指向不存在的数据：{target}")

    provenance = doc.get("provenance", {})
    previous = provenance.get("previous_asset_ids", [])
    if len(previous) != 42 or len(set(previous)) != 42:
        errors.append("previous_asset_ids 必须精确保留原有 42 个唯一 ID")
    if provenance.get("text_assets_retained") != 114 or provenance.get("multimodal_assets_added") != 61:
        errors.append("provenance 必须保留 114 项文本资产并登记 61 项多模态扩展")
    missing_previous = sorted(set(previous) - set(by_id))
    if missing_previous:
        errors.append(f"原有资产丢失：{missing_previous}")
    coverage = doc.get("coverage_requirements")
    if not isinstance(coverage, dict) or not coverage:
        errors.append("coverage_requirements 必须非空")
        coverage = {}
    covered_caps = set()
    for cap, rule in coverage.items():
        covered_caps.add(cap)
        if rule.get("required") is not True:
            errors.append(f"coverage[{cap}] 必须为 required=true")
        training = rule.get("training_candidates", [])
        eval_ids = rule.get("eval_ids", [])
        if not training or not eval_ids:
            errors.append(f"coverage[{cap}] 训练和评测候选均不能为空")
        for ref in training:
            if ref not in by_id:
                errors.append(f"coverage[{cap}] 训练引用不存在：{ref}")
            elif by_id[ref]["usage_tier"] == "eval_only":
                errors.append(f"coverage[{cap}] 把 eval_only 当训练数据：{ref}")
            elif cap not in by_id[ref].get("capabilities", []):
                errors.append(f"coverage[{cap}] 与 {ref}.capabilities 不一致")
        for ref in eval_ids:
            if ref not in by_id:
                errors.append(f"coverage[{cap}] 评测引用不存在：{ref}")
            elif "evaluation" not in by_id[ref].get("stages", []):
                errors.append(f"coverage[{cap}] 的 {ref} 不含 evaluation 阶段")
            elif cap not in by_id[ref].get("capabilities", []):
                errors.append(f"coverage[{cap}] 与 {ref}.capabilities 不一致")
    for did, item in by_id.items():
        for cap in item.get("capabilities", []):
            if cap not in covered_caps:
                errors.append(f"{did} 引用了未定义能力：{cap}")

    tier_counts = Counter(x["usage_tier"] for x in by_id.values())
    if not tier_counts.get("eval_only"):
        errors.append("缺少 eval_only 资产")
    if not tier_counts.get("local_required"):
        errors.append("缺少 local_required 资产")
    summary = {
        "total_assets": len(by_id), "usage_tier": dict(sorted(tier_counts.items())),
        "previous_assets_retained": len(set(previous) & set(by_id)),
        "text_assets_retained": provenance.get("text_assets_retained"),
        "text_only_assets": sum(item.get("modalities") == ["text"] for item in by_id.values()),
        "multimodal_assets_added": provenance.get("multimodal_assets_added"),
        "non_text_only_assets": sum(item.get("modalities") != ["text"] for item in by_id.values()),
        "modality_membership": dict(sorted(Counter(modality for item in by_id.values() for modality in item.get("modalities", [])).items())),
        "required_capabilities": len(coverage),
        "commercial_status": dict(sorted(Counter(x["license"]["commercial_status"] for x in by_id.values()).items())),
    }
    return errors, warnings, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--expect-total", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors, warnings, summary = validate(args.path)
    if args.expect_total is not None and summary.get("total_assets") != args.expect_total:
        errors.append(f"资产总数 {summary.get('total_assets')} != 预期 {args.expect_total}")
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors, "warnings": warnings, "summary": summary}, ensure_ascii=False, indent=2))
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        if not errors:
            print(f"VALIDATION PASSED: {summary['total_assets']} assets; {summary['required_capabilities']} required capabilities; 0 errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
