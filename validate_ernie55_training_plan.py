#!/usr/bin/env python3
"""Validate ERNIE 5.5 experiment references against the canonical dataset list."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parent


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 ERNIE 5.5 与代理小模型训练计划")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--catalog", type=Path, default=ROOT / "datasets-list.yaml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan_path = args.plan.resolve()
    catalog_path = args.catalog.resolve()
    plan = load_yaml(plan_path)
    catalog = load_yaml(catalog_path)
    assets = {item["id"]: item for item in catalog["datasets"]}
    errors: list[str] = []
    warnings: list[str] = []

    model = plan.get("models", {}).get("ernie55_flash_base", {})
    revision = model.get("revision", "")
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        errors.append("ERNIE BF16 模型必须固定 40 位不可变 revision")
    bridge_revision = model.get("chat_template", {}).get("bridge_revision", "")
    if not re.fullmatch(r"[0-9a-f]{40}", bridge_revision):
        errors.append("聊天模板所属 Bridge 必须固定 40 位 commit")
    if model.get("chat_template", {}).get("train_inference_must_match") is not True:
        errors.append("训练与推理聊天模板必须强制一致")

    experiments = plan.get("experiments", [])
    ids = [item.get("id") for item in experiments]
    if len(ids) != len(set(ids)):
        errors.append("实验 ID 必须唯一")
    known_experiments = set(ids) | {"best_sft"}
    train_refs = 0
    eval_refs = 0

    for experiment in experiments:
        eid = experiment.get("id", "<missing>")
        parent = experiment.get("parent")
        if parent is not None and parent not in known_experiments:
            errors.append(f"{eid}: 未知父实验 {parent}")

        train = experiment.get("train", [])
        weights = []
        local_required = False
        for ref in train:
            dataset_id = ref.get("dataset")
            train_refs += 1
            asset = assets.get(dataset_id)
            if asset is None:
                errors.append(f"{eid}: 训练数据 {dataset_id} 不在 canonical 总表")
                continue
            if asset.get("train_prohibited") or asset.get("usage_tier") == "eval_only":
                errors.append(f"{eid}: eval_only 数据 {dataset_id} 不得训练")
            if experiment.get("stage") not in asset.get("stages", []):
                errors.append(f"{eid}: {dataset_id} 不支持阶段 {experiment.get('stage')}")
            local_required |= asset.get("usage_tier") == "local_required"
            weight = ref.get("weight")
            if not isinstance(weight, (int, float)) or weight <= 0:
                errors.append(f"{eid}: {dataset_id} 权重必须为正数")
            else:
                weights.append(float(weight))

        if train and not math.isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-9):
            errors.append(f"{eid}: 训练权重之和必须为 1，当前为 {sum(weights)}")
        if local_required and experiment.get("track") != "business_data_required":
            errors.append(f"{eid}: 含本地必需数据时 track 必须为 business_data_required")

        for alternative in experiment.get("alternatives", []):
            replacement = alternative.get("with")
            if replacement not in assets:
                errors.append(f"{eid}: 替代数据 {replacement} 不在 canonical 总表")
            elif assets[replacement].get("train_prohibited"):
                errors.append(f"{eid}: 替代数据 {replacement} 不得训练")

        for dataset_id in experiment.get("eval", []):
            eval_refs += 1
            asset = assets.get(dataset_id)
            if asset is None:
                errors.append(f"{eid}: 评测数据 {dataset_id} 不在 canonical 总表")
            elif asset.get("usage_tier") not in {"eval_only", "local_required"}:
                errors.append(f"{eid}: {dataset_id} 不是独立评测或本地必需评测")

        if experiment.get("stage") == "rlvr" and not experiment.get("verifier"):
            errors.append(f"{eid}: RLVR 必须声明验证器")

    by_id = {item["id"]: item for item in experiments}
    tool = by_id.get("tool_sft")
    if tool:
        tool_train = {ref["dataset"] for ref in tool.get("train", [])}
        if "local_no_tool_negative" not in tool_train:
            errors.append("tool_sft: 必须包含 local_no_tool_negative")

    if not plan.get("models", {}).get("smaller_base_models", {}).get("candidates"):
        warnings.append("更小 Base 模型尚未提供；当前只能确定代理实验协议，不能生成模型专属启动参数")
    warnings.append("本校验只验证引用、阶段、权重与隔离关系，不代表数据 revision、许可、质量或验证器已签署")

    result = {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "experiments": len(experiments),
            "train_references": train_refs,
            "evaluation_references": eval_refs,
            "canonical_assets": len(assets),
            "ernie_revision": revision,
            "bridge_revision": bridge_revision,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else "\n".join(errors + warnings))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
