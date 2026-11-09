#!/usr/bin/env python3
"""校验后训练数据 Manifest；仅依赖 PyYAML，不下载数据、不启动训练。"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

import yaml


ALLOWED_STAGES = {"sft", "preference", "rlvr"}
PLACEHOLDER_MARKERS = ("REPLACE_ME", "PIN_ME", "REVIEW_ME", "VERIFY_FIELDS")


def is_placeholder(value: Any) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    upper = value.upper()
    return not value.strip() or any(marker in upper for marker in PLACEHOLDER_MARKERS)


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def validate(manifest: dict[str, Any], profile_override: str | None, allow_placeholders: bool):
    errors: list[str] = []
    warnings: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def pending(condition: bool, message: str) -> None:
        """模板模式跳过待填写项，但保留结构错误。"""
        if not condition and not allow_placeholders:
            errors.append(message)

    require(manifest.get("manifest_version") == "1.0", "manifest_version 必须为 '1.0'")
    project = as_dict(manifest.get("project"))
    datasets = as_dict(manifest.get("datasets"))
    profiles = as_dict(manifest.get("profiles"))
    preflight = as_dict(manifest.get("preflight"))
    signoff = as_dict(manifest.get("signoff"))

    require(bool(project), "缺少 project")
    require(bool(datasets), "缺少 datasets")
    require(bool(profiles), "缺少 profiles")

    profile_name = profile_override or project.get("selected_profile")
    require(profile_name in profiles, f"未找到所选 profile：{profile_name}")
    if profile_name not in profiles:
        return errors, warnings, None, []

    selected = as_dict(profiles[profile_name])
    selected_stage = selected.get("stage")

    for name, profile in profiles.items():
        profile = as_dict(profile)
        stage = profile.get("stage")
        require(stage in ALLOWED_STAGES, f"profile {name} 的 stage 无效：{stage}")
        mixture = profile.get("mixture")
        require(isinstance(mixture, list) and bool(mixture), f"profile {name} 缺少 mixture")
        if not isinstance(mixture, list):
            continue

        total_weight = 0.0
        for index, item in enumerate(mixture):
            item = as_dict(item)
            dataset_name = item.get("dataset")
            weight = item.get("weight")
            require(dataset_name in datasets, f"profile {name}[{index}] 引用了未知数据集：{dataset_name}")
            require(
                isinstance(weight, (int, float)) and not isinstance(weight, bool) and weight > 0,
                f"profile {name}[{index}] 的 weight 必须为正数",
            )
            if isinstance(weight, (int, float)) and not isinstance(weight, bool):
                total_weight += float(weight)
            if dataset_name in datasets:
                dataset_stage = as_dict(datasets[dataset_name]).get("stage")
                require(
                    dataset_stage == stage,
                    f"profile {name} 的阶段 {stage} 与数据集 {dataset_name} 的阶段 {dataset_stage} 不一致",
                )
        require(
            math.isclose(total_weight, 1.0, rel_tol=0.0, abs_tol=1e-6),
            f"profile {name} 的权重之和必须为 1，当前为 {total_weight:.8f}",
        )

    for name, dataset in datasets.items():
        dataset = as_dict(dataset)
        require(dataset.get("stage") in ALLOWED_STAGES, f"数据集 {name} 的 stage 无效")
        source = as_dict(dataset.get("source"))
        data = as_dict(dataset.get("data"))
        license_info = as_dict(dataset.get("license"))
        access = as_dict(dataset.get("access"))
        processing = as_dict(dataset.get("processing"))

        require(source.get("provider") in {"huggingface", "manual", "local"}, f"数据集 {name} 的 provider 无效")
        require(isinstance(source.get("split"), str) and bool(source.get("split")), f"数据集 {name} 缺少 split")
        require(bool(data.get("format")), f"数据集 {name} 缺少 data.format")
        require(bool(data.get("adapter")), f"数据集 {name} 缺少 data.adapter")
        require(bool(license_info.get("id")), f"数据集 {name} 缺少 license.id")
        require(
            license_info.get("commercial_status")
            in {"allowed_with_obligations", "noncommercial", "review_required", "internal_review_required"},
            f"数据集 {name} 的 commercial_status 无效",
        )
        require(isinstance(access.get("gated"), bool), f"数据集 {name} 缺少 access.gated")
        require(isinstance(processing.get("decontaminate"), bool), f"数据集 {name} 缺少 processing.decontaminate")
        if dataset.get("stage") == "rlvr":
            verifier = as_dict(dataset.get("verifier"))
            require(bool(verifier.get("type")), f"RLVR 数据集 {name} 缺少 verifier.type")
            if verifier.get("type") == "sandbox_unit_tests":
                require(verifier.get("network") is False, f"代码验证器 {name} 默认必须禁用网络")
                require(verifier.get("hidden_tests_required") is True, f"代码验证器 {name} 必须要求隐藏测试")
        if processing.get("decontaminate") is False:
            warnings.append(f"数据集 {name} 关闭了去污，请确认这是有意为之")

    selected_mixture = selected.get("mixture", [])
    selected_dataset_names = [as_dict(item).get("dataset") for item in selected_mixture]
    selected_datasets = [(name, as_dict(datasets[name])) for name in selected_dataset_names if name in datasets]

    base_model = as_dict(project.get("base_model"))
    pending(not is_placeholder(project.get("output_dir")), "请填写 project.output_dir")
    pending(not is_placeholder(base_model.get("id")), "请填写 project.base_model.id")
    pending(not is_placeholder(base_model.get("revision")), "请固定 project.base_model.revision")

    runtime = as_dict(manifest.get("runtime"))
    require(runtime.get("trust_remote_code") is False, "runtime.trust_remote_code 必须保持 false；例外需单独安全审查")

    for name, dataset in selected_datasets:
        source = as_dict(dataset.get("source"))
        license_info = as_dict(dataset.get("license"))
        access = as_dict(dataset.get("access"))
        data = as_dict(dataset.get("data"))

        if preflight.get("fail_on_disabled_dataset", True):
            require(dataset.get("enabled") is True, f"当前 profile 使用的数据集 {name} 尚未启用")
        if preflight.get("require_immutable_revisions", True):
            pending(not is_placeholder(source.get("revision")), f"请固定数据集 {name} 的不可变 revision")
            if isinstance(source.get("revision"), str):
                require(source.get("revision") != "main", f"数据集 {name} 不能使用浮动 main 作为正式 revision")
        if source.get("provider") in {"manual", "local"}:
            pending(not is_placeholder(source.get("local_path")), f"请填写数据集 {name} 的 local_path")
        if preflight.get("fail_on_unaccepted_gated_dataset", True) and access.get("gated"):
            require(access.get("terms_accepted") is True, f"数据集 {name} 需要接受访问条件后才能使用")

        if project.get("commercial_use") is True:
            require(
                license_info.get("commercial_status") == "allowed_with_obligations",
                f"商用模式下数据集 {name} 的许可状态为 {license_info.get('commercial_status')}，不能使用",
            )
            pending(not license_info.get("upstream_review_required"), f"商用模式下数据集 {name} 的上游许可审查尚未完成")
            pending(not license_info.get("teacher_terms_review_required"), f"商用模式下数据集 {name} 的教师条款审查尚未完成")

        if selected_stage == "rlvr":
            verifier = as_dict(dataset.get("verifier"))
            pending(not is_placeholder(verifier.get("implementation")), f"请配置数据集 {name} 的验证器实现")
            for revision_field in ("package_revision", "repository_revision"):
                if revision_field in verifier:
                    pending(
                        not is_placeholder(verifier.get(revision_field)),
                        f"请固定数据集 {name} 的验证器版本：verifier.{revision_field}",
                    )
            if verifier.get("type") == "sandbox_unit_tests":
                pending(not is_placeholder(verifier.get("image")), f"请固定数据集 {name} 的沙箱镜像")

        if data.get("adapter") == "VERIFY_FIELDS_THEN_MAP":
            pending(False, f"请核对数据集 {name} 的真实字段并替换适配器")

    if preflight.get("require_data_quality_signoff", True):
        pending(signoff.get("data_quality") is True, "数据质量审查尚未签署：signoff.data_quality")
    if preflight.get("require_license_signoff", True):
        pending(signoff.get("license") is True, "许可审查尚未签署：signoff.license")
    if preflight.get("require_decontamination_signoff", True):
        pending(signoff.get("decontamination") is True, "去污审查尚未签署：signoff.decontamination")
    if selected_stage == "rlvr" and preflight.get("require_verifier_signoff_for_rlvr", True):
        pending(signoff.get("verifier") is True, "RLVR 验证器审查尚未签署：signoff.verifier")

    if profile_name == "tool_sft" and preflight.get("require_no_call_negative_for_tool_profile", True):
        has_no_call = any(as_dict(dataset.get("data")).get("role") == "no_call_negative" for _, dataset in selected_datasets)
        require(has_no_call, "tool_sft 必须包含 role=no_call_negative 的数据集")

    if allow_placeholders:
        warnings.append("当前为模板结构校验模式；正式训练前请去掉 --allow-placeholders 再运行")

    return errors, warnings, (profile_name, selected_stage), selected_dataset_names


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 Base 模型后训练数据 Manifest")
    parser.add_argument("manifest", type=Path, help="YAML Manifest 路径")
    parser.add_argument("--profile", help="临时覆盖 project.selected_profile")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="只校验结构与权重，允许占位符和未签署项；不能作为开训凭证",
    )
    args = parser.parse_args()

    try:
        with args.manifest.open("r", encoding="utf-8") as handle:
            manifest = yaml.safe_load(handle)
    except FileNotFoundError:
        print(f"错误：文件不存在：{args.manifest}", file=sys.stderr)
        return 2
    except yaml.YAMLError as exc:
        print(f"错误：YAML 解析失败：{exc}", file=sys.stderr)
        return 2

    if not isinstance(manifest, dict):
        print("错误：Manifest 顶层必须是对象", file=sys.stderr)
        return 2

    errors, warnings, selected, dataset_names = validate(manifest, args.profile, args.allow_placeholders)

    for warning in warnings:
        print(f"警告：{warning}")
    if errors:
        print(f"校验失败，共 {len(errors)} 项：", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    profile_name, stage = selected
    print("Manifest 结构校验通过。")
    print(f"当前方案：{profile_name}（{stage}）")
    print(f"数据集：{', '.join(dataset_names)}")
    if not args.allow_placeholders:
        print("严格前置检查通过；可以进入具体训练框架的配置生成阶段。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
