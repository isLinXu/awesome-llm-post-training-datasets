#!/usr/bin/env python3
"""Build commercial-default and research-isolated post-training manifests."""
from __future__ import annotations

import json
import math
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parent
MODEL_ID = "baidu/ERNIE-5.5-Flash-Base-BF16"
MODEL_REVISION = "dfab899dadcff8f4d08af24b75a26c6d4d2e0b09"
BRIDGE_REVISION = "08035723e7a86f94fc54a7f4473bd0519f2ac941"

SPECS = {
    "tulu3_sft_mixture": dict(stage="sft", subset="default", split="train", adapter="messages_passthrough", fields={"messages": "messages"}, filters=["valid_roles", "nonempty_assistant", "length_histogram", "upstream_provenance_audit"]),
    "aya_dataset": dict(stage="sft", subset="default", split="train", adapter="input_target_to_messages", fields={"instruction": "inputs", "output": "targets", "language": "language", "language_code": "language_code", "annotation_type": "annotation_type"}, filters=["language_stratification", "empty_target_drop", "pii_review"]),
    "openmath_reasoning": dict(stage="sft", subset="default", split="cot", adapter="problem_solution_to_messages", fields={"problem": "problem", "solution": "generated_solution", "answer": "expected_answer", "inference_mode": "inference_mode", "source": "problem_source"}, filters=["cot_only", "answer_present", "solution_length_cap", "parent_problem_dedup"]),
    "tulu3_persona_if": dict(stage="sft", subset="default", split="train", adapter="messages_with_constraints", fields={"messages": "messages", "constraints": "constraints"}, filters=["deterministic_constraint_check", "valid_roles", "response_nonempty"]),
    "longcite_45k": dict(stage="sft", subset="default", split="train", adapter="prompt_response_to_messages", fields={"prompt": "prompt", "response": "response"}, filters=["citation_support_audit", "empty_citation_audit", "length_histogram"]),
    "opencodeinstruct": dict(stage="sft", subset="train", split="train", adapter="input_output_to_messages", fields={"prompt": "input", "response": "output", "domain": "domain", "unit_tests": "unit_tests", "execution_status": "tests_execution_status", "average_test_score": "average_test_score"}, filters=["execution_score_filter", "sandbox_replay", "parent_problem_dedup"]),
    "helpsteer3_preference": dict(stage="preference", subset="preference", split="train", adapter="helpsteer3_preference_pairs", fields={"context": "context", "response1": "response1", "response2": "response2", "overall_preference": "overall_preference", "individual_preference": "individual_preference", "language": "language", "domain": "domain"}, filters=["same_prompt_split", "preference_tie_policy", "human_label_audit"]),
    "dapo_math_17k": dict(stage="rlvr", subset="default", split="train", adapter="dapo_prompt_ground_truth", fields={"prompt": "prompt", "ground_truth": "reward_model.ground_truth", "data_source": "data_source", "ability": "ability", "extra_info": "extra_info"}, filters=["answer_normalization_audit", "benchmark_decontamination", "pass_rate_bucket"], verifier={"type": "math_answer_equivalence", "implementation": "math_verify", "package_revision": "PIN_ME_TO_MATH_VERIFY_VERSION", "network": False, "normalization_test_required": True}),
    "opencode_reasoning": dict(stage="sft", subset="split_0", split="split_0", adapter="input_output_to_messages", fields={"prompt": "input", "response": "output", "source": "source", "upstream_license": "license", "dataset": "dataset", "difficulty": "difficulty", "solution": "solution"}, filters=["split_0_only", "parent_problem_dedup", "upstream_license_inheritance", "solution_quality_audit"]),
    "chinese_r1_distill_110k": dict(stage="sft", subset="default", split="train", adapter="reasoning_content_to_messages", fields={"prompt": "input", "reasoning_content": "reasoning_content", "response": "content", "source": "repo_name", "score": "score"}, filters=["factuality_sample_audit", "score_distribution_audit", "parent_problem_dedup", "upstream_license_inheritance"]),
    "m2lingual": dict(stage="sft", subset="full_data", split="train", adapter="conversation_passthrough", fields={"messages": "conversation", "language": "language", "sample_type": "sample_type"}, filters=["full_data_only", "language_stratification", "valid_roles", "teacher_provenance_audit"]),
    "longform": dict(stage="sft", subset="default", split="train", adapter="prompt_response_to_messages", fields={"prompt": "prompt", "response": "response"}, filters=["train_split_only", "long_output_quality_audit", "upstream_license_inheritance", "global_consistency_audit"]),
    "weblinx": dict(stage="sft", subset="chat", split="train", adapter="weblinx_chat_turn_to_action_messages", fields={"demo": "demo", "turn": "turn", "action": "action", "action_history": "action_history", "utterances": "utterances", "candidates": "candidates", "clean_html": "clean_html", "viewport": "viewport"}, filters=["chat_train_only", "credential_pii_scrub", "html_length_cap", "static_trajectory_not_dynamic_environment"]),
    "falsereject_train": dict(stage="sft", subset="default", split="train", adapter="falsereject_instruct_to_messages", fields={"prompt": "prompt", "response": "instruct_response", "category": "category", "category_text": "category_text"}, filters=["instruct_response_only", "train_split_only", "safe_content_review", "overrefusal_stratification"]),
    "tulu3_preference_mixture": dict(stage="preference", subset="default", split="train", adapter="prompt_chosen_rejected_passthrough", fields={"prompt": "prompt", "chosen": "chosen", "rejected": "rejected"}, filters=["noncommercial_isolation", "same_prompt_split", "teacher_provenance_audit", "preference_pair_audit"]),
    "enigmata_data": dict(stage="rlvr", subset="default", split="train", adapter="enigmata_prompt_answer", fields={"prompt": "prompt", "answer": "answer", "task_name": "task_name", "ability": "ability", "language": "language", "meta": "meta"}, filters=["task_stratification", "enigmata_eval_instance_decontamination", "rule_verifier_coverage"], verifier={"type": "enigmata_rule_verifier", "implementation": "BytedTsinghua-SIA/Enigmata", "repository_revision": "PIN_ME_TO_ENIGMATA_GIT_COMMIT", "network": False, "all_task_verifiers_required": True}),
}

COMMERCIAL_PROFILES = {
    "commercial_general_sft": {
        "stage": "sft", "description": "商用默认通用／多语言／数学／精确指令 SFT；不包含 NC 或 review_required 数据",
        "mixture": [("tulu3_sft_mixture", 0.65), ("aya_dataset", 0.10), ("openmath_reasoning", 0.15), ("tulu3_persona_if", 0.10)],
        "overrides": {"max_seq_len": 8192, "packing": False, "assistant_only_loss": True, "row_token_budget": 250000000},
    },
    "commercial_code_sft": {
        "stage": "sft", "description": "商用默认代码专项；通用回放与代码主集分开计量",
        "mixture": [("tulu3_sft_mixture", 0.20), ("opencodeinstruct", 0.80)],
        "overrides": {"max_seq_len": 8192, "packing": False, "assistant_only_loss": True, "row_token_budget": 250000000},
    },
    "commercial_long_sft": {
        "stage": "sft", "description": "商用默认长文引用专项；长输入单独验收",
        "mixture": [("tulu3_sft_mixture", 0.60), ("longcite_45k", 0.40)],
        "overrides": {"max_seq_len": 32768, "packing": False, "assistant_only_loss": True, "row_token_budget": 200000000},
    },
    "commercial_preference_dpo": {
        "stage": "preference", "description": "最佳商用 SFT 之后的偏好实验；固定 preference config",
        "mixture": [("helpsteer3_preference", 1.0)],
        "overrides": {"max_prompt_len": 4096, "max_response_len": 4096},
    },
    "commercial_math_rlvr": {
        "stage": "rlvr", "description": "商用默认数学 RLVR；Math-Verify 版本和奖励一致性签署后启动",
        "mixture": [("dapo_math_17k", 1.0)],
        "overrides": {"max_prompt_len": 4096, "max_response_len": 8192, "rollouts_per_prompt": 8, "temperature": 0.7, "curriculum": "base_model_pass_rate_buckets"},
    },
}

RESEARCH_PROFILES = {
    "research_reasoning_sft": {
        "stage": "sft", "description": "研究隔离推理、多语言、中文蒸馏与长输出 SFT；包含 NC／待审数据",
        "mixture": [("openmath_reasoning", 0.30), ("opencode_reasoning", 0.25), ("chinese_r1_distill_110k", 0.15), ("m2lingual", 0.10), ("longform", 0.10), ("tulu3_sft_mixture", 0.10)],
        "overrides": {"max_seq_len": 16384, "packing": False, "assistant_only_loss": True, "row_token_budget": 250000000},
    },
    "research_browser_sft": {
        "stage": "sft", "description": "WebLINX 1.0 chat 静态轨迹研究；不得视为动态浏览环境训练",
        "mixture": [("weblinx", 0.80), ("tulu3_sft_mixture", 0.20)],
        "overrides": {"max_seq_len": 16384, "packing": False, "assistant_only_loss": True, "mask_tool_outputs": True, "row_token_budget": 200000000},
    },
    "research_overrefusal_sft": {
        "stage": "sft", "description": "FalseReject Instruct 防过拒研究；test 独立隔离，不使用 CoT 字段复制样本",
        "mixture": [("falsereject_train", 0.60), ("tulu3_sft_mixture", 0.40)],
        "overrides": {"max_seq_len": 8192, "packing": False, "assistant_only_loss": True, "row_token_budget": 200000000},
    },
    "research_preference_dpo": {
        "stage": "preference", "description": "Tulu 3 整包偏好研究基线；含非商小子集，禁止晋升商用",
        "mixture": [("tulu3_preference_mixture", 1.0)],
        "overrides": {"max_prompt_len": 4096, "max_response_len": 4096},
    },
    "research_enigmata_rlvr": {
        "stage": "rlvr", "description": "Enigmata 非商用规则验证 RL；固定全部任务验证器和 Eval 实例去污后启动",
        "mixture": [("enigmata_data", 1.0)],
        "overrides": {"max_prompt_len": 16384, "max_response_len": 4096, "rollouts_per_prompt": 8, "temperature": 0.7, "curriculum": "task_and_pass_rate_buckets"},
    },
}


def load_sources():
    catalog = yaml.safe_load((ROOT / "datasets-list.yaml").read_text(encoding="utf-8"))
    assets = {item["id"]: item for item in catalog["datasets"]}
    state = json.loads((ROOT / "data/dataset-catalog-state.json").read_text(encoding="utf-8"))
    return assets, state["repositories"], state["last_run"]["generated_at"]


def dataset_entry(dataset_id, assets, repositories):
    asset = assets[dataset_id]
    spec = SPECS[dataset_id]
    repo_id = asset["source"]["repo_id"]
    current = repositories[repo_id]["current"]
    revision = current["sha"]
    assert re.fullmatch(r"[0-9a-f]{40}", revision), (dataset_id, revision)
    assert not asset["train_prohibited"]
    assert asset["usage_tier"] != "eval_only"
    assert spec["stage"] in asset["stages"] or (dataset_id == "weblinx" and spec["stage"] == "sft")
    entry = {
        "canonical_id": dataset_id,
        "stage": spec["stage"],
        "enabled": True,
        "source": {
            "provider": "huggingface", "repo_id": repo_id, "revision": revision,
            "subset": spec["subset"], "split": spec["split"], "local_path": None,
        },
        "data": {"format": asset["data_format"], "adapter": spec["adapter"], "fields": spec["fields"]},
        "license": {
            "id": asset["license"]["id"], "commercial_status": asset["license"]["commercial_status"],
            "attribution_required": True,
            "upstream_review_required": bool(asset["license"]["upstream_and_teacher_terms_review_required"]),
            "teacher_terms_review_required": bool(asset["license"]["upstream_and_teacher_terms_review_required"]),
            "notes": "revision 固定不等于许可签署；商用前须完成上游和教师条款审查",
        },
        "access": {"gated": bool(current.get("gated")), "terms_accepted": False},
        "processing": {
            "max_samples": None,
            "dedup": ["exact", "minhash", "semantic_or_parent_problem"],
            "decontaminate": True,
            "filters": spec["filters"],
        },
    }
    if "verifier" in spec:
        entry["verifier"] = spec["verifier"]
    return entry


def make_manifest(kind, profiles, assets, repositories, resolved_at):
    commercial = kind == "commercial"
    used = []
    for profile in profiles.values():
        for dataset_id, _ in profile["mixture"]:
            if dataset_id not in used:
                used.append(dataset_id)
    datasets = {dataset_id: dataset_entry(dataset_id, assets, repositories) for dataset_id in used}
    if commercial:
        bad = [name for name, item in datasets.items() if item["license"]["commercial_status"] != "allowed_with_obligations"]
        assert not bad, f"Commercial recipe contains non-default licenses: {bad}"
    rendered_profiles = {}
    for name, profile in profiles.items():
        total = sum(weight for _, weight in profile["mixture"])
        assert math.isclose(total, 1.0, abs_tol=1e-9), (name, total)
        rendered_profiles[name] = {
            "stage": profile["stage"], "description": profile["description"],
            "mixture": [{"dataset": dataset_id, "weight": weight} for dataset_id, weight in profile["mixture"]],
            "overrides": profile["overrides"],
        }
    root = f"./{'commercial_default' if commercial else 'research_isolated'}"
    return {
        "manifest_version": "1.0",
        "metadata": {
            "name": f"{kind}-post-training-recipe", "created_at": "2026-11-09",
            "source_resolved_at": resolved_at, "canonical_catalog": "datasets-list.yaml",
            "weight_semantics": "归一化采样权重；不是样本行数占比，也不是有效 token 占比",
            "token_budget_semantics": "row_tokens_before_loss_mask；supervised_tokens 单独记录",
            "status": "executable_schema_pending_real_signoffs_not_training_authorization",
        },
        "project": {
            "selected_profile": next(iter(profiles)), "commercial_use": commercial, "seed": 42,
            "output_dir": f"./runs/{'commercial-default' if commercial else 'research-isolated'}",
            "base_model": {
                "id": MODEL_ID, "revision": MODEL_REVISION,
                "chat_template": "ernie55_chat_template.jinja", "chat_template_bridge_revision": BRIDGE_REVISION,
                "max_seq_len": 8192, "add_special_tokens": True,
            },
        },
        "paths": {"raw_root": f"{root}/raw", "processed_root": f"{root}/processed", "cache_root": f"{root}/cache"},
        "runtime": {"num_proc": 8, "trust_remote_code": False, "overwrite_processed": False},
        "defaults": {
            "sft": {"output_format": "messages", "assistant_only_loss": True, "mask_tool_outputs": True, "packing": False, "truncation": "drop", "max_seq_len": 8192},
            "preference": {"output_format": "prompt_chosen_rejected", "max_prompt_len": 4096, "max_response_len": 4096},
            "rlvr": {"output_format": "prompt_answer_verifier", "max_prompt_len": 4096, "max_response_len": 8192, "rollouts_per_prompt": 8, "temperature": 0.7, "correct_reward": 1.0, "incorrect_reward": 0.0},
        },
        "datasets": datasets,
        "profiles": rendered_profiles,
        "preflight": {
            "require_immutable_revisions": True, "require_data_quality_signoff": True,
            "require_license_signoff": True, "require_decontamination_signoff": True,
            "require_verifier_signoff_for_rlvr": True, "fail_on_disabled_dataset": True,
            "fail_on_unaccepted_gated_dataset": True, "require_no_call_negative_for_tool_profile": True,
        },
        "signoff": {"data_quality": False, "license": False, "decontamination": False, "verifier": False},
        "isolation": {
            "recipe_class": kind, "allow_cross_recipe_raw_cache_or_output_reuse": False,
            "research_to_commercial_promotion": "requires_new_manifest_and_full_license_review",
            "eval_only_assets_allowed_in_mixture": False,
        },
        "run_record": {
            "run_id": "REPLACE_ME", "resolved_manifest_sha256": "REPLACE_ME",
            "benchmark_versions": "REPLACE_ME", "decontamination_report": "REPLACE_ME",
            "data_quality_report": "REPLACE_ME", "license_review_report": "REPLACE_ME",
            "verifier_test_report": "REPLACE_ME",
            "notes": "记录实际样本数、row tokens、supervised tokens、长度分桶、删除原因和最终权重",
        },
    }


def pending_gates(dataset):
    """列出每个数据项仍需人工完成的开训门禁。"""
    license_info = dataset["license"]
    gates = []
    if license_info["upstream_review_required"]:
        gates.append("上游许可审查")
    if license_info["teacher_terms_review_required"]:
        gates.append("教师条款审查")
    gates.append("数据质量签署")
    if dataset["processing"]["decontaminate"]:
        gates.append("去污签署")
    verifier = dataset.get("verifier")
    if verifier:
        if str(verifier.get("package_revision", "")).startswith("PIN_ME"):
            gates.append("固定 Math-Verify 版本")
        if str(verifier.get("repository_revision", "")).startswith("PIN_ME"):
            gates.append("固定 Enigmata Git commit")
        gates.append("验证器签署")
    return "；".join(gates)


def recipe_sections(manifest):
    lines = []
    datasets = manifest["datasets"]
    for profile_name, profile in manifest["profiles"].items():
        lines += [f"### `{profile_name}`", "", profile["description"], "",
                  "| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |",
                  "|---|---|---|---|---|---:|---|---|"]
        for item in profile["mixture"]:
            dataset_id = item["dataset"]
            dataset = datasets[dataset_id]
            source = dataset["source"]
            lines.append(f"| `{dataset_id}` | `{source['repo_id']}` | `{source['revision']}` | `{source['subset']}` | `{source['split']}` | {item['weight']:.0%} | `{dataset['license']['commercial_status']}` | {pending_gates(dataset)} |")
        lines += ["", f"覆盖参数：`{json.dumps(profile['overrides'], ensure_ascii=False)}`", ""]
    return lines


def build_report(commercial, research, resolved_at):
    lines = [
        "# 商用默认／研究隔离训练配方", "",
        "> 数据源刷新时间：`" + resolved_at + "`。两套 Manifest 已固定 ERNIE BF16、数据 revision、config、split 和采样权重；`signoff=false` 是有意保留的开训门禁。", "",
        "## 1. 使用边界", "",
        "- **商用默认**：所有数据均为 `allowed_with_obligations`，不含 NC、`research_only` 或 `review_required`；仍需完成实际上游、教师条款、质量和去污签署。",
        "- **研究隔离**：包含非商用和许可待审数据，`commercial_use=false`；原始数据、缓存、处理结果和输出目录均与商用配方分离。",
        "- `enabled=true` 表示配方引用完整，不表示已获许可或质量批准。未下载全量数据、未执行样本级转换和训练冒烟前，不得称为已经开训就绪。",
        "- 采样权重不是行数或有效 token 占比；训练时必须记录实际采样量、row tokens 和 supervised tokens。", "",
        "- Base：`baidu/ERNIE-5.5-Flash-Base-BF16`", f"- Model revision：`{MODEL_REVISION}`", f"- Bridge／模板 revision：`{BRIDGE_REVISION}`", "",
        "## 2. 商用默认配方", "",
        f"Manifest：`commercial-default-manifest.yaml`；默认 profile：`{commercial['project']['selected_profile']}`；输出：`{commercial['project']['output_dir']}`。", "",
    ]
    lines += recipe_sections(commercial)
    lines += ["## 3. 研究隔离配方", "",
              f"Manifest：`research-isolated-manifest.yaml`；默认 profile：`{research['project']['selected_profile']}`；输出：`{research['project']['output_dir']}`。", ""]
    lines += recipe_sections(research)
    lines += [
        "## 4. 待签署门禁", "",
        "| 门禁 | 商用默认 | 研究隔离 | 完成标准 |", "|---|---|---|---|",
        "| 模型与数据不可变 revision | 已固定 | 已固定 | 物化时复核 SHA 与文件清单 |",
        "| config／split／配比 | 已固定 | 已固定 | 转换报告中保持相同口径 |",
        "| 数据质量 | 待签署 | 待签署 | 字段、角色、长度、事实、代码执行、偏好对和失败率报告 |",
        "| 数据许可、上游与教师条款 | 待签署 | 待签署；NC 不晋升商用 | 审查后将对应 review flag 置 false，并签署 `signoff.license` |",
        "| 母题／语义／翻译去污 | 待签署 | 待签署 | 对所有公开评测和私有／时间外评测出报告 |",
        "| ERNIE 模型许可 | 待签署 | 待签署 | 地域、商业通知／授权、衍生模型与蒸馏边界 |",
        "| 模板与 label mask | 待验证 | 待验证 | BOS、assistant-only、think 标签、工具输出 mask、训练推理一致 |",
        "| 数据转换器 | 待冒烟 | 待冒烟 | 每个 adapter 跑真实样本并验证 schema、空回答和截断率 |",
        "| RLVR 验证器 | Math-Verify 版本待固定 | Enigmata Git commit 待固定 | 奖励一致性、任务覆盖、攻击测试与 `signoff.verifier` |",
        "| 训练环境与导出 | 待验证 | 待验证 | GPU／互联／存储、2–10 step、保存恢复、HF 导出对比 |",
        "| 本地业务与私有评测 | 生产前必需 | 按研究目标补充 | 业务中文、正常请求、防过拒、不调用负例和私有／时间外评测 |",
        "| 更小 Base 模型 | 待提供 ID／revision | 待提供 ID／revision | 不直接复制 ERNIE 的 Muon、并行和学习率 |", "",
        "## 5. 校验与切换 profile", "",
        "```bash",
        "python build_training_recipes.py",
        "python validate_training_recipes.py  # 一次校验全部 10 个 profile 与路径隔离",
        "python validate_post_training_manifest.py commercial-default-manifest.yaml --profile commercial_math_rlvr --allow-placeholders",
        "python validate_post_training_manifest.py research-isolated-manifest.yaml --profile research_enigmata_rlvr --allow-placeholders",
        "# 完成真实审查后，去掉 --allow-placeholders 运行严格模式",
        "python validate_post_training_manifest.py commercial-default-manifest.yaml",
        "python validate_post_training_manifest.py research-isolated-manifest.yaml",
        "```", "",
        "`--allow-placeholders` 只证明结构、权重和引用有效，**不是开训凭证**。完成真实审查后移除该参数；严格模式通过才允许进入具体训练框架配置生成。", "",
        "研究数据要进入商用配方时，必须新建商用 Manifest 项并重新完成许可、上游、教师、质量和去污审查；禁止只改 `commercial_status` 或复用研究输出目录。",
    ]
    return "\n".join(lines) + "\n"


def main():
    assets, repositories, resolved_at = load_sources()
    commercial = make_manifest("commercial", COMMERCIAL_PROFILES, assets, repositories, resolved_at)
    research = make_manifest("research", RESEARCH_PROFILES, assets, repositories, resolved_at)
    for filename, doc in [("commercial-default-manifest.yaml", commercial), ("research-isolated-manifest.yaml", research)]:
        (ROOT / filename).write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    (ROOT / "training-recipes.md").write_text(build_report(commercial, research, resolved_at), encoding="utf-8")
    print(json.dumps({
        "commercial": {"datasets": len(commercial["datasets"]), "profiles": len(commercial["profiles"])},
        "research": {"datasets": len(research["datasets"]), "profiles": len(research["profiles"])},
        "unique_sources": len(set(commercial["datasets"]) | set(research["datasets"])),
        "source_resolved_at": resolved_at,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
