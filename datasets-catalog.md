# Base LLM 后训练数据自动目录

> 自动更新：2026-11-09T06:01:42Z；canonical 输入：`datasets-list.yaml`。本文件只生成视图，不改写人工许可和训练分层。
> 共 114 项已收录资产；待审核候选 11 项。候选数据不会自动进入训练配方。

## 分层与阶段索引

| 维度 | 值 | 数量 |
|---|---|---:|
| usage_tier | `core` | 23 |
| usage_tier | `eval_only` | 31 |
| usage_tier | `local_required` | 5 |
| usage_tier | `optional` | 37 |
| usage_tier | `research_only` | 18 |
| stage | `agent_rl` | 5 |
| stage | `agent_sft` | 6 |
| stage | `evaluation` | 36 |
| stage | `preference` | 17 |
| stage | `prm` | 3 |
| stage | `reward_model` | 15 |
| stage | `rlvr` | 12 |
| stage | `sft` | 54 |

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

## 分类目录

### 浏览与网页导航 Agent（`agent_browser`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `weblinx` | agent_sft | research_only | noncommercial | ok | 2024-12-07T04:23:40.000Z | [来源](https://huggingface.co/datasets/McGill-NLP/WebLINX) |

### 搜索与浏览 Agent（`agent_search`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `search_r1` | agent_rl | optional | review_required | not_tracked | — | [来源](https://github.com/PeterGriffinJin/Search-R1) |

### 软件工程 Agent（`agent_swe`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `r2e_gym` | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://r2e-gym.github.io/) |
| `swe_gym` | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://arxiv.org/abs/2412.21139) |
| `swe_smith` | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://github.com/SWE-bench/SWE-smith) |

### 中文指令与领域数据（`chinese`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `belle` | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/LianjiaTech/BELLE) |
| `chinese_r1_distill_110k` | sft | optional | review_required | ok | 2025-02-21T02:18:08.000Z | [来源](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k) |
| `coig_cqia` | sft | research_only | noncommercial | not_tracked | — | [来源](https://arxiv.org/html/2403.18058v2) |
| `coig_pc_lite` | sft | core | review_required | ok | 2024-06-14T01:18:23.000Z | [来源](https://huggingface.co/datasets/BAAI/COIG-PC-Lite) |
| `firefly` | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/yangjianxin1/Firefly) |

### 代码 SFT 与推理（`code`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `codecontests` | sft, rlvr | core | allowed_with_obligations | ok | 2023-06-11T12:22:30.000Z | [来源](https://huggingface.co/datasets/deepmind/code_contests) |
| `codefeedback_filtered` | sft | optional | review_required | ok | 2024-02-26T09:25:26.000Z | [来源](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction) |
| `kodcode` | sft, rlvr | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2503.02951) |
| `magicoder` | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2312.02120v2) |
| `opencode_reasoning` | sft | core | allowed_with_obligations | ok | 2025-05-04T23:54:22.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) |
| `opencodeinstruct` | sft | core | allowed_with_obligations | ok | 2025-04-28T19:08:02.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) |
| `taco` | sft, rlvr | core | review_required | ok | 2024-06-19T09:16:49.000Z | [来源](https://huggingface.co/datasets/BAAI/TACO) |

### 独立评测（`evaluation`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `agentdojo` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ethz-spylab/agentdojo) |
| `agentharm` | evaluation | eval_only | eval_only | ok | 2024-12-19T13:27:30.000Z | [来源](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) |
| `bbh` | evaluation | eval_only | eval_only | ok | 2025-07-11T17:27:58.000Z | [来源](https://huggingface.co/datasets/lukaemon/bbh) |
| `bfcl` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) |
| `bigcodebench` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/bigcode-project/bigcodebench) |
| `enigmata_eval` | evaluation | eval_only | eval_only | ok | 2025-05-27T08:14:17.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval) |
| `falsereject_test` | evaluation | eval_only | eval_only | ok | 2025-05-14T19:16:44.000Z | [来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| `gpqa_diamond` | evaluation | eval_only | eval_only | ok | 2026-09-21T22:29:06.000Z | [来源](https://huggingface.co/datasets/Idavidrein/gpqa) |
| `gsm8k_test` | evaluation | eval_only | eval_only | ok | 2026-03-23T10:18:13.000Z | [来源](https://huggingface.co/datasets/openai/gsm8k) |
| `harmbench` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/centerforaisafety/HarmBench) |
| `ifeval` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/google-research/google-research/tree/master/instruction_following_eval) |
| `livecodebench_v6` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/LiveCodeBench/LiveCodeBench) |
| `longbench_chat` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/THUDM/LongAlign) |
| `longbench_cite` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/THUDM/LongCite) |
| `longform_test` | evaluation | eval_only | eval_only | ok | 2024-03-05T15:20:00.000Z | [来源](https://huggingface.co/datasets/akoksal/LongForm) |
| `math_500` | evaluation | eval_only | eval_only | ok | 2025-12-15T11:01:40.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) |
| `mgsm` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://arxiv.org/abs/2210.03057) |
| `mind2web_test` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/OSU-NLP-Group/Mind2Web) |
| `mmlu_pro` | evaluation | eval_only | eval_only | ok | 2026-05-02T06:26:05.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro) |
| `mt_bench` | evaluation | eval_only | eval_only | ok | 2023-07-03T20:52:34.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts) |
| `omni_math` | evaluation | eval_only | eval_only | ok | 2024-10-12T09:02:05.000Z | [来源](https://huggingface.co/datasets/KbsdJames/Omni-MATH) |
| `prmbench` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ssmisya/PRMBench) |
| `processbench` | evaluation | eval_only | eval_only | ok | 2024-12-27T14:05:30.000Z | [来源](https://huggingface.co/datasets/Qwen/ProcessBench) |
| `rewardbench` | evaluation | eval_only | eval_only | ok | 2024-09-09T16:11:45.000Z | [来源](https://huggingface.co/datasets/allenai/reward-bench) |
| `rewardbench2` | evaluation | eval_only | eval_only | ok | 2025-06-04T08:53:38.000Z | [来源](https://huggingface.co/datasets/allenai/reward-bench-2) |
| `ruler` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/NVIDIA/RULER) |
| `sorry_bench_202503` | evaluation | eval_only | eval_only | ok | 2025-02-28T21:58:59.000Z | [来源](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503) |
| `strongreject` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/dsbowen/strong_reject) |
| `swebench_verified` | evaluation | eval_only | eval_only | ok | 2025-02-18T23:48:55.000Z | [来源](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) |
| `tau_bench_2_text` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/sierra-research/tau2-bench) |
| `xstest` | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/paul-rottger/exaggerated-safety) |

### 通用指令与 SFT（`general_sft`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `dolci_instruct_sft` | sft | core | allowed_with_obligations | ok | 2026-02-03T00:08:38.000Z | [来源](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT) |
| `dolly_15k` | sft | core | allowed_with_obligations | ok | 2023-06-30T18:34:13.000Z | [来源](https://huggingface.co/datasets/databricks/databricks-dolly-15k) |
| `infinity_instruct` | sft | optional | review_required | ok | 2025-12-04T07:56:39.000Z | [来源](https://huggingface.co/datasets/BAAI/Infinity-Instruct) |
| `lima` | sft | research_only | noncommercial | not_tracked | — | [来源](https://arxiv.org/html/2305.11206v4) |
| `nemotron_cascade_2_sft` | sft | optional | review_required | ok | 2026-03-19T23:57:48.000Z | [来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) |
| `no_robots` | sft | research_only | noncommercial | ok | 2024-04-18T08:40:39.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/no_robots) |
| `openhermes_2_5` | sft | optional | review_required | ok | 2024-04-15T08:18:12.000Z | [来源](https://huggingface.co/datasets/teknium/OpenHermes-2.5) |
| `smoltalk2` | sft | optional | review_required | not_tracked | — | [来源](https://huggingface.co/blog/smollm3) |
| `tulu3_sft_mixture` | sft | core | allowed_with_obligations | ok | 2024-12-02T19:48:33.000Z | [来源](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) |
| `wildchat` | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2405.01470v3) |

### 精确指令遵循（`instruction_following`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `ifeval_like_filtered` | sft | optional | review_required | ok | 2024-10-17T09:43:39.000Z | [来源](https://huggingface.co/datasets/argilla/ifeval-like-data) |
| `tulu3_persona_if` | sft | core | allowed_with_obligations | ok | 2024-11-21T15:57:21.000Z | [来源](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following) |

### 本地必需物料（`local_required`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `local_domain_safety` | sft, preference, reward_model, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_domain_zh_sft` | sft | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_no_tool_negative` | sft, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_overrefusal` | sft, preference, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| `local_private_time_eval` | evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |

### 长上下文与引用（`long_context`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `longalign_10k` | sft | optional | review_required | ok | 2024-02-22T11:39:00.000Z | [来源](https://huggingface.co/datasets/zai-org/LongAlign-10k) |
| `longcite_45k` | sft | core | allowed_with_obligations | ok | 2024-10-18T09:59:40.000Z | [来源](https://huggingface.co/datasets/zai-org/LongCite-45k) |

### 长输出生成（`long_output`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `longform` | sft | optional | review_required | ok | 2024-03-05T15:20:00.000Z | [来源](https://huggingface.co/datasets/akoksal/LongForm) |

### 数学 SFT（`math`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `numina_math_cot` | sft | optional | review_required | not_tracked | — | [来源](https://github.com/project-numina/aimo-progress-prize) |
| `openmath_reasoning` | sft | core | allowed_with_obligations | ok | 2025-05-27T18:43:44.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenMathReasoning) |
| `openmathinstruct2` | sft | core | allowed_with_obligations | ok | 2024-11-25T20:07:28.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) |

### 多语言指令数据（`multilingual`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `aya_collection` | sft | optional | allowed_with_obligations | ok | 2025-04-15T08:52:39.000Z | [来源](https://huggingface.co/datasets/CohereLabs/aya_collection) |
| `aya_dataset` | sft | core | allowed_with_obligations | ok | 2025-04-15T08:51:55.000Z | [来源](https://huggingface.co/datasets/CohereLabs/aya_dataset) |
| `m2lingual` | sft | research_only | noncommercial | ok | 2024-08-13T19:01:43.000Z | [来源](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual) |
| `oasst2` | sft, preference | optional | allowed_with_obligations | not_tracked | — | [来源](https://arxiv.org/html/2304.07327v3) |

### 偏好与奖励模型（`preference`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `arena_human_preference_140k` | preference, reward_model | optional | review_required | ok | 2025-08-01T05:03:39.000Z | [来源](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k) |
| `helpsteer` | reward_model, preference | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2406.08673v1) |
| `helpsteer2` | preference, reward_model | core | allowed_with_obligations | ok | 2024-12-18T21:06:57.000Z | [来源](https://huggingface.co/datasets/nvidia/HelpSteer2) |
| `helpsteer3_preference` | preference, reward_model | core | allowed_with_obligations | ok | 2025-11-16T07:18:00.000Z | [来源](https://huggingface.co/datasets/nvidia/HelpSteer3) |
| `hh_rlhf` | preference, reward_model | optional | allowed_with_obligations | ok | 2023-05-26T18:47:34.000Z | [来源](https://huggingface.co/datasets/Anthropic/hh-rlhf) |
| `nectar` | preference, reward_model | optional | review_required | ok | 2024-03-20T04:17:46.000Z | [来源](https://huggingface.co/datasets/berkeley-nest/Nectar) |
| `shp` | preference, reward_model | optional | review_required | ok | 2023-10-10T23:35:57.000Z | [来源](https://huggingface.co/datasets/stanfordnlp/SHP) |
| `skywork_reward_preference_80k` | preference, reward_model | optional | review_required | ok | 2024-10-25T01:58:25.000Z | [来源](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2) |
| `summarize_from_feedback` | preference, reward_model | research_only | review_required | ok | 2023-01-03T16:55:41.000Z | [来源](https://huggingface.co/datasets/openai/summarize_from_feedback) |
| `tulu3_preference_mixture` | preference, reward_model | research_only | noncommercial | ok | 2025-02-04T00:21:47.000Z | [来源](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture) |
| `ultrafeedback` | preference, reward_model | optional | review_required | ok | 2023-12-29T14:11:19.000Z | [来源](https://huggingface.co/datasets/openbmb/UltraFeedback) |
| `webgpt_comparisons` | preference, reward_model | research_only | review_required | ok | 2022-12-19T17:55:29.000Z | [来源](https://huggingface.co/datasets/openai/webgpt_comparisons) |

### 过程奖励与步级监督（`process_reward`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `math_shepherd` | prm | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/abs/2312.08935) |
| `pathfinder_prm` | prm | research_only | review_required | not_tracked | — | [来源](https://github.com/declare-lab/PathFinder-PRM) |
| `prm800k` | prm | optional | allowed_with_obligations | not_tracked | — | [来源](https://github.com/openai/prm800k) |

### 通用与蒸馏推理（`reasoning`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `limo` | sft | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2502.03387v1) |
| `mixture_of_thoughts` | sft | optional | review_required | ok | 2025-05-26T15:25:56.000Z | [来源](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts) |
| `natural_reasoning` | sft | research_only | noncommercial | ok | 2025-02-21T06:02:40.000Z | [来源](https://huggingface.co/datasets/facebook/natural_reasoning) |
| `openthoughts3` | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2506.04178v1) |
| `s1k` | sft | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2501.19393v1) |

### 代码 RLVR（`rlvr_code`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `acecode_87k` | rlvr | core | review_required | not_tracked | — | [来源](https://arxiv.org/html/2502.01718v4) |

### rlvr_general（`rlvr_general`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `enigmata_data` | rlvr | research_only | noncommercial | ok | 2025-08-13T09:00:27.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data) |
| `nemotron_cascade_2_rl` | rlvr, agent_rl, sft | optional | allowed_with_obligations | ok | 2026-03-20T03:38:20.000Z | [来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) |

### 指令遵循 RLVR（`rlvr_if`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `verinstruct` | rlvr | core | review_required | not_tracked | — | [来源](https://aclanthology.org/2025.emnlp-main.1542/) |

### 数学 RLVR（`rlvr_math`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `big_math_rl_verified` | rlvr | core | allowed_with_obligations | ok | 2025-03-25T15:33:48.000Z | [来源](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) |
| `dapo_math_17k` | rlvr | core | allowed_with_obligations | ok | 2025-04-18T11:20:51.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) |
| `deepmath_103k` | rlvr | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2504.11456v2) |
| `deepscaler_preview` | rlvr | core | allowed_with_obligations | ok | 2025-02-10T09:51:18.000Z | [来源](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset) |
| `skywork_or1_rl` | rlvr | optional | review_required | ok | 2025-05-29T02:27:10.000Z | [来源](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) |

### 安全、拒答与防过拒（`safety`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `aegis_content_safety_2` | sft, reward_model | core | allowed_with_obligations | ok | 2025-06-09T19:15:56.000Z | [来源](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) |
| `falsereject_train` | sft | research_only | noncommercial | ok | 2025-05-14T19:16:44.000Z | [来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| `pku_saferlhf` | preference, reward_model, sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/PKU-Alignment/beavertails) |
| `wildguardmix_tulu3` | sft, preference | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2411.15124v2) |

### 工具与函数调用（`tool`）

| ID | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|
| `api_bank` | sft, evaluation | optional | review_required | not_tracked | — | [来源](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) |
| `glaive_function_calling_v2` | sft | optional | allowed_with_obligations | ok | 2023-09-27T18:04:08.000Z | [来源](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2) |
| `toolace` | sft | core | review_required | not_tracked | — | [来源](https://arxiv.org/html/2409.00917v1) |
| `toolbench` | sft, agent_sft | optional | review_required | not_tracked | — | [来源](https://github.com/OpenBMB/ToolBench) |
| `toolmind` | sft, agent_sft | optional | allowed_with_obligations | ok | 2026-01-09T02:23:42.000Z | [来源](https://huggingface.co/datasets/Nanbeige/ToolMind) |
| `xlam_function_calling` | sft | core | review_required | ok | 2025-01-24T19:25:58.000Z | [来源](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) |

## 自动化边界

- 分类、规模、许可和 `usage_tier` 以人工维护的 canonical 总表为准。
- API 返回的许可仅用于变更提醒，不会自动把 `review_required` 改成可商用。
- 新发现数据只进入 `datasets-candidates.yaml`，必须人工审核后才能加入 canonical 总表。
- `eval_only` 与私有／时间外评测始终禁止训练。
