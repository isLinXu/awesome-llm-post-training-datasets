# Base 与多模态模型后训练数据自动目录

> 自动更新：2026-11-09T09:09:52Z；canonical 输入：`datasets-list.yaml`。本文件只生成视图，不改写人工许可和训练分层。
> 共 175 项已收录资产；待审核候选 11 项。候选数据不会自动进入训练配方。

## 分层、模态与阶段索引

| 维度 | 值 | 数量 |
|---|---|---:|
| usage_tier | `core` | 30 |
| usage_tier | `eval_only` | 60 |
| usage_tier | `local_required` | 8 |
| usage_tier | `optional` | 51 |
| usage_tier | `research_only` | 26 |
| modality | `audio` | 9 |
| modality | `image` | 57 |
| modality | `text` | 175 |
| modality | `video` | 16 |
| stage | `agent_rl` | 6 |
| stage | `agent_sft` | 10 |
| stage | `evaluation` | 66 |
| stage | `preference` | 26 |
| stage | `prm` | 3 |
| stage | `reward_model` | 23 |
| stage | `rlvr` | 15 |
| stage | `sft` | 73 |

## 能力覆盖

| 能力 | 训练候选 | 独立评测 |
|---|---|---|
| `general_chat` | `dolci_instruct_sft`, `tulu3_sft_mixture`, `dolly_15k`, `longform`, `nemotron_cascade_2_sft`, `smoltalk2`, `no_robots`, `oasst2`, `lima`, `wildchat`, `openhermes_2_5`, `infinity_instruct`, `local_domain_zh_sft` | `mt_bench`, `local_private_time_eval` |
| `knowledge_recall` | `dolci_instruct_sft`, `tulu3_sft_mixture`, `nemotron_cascade_2_sft`, `smoltalk2`, `aya_collection`, `natural_reasoning` | `mmlu_pro`, `gpqa_diamond`, `local_private_time_eval` |
| `multilingual` | `aya_dataset`, `aya_collection`, `m2lingual`, `helpsteer3_preference`, `oasst2`, `dolci_instruct_sft`, `wildchat` | `mgsm`, `sorry_bench_202503`, `tau_bench_2_text`, `local_private_time_eval` |
| `chinese` | `coig_pc_lite`, `coig_cqia`, `belle`, `firefly`, `chinese_r1_distill_110k`, `dolci_instruct_sft`, `longcite_45k`, `local_domain_zh_sft` | `local_private_time_eval` |
| `multiturn` | `no_robots`, `oasst2`, `wildchat`, `smoltalk2`, `tulu3_sft_mixture`, `helpsteer3_preference`, `toolmind`, `m2lingual`, `weblinx`, `toolace` | `mt_bench`, `tau_bench_2_text`, `local_private_time_eval` |
| `precise_if` | `tulu3_persona_if`, `ifeval_like_filtered`, `verinstruct`, `nemotron_cascade_2_rl`, `dolci_instruct_sft`, `tulu3_sft_mixture` | `ifeval`, `rewardbench2`, `local_private_time_eval` |
| `long_context` | `longalign_10k`, `longcite_45k`, `nemotron_cascade_2_sft` | `longbench_chat`, `longbench_cite`, `ruler`, `local_private_time_eval` |
| `grounded_citation` | `longcite_45k`, `webgpt_comparisons`, `local_domain_zh_sft` | `longbench_cite`, `local_private_time_eval` |
| `general_reasoning` | `openthoughts3`, `natural_reasoning`, `mixture_of_thoughts`, `openmathinstruct2`, `enigmata_data`, `nemotron_cascade_2_rl`, `chinese_r1_distill_110k`, `s1k`, `limo`, `openmath_reasoning`, `numina_math_cot` | `bbh`, `mmlu_pro`, `omni_math`, `gpqa_diamond`, `enigmata_eval`, `local_private_time_eval` |
| `math_sft` | `numina_math_cot`, `openmath_reasoning`, `openmathinstruct2`, `chinese_r1_distill_110k`, `openthoughts3`, `mixture_of_thoughts` | `math_500`, `gsm8k_test`, `omni_math`, `mgsm`, `local_private_time_eval` |
| `math_rlvr` | `dapo_math_17k`, `deepscaler_preview`, `deepmath_103k`, `big_math_rl_verified`, `skywork_or1_rl` | `math_500`, `gsm8k_test`, `omni_math`, `mgsm`, `local_private_time_eval` |
| `code_sft` | `kodcode`, `magicoder`, `opencode_reasoning`, `opencodeinstruct`, `codefeedback_filtered`, `mixture_of_thoughts`, `taco`, `codecontests` | `livecodebench_v6`, `bigcodebench`, `local_private_time_eval` |
| `code_rlvr` | `acecode_87k`, `kodcode`, `taco`, `codecontests`, `skywork_or1_rl` | `livecodebench_v6`, `bigcodebench`, `local_private_time_eval` |
| `tool_calling` | `xlam_function_calling`, `toolace`, `toolmind`, `glaive_function_calling_v2`, `api_bank`, `toolbench`, `local_no_tool_negative` | `bfcl`, `agentdojo`, `local_private_time_eval` |
| `multistep_tool` | `toolbench`, `api_bank`, `toolace`, `toolmind`, `weblinx`, `local_no_tool_negative` | `bfcl`, `tau_bench_2_text`, `agentdojo`, `mind2web_test`, `agentharm`, `local_private_time_eval` |
| `preference_rm` | `helpsteer2`, `helpsteer3_preference`, `tulu3_preference_mixture`, `webgpt_comparisons`, `summarize_from_feedback`, `hh_rlhf`, `shp`, `helpsteer`, `ultrafeedback`, `nectar`, `arena_human_preference_140k`, `skywork_reward_preference_80k`, `local_domain_zh_sft` | `rewardbench`, `rewardbench2`, `local_private_time_eval` |
| `safety_moderation` | `aegis_content_safety_2`, `wildguardmix_tulu3`, `pku_saferlhf`, `local_domain_safety` | `xstest`, `harmbench`, `strongreject`, `sorry_bench_202503`, `local_private_time_eval` |
| `safe_refusal` | `pku_saferlhf`, `aegis_content_safety_2`, `wildguardmix_tulu3`, `falsereject_train`, `hh_rlhf`, `local_domain_safety` | `xstest`, `falsereject_test`, `harmbench`, `strongreject`, `sorry_bench_202503`, `agentharm`, `local_private_time_eval` |
| `overrefusal` | `local_overrefusal`, `wildguardmix_tulu3`, `falsereject_train` | `xstest`, `falsereject_test`, `rewardbench`, `local_private_time_eval` |
| `process_reward` | `prm800k`, `math_shepherd`, `pathfinder_prm` | `processbench`, `prmbench`, `local_private_time_eval` |
| `search_agent` | `search_r1`, `webgpt_comparisons` | `local_private_time_eval` |
| `swe_agent` | `swe_gym`, `swe_smith`, `r2e_gym`, `nemotron_cascade_2_rl` | `swebench_verified`, `local_private_time_eval` |
| `domain_adaptation` | `local_domain_zh_sft`, `local_no_tool_negative`, `local_overrefusal`, `local_domain_safety` | `local_private_time_eval` |
| `long_output` | `longform` | `longform_test`, `local_private_time_eval` |
| `browser_agent` | `weblinx` | `mind2web_test`, `local_private_time_eval` |
| `agent_safety` | `local_domain_safety` | `agentharm`, `agentdojo`, `local_private_time_eval` |
| `visual_instruction` | `pixmo_ask_model_anything`, `pixmo_cap_qa`, `llava_onevision15_instruct_22m`, `finevision`, `llava_instruct_150k`, `llava15_mix665k`, `local_multimodal_sft` | `mmmu_validation`, `mmstar`, `mmbench_cn`, `local_private_time_eval` |
| `visual_grounding` | `pixmo_points`, `pixmo_point_explanations`, `molmo2_videopoint`, `os_atlas_action_sft`, `visual_rft_tasks` | `screenspot_v2`, `pixmo_count_test`, `local_private_time_eval` |
| `visual_counting` | `pixmo_count_train`, `pixmo_points`, `molmo2_videopoint`, `llava_onevision15_instruct_22m` | `pixmo_count_test`, `local_private_time_eval` |
| `document_chart_ocr` | `pixmo_docs`, `pixmo_cap_qa`, `llava_onevision15_instruct_22m`, `finevision`, `mantis_instruct`, `local_multimodal_sft` | `docvqa_validation`, `chartqa_test`, `ocrbench`, `mathvista_testmini`, `local_private_time_eval` |
| `multiimage_video` | `mantis_instruct`, `llava_video_178k`, `videochat_flash_training`, `molmo2_videotrack`, `molmo2_videopoint`, `local_multimodal_sft` | `mantis_eval`, `video_mme`, `mlvu`, `longvideobench`, `local_private_time_eval` |
| `visual_reasoning_rlvr` | `r1_onevision`, `visual_rft_tasks`, `llava_onevision15_instruct_22m` | `mmmu_pro_standard10`, `mathvista_testmini`, `mathvision_test`, `chartqa_test`, `cmmmu_test`, `local_private_time_eval` |
| `visual_preference_rm` | `llava_human_preference_10k`, `rlhf_v`, `rlaif_v`, `vlfeedback`, `povid`, `spa_vl_train`, `local_multimodal_preference` | `vl_rewardbench`, `mmhal_bench`, `local_private_time_eval` |
| `audio_instruction` | `voice_assistant_400k`, `local_multimodal_sft` | `voicebench`, `mmau`, `audiobench`, `air_bench`, `local_private_time_eval` |
| `audio_preference_rl` | `local_multimodal_preference` | `voicebench`, `local_private_time_eval` |
| `gui_agent` | `os_atlas_action_sft`, `gui_odyssey_train`, `android_control_train`, `local_gui_action_safety` | `screenspot_v2`, `gui_odyssey_test`, `osworld_verified`, `androidworld`, `local_private_time_eval` |
| `multimodal_safety` | `vlguard_train`, `spa_vl_train`, `safe_vid_350k`, `local_multimodal_preference`, `local_gui_action_safety` | `mm_safetybench`, `figstep`, `safevidbench`, `voicebench`, `mmhal_bench`, `local_private_time_eval` |
| `multilingual_multimodal` | `llava_onevision15_instruct_22m`, `finevision`, `local_multimodal_sft` | `cmmmu_test`, `cmmu`, `mmbench_cn`, `audiobench`, `local_private_time_eval` |

## 分类目录

### 浏览与网页导航 Agent（`agent_browser`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `weblinx` | text | agent_sft | research_only | noncommercial | ok | 2024-12-07T04:23:40.000Z | [来源](https://huggingface.co/datasets/McGill-NLP/WebLINX) |

### 搜索与浏览 Agent（`agent_search`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `search_r1` | text | agent_rl | optional | review_required | not_tracked | — | [来源](https://github.com/PeterGriffinJin/Search-R1) |

### 软件工程 Agent（`agent_swe`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `r2e_gym` | text | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://r2e-gym.github.io/) |
| `swe_gym` | text | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://arxiv.org/abs/2412.21139) |
| `swe_smith` | text | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://github.com/SWE-bench/SWE-smith) |

### 音频与语音指令（`audio_sft`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `voice_assistant_400k` | text, audio | sft | optional | review_required | ok | 2024-09-13T12:01:42.000Z | [来源](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K) |

### 中文指令与领域数据（`chinese`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `belle` | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/LianjiaTech/BELLE) |
| `chinese_r1_distill_110k` | text | sft | optional | review_required | ok | 2025-02-21T02:18:08.000Z | [来源](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k) |
| `coig_cqia` | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://arxiv.org/html/2403.18058v2) |
| `coig_pc_lite` | text | sft | core | review_required | ok | 2024-06-14T01:18:23.000Z | [来源](https://huggingface.co/datasets/BAAI/COIG-PC-Lite) |
| `firefly` | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/yangjianxin1/Firefly) |

### 代码 SFT 与推理（`code`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `codecontests` | text | sft, rlvr | core | allowed_with_obligations | ok | 2023-06-11T12:22:30.000Z | [来源](https://huggingface.co/datasets/deepmind/code_contests) |
| `codefeedback_filtered` | text | sft | optional | review_required | ok | 2024-02-26T09:25:26.000Z | [来源](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction) |
| `kodcode` | text | sft, rlvr | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2503.02951) |
| `magicoder` | text | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2312.02120v2) |
| `opencode_reasoning` | text | sft | core | allowed_with_obligations | ok | 2025-05-04T23:54:22.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) |
| `opencodeinstruct` | text | sft | core | allowed_with_obligations | ok | 2025-04-28T19:08:02.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) |
| `taco` | text | sft, rlvr | core | review_required | ok | 2024-06-19T09:16:49.000Z | [来源](https://huggingface.co/datasets/BAAI/TACO) |

### 文档、图表与 OCR（`document_sft`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `pixmo_docs` | text, image | sft | core | allowed_with_obligations | ok | 2025-02-24T17:25:46.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-docs) |

### 独立评测（`evaluation`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `agentdojo` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ethz-spylab/agentdojo) |
| `agentharm` | text | evaluation | eval_only | eval_only | ok | 2024-12-19T13:27:30.000Z | [来源](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) |
| `air_bench` | text, audio | evaluation | eval_only | eval_only | ok | 2024-05-12T08:45:15.000Z | [来源](https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset) |
| `androidworld` | text, image, video | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/google-research/android_world) |
| `audiobench` | text, audio | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/AudioLLMs/AudioBench) |
| `bbh` | text | evaluation | eval_only | eval_only | ok | 2025-07-11T17:27:58.000Z | [来源](https://huggingface.co/datasets/lukaemon/bbh) |
| `bfcl` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) |
| `bigcodebench` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/bigcode-project/bigcodebench) |
| `chartqa_test` | text, image | evaluation | eval_only | eval_only | ok | 2024-03-08T05:04:43.000Z | [来源](https://huggingface.co/datasets/lmms-lab/ChartQA) |
| `cmmmu_test` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/CMMMU-Benchmark/CMMMU) |
| `cmmu` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/FlagOpen/CMMU) |
| `docvqa_validation` | text, image | evaluation | eval_only | eval_only | ok | 2024-04-18T05:14:35.000Z | [来源](https://huggingface.co/datasets/lmms-lab/DocVQA) |
| `enigmata_eval` | text | evaluation | eval_only | eval_only | ok | 2025-05-27T08:14:17.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval) |
| `falsereject_test` | text | evaluation | eval_only | eval_only | ok | 2025-05-14T19:16:44.000Z | [来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| `figstep` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ThuCCSLab/FigStep) |
| `gpqa_diamond` | text | evaluation | eval_only | eval_only | ok | 2026-09-21T22:29:06.000Z | [来源](https://huggingface.co/datasets/Idavidrein/gpqa) |
| `gsm8k_test` | text | evaluation | eval_only | eval_only | ok | 2026-03-23T10:18:13.000Z | [来源](https://huggingface.co/datasets/openai/gsm8k) |
| `gui_odyssey_test` | text, image | evaluation | eval_only | eval_only | ok | 2025-08-04T02:22:43.000Z | [来源](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) |
| `harmbench` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/centerforaisafety/HarmBench) |
| `ifeval` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/google-research/google-research/tree/master/instruction_following_eval) |
| `livecodebench_v6` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/LiveCodeBench/LiveCodeBench) |
| `longbench_chat` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/THUDM/LongAlign) |
| `longbench_cite` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/THUDM/LongCite) |
| `longform_test` | text | evaluation | eval_only | eval_only | ok | 2024-03-05T15:20:00.000Z | [来源](https://huggingface.co/datasets/akoksal/LongForm) |
| `longvideobench` | text, image, video | evaluation | eval_only | eval_only | ok | 2024-10-14T05:43:04.000Z | [来源](https://huggingface.co/datasets/longvideobench/LongVideoBench) |
| `mantis_eval` | text, image, video | evaluation | eval_only | eval_only | ok | 2024-11-15T06:43:06.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval) |
| `math_500` | text | evaluation | eval_only | eval_only | ok | 2025-12-15T11:01:40.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) |
| `mathvision_test` | text, image | evaluation | eval_only | eval_only | ok | 2026-06-10T07:04:16.000Z | [来源](https://huggingface.co/datasets/MathLLMs/MathVision) |
| `mathvista_testmini` | text, image | evaluation | eval_only | eval_only | ok | 2024-02-11T23:09:05.000Z | [来源](https://huggingface.co/datasets/AI4Math/MathVista) |
| `mgsm` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://arxiv.org/abs/2210.03057) |
| `mind2web_test` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/OSU-NLP-Group/Mind2Web) |
| `mlvu` | text, image, video | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/JUNJIE99/MLVU) |
| `mm_safetybench` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/isXinLiu/MM-SafetyBench) |
| `mmau` | text, audio | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://sakshi113.github.io/mmau_homepage/) |
| `mmbench_cn` | text, image | evaluation | eval_only | eval_only | ok | 2023-09-13T02:11:05.000Z | [来源](https://github.com/open-compass/MMBench) |
| `mmhal_bench` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/open-compass/MMHal-Bench) |
| `mmlu_pro` | text | evaluation | eval_only | eval_only | ok | 2026-05-02T06:26:05.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro) |
| `mmmu_pro_standard10` | text, image | evaluation | eval_only | eval_only | ok | 2026-10-05T01:55:47.000Z | [来源](https://huggingface.co/datasets/MMMU/MMMU_Pro) |
| `mmmu_validation` | text, image | evaluation | eval_only | eval_only | ok | 2026-10-05T02:04:29.000Z | [来源](https://huggingface.co/datasets/MMMU/MMMU) |
| `mmstar` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/MMStar-Benchmark/MMStar) |
| `mt_bench` | text | evaluation | eval_only | eval_only | ok | 2023-07-03T20:52:34.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts) |
| `ocrbench` | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/Yuliang-Liu/MultimodalOCR) |
| `omni_math` | text | evaluation | eval_only | eval_only | ok | 2024-10-12T09:02:05.000Z | [来源](https://huggingface.co/datasets/KbsdJames/Omni-MATH) |
| `osworld_verified` | text, image, video | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/xlang-ai/OSWorld) |
| `pixmo_count_test` | text, image | evaluation | eval_only | eval_only | ok | 2024-11-30T04:08:58.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-count) |
| `prmbench` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ssmisya/PRMBench) |
| `processbench` | text | evaluation | eval_only | eval_only | ok | 2024-12-27T14:05:30.000Z | [来源](https://huggingface.co/datasets/Qwen/ProcessBench) |
| `rewardbench` | text | evaluation | eval_only | eval_only | ok | 2024-09-09T16:11:45.000Z | [来源](https://huggingface.co/datasets/allenai/reward-bench) |
| `rewardbench2` | text | evaluation | eval_only | eval_only | ok | 2025-06-04T08:53:38.000Z | [来源](https://huggingface.co/datasets/allenai/reward-bench-2) |
| `ruler` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/NVIDIA/RULER) |
| `safevidbench` | text, image, video | evaluation | eval_only | eval_only | ok | 2025-11-27T11:30:31.000Z | [来源](https://huggingface.co/datasets/yxwang/SafeVid-350K) |
| `screenspot_v2` | text, image | evaluation | eval_only | eval_only | ok | 2025-02-10T11:15:38.000Z | [来源](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2) |
| `sorry_bench_202503` | text | evaluation | eval_only | eval_only | ok | 2025-02-28T21:58:59.000Z | [来源](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503) |
| `strongreject` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/dsbowen/strong_reject) |
| `swebench_verified` | text | evaluation | eval_only | eval_only | ok | 2025-02-18T23:48:55.000Z | [来源](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) |
| `tau_bench_2_text` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/sierra-research/tau2-bench) |
| `video_mme` | text, image, video, audio | evaluation | eval_only | eval_only | ok | 2024-07-04T08:14:20.000Z | [来源](https://huggingface.co/datasets/lmms-lab/Video-MME) |
| `vl_rewardbench` | text, image | evaluation | eval_only | eval_only | ok | 2025-05-19T10:50:44.000Z | [来源](https://huggingface.co/datasets/MMInstruction/VL-RewardBench) |
| `voicebench` | text, audio | evaluation | eval_only | eval_only | ok | 2025-04-19T16:49:38.000Z | [来源](https://huggingface.co/datasets/hlt-lab/voicebench) |
| `xstest` | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/paul-rottger/exaggerated-safety) |

### 通用指令与 SFT（`general_sft`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `dolci_instruct_sft` | text | sft | core | allowed_with_obligations | ok | 2026-02-03T00:08:38.000Z | [来源](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT) |
| `dolly_15k` | text | sft | core | allowed_with_obligations | ok | 2023-06-30T18:34:13.000Z | [来源](https://huggingface.co/datasets/databricks/databricks-dolly-15k) |
| `infinity_instruct` | text | sft | optional | review_required | ok | 2025-12-04T07:56:39.000Z | [来源](https://huggingface.co/datasets/BAAI/Infinity-Instruct) |
| `lima` | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://arxiv.org/html/2305.11206v4) |
| `nemotron_cascade_2_sft` | text | sft | optional | review_required | ok | 2026-03-19T23:57:48.000Z | [来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) |
| `no_robots` | text | sft | research_only | noncommercial | ok | 2024-04-18T08:40:39.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/no_robots) |
| `openhermes_2_5` | text | sft | optional | review_required | ok | 2024-04-15T08:18:12.000Z | [来源](https://huggingface.co/datasets/teknium/OpenHermes-2.5) |
| `smoltalk2` | text | sft | optional | review_required | not_tracked | — | [来源](https://huggingface.co/blog/smollm3) |
| `tulu3_sft_mixture` | text | sft | core | allowed_with_obligations | ok | 2024-12-02T19:48:33.000Z | [来源](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) |
| `wildchat` | text | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2405.01470v3) |

### GUI Agent 与动作轨迹（`gui_agent`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `android_control_train` | text, image | agent_sft | research_only | review_required | not_tracked | — | [来源](https://github.com/google-research/google-research/tree/master/android_control) |
| `gui_odyssey_train` | text, image | agent_sft | core | allowed_with_obligations | ok | 2025-08-04T02:22:43.000Z | [来源](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) |
| `os_atlas_action_sft` | text, image | agent_sft | core | allowed_with_obligations | ok | 2024-12-04T10:26:47.000Z | [来源](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data) |

### 精确指令遵循（`instruction_following`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `ifeval_like_filtered` | text | sft | optional | review_required | ok | 2024-10-17T09:43:39.000Z | [来源](https://huggingface.co/datasets/argilla/ifeval-like-data) |
| `tulu3_persona_if` | text | sft | core | allowed_with_obligations | ok | 2024-11-21T15:57:21.000Z | [来源](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following) |

### 本地必需物料（`local_required`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `local_domain_safety` | text | sft, preference, reward_model, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_domain_zh_sft` | text | sft | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_gui_action_safety` | text, image, video | agent_sft, agent_rl, preference, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_multimodal_preference` | text, image, video, audio | preference, reward_model, rlvr | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_multimodal_sft` | text, image, video, audio | sft | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_no_tool_negative` | text | sft, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_overrefusal` | text | sft, preference, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_private_time_eval` | text, image, video, audio | evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |

### 长上下文与引用（`long_context`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `longalign_10k` | text | sft | optional | review_required | ok | 2024-02-22T11:39:00.000Z | [来源](https://huggingface.co/datasets/zai-org/LongAlign-10k) |
| `longcite_45k` | text | sft | core | allowed_with_obligations | ok | 2024-10-18T09:59:40.000Z | [来源](https://huggingface.co/datasets/zai-org/LongCite-45k) |

### 长输出生成（`long_output`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `longform` | text | sft | optional | review_required | ok | 2024-03-05T15:20:00.000Z | [来源](https://huggingface.co/datasets/akoksal/LongForm) |

### 数学 SFT（`math`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `numina_math_cot` | text | sft | optional | review_required | not_tracked | — | [来源](https://github.com/project-numina/aimo-progress-prize) |
| `openmath_reasoning` | text | sft | core | allowed_with_obligations | ok | 2025-05-27T18:43:44.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenMathReasoning) |
| `openmathinstruct2` | text | sft | core | allowed_with_obligations | ok | 2024-11-25T20:07:28.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) |

### 多图交错指令（`multiimage_sft`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `mantis_instruct` | text, image | sft | optional | review_required | ok | 2024-12-25T01:43:11.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct) |

### 多语言指令数据（`multilingual`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `aya_collection` | text | sft | optional | allowed_with_obligations | ok | 2025-04-15T08:52:39.000Z | [来源](https://huggingface.co/datasets/CohereLabs/aya_collection) |
| `aya_dataset` | text | sft | core | allowed_with_obligations | ok | 2025-04-15T08:51:55.000Z | [来源](https://huggingface.co/datasets/CohereLabs/aya_dataset) |
| `m2lingual` | text | sft | research_only | noncommercial | ok | 2024-08-13T19:01:43.000Z | [来源](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual) |
| `oasst2` | text | sft, preference | optional | allowed_with_obligations | not_tracked | — | [来源](https://arxiv.org/html/2304.07327v3) |

### 多模态偏好与奖励模型（`multimodal_preference`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `llava_human_preference_10k` | text, image | preference, reward_model | optional | review_required | ok | 2023-09-27T01:03:58.000Z | [来源](https://huggingface.co/datasets/zhiqings/LLaVA-Human-Preference-10K) |
| `povid` | text, image | preference, reward_model | optional | review_required | ok | 2024-04-01T08:56:50.000Z | [来源](https://huggingface.co/datasets/YiyangAiLab/POVID_preference_data_for_VLLMs) |
| `rlaif_v` | text, image | preference, reward_model | research_only | noncommercial | ok | 2025-10-14T08:35:37.000Z | [来源](https://huggingface.co/datasets/openbmb/RLAIF-V-Dataset) |
| `rlhf_v` | text, image | preference, reward_model | research_only | noncommercial | not_tracked | — | [来源](https://github.com/rlhf-v/rlhf-v) |
| `vlfeedback` | text, image | preference, reward_model | optional | review_required | ok | 2024-10-17T05:40:23.000Z | [来源](https://huggingface.co/datasets/MMInstruction/VLFeedback) |

### 多模态推理蒸馏（`multimodal_reasoning`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `r1_onevision` | text, image | sft, rlvr | optional | review_required | ok | 2025-03-18T15:25:45.000Z | [来源](https://huggingface.co/datasets/Fancy-MLLM/R1-Onevision) |

### 多模态 RLVR（`multimodal_rlvr`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `visual_rft_tasks` | text, image | rlvr | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2503.01785v1) |

### 多模态安全与幻觉（`multimodal_safety`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `safe_vid_350k` | text, image, video | preference, reward_model | research_only | noncommercial | ok | 2025-11-27T11:30:31.000Z | [来源](https://huggingface.co/datasets/yxwang/SafeVid-350K) |
| `spa_vl_train` | text, image | preference, reward_model | research_only | review_required | not_tracked | — | [来源](https://sqrtizhang.github.io/SPA-VL/) |
| `vlguard_train` | text, image | sft | optional | review_required | ok | 2025-01-19T00:32:34.000Z | [来源](https://huggingface.co/datasets/ys-zong/VLGuard) |

### 偏好与奖励模型（`preference`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `arena_human_preference_140k` | text | preference, reward_model | optional | review_required | ok | 2025-08-01T05:03:39.000Z | [来源](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k) |
| `helpsteer` | text | reward_model, preference | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2406.08673v1) |
| `helpsteer2` | text | preference, reward_model | core | allowed_with_obligations | ok | 2024-12-18T21:06:57.000Z | [来源](https://huggingface.co/datasets/nvidia/HelpSteer2) |
| `helpsteer3_preference` | text | preference, reward_model | core | allowed_with_obligations | ok | 2025-11-16T07:18:00.000Z | [来源](https://huggingface.co/datasets/nvidia/HelpSteer3) |
| `hh_rlhf` | text | preference, reward_model | optional | allowed_with_obligations | ok | 2023-05-26T18:47:34.000Z | [来源](https://huggingface.co/datasets/Anthropic/hh-rlhf) |
| `nectar` | text | preference, reward_model | optional | review_required | ok | 2024-03-20T04:17:46.000Z | [来源](https://huggingface.co/datasets/berkeley-nest/Nectar) |
| `shp` | text | preference, reward_model | optional | review_required | ok | 2023-10-10T23:35:57.000Z | [来源](https://huggingface.co/datasets/stanfordnlp/SHP) |
| `skywork_reward_preference_80k` | text | preference, reward_model | optional | review_required | ok | 2024-10-25T01:58:25.000Z | [来源](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2) |
| `summarize_from_feedback` | text | preference, reward_model | research_only | review_required | ok | 2023-01-03T16:55:41.000Z | [来源](https://huggingface.co/datasets/openai/summarize_from_feedback) |
| `tulu3_preference_mixture` | text | preference, reward_model | research_only | noncommercial | ok | 2025-02-04T00:21:47.000Z | [来源](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture) |
| `ultrafeedback` | text | preference, reward_model | optional | review_required | ok | 2023-12-29T14:11:19.000Z | [来源](https://huggingface.co/datasets/openbmb/UltraFeedback) |
| `webgpt_comparisons` | text | preference, reward_model | research_only | review_required | ok | 2022-12-19T17:55:29.000Z | [来源](https://huggingface.co/datasets/openai/webgpt_comparisons) |

### 过程奖励与步级监督（`process_reward`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `math_shepherd` | text | prm | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/abs/2312.08935) |
| `pathfinder_prm` | text | prm | research_only | review_required | not_tracked | — | [来源](https://github.com/declare-lab/PathFinder-PRM) |
| `prm800k` | text | prm | optional | allowed_with_obligations | not_tracked | — | [来源](https://github.com/openai/prm800k) |

### 通用与蒸馏推理（`reasoning`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `limo` | text | sft | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2502.03387v1) |
| `mixture_of_thoughts` | text | sft | optional | review_required | ok | 2025-05-26T15:25:56.000Z | [来源](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts) |
| `natural_reasoning` | text | sft | research_only | noncommercial | ok | 2025-02-21T06:02:40.000Z | [来源](https://huggingface.co/datasets/facebook/natural_reasoning) |
| `openthoughts3` | text | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2506.04178v1) |
| `s1k` | text | sft | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2501.19393v1) |

### 代码 RLVR（`rlvr_code`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `acecode_87k` | text | rlvr | core | review_required | not_tracked | — | [来源](https://arxiv.org/html/2502.01718v4) |

### rlvr_general（`rlvr_general`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `enigmata_data` | text | rlvr | research_only | noncommercial | ok | 2025-08-13T09:00:27.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data) |
| `nemotron_cascade_2_rl` | text | rlvr, agent_rl, sft | optional | allowed_with_obligations | ok | 2026-03-20T03:38:20.000Z | [来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) |

### 指令遵循 RLVR（`rlvr_if`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `verinstruct` | text | rlvr | core | review_required | not_tracked | — | [来源](https://aclanthology.org/2025.emnlp-main.1542/) |

### 数学 RLVR（`rlvr_math`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `big_math_rl_verified` | text | rlvr | core | allowed_with_obligations | ok | 2025-03-25T15:33:48.000Z | [来源](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) |
| `dapo_math_17k` | text | rlvr | core | allowed_with_obligations | ok | 2025-04-18T11:20:51.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) |
| `deepmath_103k` | text | rlvr | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2504.11456v2) |
| `deepscaler_preview` | text | rlvr | core | allowed_with_obligations | ok | 2025-02-10T09:51:18.000Z | [来源](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset) |
| `skywork_or1_rl` | text | rlvr | optional | review_required | ok | 2025-05-29T02:27:10.000Z | [来源](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) |

### 安全、拒答与防过拒（`safety`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `aegis_content_safety_2` | text | sft, reward_model | core | allowed_with_obligations | ok | 2025-06-09T19:15:56.000Z | [来源](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) |
| `falsereject_train` | text | sft | research_only | noncommercial | ok | 2025-05-14T19:16:44.000Z | [来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| `pku_saferlhf` | text | preference, reward_model, sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/PKU-Alignment/beavertails) |
| `wildguardmix_tulu3` | text | sft, preference | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2411.15124v2) |

### 工具与函数调用（`tool`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `api_bank` | text | sft, evaluation | optional | review_required | not_tracked | — | [来源](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) |
| `glaive_function_calling_v2` | text | sft | optional | allowed_with_obligations | ok | 2023-09-27T18:04:08.000Z | [来源](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2) |
| `toolace` | text | sft | core | review_required | not_tracked | — | [来源](https://arxiv.org/html/2409.00917v1) |
| `toolbench` | text | sft, agent_sft | optional | review_required | not_tracked | — | [来源](https://github.com/OpenBMB/ToolBench) |
| `toolmind` | text | sft, agent_sft | optional | allowed_with_obligations | ok | 2026-01-09T02:23:42.000Z | [来源](https://huggingface.co/datasets/Nanbeige/ToolMind) |
| `xlam_function_calling` | text | sft | core | review_required | ok | 2025-01-24T19:25:58.000Z | [来源](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) |

### 视频指令与时空理解（`video_sft`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `llava_video_178k` | text, image, video | sft | optional | review_required | ok | 2024-10-11T04:59:25.000Z | [来源](https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K) |
| `molmo2_videopoint` | text, image, video | sft | core | allowed_with_obligations | ok | 2026-03-16T01:32:31.000Z | [来源](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint) |
| `molmo2_videotrack` | text, image, video | sft | optional | allowed_with_obligations | ok | 2025-12-16T15:37:13.000Z | [来源](https://huggingface.co/datasets/allenai/Molmo2-VideoTrack) |
| `videochat_flash_training` | text, image, video | sft | optional | review_required | ok | 2025-06-24T07:51:17.000Z | [来源](https://huggingface.co/datasets/OpenGVLab/VideoChat-Flash-Training-Data) |

### vision_grounding（`vision_grounding`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `pixmo_count_train` | text, image | sft | core | allowed_with_obligations | ok | 2024-11-30T04:08:58.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-count) |
| `pixmo_point_explanations` | text, image | sft | optional | allowed_with_obligations | ok | 2024-12-05T18:45:24.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-point-explanations) |
| `pixmo_points` | text, image | sft | core | allowed_with_obligations | ok | 2024-11-27T22:12:24.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-points) |

### 视觉指令与 SFT（`vision_sft`）

| ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| `finevision` | text, image | sft | optional | review_required | ok | 2025-10-21T10:12:56.000Z | [来源](https://huggingface.co/datasets/HuggingFaceM4/FineVision) |
| `llava15_mix665k` | text, image | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/haotian-liu/LLaVA) |
| `llava_instruct_150k` | text, image | sft | research_only | noncommercial | ok | 2024-01-03T01:59:20.000Z | [来源](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K) |
| `llava_onevision15_instruct_22m` | text, image | sft | optional | review_required | ok | 2026-07-16T16:14:35.000Z | [来源](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data) |
| `pixmo_ask_model_anything` | text, image | sft | core | allowed_with_obligations | ok | 2024-12-05T18:45:02.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-ask-model-anything) |
| `pixmo_cap_qa` | text, image | sft | optional | allowed_with_obligations | ok | 2024-12-05T18:49:29.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-cap-qa) |

## 自动化边界

- 分类、模态、规模、许可和 `usage_tier` 以人工维护的 canonical 总表为准。
- API 返回的许可仅用于变更提醒，不会自动把 `review_required` 改成可商用。
- 新发现数据只进入 `datasets-candidates.yaml`，必须人工审核后才能加入 canonical 总表。
- 多模态资产不会自动进入现有 ERNIE 文本配方；`eval_only` 与私有／时间外评测始终禁止训练。
