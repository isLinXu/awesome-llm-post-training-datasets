#!/usr/bin/env python3
"""Curated multimodal extension merged by build_datasets_list.py.

Only post-training understanding/alignment assets are included. Media generation,
raw captioning and modality-alignment pretraining are deliberately out of scope.
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
TODAY = "2026-11-09"
MM_CAPS = {
    "visual_instruction", "visual_grounding", "visual_counting", "document_chart_ocr",
    "multiimage_video", "visual_reasoning_rlvr", "visual_preference_rm",
    "audio_instruction", "audio_preference_rl", "gui_agent", "multimodal_safety",
    "multilingual_multimodal",
}
ASSETS = []


def add(id, name, category, stages, tier, value, unit, note, url, repo, lic, comm,
        access, fmt, caps, risks, rec, modalities, split="train", config=None,
        sha=None, verified="official_checked", relations=None):
    assert set(caps) <= MM_CAPS, (id, set(caps) - MM_CAPS)
    source = {
        "provider": "huggingface" if repo else ("local" if access == "local" else "official_project"),
        "repo_id": repo, "url": url, "split": split,
        "revision_policy": "pin_immutable_revision_before_use",
    }
    if config:
        source["config"] = config
    if sha:
        source["observed_revision"] = sha
    ASSETS.append({
        "id": id, "name": name, "category": category, "stages": stages,
        "usage_tier": tier, "modalities": modalities,
        "scale": {"value": value, "unit": unit, "note": note},
        "source": source, "data_format": fmt, "capabilities": caps,
        "license": {"id": lic, "commercial_status": comm,
                    "upstream_and_teacher_terms_review_required": comm != "internal_review_required"},
        "access": access, "risks": risks, "recommendation": rec,
        "train_prohibited": tier == "eval_only", "eval_isolation_required": tier == "eval_only",
        "relations": relations or [],
        "verification": {"status": verified, "checked_at": TODAY},
    })


def hf(id, name, category, stages, tier, value, unit, note, repo, lic, comm, fmt,
       caps, risks, rec, modalities=("text", "image"), split="train", config=None,
       sha=None, access="public", verified="official_checked", relations=None):
    add(id, name, category, stages, tier, value, unit, note,
        f"https://huggingface.co/datasets/{repo}", repo, lic, comm, access, fmt,
        caps, risks, rec, list(modalities), split, config, sha, verified, relations)


def project(id, name, category, stages, tier, value, unit, note, url, lic, comm,
            fmt, caps, risks, rec, modalities=("text", "image"), split="train",
            verified="official_checked", relations=None, access="public"):
    add(id, name, category, stages, tier, value, unit, note, url, None, lic, comm,
        access, fmt, caps, risks, rec, list(modalities), split, None, None, verified, relations)


def ev(id, name, value, unit, note, url, repo, caps, rec, lic="mixed-see-official-card",
       modalities=("text", "image"), split="test", config=None, sha=None,
       verified="official_checked"):
    add(id, name, "evaluation", ["evaluation"], "eval_only", value, unit, note,
        url, repo, lic, "eval_only", "public", "multimodal_evaluation", caps,
        ["公开多模态评测污染", "固定媒体文件、split、prompt、抽帧／解码和评分器版本"],
        [rec], list(modalities), split, config, sha, verified)


# 通用图像指令与大规模混合集。预训练／mid-training 不在此登记。
hf("llava_instruct_150k", "LLaVA-Instruct-150K", "vision_sft", ["sft"], "research_only",
   157710, "instruction_samples", "当前 FineVision 同名子集也为 157,710；不得与 558K 特征对齐集混写",
   "liuhaotian/LLaVA-Instruct-150K", "CC-BY-4.0 + GPT-4/upstream-terms", "noncommercial",
   "image_conversations", ["visual_instruction", "multilingual_multimodal"],
   ["GPT-4 输出与原始图像上游条款", "LLaVA 项目研究／非商用约束"],
   ["仅作研究视觉指令基线；与 FineVision、LLaVA-1.5、Mantis 按来源去重"],
   sha="9d451dc7629cfe0469f6ae4432b765cd603d5fcb")
project("llava15_mix665k", "LLaVA-1.5 Mix665K", "vision_sft", ["sft"], "research_only",
   665000, "samples_approx", "学术任务与 GPT 生成指令混合；558K 是特征对齐预训练，不属于本资产",
   "https://github.com/haotian-liu/LLaVA", "research/noncommercial + mixed-upstream", "noncommercial",
   "multi_source_image_conversations", ["visual_instruction", "document_chart_ocr"],
   ["非商用", "多上游图像和教师条款", "与 Mantis、FineVision、OneVision 大量重叠"],
   ["研究隔离的经典视觉 SFT 配方基线，不进入商用默认"],
   relations=[{"type": "overlap", "target": "llava_instruct_150k", "action": "source_and_content_deduplicate"}])
hf("llava_onevision15_instruct_22m", "LLaVA-OneVision-1.5-Instruct-Data", "vision_sft", ["sft"], "optional",
   22000000, "samples_approx", "22M 官方口径、124 类；part-* 与完整 config 可能重复，不能对全部 config 行数求和",
   "mvp-lab/LLaVA-OneVision-1.5-Instruct-Data", "Apache-2.0 + mixed-upstream", "review_required",
   "image_conversations_by_source", ["visual_instruction", "visual_grounding", "visual_counting", "document_chart_ocr", "visual_reasoning_rlvr", "multilingual_multimodal"],
   ["多上游许可和 GPT 教师输出", "含医学等范围外 config，必须逐 config 选择", "与 PixMo、FineVision、文本数学／代码数据重叠"],
   ["按 config 建立配方，不做全包无差别训练；固定 22M 版本并逐来源签署"],
   sha="0efb7ad47f8ba36e1d262545cadec4cd8960dc5f",
   relations=[{"type": "overlap", "target": "pixmo_docs", "action": "source_level_deduplicate"}, {"type": "overlap", "target": "llava_instruct_150k", "action": "source_level_deduplicate"}])
hf("finevision", "FineVision", "vision_sft", ["sft"], "optional", 24000000, "samples_approx",
   "约 24M；200+ config 含完整集与分片，禁止直接汇总所有 config",
   "HuggingFaceM4/FineVision", "no-unified-license-in-card + mixed-upstream", "review_required",
   "multiimage_messages_quality_ratings", ["visual_instruction", "visual_grounding", "document_chart_ocr", "multiimage_video", "gui_agent", "multilingual_multimodal"],
   ["当前卡片无统一许可字段", "含 LLaVA、GUI、医学等异质来源", "与 OneVision 合并必须去重"],
   ["作为大规模待审混合池；逐 config 审许可、媒体权利和评测污染"],
   sha="3c380a731a3429c1d04693d6ec16d7e683def84c",
   relations=[{"type": "overlap", "target": "llava_instruct_150k", "action": "source_level_deduplicate"}, {"type": "overlap", "target": "llava_onevision15_instruct_22m", "action": "deduplicate_before_merged46m"}])

# PixMo 人工／程序标注系列，config、split 与媒体可用性分别审查。
hf("pixmo_ask_model_anything", "PixMo-Ask-Model-Anything", "vision_sft", ["sft"], "core", 161737, "samples",
   "default/train 精确行数；图像通过 URL＋SHA 引用", "allenai/pixmo-ask-model-anything", "ODC-By", "allowed_with_obligations",
   "image_url_question_answer", ["visual_instruction"], ["图像 URL 失效、隐私与上游图像权利", "答案开放域质量需抽检"],
   ["开放视觉指令主候选；下载时核对 image_sha256、可用率和隐私"], sha="739ffd8b417737da31e5069b9c8ff6a72a7d58b6")
hf("pixmo_points", "PixMo-Points", "vision_grounding", ["sft"], "core", 2376222, "samples",
   "default/train 精确行数；每行可含多个点，行数不等于点数", "allenai/pixmo-points", "ODC-By", "allowed_with_obligations",
   "image_points_count_label", ["visual_grounding", "visual_counting"], ["坐标系、图像缩放和无效 URL", "集合标签许可不替代图像权利审查"],
   ["定位与计数主候选；固定坐标归一化和点／样本两种配比"], sha="2b5c6931e790e00ae00d4a2857e5f95d88f09a66")
hf("pixmo_point_explanations", "PixMo-Point-Explanations", "vision_grounding", ["sft"], "optional", 79551, "samples",
   "default/train 精确行数；含解析点与文本解释", "allenai/pixmo-point-explanations", "ODC-By", "allowed_with_obligations",
   "image_question_response_points", ["visual_grounding", "visual_instruction"], ["文本中的点需与 parsed_response 一致", "图像 URL 和隐私审查"],
   ["可解释指向补集；分别监督文本和点坐标并做解析校验"], sha="08a566fa00747e4c1c7e8481c350763b469c209c")
hf("pixmo_docs", "PixMo-Docs", "document_sft", ["sft"], "core", 251165, "train_samples_total",
   "charts 116,814＋diagrams 16,551＋other 71,282＋tables 46,518；各 config 另有 1,024 validation",
   "allenai/pixmo-docs", "ODC-By", "allowed_with_obligations", "document_images_questions",
   ["document_chart_ocr", "visual_instruction"], ["四 config 分布不同", "文档隐私、图像权利和 validation 隔离"],
   ["文档／图表主候选；固定四 config train，validation 不进训练"], split="train", config="charts,diagrams,other,tables", sha="d887597bf4af2bc61a4210071a8cef898287e6fb")
hf("pixmo_count_train", "PixMo-Count train", "vision_grounding", ["sft"], "core", 36916, "train_samples",
   "train 36,916；validation/test 各 540，独立资产隔离", "allenai/pixmo-count", "ODC-By", "allowed_with_obligations",
   "image_count_points_label", ["visual_counting", "visual_grounding"], ["点与计数必须一致", "同图跨 split 泄漏检查"],
   ["计数训练主候选；只用 train，并按图像 SHA 对测试集去污"], split="train", sha="ebf51cf70e45d12374e64d475862e4f8d21d31d0")
hf("pixmo_cap_qa", "PixMo-Cap-QA", "vision_sft", ["sft"], "optional", 271714, "samples",
   "default/train 精确行数；caption-conditioned QA", "allenai/pixmo-cap-qa", "ODC-By", "allowed_with_obligations",
   "image_caption_question_answer", ["visual_instruction", "document_chart_ocr"], ["依赖图像描述可能引入二阶错误", "图像 URL 与文本质量"],
   ["细粒度视觉问答补集；抽检问题是否真正需要图像"], sha="fd3ff4b2905455ab5edfd6d06039ea6027948521")

# 多图、视频与时空定位。
hf("mantis_instruct", "Mantis-Instruct", "multiimage_sft", ["sft"], "optional", 721000, "samples_approx",
   "官方论文约 721K、14 个多图核心子集；当前 HF 还含单图补集，分别按 config 计数",
   "TIGER-Lab/Mantis-Instruct", "Apache-2.0 + mixed-upstream", "review_required",
   "multiimage_conversations", ["multiimage_video", "visual_instruction", "document_chart_ocr"],
   ["多上游许可、视频来源和 GPT-4 输出", "部分多图样本由单图拼接", "与 LLaVA／DocVQA／ChartQA 重叠"],
   ["按 14 个核心 config 做跨图指代、比较、推理和时序消融"], config="14_core_configs", sha="01a9edfe0bb8c2582431308c5b2645a9f4796939",
   relations=[{"type": "overlap", "target": "llava15_mix665k", "action": "source_level_deduplicate"}])
hf("llava_video_178k", "LLaVA-Video-178K", "video_sft", ["sft"], "optional", 178000, "source_videos",
   "178K 是视频数；论文约 1.6M 指令，caption/open_ended/multi_choice 分开，不写成 178K QA",
   "lmms-lab/LLaVA-Video-178K", "no-explicit-license-in-card + mixed-video-upstream", "review_required",
   "video_instruction_by_duration_and_type", ["multiimage_video"], ["当前卡片无统一许可", "YouTube／学术视频与 GPT-4o 条款", "媒体下载漂移"],
   ["按视频时长、来源和问答类型建 profile；固定媒体哈希和字幕协议"], config="by_duration_and_source", sha="6d8c562dc26d70042a0d9704d1cae58c94b89098", modalities=("text", "image", "video"))
hf("videochat_flash_training", "VideoChat-Flash-Training-Data", "video_sft", ["sft"], "optional", None, "video_instruction_samples",
   "长上下文视频指令混合包；当前 API 未提供统一切分行数", "OpenGVLab/VideoChat-Flash-Training-Data", "Apache-2.0 + mixed-upstream", "review_required",
   "long_video_instructions", ["multiimage_video"], ["上游视频与教师条款", "长视频存储、抽帧和时间标注成本"],
   ["长视频指令补集；固定子目录、媒体清单和帧预算"], sha="be87f5516a709be079cec8b727dd2287bf2dd70f", modalities=("text", "image", "video"))
hf("molmo2_videotrack", "Molmo2-VideoTrack", "video_sft", ["sft"], "optional", None, "video_track_samples",
   "default/train；当前 API 未提供固定行数", "allenai/Molmo2-VideoTrack", "ODC-By", "allowed_with_obligations",
   "video_temporal_tracks", ["multiimage_video", "visual_grounding"], ["视频上游权利和轨迹标注噪声", "时间戳与帧率绑定"],
   ["视频跟踪补集；固定 2fps／原始时间戳协议并验证轨迹"], sha="5940b8225a8565f7793f7090f6bf69909237434d", modalities=("text", "image", "video"))
hf("molmo2_videopoint", "Molmo2-VideoPoint default", "video_sft", ["sft"], "core", 658340, "train_samples",
   "default/train 精确行数；其他类别 config 不与其直接相加", "allenai/Molmo2-VideoPoint", "ODC-By", "allowed_with_obligations",
   "video_question_timestamped_points", ["multiimage_video", "visual_grounding", "visual_counting"],
   ["default 与类别 config 可能重复", "标注 unsure、时间戳和坐标验证", "视频上游权利"],
   ["时空指向主候选；固定 default/train，过滤 unsure 并验证点／时间戳"], config="default", sha="65a7347ebbb501a14002418877e9a7de43510047", modalities=("text", "image", "video"))

# 视觉偏好：人类修正、AI 反馈和构造负例分开。
hf("llava_human_preference_10k", "LLaVA-Human-Preference-10K", "multimodal_preference", ["preference", "reward_model"], "optional", None, "human_preference_pairs",
   "名称 10K，公开项目约 9.42K；当前 API 无切分行数", "zhiqings/LLaVA-Human-Preference-10K", "Apache-2.0 + upstream-terms", "review_required",
   "image_prompt_chosen_rejected_human", ["visual_preference_rm"], ["图像与原始响应上游条款", "名称不等于精确行数"],
   ["人类视觉偏好基线；固定文件后按独立提示计数"], sha="e60c9e520dde0c331f1b833ec991789ed238554c")
project("rlhf_v", "RLHF-V", "multimodal_preference", ["preference", "reward_model"], "research_only", 1400, "segment_level_human_corrections_approx",
   "约 1.4K 段级人类修正，不与整句偏好对直接等量混合", "https://github.com/rlhf-v/rlhf-v", "CC-BY-NC-4.0", "noncommercial",
   "segment_level_human_correction", ["visual_preference_rm"], ["非商用", "细粒度修正与整句 pair 标注单位不同"],
   ["非商用人类细粒度幻觉修正研究；单独建 profile"])
hf("rlaif_v", "RLAIF-V-Dataset", "multimodal_preference", ["preference", "reward_model"], "research_only", None, "ai_feedback_pairs",
   "开源模型反馈；当前卡片未给切分行数", "openbmb/RLAIF-V-Dataset", "CC-BY-NC-4.0", "noncommercial",
   "image_question_chosen_rejected_ai", ["visual_preference_rm"], ["非商用", "AI 反馈偏差和上游图像权利"],
   ["非商用 AI 反馈对照组；不得与人类偏好混称人工标注"], sha="cdfc8c13778434e38afd538b0641ea942df4af78")
hf("vlfeedback", "VLFeedback", "multimodal_preference", ["preference", "reward_model"], "optional", 80258, "prompts",
   "default/train 80,258 提示；多模型回答可展开 pair，但 pair 数不等于独立提示数", "MMInstruction/VLFeedback", "no-explicit-license-in-card + GPT-4V/upstream", "review_required",
   "image_prompt_multi_model_ai_feedback", ["visual_preference_rm"], ["当前无统一许可", "GPT-4V 反馈与多供应商输出条款", "偏好对膨胀"],
   ["大规模 AI 反馈补集；按独立提示切分并保留模型来源"], sha="137dcea93e7667decc117c54b60f7401c6903310")
hf("povid", "POVID preference data", "multimodal_preference", ["preference", "reward_model"], "optional", None, "constructed_preference_pairs",
   "构造负例偏好数据；当前 API 未给切分行数", "YiyangAiLab/POVID_preference_data_for_VLLMs", "CC-BY-4.0 + upstream-terms", "review_required",
   "image_prompt_constructed_negative", ["visual_preference_rm"], ["构造负例不等于人类偏好", "负例类型单一可能造成风格捷径"],
   ["构造幻觉负例补集；与人工和 AI 反馈分组消融"], sha="177dd9493f865950a3bec48ef6b9ffd7b50e3f73")

# 推理蒸馏与规则奖励任务分资产登记。
hf("r1_onevision", "R1-Onevision", "multimodal_reasoning", ["sft", "rlvr"], "optional", None, "reasoning_samples_and_rl_tasks",
   "自然场景、科学、数学、OCR 和图表；SFT 与 RL 文件／配置必须分别固定", "Fancy-MLLM/R1-Onevision", "Apache-2.0 + mixed-upstream", "review_required",
   "image_formalized_reasoning_and_verifier_tasks", ["visual_reasoning_rlvr"], ["蒸馏轨迹不等于 RLVR 题集", "不同任务验证器和上游许可不同"],
   ["按任务拆分 SFT 与 RL；数学、OCR、检测等奖励分别重跑"], sha="904e96cb76d92ae40746e84c6b9809eb839937fd")
project("visual_rft_tasks", "Visual-RFT task data", "multimodal_rlvr", ["rlvr"], "research_only", None, "task_specific_rl_configs",
   "分类、检测、grounding 等任务分别使用官方数据与奖励；不是一个无差别全量包", "https://arxiv.org/html/2503.01785v1", "mixed-see-task-upstream", "review_required",
   "image_task_prompt_rule_verifier", ["visual_reasoning_rlvr", "visual_grounding"], ["COCO／LVIS／LISA 等上游许可不同", "IoU、分类和格式奖励不可混作通用正确性"],
   ["按任务和固定切分复现；验证器签署后才进入 RLVR 配方"])

# GUI：grounding 与 action trajectory 分开；AndroidControl 当前 API 401，保留部分核验状态。
hf("os_atlas_action_sft", "OS-Atlas action fine-tuning data", "gui_agent", ["agent_sft"], "core", None, "gui_action_samples",
   "只登记下游 action SFT；13M GUI elements 属 Base grounding 预训练，不冒充 Agent 轨迹", "OS-Copilot/OS-Atlas-Data", "Apache-2.0 + upstream-terms", "allowed_with_obligations",
   "screenshot_history_action", ["gui_agent", "visual_grounding"], ["grounding 与 action 子目录不同", "截屏隐私、账号和坐标／动作 schema"],
   ["GUI 动作 SFT 候选；只选 action 子集并固定平台、历史和动作 schema"], config="action_sft_only", sha="e3a4c90c5f6129c25efdaa0671b08a11f7cb8f3f")
hf("gui_odyssey_train", "GUIOdyssey train splits", "gui_agent", ["agent_sft"], "core", 8834, "episodes_total_before_split",
   "全集 8,834 episodes；实际训练量取决于 random/task/device/app 官方 split，不能写为单一训练行数", "hflqf88888/GUIOdyssey", "CC-BY-4.0", "allowed_with_obligations",
   "cross_app_screenshot_action_episodes", ["gui_agent", "multiimage_video"], ["episode 与 action step 不可混计", "四种 split 不能交叉泄漏", "截屏隐私和失败轨迹"],
   ["跨 App 轨迹主候选；每次实验固定一种官方 split 和动作历史长度"], split="official_train_split", config="random|task|device|app", sha="61632d0f3f4d51d7e9561ce4f84347dd06b2019d")
project("android_control_train", "AndroidControl train", "gui_agent", ["agent_sft"], "research_only", None, "gui_action_episodes",
   "High-Level／Low-Level 与训练／测试分开；当前 HF API 401，未登记精确规模", "https://github.com/google-research/google-research/tree/master/android_control", "mixed-see-official-card", "review_required",
   "android_screenshot_action_episodes", ["gui_agent"], ["当前直接数据卡未核验", "高低级指令、设备切分和测试泄漏"],
   ["访问恢复后补齐 revision、许可和 split；此前只作研究候选"], verified="partial_official_reference")

# 音频后训练。原始 ASR/TTS 预训练集不单独纳入。
hf("voice_assistant_400k", "VoiceAssistant-400K", "audio_sft", ["sft"], "optional", 470054, "train_samples",
   "当前 default/train 470,054，不是名称中的 400K；question_audio＋文本答案＋answer_snac", "gpt-omni/VoiceAssistant-400K", "Apache-2.0 + GPT-4o/TTS-terms", "review_required",
   "speech_question_text_answer_snac", ["audio_instruction"], ["英文合成语音与教师／TTS 条款", "回答音频是 SNAC token 而非普通波形", "缺少独立测试切分"],
   ["语音助手 SFT 候选；固定采样率、SNAC codec、说话人和文本／音频 loss mask"], sha="65dab707fcdd3d43dcfb834398aa9fed4116be3a", modalities=("text", "audio"))

# 多模态安全训练／偏好。
hf("vlguard_train", "VLGuard train", "multimodal_safety", ["sft"], "optional", None, "safety_instruction_samples",
   "gated=auto；训练与测试文件、safe/unsafe 子集分别固定", "ys-zong/VLGuard", "MIT + gated-and-upstream-terms", "review_required",
   "image_safety_instruction_response", ["multimodal_safety"], ["需接受访问条件", "危险图像与文本隔离", "安全回答和原始 unsafe 内容不可混作普通 SFT"],
   ["访问条件归档后作安全指令补集；只使用审查后的响应"], split="train", sha="b0be37a1ab7accb14e10d6a0ec3ce62cfaff2d46", access="gated_terms")
project("spa_vl_train", "SPA-VL train", "multimodal_safety", ["preference", "reward_model"], "research_only", 93258, "preference_pairs",
   "train 93,258；validation 7,000、HarmEval 265、HelpEval 265 独立，不相加", "https://sqrtizhang.github.io/SPA-VL/", "mixed-model-output-and-upstream", "review_required",
   "image_safety_preference_pairs", ["multimodal_safety", "visual_preference_rm"], ["chosen 也可能含不安全响应", "多模型输出和图像上游条款", "安全与有用性需双目标"],
   ["研究隔离安全偏好；分别审核 chosen/rejected， HarmEval/HelpEval 只评测"], split="train")
hf("safe_vid_350k", "SafeVid-350K", "multimodal_safety", ["preference", "reward_model"], "research_only", 350000, "video_safety_preference_pairs_approx",
   "官方论文约 350K 视频安全偏好对", "yxwang/SafeVid-350K", "CC-BY-NC-SA-4.0", "noncommercial",
   "video_safety_preference_pairs", ["multimodal_safety", "visual_preference_rm"], ["非商用及相同方式共享", "视频、文字描述和教师输出上游", "静态文本安全不等于视频时序安全"],
   ["非商用视频安全偏好补集；SafeVidBench 独立评测"], sha="6e2309a536d5bccced78454511404becd8744448", modalities=("text", "image", "video"))

# 本地不可替代物料。
def local(id, name, stages, caps, fmt, rec, modalities):
    add(id, name, "local_required", stages, "local_required", None, "internal_records",
        "由业务方定义媒体规模、时长、切分、脱敏和不可变版本", "internal://dataset-registry/" + id,
        None, "INTERNAL", "internal_review_required", "local", fmt, caps,
        ["媒体权利、肖像／声音同意、隐私、机密与业务分布审查", "不得上传公共训练平台"],
        [rec], modalities, verified="local_definition_required")

local("local_multimodal_sft", "真实业务多模态与中文指令 SFT", ["sft"],
      ["visual_instruction", "multilingual_multimodal", "audio_instruction", "document_chart_ocr", "multiimage_video"],
      "image_video_audio_business_messages", "覆盖真实中文图像、文档、视频和语音请求、失败案例与人工回答；记录媒体同意、时长和有效 token", ["text", "image", "video", "audio"])
local("local_multimodal_preference", "多模态人类偏好与音频 RL 物料", ["preference", "reward_model", "rlvr"],
      ["visual_preference_rm", "audio_preference_rl", "multimodal_safety"], "human_and_verifiable_multimodal_preferences",
      "公共音频偏好／RLVR 数据不足，由业务方建设人类语音偏好、可验证音频任务和图像／视频偏好；按独立提示切分", ["text", "image", "video", "audio"])
local("local_gui_action_safety", "本地 GUI 动作与危险操作安全数据", ["agent_sft", "agent_rl", "preference", "evaluation"],
      ["gui_agent", "multimodal_safety"], "gui_state_action_policy_labels",
      "覆盖真实应用、中文界面、账号脱敏、提示注入、不可逆动作确认和正常请求防过拒；静态轨迹与在线环境同时验收", ["text", "image", "video"])

# 独立评测。训练与测试即使同 repo 也拆资产。
ev("pixmo_count_test", "PixMo-Count test", 540, "test_samples", "只用 test 540；train 36,916 和 validation 540 独立",
   "https://huggingface.co/datasets/allenai/pixmo-count", "allenai/pixmo-count", ["visual_counting", "visual_grounding"],
   "计数与点定位独立评测；按图像 SHA 对训练集去污", "ODC-By", split="test", sha="ebf51cf70e45d12374e64d475862e4f8d21d31d0")
ev("mmmu_validation", "MMMU validation", 900, "validation_questions", "30 科目各 30；dev/test 不纳入本资产",
   "https://huggingface.co/datasets/MMMU/MMMU", "MMMU/MMMU", ["visual_instruction", "multilingual_multimodal"],
   "多学科视觉理解评测；固定全部科目 validation，test 通过官方协议另测", "Apache-2.0", split="validation", config="all_subjects", sha="876ce5cb130f7f7e290ce4d9984357737d4db5cf")
ev("mmmu_pro_standard10", "MMMU-Pro standard 10 options", 1730, "test_questions", "standard 10 options；不与 4 options 或 vision config 混写",
   "https://huggingface.co/datasets/MMMU/MMMU_Pro", "MMMU/MMMU_Pro", ["visual_reasoning_rlvr", "visual_instruction"],
   "鲁棒多学科推理评测；固定 10 options 并过滤纯文本可答泄漏检查", "Apache-2.0", config="standard (10 options)", sha="0d7426df4ccb3d8704a992fe6850abee7c262127")
ev("mathvista_testmini", "MathVista testmini", 1000, "testmini_questions", "testmini 1,000；完整 test 5,141，分数不可混写",
   "https://huggingface.co/datasets/AI4Math/MathVista", "AI4Math/MathVista", ["visual_reasoning_rlvr", "document_chart_ocr"],
   "视觉数学推理评测；固定 testmini、答案类型和数值精度", "CC-BY-SA-4.0", split="testmini", sha="2b6ad69445fbb5695c9b165475e8decdbeb97747")
ev("mathvision_test", "MathVision test", 3040, "test_questions", "test 3,040；testmini 304 分开",
   "https://huggingface.co/datasets/MathLLMs/MathVision", "MathLLMs/MathVision", ["visual_reasoning_rlvr"],
   "竞赛视觉数学保留评测；solution 字段不得转训练", "MIT", split="test", sha="2837ddb3f13abaf6b3997c12d80753e5470bd46a")
ev("docvqa_validation", "DocVQA validation", 5349, "validation_questions", "DocVQA/validation 5,349；test 5,188 和 InfographicVQA 分开",
   "https://huggingface.co/datasets/lmms-lab/DocVQA", "lmms-lab/DocVQA", ["document_chart_ocr"],
   "文档问答独立评测；固定 DocVQA config、validation 和 ANLS", "Apache-2.0", split="validation", config="DocVQA", sha="539088ef8a8ada01ac8e2e6d4e372586748a265e")
ev("chartqa_test", "ChartQA test", 2500, "test_questions", "当前 lmms-lab default/test 2,500",
   "https://huggingface.co/datasets/lmms-lab/ChartQA", "lmms-lab/ChartQA", ["document_chart_ocr", "visual_reasoning_rlvr"],
   "图表问答评测；human／augmented 类型分别报告", "no-explicit-license-in-card", split="test", sha="9e63b7df1592a1c2158e735cc1725454aef0d6d9")
ev("ocrbench", "OCRBench", None, "ocr_tasks", "当前 lmms-lab HF API 401；固定官方仓库任务文件后再计数",
   "https://github.com/Yuliang-Liu/MultimodalOCR", None, ["document_chart_ocr"],
   "多场景 OCR 独立评测；固定任务文件与答案归一化", verified="partial_official_reference")
ev("mmstar", "MMStar", None, "test_questions", "当前 lmms-lab HF API 401；不凭二手文章填规模",
   "https://github.com/MMStar-Benchmark/MMStar", None, ["visual_instruction", "visual_reasoning_rlvr"],
   "视觉依赖综合能力评测；同时报告纯文本可答性检查", verified="partial_official_reference")
ev("mantis_eval", "Mantis-Eval", 217, "test_questions", "mantis_eval/test 217；不得并入 Mantis-Instruct",
   "https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval", "TIGER-Lab/Mantis-Eval", ["multiimage_video"],
   "多图跨图指代、比较和推理评测；按 category 分报", "Apache-2.0", config="mantis_eval", sha="a3d92f9eb22c31d8c2d9d5b432c5a0ff1ef6dfd5", modalities=("text", "image", "video"))
ev("video_mme", "Video-MME", 2700, "test_questions", "videomme/test 2,700；字幕／无字幕和时长分桶分别报告",
   "https://huggingface.co/datasets/lmms-lab/Video-MME", "lmms-lab/Video-MME", ["multiimage_video"],
   "短视频到长视频综合评测；固定字幕、FPS、帧数和媒体版本", "no-explicit-license-in-card", config="videomme", sha="ead1408f75b618502df9a1d8e0950166bf0a2a0b", modalities=("text", "image", "video", "audio"))
ev("mlvu", "MLVU", None, "long_video_tasks", "当前 MLVU/MLVU HF API 401；按官方任务与 dev/test 文件固定",
   "https://github.com/JUNJIE99/MLVU", None, ["multiimage_video"],
   "长视频多任务评测；固定任务、字幕、抽帧与生成／选择评分协议", modalities=("text", "image", "video"), verified="partial_official_reference")
ev("longvideobench", "LongVideoBench", None, "long_video_questions", "gated=auto；接受访问条件并固定发布包后计数",
   "https://huggingface.co/datasets/longvideobench/LongVideoBench", "longvideobench/LongVideoBench", ["multiimage_video"],
   "长视频引用／推理评测；保留时间戳答案协议，NC-SA 仅限评测隔离", "CC-BY-NC-SA-4.0", sha="60d1c89c1919a198b73be39c2babb213b29d6a5c", modalities=("text", "image", "video"))
ev("vl_rewardbench", "VL-RewardBench", 1247, "test_samples_current_card", "当前 default/test 1,247；论文常用 1,250，口径差异保留",
   "https://huggingface.co/datasets/MMInstruction/VL-RewardBench", "MMInstruction/VL-RewardBench", ["visual_preference_rm"],
   "视觉奖励模型评测；按 general／hallucination／reasoning 分报并固定当前版本", "MIT", sha="0e6e62701eba92818a69ce95af0ed7aa0648b176")
ev("mmhal_bench", "MMHal-Bench", None, "hallucination_questions", "固定官方问题、图像和 GPT judge 版本",
   "https://github.com/open-compass/MMHal-Bench", None, ["visual_preference_rm", "multimodal_safety"],
   "视觉幻觉评测；judge 输出不得反哺训练", modalities=("text", "image"), verified="partial_official_reference")
ev("mm_safetybench", "MM-SafetyBench", None, "adversarial_safety_questions", "Text-only／SD／Typo／SD+Typo 分开；NC 研究评测",
   "https://github.com/isXinLiu/MM-SafetyBench", None, ["multimodal_safety"],
   "视觉越狱安全评测；分别报告 ASR 与正常请求可用性", "CC-BY-NC-4.0")
ev("figstep", "FigStep", None, "typographic_jailbreak_prompts", "固定图像化有害指令与评估器，禁止转训练",
   "https://github.com/ThuCCSLab/FigStep", None, ["multimodal_safety"],
   "排版图像越狱评测；危险内容隔离访问", modalities=("text", "image"), verified="partial_official_reference")
ev("safevidbench", "SafeVidBench", None, "video_safety_questions", "SafeVid-350K 训练偏好与本评测严格分开",
   "https://huggingface.co/datasets/yxwang/SafeVid-350K", "yxwang/SafeVid-350K", ["multimodal_safety"],
   "视频时序安全评测；固定视频、类别、judge 与 ASR／有用性指标", "CC-BY-NC-SA-4.0", sha="6e2309a536d5bccced78454511404becd8744448", modalities=("text", "image", "video"))
ev("screenspot_v2", "ScreenSpot-v2", None, "gui_grounding_samples", "mobile／desktop／web 分平台；当前 API 无统一切分行数",
   "https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2", "OS-Copilot/ScreenSpot-v2", ["gui_agent", "visual_grounding"],
   "GUI 元素定位评测；固定坐标归一化、平台和点击命中规则", "Apache-2.0", sha="5efbb1f1b5463a575f2eb7bc30fe29e49c15f93c")
ev("gui_odyssey_test", "GUIOdyssey test splits", None, "test_episodes", "与所选 random/task/device/app train split 一一对应",
   "https://huggingface.co/datasets/hflqf88888/GUIOdyssey", "hflqf88888/GUIOdyssey", ["gui_agent", "multiimage_video"],
   "跨 App 动作匹配与任务成功率评测；严格使用对应 test split", "CC-BY-4.0", split="official_test_split", config="random|task|device|app", sha="61632d0f3f4d51d7e9561ce4f84347dd06b2019d")
ev("osworld_verified", "OSWorld Verified", None, "executable_desktop_tasks", "固定环境镜像、任务包和验证器；不是静态截图 QA",
   "https://github.com/xlang-ai/OSWorld", None, ["gui_agent"],
   "真实桌面在线 Agent 评测；报告任务成功率、危险动作和环境版本", modalities=("text", "image", "video"))
ev("androidworld", "AndroidWorld", None, "executable_mobile_tasks", "固定任务套件、设备镜像和随机种子",
   "https://github.com/google-research/android_world", None, ["gui_agent"],
   "移动在线 Agent 评测；静态动作准确率不能替代任务成功率", modalities=("text", "image", "video"))
ev("voicebench", "VoiceBench", None, "multi_config_speech_eval", "AlpacaEval／CommonEval／SD-QA／MMSU／IFEval／AdvBench 等分别固定",
   "https://huggingface.co/datasets/hlt-lab/voicebench", "hlt-lab/voicebench", ["audio_instruction", "audio_preference_rl", "multimodal_safety"],
   "语音助手内容、指令、口音与安全评测；固定 TTS 声音、judge 和输出模态", "Apache-2.0", config="multiple_official_configs", sha="b02edcef1330480be3a11bd6f7434ac32f05ad08", modalities=("text", "audio"))
ev("mmau", "MMAU", None, "audio_reasoning_questions", "speech／sound／music 与 information extraction／reasoning 分报",
   "https://sakshi113.github.io/mmau_homepage/", None, ["audio_instruction"],
   "音频理解与推理评测；固定 test／mini、选项和 judge", modalities=("text", "audio"), verified="partial_official_reference")
ev("audiobench", "AudioBench suite", None, "versioned_audio_tasks", "50+ 数据集是套件而非同质单集；逐 config 和版本固定",
   "https://github.com/AudioLLMs/AudioBench", None, ["audio_instruction", "multilingual_multimodal"],
   "语音、声场和说话人理解评测；逐任务报告，不能汇总未经核验的总行数", modalities=("text", "audio"))
ev("air_bench", "AIR-Bench", None, "audio_instruction_eval_samples", "当前数据卡 CC-BY-NC-4.0；各音频任务／维度分别固定",
   "https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset", "qyang1021/AIR-Bench-Dataset", ["audio_instruction"],
   "开放音频指令与基础能力评测；固定 chat／foundation 维度和 judge", "CC-BY-NC-4.0", sha="8fa643aefd1d7248fd55fcf3e7ad22c81bbac1fa", modalities=("text", "audio"))
ev("cmmmu_test", "CMMMU test", 11000, "test_questions", "全集 12,012＝dev 112＋validation 900＋test 11,000；本项仅 test",
   "https://github.com/CMMMU-Benchmark/CMMMU", None, ["multilingual_multimodal", "visual_reasoning_rlvr"],
   "中文大学多学科评测；通过官方 EvalAI 协议，禁止将题解转训练", verified="official_checked")
ev("cmmu", "CMMU validation / hosted test", 3603, "questions_total_official", "七学科 3,603 题；validation 下载与 hosted test 分开报告",
   "https://github.com/FlagOpen/CMMU", None, ["multilingual_multimodal", "visual_reasoning_rlvr"],
   "中文教育多学科评测；填空题固定规则或 GPT judge 并分别报告", split="validation_and_hosted_test", verified="official_checked")
ev("mmbench_cn", "MMBench-CN", None, "chinese_multimodal_questions", "dev-CN 与 test-CN 分开，CircularEval 等协议固定",
   "https://github.com/open-compass/MMBench", "opencompass/MMBench", ["multilingual_multimodal", "visual_instruction"],
   "中文综合视觉理解评测；固定 CN split 和选项循环协议", "CC-BY-4.0", split="dev_cn_or_test_cn_separate", sha="47abe7b8f225cbff9942881db01dc33d2313483c")


COVERAGE = {
    "visual_instruction": (["pixmo_ask_model_anything", "pixmo_cap_qa", "llava_onevision15_instruct_22m", "finevision", "llava_instruct_150k", "llava15_mix665k", "local_multimodal_sft"], ["mmmu_validation", "mmstar", "mmbench_cn", "local_private_time_eval"]),
    "visual_grounding": (["pixmo_points", "pixmo_point_explanations", "molmo2_videopoint", "os_atlas_action_sft", "visual_rft_tasks"], ["screenspot_v2", "pixmo_count_test", "local_private_time_eval"]),
    "visual_counting": (["pixmo_count_train", "pixmo_points", "molmo2_videopoint", "llava_onevision15_instruct_22m"], ["pixmo_count_test", "local_private_time_eval"]),
    "document_chart_ocr": (["pixmo_docs", "pixmo_cap_qa", "llava_onevision15_instruct_22m", "finevision", "mantis_instruct", "local_multimodal_sft"], ["docvqa_validation", "chartqa_test", "ocrbench", "mathvista_testmini", "local_private_time_eval"]),
    "multiimage_video": (["mantis_instruct", "llava_video_178k", "videochat_flash_training", "molmo2_videotrack", "molmo2_videopoint", "local_multimodal_sft"], ["mantis_eval", "video_mme", "mlvu", "longvideobench", "local_private_time_eval"]),
    "visual_reasoning_rlvr": (["r1_onevision", "visual_rft_tasks", "llava_onevision15_instruct_22m"], ["mmmu_pro_standard10", "mathvista_testmini", "mathvision_test", "chartqa_test", "cmmmu_test", "local_private_time_eval"]),
    "visual_preference_rm": (["llava_human_preference_10k", "rlhf_v", "rlaif_v", "vlfeedback", "povid", "spa_vl_train", "local_multimodal_preference"], ["vl_rewardbench", "mmhal_bench", "local_private_time_eval"]),
    "audio_instruction": (["voice_assistant_400k", "local_multimodal_sft"], ["voicebench", "mmau", "audiobench", "air_bench", "local_private_time_eval"]),
    "audio_preference_rl": (["local_multimodal_preference"], ["voicebench", "local_private_time_eval"]),
    "gui_agent": (["os_atlas_action_sft", "gui_odyssey_train", "android_control_train", "local_gui_action_safety"], ["screenspot_v2", "gui_odyssey_test", "osworld_verified", "androidworld", "local_private_time_eval"]),
    "multimodal_safety": (["vlguard_train", "spa_vl_train", "safe_vid_350k", "local_multimodal_preference", "local_gui_action_safety"], ["mm_safetybench", "figstep", "safevidbench", "voicebench", "mmhal_bench", "local_private_time_eval"]),
    "multilingual_multimodal": (["llava_onevision15_instruct_22m", "finevision", "local_multimodal_sft"], ["cmmmu_test", "cmmu", "mmbench_cn", "audiobench", "local_private_time_eval"]),
}

DEFERRED = [
    {"name": "Audio-FLAN", "status": "deferred", "reason": "论文召回超 1 亿实例、80 任务且含音频生成；需先固定官方理解子集、许可和生成／理解边界，不整包纳入"},
    {"name": "AudioBench/MMAU direct HF cards", "status": "partially_verified", "reason": "官方项目与论文已核验，但当前猜测的 HF repo 返回 401；不登记未经核实的 HF revision 或统一行数"},
    {"name": "OCRBench/MMStar/BLINK/MLVU direct HF cards", "status": "partially_verified", "reason": "当前直接 HF API 返回 401；已保留官方项目入口和 eval_only 定义，未编造 SHA 或许可"},
    {"name": "CMMMU/CMMU direct HF cards", "status": "partially_verified", "reason": "官方 GitHub 与论文规模已核验，直接 HF API 401；固定发布包后再补 revision"},
    {"name": "GUI-R1 / Video-R1 / VideoChat-R1", "status": "deferred", "reason": "代码和奖励流程可召回，但本版未核验统一固定数据包；不把方法仓库当同质数据集"},
    {"name": "LLaVA 558K / LLaVA-OneVision-1.5-Mid-Training-85M", "status": "out_of_scope", "reason": "分别是特征对齐预训练和 mid-training，不属于本后训练清单"},
    {"name": "text-to-image / speech, music and video generation", "status": "out_of_scope", "reason": "本库覆盖后训练理解、指令、对齐与 Agent，不扩展到媒体生成数据"},
    {"name": "medical imaging / remote sensing", "status": "out_of_scope", "reason": "保留为专门领域审查范围；OneVision/FineVision 内相关 config 默认不选"},
]


def extend(datasets, coverage, caps):
    """Merge into the text catalog while preserving every original asset and recipe ID."""
    for item in datasets:
        item.setdefault("modalities", ["text"])
    private_eval = next(item for item in datasets if item["id"] == "local_private_time_eval")
    caps.update(MM_CAPS)
    private_eval["capabilities"] = sorted(caps)
    private_eval["modalities"] = ["text", "image", "video", "audio"]
    private_eval["recommendation"] = ["冻结文本、图像、视频、音频与 GUI 私有／时间外评测；覆盖中文、业务分布、安全和污染检查，严禁训练"]
    ids = {item["id"] for item in datasets}
    assert not ids & {item["id"] for item in ASSETS}
    datasets.extend(ASSETS)
    coverage.update(COVERAGE)
    return datasets, coverage


def write_extension():
    doc = {
        "schema_version": "1.0",
        "metadata": {"name": "multimodal-post-training-datasets-extension", "created_at": TODAY, "canonical_subset": True},
        "scope": {
            "modalities": ["text", "image", "video", "audio"],
            "included": ["multimodal instruction/SFT", "preference/reward model", "RLVR", "GUI Agent", "independent evaluation"],
            "excluded": ["media generation", "raw caption pretraining", "feature-alignment pretraining", "mid-training"],
        },
        "datasets": ASSETS,
        "coverage_requirements": {key: {"required": True, "training_candidates": value[0], "eval_ids": value[1]} for key, value in COVERAGE.items()},
        "excluded_or_deferred_candidates": DEFERRED,
    }
    with (ROOT / "datasets-multimodal.yaml").open("w", encoding="utf-8") as handle:
        yaml.safe_dump(doc, handle, allow_unicode=True, sort_keys=False, width=120)
    print(f"Wrote {len(ASSETS)} multimodal assets and {len(COVERAGE)} capabilities")


if __name__ == "__main__":
    write_extension()
