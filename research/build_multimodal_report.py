#!/usr/bin/env python3
"""Build the Chinese multimodal research report from canonical and official snapshots."""
from collections import Counter
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOC = yaml.safe_load((ROOT / "datasets-list.yaml").read_text(encoding="utf-8"))
MM = yaml.safe_load((ROOT / "datasets-multimodal.yaml").read_text(encoding="utf-8"))
ASSETS = MM["datasets"]
BY_ID = {item["id"]: item for item in ASSETS}
SNAPSHOT = json.loads((ROOT / "research" / "multimodal-official-cards.json").read_text(encoding="utf-8"))
HF_OK = sum("metadata" in record for record in SNAPSHOT)
HF_ERROR = len(SNAPSHOT) - HF_OK


def link(asset_id, label=None):
    item = BY_ID[asset_id]
    url = item["source"]["url"]
    if not url.startswith("https://"):
        return label or item["name"]
    return f"[{label or item['name']}]({url})"


def asset_rows(ids):
    lines = []
    for asset_id in ids:
        item = BY_ID[asset_id]
        scale = item["scale"]
        size = f"{scale['value']:,} " if scale["value"] is not None else "未填固定值；"
        lines.append(
            f"| {item['name']}<br>`{asset_id}` | {', '.join(item['modalities'])} | {', '.join(item['stages'])}／{item['usage_tier']} | "
            f"{size}{scale['unit']}；{scale['note']} | {item['license']['id']} | {link(asset_id, '官方来源')} |"
        )
    return lines


counts = Counter(item["usage_tier"] for item in ASSETS)
verification = Counter(item["verification"]["status"] for item in ASSETS)
modality_counts = Counter(modality for item in ASSETS for modality in item["modalities"])
lines = [
    "# 多模态 Base 模型后训练数据集调研与物料清单",
    "",
    "> 快照：2026-11-09。范围是图像、视频、音频与 GUI Agent 的后训练理解、指令、偏好／奖励、RLVR、安全和独立评测；不纳入媒体生成、raw caption、特征对齐预训练或 mid-training。",
    "",
    "## 1. 结论与交付边界",
    "",
    f"本次在保留原 **114 项文本资产**的基础上新增 **{len(ASSETS)} 项多模态资产、{len(MM['coverage_requirements'])} 项能力**，合并后 canonical 共 **{len(DOC['datasets'])} 项资产、{len(DOC['coverage_requirements'])} 项能力**。新增部分包含 **{len(ASSETS)-counts['eval_only']} 项训练／研究／本地物料**和 **{counts['eval_only']} 项 eval_only 独立评测**。",
    "",
    "这里的“补齐”是能力与治理覆盖闭合，不是穷尽公开数据，也不代表获得训练或商用授权。现有 `commercial-default-manifest.yaml` 与 `research-isolated-manifest.yaml` 仍是 **ERNIE 文本专用**；多模态 Base、processor、输入契约和硬件未指定前，不生成虚构的多模态启动配方。",
    "",
    f"官方 HF 批量快照共请求 **{len(SNAPSHOT)} 个候选 repo**：**{HF_OK} 个成功、{HF_ERROR} 个当前返回 401**。成功项记录了 SHA、lastModified、gated、license、configs、features 和可得行数；失败项只保留官方项目／论文口径，不编造 revision。该比例是元数据可访问率，不是样本内容审计率。",
    "",
    "![多模态资产与能力覆盖](research/multimodal-asset-coverage.png)",
    "",
    "### 新增资产分层",
    "",
    "| 指标 | 数量 | 说明 |",
    "|---|---:|---|",
]
for tier in ("core", "optional", "research_only", "eval_only", "local_required"):
    lines.append(f"| {tier} | {counts[tier]} | 多模态扩展实际计数 |")
for modality in ("text", "image", "video", "audio"):
    lines.append(f"| modality={modality} | {modality_counts[modality]} | 集合计数；多模态资产可重复属于多个模态 |")
lines += [
    "",
    "## 2. 调研方法与召回入口",
    "",
    "调研经过多轮主题检索，先覆盖 MLLM 后训练索引，再分别核查视觉指令、PixMo、视频、文档／OCR、偏好、RLVR、GUI、音频、安全、中文／多语言和独立评测。awesome 清单只用于召回，规模、许可、split 和字段回到官方项目、论文或 Hugging Face 数据卡。",
    "",
    "- [Awesome Post-Training for MLLMs](https://github.com/zchoi/Awesome-Post-Training-for-MLLMs)：召回 MLLM SFT、偏好与 RL 方向。",
    "- [awesome-llm-post-training](https://github.com/mbzuai-oryx/awesome-llm-post-training)：交叉检查训练阶段分类。",
    "- [awesome-instruction-dataset](https://github.com/yaodongC/awesome-instruction-dataset)：补指令数据入口，不直接继承二手许可和规模。",
    "- [LLaVA-OneVision-2](https://github.com/EvolvingLMMs-Lab/LLaVA-OneVision-2)：核对新一代图像／视频配方与 22M Instruct、FineVision、长视频数据的关系。",
    "- [AudioBench](https://github.com/AudioLLMs/AudioBench)：核对音频评测是 50+ 任务套件，而不是可随意汇总行数的同质数据集。",
    "",
    "完整官方元数据快照见 `research/multimodal-official-cards.json`；紧凑切分与字段摘要见 `research/multimodal-metadata-summary.json`。这些文件只保存元数据和数据卡文本，不下载全量媒体样本。",
    "",
    "## 3. 通用图像指令、文档、定位与计数",
    "",
    "| 数据集／ID | 模态 | 阶段／层级 | 规模与口径 | 许可口径 | 来源 |",
    "|---|---|---|---|---|---|",
]
lines += asset_rows(["llava_instruct_150k", "llava15_mix665k", "llava_onevision15_instruct_22m", "finevision", "pixmo_ask_model_anything", "pixmo_points", "pixmo_point_explanations", "pixmo_docs", "pixmo_count_train", "pixmo_cap_qa"])
lines += [
    "",
    "关键边界：",
    "",
    "1. **LLaVA-Instruct-150K、LLaVA-1.5 Mix665K 和 558K 特征对齐预训练不是同一资产**；最后一项不在本后训练清单。",
    "2. **OneVision 的 part-* 与完整 config 可能重复，FineVision 也含完整集和分片**；不能把全部 config 行数直接求和。Merged46M 必须先做来源与内容去重。",
    "3. **PixMo 的样本行数不等于点、物体或媒体文件数**；图像 URL 可用率、SHA、隐私和上游图像权利是独立门禁。",
    "4. `pixmo_count_train` 与 `pixmo_count_test` 同 repo 但拆资产；test 540 条永远禁止训练。",
    "",
    "## 4. 多图、视频与时空理解",
    "",
    "| 数据集／ID | 模态 | 阶段／层级 | 规模与口径 | 许可口径 | 来源 |",
    "|---|---|---|---|---|---|",
]
lines += asset_rows(["mantis_instruct", "llava_video_178k", "videochat_flash_training", "molmo2_videotrack", "molmo2_videopoint"])
lines += [
    "",
    "Mantis 的约 721K 是论文中的 14 个多图核心子集口径，当前 HF 还含单图补集。部分多图样本由单图对话拼接，且与 LLaVA、DocVQA、ChartQA 存在上游重叠。[Mantis 官方项目](https://github.com/TIGER-AI-Lab/Mantis)",
    "",
    "LLaVA-Video-178K 的 178K 指视频来源，不是 QA 总量；caption、open-ended、multiple-choice 和时长／来源 config 分开。视频训练记录必须包含媒体哈希、FPS、帧数、时长、是否使用字幕、媒体 token 和 supervised text token。[LLaVA-Video 官方论文](https://arxiv.org/abs/2410.02713)",
    "",
    "## 5. 多模态偏好、推理蒸馏与 RLVR",
    "",
    "| 数据集／ID | 模态 | 阶段／层级 | 规模与口径 | 许可口径 | 来源 |",
    "|---|---|---|---|---|---|",
]
lines += asset_rows(["llava_human_preference_10k", "rlhf_v", "rlaif_v", "vlfeedback", "povid", "r1_onevision", "visual_rft_tasks"])
lines += [
    "",
    "偏好数据按三类分开：**人类修正／排序、AI 反馈、构造负例**。不得把 pair 展开数当独立提示数，也不得把 chosen 默认成安全答案。VL-RewardBench 当前卡片为 1,247 条，和论文常用的 1,250 口径差异被显式保留。[VL-RewardBench 官方项目](https://vl-rewardbench.github.io/)",
    "",
    "RLVR 与推理蒸馏必须分离：长 CoT 文件属于 SFT；在线 RL 需要 prompt、ground truth／环境和任务验证器。Visual-RFT 的分类正确性、检测 IoU、grounding 坐标和格式奖励不能合并为一个“通用正确性”。[Visual-RFT 官方论文](https://arxiv.org/html/2503.01785v1)",
    "",
    "## 6. 音频指令、GUI Agent 与安全",
    "",
    "| 数据集／ID | 模态 | 阶段／层级 | 规模与口径 | 许可口径 | 来源 |",
    "|---|---|---|---|---|---|",
]
lines += asset_rows(["voice_assistant_400k", "os_atlas_action_sft", "gui_odyssey_train", "android_control_train", "vlguard_train", "spa_vl_train", "safe_vid_350k", "local_multimodal_sft", "local_multimodal_preference", "local_gui_action_safety"])
lines += [
    "",
    "VoiceAssistant 当前公开 train 为 470,054 条，不能沿用名称中的 400K；`answer_snac` 是 codec token，不等于直接提供波形。训练前固定采样率、SNAC 解码器、说话人、文本／音频 loss mask 和输出模态。[Mini-Omni 官方项目](https://github.com/gpt-omni/mini-omni)",
    "",
    "GUI 的 13M elements、episode、action step、在线 task 是四种不同单位。OS-Atlas 只登记 action SFT，grounding 预训练不冒充 Agent 轨迹；GUIOdyssey 必须在 random／task／device／app 中选择一种官方切分并配套对应测试。[OS-Atlas](https://osatlas.github.io/), [GUIOdyssey](https://github.com/OpenGVLab/GUI-Odyssey)",
    "",
    "安全侧同时评估危险请求攻击成功率、正常请求效用、幻觉和过拒。SPA-VL 的 train／validation／HarmEval／HelpEval 分开；MM-SafetyBench 为 CC BY-NC 4.0，只进研究评测隔离。[SPA-VL](https://sqrtizhang.github.io/SPA-VL/), [MM-SafetyBench](https://github.com/isXinLiu/MM-SafetyBench)",
    "",
    "**音频公开人类偏好与可验证 RL 数据仍是缺口。** 本版没有为追求阶段齐全而虚构公共数据，改由 `local_multimodal_preference` 明确本地建设责任，VoiceBench 仅用于独立语音助手评测。",
    "",
    "## 7. 独立评测与中文覆盖",
    "",
    "所有公共 benchmark 均为 `eval_only`。同 repo 训练／测试拆资产，judge 输出不得反哺训练；图像尺寸、视频抽帧、字幕、音频采样、选项协议和评分器均需固定。",
    "",
    "| 领域 | 独立评测 |",
    "|---|---|",
    f"| 综合视觉与推理 | {', '.join(link(x) for x in ['mmmu_validation', 'mmmu_pro_standard10', 'mmstar', 'mathvista_testmini', 'mathvision_test'])} |",
    f"| 文档、图表与 OCR | {', '.join(link(x) for x in ['docvqa_validation', 'chartqa_test', 'ocrbench'])} |",
    f"| 多图与视频 | {', '.join(link(x) for x in ['mantis_eval', 'video_mme', 'mlvu', 'longvideobench'])} |",
    f"| 偏好、幻觉与安全 | {', '.join(link(x) for x in ['vl_rewardbench', 'mmhal_bench', 'mm_safetybench', 'figstep', 'safevidbench'])} |",
    f"| GUI | {', '.join(link(x) for x in ['screenspot_v2', 'gui_odyssey_test', 'osworld_verified', 'androidworld'])} |",
    f"| 音频 | {', '.join(link(x) for x in ['voicebench', 'mmau', 'audiobench', 'air_bench'])} |",
    f"| 中文／多语言 | {', '.join(link(x) for x in ['cmmmu_test', 'cmmu', 'mmbench_cn', 'audiobench'])} |",
    "",
    "CMMMU 全集 12,012 题，dev 112、validation 900、test 11,000；本清单只把 test 11,000 作为该资产规模。CMMU 的 validation 与 hosted test 分开，填空题使用规则或 GPT judge 的分数不能直接混比。[CMMMU](https://github.com/CMMMU-Benchmark/CMMMU), [CMMU](https://github.com/FlagOpen/CMMU)",
    "",
    "**中文公开 benchmark 不等于中文训练数据。** 当前中文／多语言训练主要依赖 OneVision／FineVision 中经审查的子集和本地真实业务多模态 SFT；公开中文评测不能反向转训练。",
    "",
    "## 8. 能力覆盖矩阵",
    "",
    "| 能力 | 训练候选数 | 独立评测引用数 | 训练候选 | 独立评测 |",
    "|---|---:|---:|---|---|",
]
for cap, rule in MM["coverage_requirements"].items():
    lines.append(f"| `{cap}` | {len(rule['training_candidates'])} | {len(rule['eval_ids'])} | {', '.join('`'+x+'`' for x in rule['training_candidates'])} | {', '.join('`'+x+'`' for x in rule['eval_ids'])} |")
lines += [
    "",
    "## 9. 延期、范围外与未闭合缺口",
    "",
    "| 候选 | 状态 | 原因 |",
    "|---|---|---|",
]
for item in MM["excluded_or_deferred_candidates"]:
    lines.append(f"| {item['name']} | {item['status']} | {item['reason']} |")
lines += [
    "",
    "仍需训练前闭合的缺口：",
    "",
    "1. 大合集逐 config 的上游许可、教师条款、媒体权利和重复谱系尚未全部签署。",
    "2. 当前调研未下载全量媒体、未执行完整样本级质量审核，也未测量 URL 失效率、图像／视频／音频有效时长和 supervised tokens。",
    "3. 多模态 RLVR 验证器、GUI 在线环境、音频 codec 和模型 processor 必须在具体 Base 确定后实际重跑。",
    "4. 中文人工多模态指令、多语言人类偏好、公开音频偏好／RLVR、真实业务 GUI 危险动作和私有时间外评测仍需本地建设。",
    "",
    "## 10. 训练前门禁",
    "",
]
for item in DOC["global_preflight"]:
    lines.append(f"- [ ] {item}")
lines += [
    "- [ ] 多模态配方另行确认 Base 模型、processor、媒体输入契约和硬件；不得复用 ERNIE 文本配方冒充多模态配方。",
    "",
    "机器校验：`python validate_datasets_list.py datasets-list.yaml --expect-total 175`。",
    "",
]
import sys
sys.path.insert(0, str(ROOT))
from dataset_markdown_links import link_dataset_table_entries
report = link_dataset_table_entries("\n".join(lines), {item["id"]: item for item in DOC["datasets"]})
(ROOT / "multimodal-post-training-datasets-zh.md").write_text(report, encoding="utf-8")
print(f"Wrote multimodal report: {len(ASSETS)} assets, {len(MM['coverage_requirements'])} capabilities, HF {HF_OK}/{len(SNAPSHOT)}")
print("verification:", dict(sorted(verification.items())))
