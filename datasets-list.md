# Base 与多模态模型后训练 datasets-list

> 范围：文本、图像、视频、音频 Base 模型的 instruction/SFT、偏好、RLVR、PRM、Agent 与独立评测数据物料。这里的“完整”是能力与治理覆盖完整，不是穷尽公开数据集，也不代表所有条目已获商用批准。

## 1. 验收结论

- 共 **175 项资产**：文本 **114/114 全部保留**，多模态扩展 **61 项**；最初 **42/42 保留**。
- **core 30**；**eval_only 60**；**local_required 8**；**optional 51**；**research_only 26**。
- **38 项必需能力均有训练候选和独立评测引用**，结构覆盖已闭合；实际训练仍受版本、许可、质量、去污和验证器签署约束。
- **现有商用默认／研究隔离配方仍是 ERNIE 文本专用**：多模态资产不会自动进入；多模态 Base、processor 与硬件未指定前不伪造启动配方。
- 公开数据无法替代八类本地物料：真实业务中文、无需工具负例、正常请求防过拒、领域安全、私有／时间外评测、真实业务多模态、多模态偏好／音频 RL、本地 GUI 动作安全。
- **eval_only 资产严禁训练**；同 repo 的训练与测试切分、静态 GUI 轨迹与在线环境均分开管理。

## 2. 推荐配方骨架（不是全量混用清单）

| 阶段 | 首轮候选 | 使用原则 |
|---|---|---|
| 通用 SFT | Dolci-Instruct-SFT 或 Tulu 3 SFT Mixture；人工小集可补 Dolly | 主集先二选一；按有效 token 和子集消融，避免大合集直接相加 |
| 中文与多语言 | 本地真实业务中文 + COIG-PC-Lite + Aya Dataset；研究侧补 M2Lingual | COIG 与中文 R1 蒸馏先复核上游；Aya 与 Aya Collection 按来源去重 |
| 精确指令 | Tulu 3 Persona IF + IFEval-like filtered；需要 RL 时再加 VerInstruct | 硬约束用程序验证，IFEval 只做评测；IFEval-like 必须另行去污 |
| 长文、长输出与引用 | LongCite-45k + LongForm；长输入不足时加 LongAlign | 长输入、长输出和引用分别验收；LongForm test 独立 |
| 数学 SFT/RLVR | OpenMathInstruct-2 降采样或 OpenMathReasoning；DAPO-Math-17k/DeepScaleR | 母题去污、答案等价验证，MATH-500/GSM8K/Omni-MATH/MGSM 隔离 |
| 代码 SFT/RLVR | OpenCodeInstruct 或 OpenCodeReasoning；TACO/CodeContests/AceCode | 蒸馏与可执行题分开，沙箱重跑并保留隐藏测试 |
| 工具与浏览 | xLAM + ToolACE + ToolMind + 本地不调用负例；研究侧补 WebLINX | 固定 Schema、实际执行和来源去重；静态网页轨迹不等于动态环境 |
| 偏好/奖励模型 | HelpSteer3 或 HelpSteer2；按许可补 Arena/Skywork v0.2 | 保留同提示切分；RewardBench/RewardBench 2 仅评测 |
| 安全与 Agent 安全 | Aegis 2.0 分类 + 本地政策/防过拒/工具注入数据；研究侧补 FalseReject | 危险原文不直接当普通聊天 SFT；同时测拒答、过拒、攻击成功率与任务效用 |
| PRM/Agent | PRM800K；Search-R1/SWE-Gym/Nemotron RL 等按环境能力选择 | 严格切分；环境、任务、轨迹、训练子集和 RL／蒸馏配置分别计数 |
| 视觉指令与文档 | PixMo Ask／Docs＋本地中文多模态；大合集按 config 消融 | 图像 SHA、隐私、上游权利和 OCR／定位格式分别验收；558K 对齐预训练不纳入 |
| 多图与视频 | Mantis＋LLaVA-Video／VideoChat-Flash；Molmo2 补时空指向 | 视频数、问答数、帧数、时长和媒体 token 分开配比；固定字幕与抽帧协议 |
| 多模态偏好／RLVR | 人类偏好、AI 反馈、构造负例分 profile；R1-Onevision／Visual-RFT 按任务选 | 不混标偏好来源；数学、坐标、检测和格式奖励分别重跑 |
| 音频与 GUI | VoiceAssistant＋本地音频偏好；OS-Atlas action＋GUIOdyssey＋本地动作安全 | 固定 SNAC／采样率；GUI 区分 episode、action step、grounding 和在线任务成功率 |
| 多模态安全 | VLGuard＋本地政策；SPA-VL／SafeVid 研究隔离 | chosen 也需安全审核；同时测 ASR、正常请求效用、幻觉和过拒 |

## 3. 能力覆盖矩阵

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

## 4. 分层数量与许可状态

### 使用层级

| usage_tier | 数量 |
|---|---:|
| core | 30 |
| eval_only | 60 |
| local_required | 8 |
| optional | 51 |
| research_only | 26 |

### 公共训练／研究资产的 commercial_status

| 状态 | 数量 | 含义 |
|---|---:|---|
| allowed_with_obligations | 34 | 许可字段较明确，但仍须署名、上游和教师条款审查 |
| noncommercial | 17 | 非商用研究隔离 |
| review_required | 56 | 许可、访问条件、上游或教师条款待复核 |

## 5. 全量资产目录

### agent_browser

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `weblinx` | text | agent_sft／research_only | chat_turns；固定 WebLINX 1.0 chat train；WebLINX 1.1/BrowserGym 是不同版本，规模不混写 | CC-BY-NC-SA-4.0／noncommercial | 非商用静态浏览轨迹研究；固定 1.0、脱敏并用 BrowserGym 版本另做动态评测；风险：非商用及相同方式共享义务；原始轨迹可能含测试账号、密码和动态 HTML；文本投影不保证动态环境可复现 | [官方来源](https://huggingface.co/datasets/McGill-NLP/WebLINX) |

### agent_search

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `search_r1` | text | agent_rl／optional | 169,615 questions；NQ 79,168 + HotpotQA 90,447 的可复现训练口径 | mixed-review-required／review_required | 端到端搜索 RL 基线；环境观测屏蔽策略梯度；风险：检索器、语料快照和动作空间决定可复现性；上游数据许可分离 | [官方来源](https://github.com/PeterGriffinJin/Search-R1) |

### agent_swe

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `swe_gym` | text | agent_sft, agent_rl／optional | 2,438 executable_tasks；论文 SFT 仅使用 491 条成功轨迹 | mixed-review-required／review_required | 仓库级 Agent 小闭环候选；风险：任务数不等于轨迹数；仓库提交、依赖、测试与许可需固定 | [官方来源](https://arxiv.org/abs/2412.21139) |
| `swe_smith` | text | agent_sft, agent_rl／optional | 52,000 task_instances；当前约 52K 任务、26K 轨迹、250+ 环境；训练子集另计 | mixed-review-required／review_required | 大规模 SWE 环境和轨迹生成候选；风险：任务、轨迹和实际训练子集不可混计；版本口径会变化 | [官方来源](https://github.com/SWE-bench/SWE-smith) |
| `r2e_gym` | text | agent_sft, agent_rl／optional | 8,100 executable_tasks；约 8.1K 可执行任务 | mixed-review-required／review_required | 仓库级 Agent RL；按仓库隔离切分；风险：同仓库随机切分泄漏；环境与底层代码许可分离 | [官方来源](https://r2e-gym.github.io/) |

### audio_sft

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `voice_assistant_400k` | text, audio | sft／optional | 470,054 train_samples；当前 default/train 470,054，不是名称中的 400K；question_audio＋文本答案＋answer_snac | Apache-2.0 + GPT-4o/TTS-terms／review_required | 语音助手 SFT 候选；固定采样率、SNAC codec、说话人和文本／音频 loss mask；风险：英文合成语音与教师／TTS 条款；回答音频是 SNAC token 而非普通波形；缺少独立测试切分 | [官方来源](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K) |

### chinese

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `coig_pc_lite` | text | sft／core | 52,232 samples；中文指令样本精确数 | Apache-2.0（项目口径）；HF unknown／review_required | 中文候选补集；完成许可复核后再进入商用默认配方；风险：当前 HF 许可字段 unknown，商用前必须核对固定版本许可原文 | [官方来源](https://huggingface.co/datasets/BAAI/COIG-PC-Lite) |
| `coig_cqia` | text | sft／research_only | 48,373 samples；23 个中文互联网来源 | CC-BY-NC-4.0／noncommercial | 非商用中文分布研究补集；风险：非商用；隐私、事实性和论坛噪声 | [官方来源](https://arxiv.org/html/2403.18058v2) |
| `belle` | text | sft／research_only | 1,500,000 samples；约 150 万中文 Self-Instruct | research-only-custom／noncommercial | 仅作非商用中文合成数据基线；风险：项目禁止商用；模板化和教师错误 | [官方来源](https://github.com/LianjiaTech/BELLE) |
| `firefly` | text | sft／research_only | 1,150,000 samples；约 115 万、23 类中文任务 | CC-BY-NC-SA-4.0／noncommercial | 非商用中文多任务训练；风险：非商用及相同方式共享义务 | [官方来源](https://github.com/yangjianxin1/Firefly) |
| `chinese_r1_distill_110k` | text | sft／optional | 110,000 samples；Math 36,568、Exam 2,432、STEM 12,648、General 58,352 | Apache-2.0 + mixed-upstream／review_required | 中文推理蒸馏补集；按 repo_name 继承许可审查、事实抽检与母题去污；风险：官方承认事实性未经严格验证；模型评分可能不准确；COIG-CQIA/GSM8K_zh 等上游许可和评测重叠 | [官方来源](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k) |

### code

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `kodcode` | text | sft, rlvr／optional | 447,000 problem_solution_test_triples；约 44.7 万题目—解答—测试三元组 | review-required／review_required | 沙箱重跑后用于代码 SFT 或 RLVR；风险：测试覆盖与环境依赖；许可需按固定版本复核 | [官方来源](https://arxiv.org/html/2503.02951) |
| `magicoder` | text | sft／optional | 75,000 samples；OSS-Instruct 约 75K；Self-OSS-Instruct 另约 50K | mixed-review-required／review_required | 代码指令入门补集；逐来源审查；风险：不自带可靠单元测试；开源代码启发不等于统一许可 | [官方来源](https://arxiv.org/html/2312.02120v2) |
| `opencode_reasoning` | text | sft／core | 735,255 python_reasoning_samples；28,319 道独立竞赛题；split_0 567,850 + split_1 167,405 | CC-BY-4.0／allowed_with_obligations | 代码推理 SFT 主候选；按母题去重并核验所用上游；风险：题目与 TACO/APPS/CodeContests 等重叠；是蒸馏样本集而非直接 RLVR 题目库 | [官方来源](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) |
| `taco` | text | sft, rlvr／core | 25,443 train_problems；另有 1,000 test；约 155 万验证解答 | Apache-2.0 + mixed-upstream／review_required | 可执行代码题主候选；过滤无测试样本并复核上游权利；风险：HackerRank 等部分上游权利官方也不确定；测试字段有缺失和更新历史 | [官方来源](https://huggingface.co/datasets/BAAI/TACO) |
| `codecontests` | text | sft, rlvr／core | 13,328 train_problems；另 validation 117、test 165；含正确／错误人类解和多类测试 | CC-BY-4.0／allowed_with_obligations | 竞赛代码执行奖励主候选；隐藏测试仅作验证；风险：私有测试不得作为模型输入；多平台来源与重复题 | [官方来源](https://huggingface.co/datasets/deepmind/code_contests) |
| `opencodeinstruct` | text | sft／core | 5,000,000 instruction_response_pairs；精确 500 万 Python 代码 SFT；含 domain、unit_tests、执行状态和平均分 | CC-BY-4.0／allowed_with_obligations | 大规模代码 SFT 主候选；按执行分数过滤、沙箱复跑并按母题去重；风险：The Stack V2、TACO 与教师生成上游需复核；有测试字段不等于全部样本可直接转 RLVR | [官方来源](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) |
| `codefeedback_filtered` | text | sft／optional | 156,000 samples_approx；README 称约 156K；从 287K 查询筛选复杂度 4/5 的单轮代码指令 | Apache-2.0 + teacher-terms／review_required | 复杂代码指令可选补集；按固定文件实际计数并做教师条款与来源去重审查；风险：README 156K 与历史规模标签口径需固定版本复核；部分数据由 OpenAI 模型生成；Magicoder/ShareGPT/Evol-Instruct 来源重叠 | [官方来源](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction) |

### document_sft

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `pixmo_docs` | text, image | sft／core | 251,165 train_samples_total；charts 116,814＋diagrams 16,551＋other 71,282＋tables 46,518；各 config 另有 1,024 validation | ODC-By／allowed_with_obligations | 文档／图表主候选；固定四 config train，validation 不进训练；风险：四 config 分布不同；文档隐私、图像权利和 validation 隔离 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-docs) |

### evaluation

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `ifeval` | text | evaluation／eval_only | prompts；使用官方 input_data 固定版本；程序检查可验证指令 | Apache-2.0／eval_only | 精确指令独立评测；不得使用其提示改写训练；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/google-research/google-research/tree/master/instruction_following_eval) |
| `longbench_chat` | text | evaluation／eval_only | queries；10K–100K 真实用户长上下文查询；GPT-4 judge | mixed-see-official-card／eval_only | 长输入指令遵循评测；judge 版本固定；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/THUDM/LongAlign) |
| `longbench_cite` | text | evaluation／eval_only | queries；来自 LongBench 与 LongBench-Chat 的引用评测 | mixed-see-official-card／eval_only | 分别报告答案正确性和引用质量；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/THUDM/LongCite) |
| `mmlu_pro` | text | evaluation／eval_only | 12,032 test_questions；另 validation 70；持续修订，必须记录 revision | MIT／eval_only | 知识与推理评测；不将 CoT 字段用于训练；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro) |
| `bbh` | text | evaluation／eval_only | task_configs；27 个 config，分别固定并汇总；不要无版本引用单一总数 | mixed-see-official-card／eval_only | 通用推理评测；按任务报告宏平均与样本加权；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/lukaemon/bbh) |
| `math_500` | text | evaluation／eval_only | 500 problems；PRM800K 官方 MATH 切分的 500 题子集 | mixed-see-official-card／eval_only | 高难数学保留评测；尤其检查 PRM800K 污染；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) |
| `gsm8k_test` | text | evaluation／eval_only | 1,319 test_problems；train 7,473 不纳入本 eval_only 资产 | MIT／eval_only | 基础多步数学保留评测；与训练切分隔离；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/openai/gsm8k) |
| `livecodebench_v6` | text | evaluation／eval_only | 1,055 problems；题目发布时间为 2023-05 至 2025-04；必须写 release_v6 | MIT／eval_only | 代码生成、执行、修复和输出预测评测；优先 Base 之后时间窗；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/LiveCodeBench/LiveCodeBench) |
| `bfcl` | text | evaluation／eval_only | versioned_test_cases；按 BFCL 版本和类别计数；含 AST、可执行、多轮、多步等 | Apache-2.0／eval_only | 函数调用独立评测；固定版本、工具 Schema 和类别；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) |
| `rewardbench` | text | evaluation／eval_only | 2,985 preference_pairs；raw 5,123；filtered 2,985，含 Chat/Chat Hard/Safety/Reasoning | ODC-By-1.0 + mixed-upstream／eval_only | 奖励模型评测；Skywork 等训练集必须使用对应去污版；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/allenai/reward-bench) |
| `processbench` | text | evaluation／eval_only | annotated_solutions；GSM8K/MATH/OlympiadBench/OmniMATH 四个文件分开计数 | Apache-2.0／eval_only | 步级错误定位评测；不得转 PRM 训练；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/Qwen/ProcessBench) |
| `swebench_verified` | text | evaluation／eval_only | 500 issue_pr_pairs；人工验证的 SWE-bench test 子集 | mixed-see-official-card／eval_only | 仓库级软件工程保留评测；gold patch/test patch 不输入模型；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) |
| `xstest` | text | evaluation／eval_only | prompts；固定 exaggerated-safety 官方版本；safe/unsafe 分开报告 | CC-BY-4.0／eval_only | 拒答与过拒双向评测；不可只报 unsafe 拒答率；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/paul-rottger/exaggerated-safety) |
| `longform_test` | text | evaluation／eval_only | 2,045 test_samples；LongForm 官方 test；train 23,652 与 validation 2,042 均不得混入 | MIT + mixed-upstream／eval_only | 长输出独立评测；除长度外同时评分任务完成、事实与全局一致性；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/akoksal/LongForm) |
| `omni_math` | text | evaluation／eval_only | 4,428 competition_problems；33 个子领域、10 个难度级别；奥林匹克级数学 | Apache-2.0／eval_only | 高难数学保留评测；OpenMathInstruct/Numina 等必须按母题去污；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/KbsdJames/Omni-MATH) |
| `gpqa_diamond` | text | evaluation／eval_only | 198 questions；固定 gpqa_diamond config；不得与 Main 448 或 Extended 混写 | CC-BY-4.0 + gated-terms／eval_only | 研究生级科学推理评测；遵守 gated 条款，不公开传播题目文本；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/Idavidrein/gpqa) |
| `ruler` | text | evaluation／eval_only | configurable_tasks；4 类、13 个可配置任务；rulerv1-ns/rulerv2-ns 分支和生成长度必须固定 | Apache-2.0／eval_only | 长上下文合成评测；记录分支、任务配置、长度、种子与 tokenizer；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/NVIDIA/RULER) |
| `bigcodebench` | text | evaluation／eval_only | 1,140 full_tasks；Hard 148；Complete/Instruct 两种提示模式分别报告 | Apache-2.0／eval_only | 实用代码生成执行评测；固定包版本、subset、split 与沙箱；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/bigcode-project/bigcodebench) |
| `mgsm` | text | evaluation／eval_only | 250 parallel_problems_per_language；同一 250 道 GSM8K 题人工译为 10 种语言，另有英文；按语言分别报告 | mixed-see-official-card／eval_only | 多语言数学保留评测；与 GSM8K_zh 及翻译训练数据做跨语言母题去污；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://arxiv.org/abs/2210.03057) |
| `mt_bench` | text | evaluation／eval_only | 80 multi_turn_prompts；固定官方 80 个两轮提示与 judge；不能把 judge 输出用于训练 | Apache-2.0／eval_only | 通用多轮对话评测；固定提示、参考回答、judge 和采样参数；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts) |
| `rewardbench2` | text | evaluation／eval_only | 1,865 test_samples；Factuality/Precise IF/Math/Safety/Focus/Ties 六类；单轮 | ODC-By + third-party-model-terms／eval_only | 新一代奖励模型评测；按官方六类计分，不能沿用 RewardBench v1 算法；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/allenai/reward-bench-2) |
| `prmbench` | text | evaluation／eval_only | step_level_evaluation_samples；固定官方 prmtest_classified 数据与版本；规模未从官方卡片直接核实则不填 | mixed-see-official-card／eval_only | 细粒度过程奖励评测；与 PathFinder/PRM800K 按母题和轨迹去污；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/ssmisya/PRMBench) |
| `harmbench` | text | evaluation／eval_only | red_teaming_behaviors；标准化自动红队框架；按标准/上下文行为和固定分类器分别报告 | mixed-see-official-card／eval_only | 攻击与防御双向安全评测；固定行为集、攻击方法、分类器和试验次数；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/centerforaisafety/HarmBench) |
| `strongreject` | text | evaluation／eval_only | 313 forbidden_prompts；full 313、small 60；使用维护中的 dsbowen/strong_reject 而非旧仓库 | MIT + unlicensed-upstream-subsets／eval_only | 越狱鲁棒性评测；分别报告空攻击基线和各攻击，不只看拒答率；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/dsbowen/strong_reject) |
| `sorry_bench_202503` | text | evaluation／eval_only | 9,240 unsafe_instructions；base 440＋20 种语言/格式变换 8,800；44 类，gated 自定义协议 | sorry-bench-custom／eval_only | 安全拒答评测；接受并归档数据协议，不向第三方转移数据；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503) |
| `agentharm` | text | evaluation／eval_only | 44 public_test_base_behaviors；176 augmented；另有 validation 8 base／32 augmented；当前公开包不是论文全集 440 | MIT + safety-only-additional-clause／eval_only | Agent 有害与良性行为评测；canary 禁止训练，仅限改善 AI 安全/安保；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) |
| `mind2web_test` | text | evaluation／eval_only | 1,341 test_tasks；Cross Task 252、Cross Website 177、Cross Domain 912；train 1,009 不在本资产内 | CC-BY-4.0 + test-distribution-terms／eval_only | 浏览 Agent 跨任务/网站/领域评测；测试 zip 不再公开传播，canary 严禁训练；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/OSU-NLP-Group/Mind2Web) |
| `agentdojo` | text | evaluation／eval_only | dynamic_attack_defense_tasks；动态提示注入攻防环境；固定 suite、user task、attack、defense 与模型 | mixed-see-official-card／eval_only | 工具 Agent 提示注入攻防评测；分开报告效用和攻击成功率；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/ethz-spylab/agentdojo) |
| `enigmata_eval` | text | evaluation／eval_only | 4,758 puzzle_instances；Easy/Medium/Hard；36 任务、7 类，与 Enigmata-Data 严格分离 | Apache-2.0／eval_only | 逻辑谜题独立评测；训练生成器运行官方泄漏检查并固定任务排除清单；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval) |
| `falsereject_test` | text | evaluation／eval_only | 1,187 human_annotated_prompts；人工标注的看似有害但良性提示；训练 14,624 条单独管理 | CC-BY-NC-4.0／eval_only | 防过拒独立评测；固定 judge 并报告 Compliance Rate 与 USR_Benign；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| `tau_bench_2_text` | text | evaluation／eval_only | 900 single_trial_calls；6 语言×3 域×50 冻结任务；v2.0 与 v1.x 分数不可直接比较 | MIT／eval_only | 政策约束多轮工具 Agent 评测；固定 v2.0.0、text-v1、语言包与 pass^k；风险：公开评测污染；必须固定版本与切分 | [官方来源](https://github.com/sierra-research/tau2-bench) |
| `pixmo_count_test` | text, image | evaluation／eval_only | 540 test_samples；只用 test 540；train 36,916 和 validation 540 独立 | ODC-By／eval_only | 计数与点定位独立评测；按图像 SHA 对训练集去污；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-count) |
| `mmmu_validation` | text, image | evaluation／eval_only | 900 validation_questions；30 科目各 30；dev/test 不纳入本资产 | Apache-2.0／eval_only | 多学科视觉理解评测；固定全部科目 validation，test 通过官方协议另测；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/MMMU/MMMU) |
| `mmmu_pro_standard10` | text, image | evaluation／eval_only | 1,730 test_questions；standard 10 options；不与 4 options 或 vision config 混写 | Apache-2.0／eval_only | 鲁棒多学科推理评测；固定 10 options 并过滤纯文本可答泄漏检查；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/MMMU/MMMU_Pro) |
| `mathvista_testmini` | text, image | evaluation／eval_only | 1,000 testmini_questions；testmini 1,000；完整 test 5,141，分数不可混写 | CC-BY-SA-4.0／eval_only | 视觉数学推理评测；固定 testmini、答案类型和数值精度；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/AI4Math/MathVista) |
| `mathvision_test` | text, image | evaluation／eval_only | 3,040 test_questions；test 3,040；testmini 304 分开 | MIT／eval_only | 竞赛视觉数学保留评测；solution 字段不得转训练；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/MathLLMs/MathVision) |
| `docvqa_validation` | text, image | evaluation／eval_only | 5,349 validation_questions；DocVQA/validation 5,349；test 5,188 和 InfographicVQA 分开 | Apache-2.0／eval_only | 文档问答独立评测；固定 DocVQA config、validation 和 ANLS；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/lmms-lab/DocVQA) |
| `chartqa_test` | text, image | evaluation／eval_only | 2,500 test_questions；当前 lmms-lab default/test 2,500 | no-explicit-license-in-card／eval_only | 图表问答评测；human／augmented 类型分别报告；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/lmms-lab/ChartQA) |
| `ocrbench` | text, image | evaluation／eval_only | ocr_tasks；当前 lmms-lab HF API 401；固定官方仓库任务文件后再计数 | mixed-see-official-card／eval_only | 多场景 OCR 独立评测；固定任务文件与答案归一化；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/Yuliang-Liu/MultimodalOCR) |
| `mmstar` | text, image | evaluation／eval_only | test_questions；当前 lmms-lab HF API 401；不凭二手文章填规模 | mixed-see-official-card／eval_only | 视觉依赖综合能力评测；同时报告纯文本可答性检查；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/MMStar-Benchmark/MMStar) |
| `mantis_eval` | text, image, video | evaluation／eval_only | 217 test_questions；mantis_eval/test 217；不得并入 Mantis-Instruct | Apache-2.0／eval_only | 多图跨图指代、比较和推理评测；按 category 分报；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval) |
| `video_mme` | text, image, video, audio | evaluation／eval_only | 2,700 test_questions；videomme/test 2,700；字幕／无字幕和时长分桶分别报告 | no-explicit-license-in-card／eval_only | 短视频到长视频综合评测；固定字幕、FPS、帧数和媒体版本；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/lmms-lab/Video-MME) |
| `mlvu` | text, image, video | evaluation／eval_only | long_video_tasks；当前 MLVU/MLVU HF API 401；按官方任务与 dev/test 文件固定 | mixed-see-official-card／eval_only | 长视频多任务评测；固定任务、字幕、抽帧与生成／选择评分协议；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/JUNJIE99/MLVU) |
| `longvideobench` | text, image, video | evaluation／eval_only | long_video_questions；gated=auto；接受访问条件并固定发布包后计数 | CC-BY-NC-SA-4.0／eval_only | 长视频引用／推理评测；保留时间戳答案协议，NC-SA 仅限评测隔离；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/longvideobench/LongVideoBench) |
| `vl_rewardbench` | text, image | evaluation／eval_only | 1,247 test_samples_current_card；当前 default/test 1,247；论文常用 1,250，口径差异保留 | MIT／eval_only | 视觉奖励模型评测；按 general／hallucination／reasoning 分报并固定当前版本；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/MMInstruction/VL-RewardBench) |
| `mmhal_bench` | text, image | evaluation／eval_only | hallucination_questions；固定官方问题、图像和 GPT judge 版本 | mixed-see-official-card／eval_only | 视觉幻觉评测；judge 输出不得反哺训练；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/open-compass/MMHal-Bench) |
| `mm_safetybench` | text, image | evaluation／eval_only | adversarial_safety_questions；Text-only／SD／Typo／SD+Typo 分开；NC 研究评测 | CC-BY-NC-4.0／eval_only | 视觉越狱安全评测；分别报告 ASR 与正常请求可用性；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/isXinLiu/MM-SafetyBench) |
| `figstep` | text, image | evaluation／eval_only | typographic_jailbreak_prompts；固定图像化有害指令与评估器，禁止转训练 | mixed-see-official-card／eval_only | 排版图像越狱评测；危险内容隔离访问；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/ThuCCSLab/FigStep) |
| `safevidbench` | text, image, video | evaluation／eval_only | video_safety_questions；SafeVid-350K 训练偏好与本评测严格分开 | CC-BY-NC-SA-4.0／eval_only | 视频时序安全评测；固定视频、类别、judge 与 ASR／有用性指标；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/yxwang/SafeVid-350K) |
| `screenspot_v2` | text, image | evaluation／eval_only | gui_grounding_samples；mobile／desktop／web 分平台；当前 API 无统一切分行数 | Apache-2.0／eval_only | GUI 元素定位评测；固定坐标归一化、平台和点击命中规则；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2) |
| `gui_odyssey_test` | text, image | evaluation／eval_only | test_episodes；与所选 random/task/device/app train split 一一对应 | CC-BY-4.0／eval_only | 跨 App 动作匹配与任务成功率评测；严格使用对应 test split；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) |
| `osworld_verified` | text, image, video | evaluation／eval_only | executable_desktop_tasks；固定环境镜像、任务包和验证器；不是静态截图 QA | mixed-see-official-card／eval_only | 真实桌面在线 Agent 评测；报告任务成功率、危险动作和环境版本；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/xlang-ai/OSWorld) |
| `androidworld` | text, image, video | evaluation／eval_only | executable_mobile_tasks；固定任务套件、设备镜像和随机种子 | mixed-see-official-card／eval_only | 移动在线 Agent 评测；静态动作准确率不能替代任务成功率；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/google-research/android_world) |
| `voicebench` | text, audio | evaluation／eval_only | multi_config_speech_eval；AlpacaEval／CommonEval／SD-QA／MMSU／IFEval／AdvBench 等分别固定 | Apache-2.0／eval_only | 语音助手内容、指令、口音与安全评测；固定 TTS 声音、judge 和输出模态；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/hlt-lab/voicebench) |
| `mmau` | text, audio | evaluation／eval_only | audio_reasoning_questions；speech／sound／music 与 information extraction／reasoning 分报 | mixed-see-official-card／eval_only | 音频理解与推理评测；固定 test／mini、选项和 judge；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://sakshi113.github.io/mmau_homepage/) |
| `audiobench` | text, audio | evaluation／eval_only | versioned_audio_tasks；50+ 数据集是套件而非同质单集；逐 config 和版本固定 | mixed-see-official-card／eval_only | 语音、声场和说话人理解评测；逐任务报告，不能汇总未经核验的总行数；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/AudioLLMs/AudioBench) |
| `air_bench` | text, audio | evaluation／eval_only | audio_instruction_eval_samples；当前数据卡 CC-BY-NC-4.0；各音频任务／维度分别固定 | CC-BY-NC-4.0／eval_only | 开放音频指令与基础能力评测；固定 chat／foundation 维度和 judge；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset) |
| `cmmmu_test` | text, image | evaluation／eval_only | 11,000 test_questions；全集 12,012＝dev 112＋validation 900＋test 11,000；本项仅 test | mixed-see-official-card／eval_only | 中文大学多学科评测；通过官方 EvalAI 协议，禁止将题解转训练；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/CMMMU-Benchmark/CMMMU) |
| `cmmu` | text, image | evaluation／eval_only | 3,603 questions_total_official；七学科 3,603 题；validation 下载与 hosted test 分开报告 | mixed-see-official-card／eval_only | 中文教育多学科评测；填空题固定规则或 GPT judge 并分别报告；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/FlagOpen/CMMU) |
| `mmbench_cn` | text, image | evaluation／eval_only | chinese_multimodal_questions；dev-CN 与 test-CN 分开，CircularEval 等协议固定 | CC-BY-4.0／eval_only | 中文综合视觉理解评测；固定 CN split 和选项循环协议；风险：公开多模态评测污染；固定媒体文件、split、prompt、抽帧／解码和评分器版本 | [官方来源](https://github.com/open-compass/MMBench) |

### general_sft

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `dolci_instruct_sft` | text | sft／core | 2,150,000 samples；约 215 万；多能力、多语言混合集 | ODC-By-1.0／allowed_with_obligations | 作为通用主集候选；不要与其他大合集无去重叠加；风险：混合集上游与教师条款仍需逐项审查 | [官方来源](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT) |
| `nemotron_cascade_2_sft` | text | sft／optional | 15,870,000 samples；约 1,587 万；含 Agent、SWE、安全和长上下文 | NVIDIA Open Model License／review_required | 按来源、长度和质量抽样后做大规模消融；风险：自定义模型许可；全量训练成本高且子集异质 | [官方来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) |
| `tulu3_sft_mixture` | text | sft／core | 939,344 samples；最终公开 SFT 配方样本数 | ODC-By-1.0／allowed_with_obligations | 作为成熟配比与去污基线；与 Dolci 二选一为主；风险：含多上游数据，仍需谱系和教师条款审查 | [官方来源](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) |
| `smoltalk2` | text | sft／optional | 2,000,000 samples；约 200 万；含数学、代码、多轮和工具子集 | mixed-review-required／review_required | 中小模型多能力 SFT；逐子集固定版本；风险：多上游混合，不能只凭合集标签推断权利 | [官方来源](https://huggingface.co/blog/smollm3) |
| `no_robots` | text | sft／research_only | 10,000 conversations；约 1 万条人工编写对话 | CC-BY-NC-4.0／noncommercial | 用于非商用人工风格基准和小数据冷启动；风险：非商用；规模不足以独立建立广泛能力 | [官方来源](https://huggingface.co/datasets/HuggingFaceH4/no_robots) |
| `lima` | text | sft／research_only | 1,000 samples；精选小样本风格对齐集 | CC-BY-NC-SA-4.0／noncommercial | 仅用于非商用小数据质量消融；风险：非商用及相同方式共享义务；不能外推为全能力训练配方 | [官方来源](https://arxiv.org/html/2305.11206v4) |
| `wildchat` | text | sft／optional | 650,000 conversations；约 65 万对话、100 万轮次、204 种语言 | mixed-review-required／review_required | 只作受控真实分布补充，不作默认干净主集；风险：隐私、毒性、语言错标、提示注入和服务条款 | [官方来源](https://arxiv.org/html/2405.01470v3) |
| `openhermes_2_5` | text | sft／optional | 1,000,000 samples；约百万级 GPT-4 合成多源合集；legacy | unknown／review_required | 仅作 legacy 可选集，不作为新默认主集；风险：本次数据卡未见明确许可；多源重复和教师条款 | [官方来源](https://huggingface.co/datasets/teknium/OpenHermes-2.5) |
| `infinity_instruct` | text | sft／optional | 7,449,106 samples；此处固定为 7M config；3M/0613/0625/Gen 等配置分别计数 | CC-BY-SA-4.0／review_required | 可选大合集；不直接作为默认商用主集；风险：需登录接受条件；上游含 OpenHermes/FLAN/BELLE/COIG-CQIA/WildChat，继承许可与重复风险 | [官方来源](https://huggingface.co/datasets/BAAI/Infinity-Instruct) |
| `dolly_15k` | text | sft／core | 15,000 instruction_records；约 15K 人工编写英文指令，覆盖 8 类任务 | CC-BY-SA-3.0／allowed_with_obligations | 可商用人工指令冷启动与风格补集；保留署名和相同方式共享义务；风险：Wikipedia context 需保留来源和 ShareAlike 义务；规模小且英文单一 | [官方来源](https://huggingface.co/datasets/databricks/databricks-dolly-15k) |

### gui_agent

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `os_atlas_action_sft` | text, image | agent_sft／core | gui_action_samples；只登记下游 action SFT；13M GUI elements 属 Base grounding 预训练，不冒充 Agent 轨迹 | Apache-2.0 + upstream-terms／allowed_with_obligations | GUI 动作 SFT 候选；只选 action 子集并固定平台、历史和动作 schema；风险：grounding 与 action 子目录不同；截屏隐私、账号和坐标／动作 schema | [官方来源](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data) |
| `gui_odyssey_train` | text, image | agent_sft／core | 8,834 episodes_total_before_split；全集 8,834 episodes；实际训练量取决于 random/task/device/app 官方 split，不能写为单一训练行数 | CC-BY-4.0／allowed_with_obligations | 跨 App 轨迹主候选；每次实验固定一种官方 split 和动作历史长度；风险：episode 与 action step 不可混计；四种 split 不能交叉泄漏；截屏隐私和失败轨迹 | [官方来源](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) |
| `android_control_train` | text, image | agent_sft／research_only | gui_action_episodes；High-Level／Low-Level 与训练／测试分开；当前 HF API 401，未登记精确规模 | mixed-see-official-card／review_required | 访问恢复后补齐 revision、许可和 split；此前只作研究候选；风险：当前直接数据卡未核验；高低级指令、设备切分和测试泄漏 | [官方来源](https://github.com/google-research/google-research/tree/master/android_control) |

### instruction_following

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `tulu3_persona_if` | text | sft／core | 29,980 instruction_response_pairs；25 类可验证约束；messages + constraints | ODC-By-1.0／allowed_with_obligations | 精确指令 SFT 主补集；训练前运行确定性约束检查；风险：以英文合成数据为主；约束标签不等于每条响应均已程序验证 | [官方来源](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following) |
| `ifeval_like_filtered` | text | sft／optional | 56,339 filtered_samples；default 550,000；filtered 仅保留 prompt_level_strict_acc=True 的 56,339 条 | Qwen license (other)／review_required | 只用 filtered 配置作精确指令补集；对 IFEval 母题与提示隔离并复核 Qwen 条款；风险：Qwen2.5-72B-Instruct 教师条款；名称含 IFEval-like 不代表已对 IFEval 去污；default 可能含冲突指令和错误回答 | [官方来源](https://huggingface.co/datasets/argilla/ifeval-like-data) |

### local_required

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `local_domain_zh_sft` | text | sft／local_required | internal_records；由业务方定义规模、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 覆盖真实用户、真实知识库、失败工单和人工高质量回答；作为中文与领域效果的主要增量；风险：权利、隐私、机密和业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_no_tool_negative` | text | sft, evaluation／local_required | internal_records；由业务方定义规模、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 工具可用但无需调用时必须直接回答；与工具 SFT 同 profile 配比；风险：权利、隐私、机密和业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_overrefusal` | text | sft, preference, evaluation／local_required | internal_records；由业务方定义规模、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 覆盖医疗、法律、代码安全、敏感实体但合法的请求；保留合理回答与解释性拒答边界；风险：权利、隐私、机密和业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_domain_safety` | text | sft, preference, reward_model, evaluation／local_required | internal_records；由业务方定义规模、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 按实际产品政策标注，而非照搬历史通用安全偏好；覆盖工具返回注入、数据外泄和危险动作；危险内容隔离访问；风险：权利、隐私、机密和业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_private_time_eval` | text, image, video, audio | evaluation／local_required | internal_records；由业务方定义规模、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 冻结文本、图像、视频、音频与 GUI 私有／时间外评测；覆盖中文、业务分布、安全和污染检查，严禁训练；风险：权利、隐私、机密和业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_multimodal_sft` | text, image, video, audio | sft／local_required | internal_records；由业务方定义媒体规模、时长、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 覆盖真实中文图像、文档、视频和语音请求、失败案例与人工回答；记录媒体同意、时长和有效 token；风险：媒体权利、肖像／声音同意、隐私、机密与业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_multimodal_preference` | text, image, video, audio | preference, reward_model, rlvr／local_required | internal_records；由业务方定义媒体规模、时长、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 公共音频偏好／RLVR 数据不足，由业务方建设人类语音偏好、可验证音频任务和图像／视频偏好；按独立提示切分；风险：媒体权利、肖像／声音同意、隐私、机密与业务分布审查；不得上传公共训练平台 | 内部登记项 |
| `local_gui_action_safety` | text, image, video | agent_sft, agent_rl, preference, evaluation／local_required | internal_records；由业务方定义媒体规模、时长、切分、脱敏和不可变版本 | INTERNAL／internal_review_required | 覆盖真实应用、中文界面、账号脱敏、提示注入、不可逆动作确认和正常请求防过拒；静态轨迹与在线环境同时验收；风险：媒体权利、肖像／声音同意、隐私、机密与业务分布审查；不得上传公共训练平台 | 内部登记项 |

### long_context

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `longalign_10k` | text | sft／optional | 9,888 samples；当前 train 9,888；名称口径 10K，长度约 8K–64K | unknown／review_required | 长输入对齐补集；许可复核与长度 token 配比后使用；风险：当前 HF 未见明确许可字段；长输入不等于长输出或引用能力 | [官方来源](https://huggingface.co/datasets/zai-org/LongAlign-10k) |
| `longcite_45k` | text | sft／core | 45,000 samples；名称口径约 45K；中英文长文句级引用 | Apache-2.0／allowed_with_obligations | 长文 grounded generation 与句级引用主补集；风险：引用格式需保留；应抽检引用支持与空引用 | [官方来源](https://huggingface.co/datasets/zai-org/LongCite-45k) |

### long_output

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `longform` | text | sft／optional | 23,652 train_samples；validation 2,042、test 2,045 分开隔离；长输出指令跟随 | MIT + upstream-and-OpenAI-terms／review_required | 长输出 SFT 结构补集；只使用 train，独立保留 test，并抽检全局一致性；风险：卡片明确含 OpenAI 与 WikiHow 上游限制；C4/Wikipedia/Stack Exchange/NIv2/BigBench 等来源需逐项审查 | [官方来源](https://huggingface.co/datasets/akoksal/LongForm) |

### math

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `numina_math_cot` | text | sft／optional | 860,000 samples；约 86 万数学 CoT | review-required／review_required | 数学 SFT；按母题去污后使用；风险：母题重复和公开数学基准重叠 | [官方来源](https://github.com/project-numina/aimo-progress-prize) |
| `openmath_reasoning` | text | sft／core | 3,200,000 cot_samples；约 320 万 CoT；另有约 170 万 TIR，分开使用不相加 | CC-BY-4.0／allowed_with_obligations | 数学蒸馏主候选；CoT 与 TIR 分 profile；风险：长序列成本和教师偏差；CoT/TIR 格式不同 | [官方来源](https://huggingface.co/datasets/nvidia/OpenMathReasoning) |
| `openmathinstruct2` | text | sft／core | 13,972,791 problem_solution_pairs；另有公平降采样 train_1M/train_2M/train_5M；Llama-3.1-405B-Instruct 生成 | CC-BY-4.0／allowed_with_obligations | 数学 SFT 主候选；优先从公平降采样 split 消融并继续做 Omni-MATH 等母题去污；风险：GSM8K/MATH 母题及增广谱系；增广题答案来自 majority voting；官方建议过滤约 564 个超长问题 | [官方来源](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) |

### multiimage_sft

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `mantis_instruct` | text, image | sft／optional | 721,000 samples_approx；官方论文约 721K、14 个多图核心子集；当前 HF 还含单图补集，分别按 config 计数 | Apache-2.0 + mixed-upstream／review_required | 按 14 个核心 config 做跨图指代、比较、推理和时序消融；风险：多上游许可、视频来源和 GPT-4 输出；部分多图样本由单图拼接；与 LLaVA／DocVQA／ChartQA 重叠 | [官方来源](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct) |

### multilingual

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `oasst2` | text | sft, preference／optional | message_tree；35 种语言；按消息树路径抽取后再计数 | Apache-2.0／allowed_with_obligations | 多语言人工对话与偏好研究补集；风险：原始结构不是平铺对话；各语言质量不均 | [官方来源](https://arxiv.org/html/2304.07327v3) |
| `aya_dataset` | text | sft／core | instruction_pairs；含 original-annotations 与 re-annotations；当前语言标签与历史论文口径不同，须按固定版本计数 | Apache-2.0／allowed_with_obligations | 多语言人工数据主补集；固定 config 后统计语言与样本数；风险：与 Aya Collection 内嵌 Aya-Dataset 记录重复；版本语言数不可混写 | [官方来源](https://huggingface.co/datasets/CohereLabs/aya_dataset) |
| `aya_collection` | text | sft／optional | task_instances；多来源模板化合集；含 dataset_name=Aya-Dataset 的记录 | Apache-2.0／allowed_with_obligations | 多语言任务补集；先按 dataset_name、语言和文本去重；风险：与 Aya Dataset 直接相加会重复；多上游任务需来源级去重 | [官方来源](https://huggingface.co/datasets/CohereLabs/aya_collection) |
| `m2lingual` | text | sft／research_only | 173,672 dataset_rows；70 语言、17 任务；卡片另称 182K IR pairs，行数与 pairs 不混写 | CC-BY-NC-SA-4.0／noncommercial | 非商用多语言多轮研究补集；固定 full_data 并按语言和 sample_type 分层；风险：非商用及相同方式共享义务；GPT-4 教师和 Aya 种子谱系需审查；full_data/seed_data/seed_evol_data 配置不可混加 | [官方来源](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual) |

### multimodal_preference

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `llava_human_preference_10k` | text, image | preference, reward_model／optional | human_preference_pairs；名称 10K，公开项目约 9.42K；当前 API 无切分行数 | Apache-2.0 + upstream-terms／review_required | 人类视觉偏好基线；固定文件后按独立提示计数；风险：图像与原始响应上游条款；名称不等于精确行数 | [官方来源](https://huggingface.co/datasets/zhiqings/LLaVA-Human-Preference-10K) |
| `rlhf_v` | text, image | preference, reward_model／research_only | 1,400 segment_level_human_corrections_approx；约 1.4K 段级人类修正，不与整句偏好对直接等量混合 | CC-BY-NC-4.0／noncommercial | 非商用人类细粒度幻觉修正研究；单独建 profile；风险：非商用；细粒度修正与整句 pair 标注单位不同 | [官方来源](https://github.com/rlhf-v/rlhf-v) |
| `rlaif_v` | text, image | preference, reward_model／research_only | ai_feedback_pairs；开源模型反馈；当前卡片未给切分行数 | CC-BY-NC-4.0／noncommercial | 非商用 AI 反馈对照组；不得与人类偏好混称人工标注；风险：非商用；AI 反馈偏差和上游图像权利 | [官方来源](https://huggingface.co/datasets/openbmb/RLAIF-V-Dataset) |
| `vlfeedback` | text, image | preference, reward_model／optional | 80,258 prompts；default/train 80,258 提示；多模型回答可展开 pair，但 pair 数不等于独立提示数 | no-explicit-license-in-card + GPT-4V/upstream／review_required | 大规模 AI 反馈补集；按独立提示切分并保留模型来源；风险：当前无统一许可；GPT-4V 反馈与多供应商输出条款；偏好对膨胀 | [官方来源](https://huggingface.co/datasets/MMInstruction/VLFeedback) |
| `povid` | text, image | preference, reward_model／optional | constructed_preference_pairs；构造负例偏好数据；当前 API 未给切分行数 | CC-BY-4.0 + upstream-terms／review_required | 构造幻觉负例补集；与人工和 AI 反馈分组消融；风险：构造负例不等于人类偏好；负例类型单一可能造成风格捷径 | [官方来源](https://huggingface.co/datasets/YiyangAiLab/POVID_preference_data_for_VLLMs) |

### multimodal_reasoning

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `r1_onevision` | text, image | sft, rlvr／optional | reasoning_samples_and_rl_tasks；自然场景、科学、数学、OCR 和图表；SFT 与 RL 文件／配置必须分别固定 | Apache-2.0 + mixed-upstream／review_required | 按任务拆分 SFT 与 RL；数学、OCR、检测等奖励分别重跑；风险：蒸馏轨迹不等于 RLVR 题集；不同任务验证器和上游许可不同 | [官方来源](https://huggingface.co/datasets/Fancy-MLLM/R1-Onevision) |

### multimodal_rlvr

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `visual_rft_tasks` | text, image | rlvr／research_only | task_specific_rl_configs；分类、检测、grounding 等任务分别使用官方数据与奖励；不是一个无差别全量包 | mixed-see-task-upstream／review_required | 按任务和固定切分复现；验证器签署后才进入 RLVR 配方；风险：COCO／LVIS／LISA 等上游许可不同；IoU、分类和格式奖励不可混作通用正确性 | [官方来源](https://arxiv.org/html/2503.01785v1) |

### multimodal_safety

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `vlguard_train` | text, image | sft／optional | safety_instruction_samples；gated=auto；训练与测试文件、safe/unsafe 子集分别固定 | MIT + gated-and-upstream-terms／review_required | 访问条件归档后作安全指令补集；只使用审查后的响应；风险：需接受访问条件；危险图像与文本隔离；安全回答和原始 unsafe 内容不可混作普通 SFT | [官方来源](https://huggingface.co/datasets/ys-zong/VLGuard) |
| `spa_vl_train` | text, image | preference, reward_model／research_only | 93,258 preference_pairs；train 93,258；validation 7,000、HarmEval 265、HelpEval 265 独立，不相加 | mixed-model-output-and-upstream／review_required | 研究隔离安全偏好；分别审核 chosen/rejected， HarmEval/HelpEval 只评测；风险：chosen 也可能含不安全响应；多模型输出和图像上游条款；安全与有用性需双目标 | [官方来源](https://sqrtizhang.github.io/SPA-VL/) |
| `safe_vid_350k` | text, image, video | preference, reward_model／research_only | 350,000 video_safety_preference_pairs_approx；官方论文约 350K 视频安全偏好对 | CC-BY-NC-SA-4.0／noncommercial | 非商用视频安全偏好补集；SafeVidBench 独立评测；风险：非商用及相同方式共享；视频、文字描述和教师输出上游；静态文本安全不等于视频时序安全 | [官方来源](https://huggingface.co/datasets/yxwang/SafeVid-350K) |

### preference

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `hh_rlhf` | text | preference, reward_model／optional | 169,352 preference_pairs；人工偏好对；含有用性和无害性子集 | MIT／allowed_with_obligations | 经典偏好与奖励模型基线；隔离危险内容；风险：有害、偏见和隐私文本；历史偏好不等于现代安全规范 | [官方来源](https://huggingface.co/datasets/Anthropic/hh-rlhf) |
| `shp` | text | preference, reward_model／optional | 385,563 raw_preference_samples；不要与 SHP-2 的约 480 万行混淆 | unknown／review_required | 领域化人类偏好研究；先复核权利；风险：许可字段不明确；点赞不等于事实或安全 | [官方来源](https://huggingface.co/datasets/stanfordnlp/SHP) |
| `helpsteer` | text | reward_model, preference／optional | 37,120 scored_responses；多维评分响应 | review-required／review_required | 属性奖励模型研究的旧版基线；风险：与 HelpSteer2 版本和规模不可混写 | [官方来源](https://arxiv.org/html/2406.08673v1) |
| `helpsteer2` | text | preference, reward_model／core | 21,362 responses；约 1 万独立提示，可构造约 1 万偏好对 | CC-BY-4.0／allowed_with_obligations | 细粒度奖励模型与 DPO 首选候选之一；风险：响应数不等于提示数；需检查同提示标注一致性和来源 | [官方来源](https://huggingface.co/datasets/nvidia/HelpSteer2) |
| `ultrafeedback` | text | preference, reward_model／optional | 63,967 prompts；约 34 万个回答评分 | MIT／review_required | AI 反馈补集；教师条款通过后使用；风险：GPT-4 教师服务条款；自动评分偏差和上游谱系 | [官方来源](https://huggingface.co/datasets/openbmb/UltraFeedback) |
| `nectar` | text | preference, reward_model／optional | 183,000 prompts；每题 7 回答，可构造约 380 万对；构造对数不等于独立样本数 | Apache-2.0／review_required | 多回答排序研究；按独立提示规划采样；风险：GPT-4 输出条款和底层提示来源；偏好对数量膨胀 | [官方来源](https://huggingface.co/datasets/berkeley-nest/Nectar) |
| `arena_human_preference_140k` | text | preference, reward_model／optional | 135,634 human_votes；text-only 类别当前 train 精确数；含 tie 和 both_bad | CC-BY-4.0（用户提示）／review_required | 现代真实人类偏好补集；过滤图像字段并逐模型审查输出条款；风险：模型输出受各供应商条款约束；真实用户隐私、多轮上下文模型不一致 | [官方来源](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k) |
| `skywork_reward_preference_80k` | text | preference, reward_model／optional | 77,016 preference_pairs；v0.2 为 RewardBench 去污版；v0.1 删除 4,957 对 | mixed-review-required／review_required | 奖励模型训练补集；固定 v0.2 并继续谱系审查；风险：多上游许可和 Magpie 教师来源；不可回退到 RewardBench 污染版 | [官方来源](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2) |
| `helpsteer3_preference` | text | preference, reward_model／core | 40,476 preference_samples；95% train／5% validation；General/STEM/Code/Multilingual，含多轮上下文与最多 3 人标注 | CC-BY-4.0／allowed_with_obligations | 偏好与奖励模型主候选；固定 preference config 并按同提示切分；风险：Preference/Feedback/Edit/Edit Quality/Principle 配置不可混加；多领域不等于各语言均衡 | [官方来源](https://huggingface.co/datasets/nvidia/HelpSteer3) |
| `tulu3_preference_mixture` | text | preference, reward_model／research_only | 272,898 preference_pairs；官方明确部分子集非商用并作为研究 artifact 发布 | ODC-BY-1.0 + noncommercial-subsets／noncommercial | 仅作非商用偏好配方研究基线；商用配方不得直接继承整包；风险：不能只看 ODC 标签推断整包可商用；含 GPT-4/Claude/Llama/Qwen/Gemma 等多教师 | [官方来源](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture) |
| `webgpt_comparisons` | text | preference, reward_model／research_only | 19,578 comparisons；双答案、引用摘录和人类偏好分数；官方卡片未给明确许可 | no-explicit-license／review_required | 许可签署后用于带引用答案偏好研究；不得默认可商用；风险：无明确许可；引用摘录的网页上游权利；历史浏览器和答案分布 | [官方来源](https://huggingface.co/datasets/openai/webgpt_comparisons) |
| `summarize_from_feedback` | text | preference, reward_model／research_only | comparison_and_axis_rows；comparisons/axis 配置与切分不同；官方卡片未给明确许可和统一精确规模 | no-explicit-license + mixed-upstream／review_required | 许可和上游审查后作摘要偏好研究基线；不填未经核实的统一规模；风险：无明确许可；TL;DR 及验证/测试中的 CNN/Daily Mail 上游限制；配置和切分不可混加 | [官方来源](https://huggingface.co/datasets/openai/summarize_from_feedback) |

### process_reward

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `prm800k` | text | prm／optional | 800,000 step_labels；另含 7.5 万解答、1.2 万题 | MIT／allowed_with_obligations | 数学 PRM 主候选；严格执行官方切分与独立时间外评测；风险：训练集纳入 4.5K MATH 测试题，MATH 切分污染风险极高 | [官方来源](https://github.com/openai/prm800k) |
| `math_shepherd` | text | prm／research_only | 445,000 automatic_step_labels；约 40–44.5 万，论文口径有差异 | no-explicit-license／review_required | 仅限许可明确后的 PRM 研究，不标 Apache；风险：结果回推不等于每步因果正确；无明确许可 | [官方来源](https://arxiv.org/abs/2312.08935) |
| `pathfinder_prm` | text | prm／research_only | 400,000 samples_approx；由 PRM800K 与 RLHFlow Mistral traces 增广；Math/Consistency/Optimality 三维步级标签 | review-required／review_required | 许可复核后用于非默认 PRM 研究；严格继承母题切分并单独评测三维标签；风险：数据许可未在官方项目中明确；继承 PRM800K 的 MATH 切分污染风险；自动增广标签需抽检 | [官方来源](https://github.com/declare-lab/PathFinder-PRM) |

### reasoning

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `openthoughts3` | text | sft／optional | 1,200,000 samples；约 120 万；数学、科学、代码和谜题 | review-required／review_required | 长推理蒸馏候选；先做过程抽检与长度消融；风险：答案正确不代表过程严谨；版本、许可和教师条款需固定后复核 | [官方来源](https://arxiv.org/html/2506.04178v1) |
| `s1k` | text | sft／research_only | 1,000 samples；约 1,000 条高难筛选样本 | review-required／review_required | 小样本推理冷启动研究，不作通用底座；风险：结论依赖基座与筛选方法；许可按发布版本复核 | [官方来源](https://arxiv.org/html/2501.19393v1) |
| `limo` | text | sft／research_only | 817 samples；817 条精选推理样本 | review-required／review_required | 推理激活假设和数据质量消融；风险：小样本结论不可泛化到所有 Base | [官方来源](https://arxiv.org/html/2502.03387v1) |
| `natural_reasoning` | text | sft／research_only | 1,100,000 questions；公开 110 万子集；18.29% 无参考答案 | CC-BY-NC-4.0／noncommercial | 非商用通用推理研究主候选；按答案类型分层；风险：非商用；模型回答可能存在事实和推理错误；无参考答案样本不能直接 RLVR | [官方来源](https://huggingface.co/datasets/facebook/natural_reasoning) |
| `mixture_of_thoughts` | text | sft／optional | 349,317 reasoning_traces；all config 精确数；math 93,733、code 83,070、science 172,514 | mixed-review-required／review_required | 数学、代码、科学长推理混合补集；按 domain 分开消融；风险：R1 蒸馏与多上游许可；科学子集不能等同全领域开放推理 | [官方来源](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts) |

### rlvr_code

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `acecode_87k` | text | rlvr／core | 87,000 problems；约 8.7 万带合成筛选测试的题 | review-required／review_required | 轻量代码 RLVR 候选；验证器签署后启用；风险：公开测试过拟合；需独立隐藏测试和资源限制 | [官方来源](https://arxiv.org/html/2502.01718v4) |

### rlvr_general

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `nemotron_cascade_2_rl` | text | rlvr, agent_rl, sft／optional | 73,809 config_rows_total；IF-RL 45,879、multi-domain-RL 18,147、MOPD 6,171、SWE-RL 3,612；四配置分开使用 | ODC-By／allowed_with_obligations | 按 IF、通用 RL、MOPD、SWE 四 profile 分开消融；逐配置验证奖励与上游；风险：MOPD 是 on-policy distillation，不是同质 RLVR；SWE-Gym/R2E-Gym 等上游许可与重复；总数只为目录口径，训练不得混配后直接相加 | [官方来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) |
| `enigmata_data` | text | rlvr／research_only | generator_tasks；36 任务、7 类；generator＋rule verifier，可控制难度生成实例，固定包规模不猜数 | CC-BY-NC-4.0／noncommercial | 非商用逻辑谜题 RLVR；固定生成器种子、难度和任务排除清单；风险：非商用；生成器可扩展不等于已固定训练集规模；必须与 Enigmata-Eval 做实例级泄漏检查 | [官方来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data) |

### rlvr_if

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `verinstruct` | text | rlvr／core | 22,000 samples；约 2.2 万带规则或 LLM 验证信号的指令样本 | review-required／review_required | 精确指令 RLVR；硬规则与 LLM 判断分报；风险：LLM 验证器不等于绝对可验证；表面约束过拟合 | [官方来源](https://aclanthology.org/2025.emnlp-main.1542/) |

### rlvr_math

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `dapo_math_17k` | text | rlvr／core | 17,000 problems；prompt + reward_model.ground_truth | Apache-2.0／allowed_with_obligations | 数学 RLVR 快速闭环主候选；风险：答案归一化与基准重复 | [官方来源](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) |
| `deepscaler_preview` | text | rlvr／core | 40,000 problems；约 4 万题，带答案和参考解答 | MIT／allowed_with_obligations | 主要使用题目＋最终答案；不盲信 solution；风险：部分参考解答与最终答案可能不一致 | [官方来源](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset) |
| `deepmath_103k` | text | rlvr／optional | 103,000 problems；约 95K 难度 5–9、8K 难度 3–5 | review-required／review_required | 高难数学 RL 课程候选；转开放题或降低可猜性；风险：选择／判断题猜测奖励；许可按固定版本复核 | [官方来源](https://arxiv.org/html/2504.11456v2) |
| `big_math_rl_verified` | text | rlvr／core | 251,122 problems；含 47,010 选择题改开放题与指定模型 solve rate | Apache-2.0／allowed_with_obligations | 访问条件归档后作为大规模数学 RLVR 候选；风险：需接受访问条件；solve rate 不是所有 Base 的通用难度；共同上游污染 | [官方来源](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) |
| `skywork_or1_rl` | text | rlvr／optional | 105,000 math_problems；另有约 13.7K 代码题，分别计数和验证 | unknown／review_required | 许可复核后作联合数学／代码 RL 补集；风险：许可不明确；多模型难度不可直接迁移 | [官方来源](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) |

### safety

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `pku_saferlhf` | text | preference, reward_model, sft／research_only | 44,600 prompts；另有 265K QA 安全标签、166.8K 偏好样本 | CC-BY-NC-4.0／noncommercial | 非商用安全奖励和有用性／无害性双目标研究；风险：非商用；危险内容与过拒风险 | [官方来源](https://github.com/PKU-Alignment/beavertails) |
| `aegis_content_safety_2` | text | sft, reward_model／core | 33,416 annotated_interactions；train 30,007、validation 1,445、test 1,964；含 5K 合成拒答训练样本 | CC-BY-4.0／allowed_with_obligations | 安全分类主候选；只将审查后的安全响应用于生成对齐；风险：官方不建议直接把原始内容当普通对话 SFT；危险文本和部分响应标签为 LLM jury；自杀相关 358 样本不分发 | [官方来源](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) |
| `wildguardmix_tulu3` | text | sft, preference／optional | 50,000 samples；Tulu 3 配方中的去污固定子集，不是原始全集规模 | review-required／review_required | 安全响应补集；只有在固定包字段、访问条件和许可复核后启用；风险：原始库访问受限，本次直接数据卡未读取；包含有害与良性场景，字段和许可须下载后复核 | [官方来源](https://arxiv.org/html/2411.15124v2) |
| `falsereject_train` | text | sft／research_only | 14,624 training_prompts；每条含 instruct_response 与 cot_response 两字段；另有 1,187 人工测试提示，不能相加为训练量 | CC-BY-NC-4.0／noncommercial | 非商用防过拒主补集；Instruct/CoT 分 profile，test 独立 eval_only；风险：非商用；Claude-3.5-Sonnet/DeepSeek-R1 教师输出需审查；看似有害但良性的提示仍需安全过滤 | [官方来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |

### tool

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `xlam_function_calling` | text | sft／core | 60,000 samples；约 6 万函数调用样本 | CC-BY-4.0／review_required | 接受并归档条件、完成执行验证后作为精确调用主候选；风险：需登录接受访问条件，页面含研究用途声明；Schema 过期与不可执行样本 | [官方来源](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) |
| `toolace` | text | sft／core | 11,512 dialogues；含多轮、并行调用和无需调用情形 | review-required／review_required | 多轮、并行和拒调能力补集；风险：许可与字段按固定版本复核；真实业务工具分布仍需自有数据 | [官方来源](https://arxiv.org/html/2409.00917v1) |
| `glaive_function_calling_v2` | text | sft／optional | 113,305 samples；函数调用样本精确数 | Apache-2.0／allowed_with_obligations | 格式基线补集；近重复去重和 Schema 验证后使用；风险：近重复；并非全部代表现实 API | [官方来源](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2) |
| `toolbench` | text | sft, agent_sft／optional | 126,486 solution_path_annotations；3,451 tools、16,464 APIs、469,585 real API calls；轨迹与调用分开计数 | Apache-2.0（项目声明）／review_required | 真实 API、多步工具研究补集；优先 StableToolBench 固定环境；风险：项目声明仅供研究教育；真实 API 漂移、密钥与结果可复现性；ChatGPT 自动生成 | [官方来源](https://github.com/OpenBMB/ToolBench) |
| `api_bank` | text | sft, evaluation／optional | 1,888 training_dialogues；训练 1,888 对话／2,138 APIs；评测另 314 对话、753 调用、73 工具 | review-required／review_required | 规划、检索、调用补集；73 工具评测部分按 eval_only 管理；风险：训练与评测切分必须隔离；许可和模拟 API 保真度需复核 | [官方来源](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) |
| `toolmind` | text | sft, agent_sft／optional | 360,000 assistant_turn_samples；160K 合成＋200K 开源增广，20K+ tools；按通过过滤的 assistant turn 拆分 | Apache-2.0／allowed_with_obligations | 大规模工具轨迹补集；执行验证、按来源去重并与评测环境隔离；风险：样本数不等于独立轨迹数；与 xLAM/Glaive/ToolACE/When2Call/APIGen-MT/τ-bench 来源级重叠；合成调用需执行验证 | [官方来源](https://huggingface.co/datasets/Nanbeige/ToolMind) |

### video_sft

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `llava_video_178k` | text, image, video | sft／optional | 178,000 source_videos；178K 是视频数；论文约 1.6M 指令，caption/open_ended/multi_choice 分开，不写成 178K QA | no-explicit-license-in-card + mixed-video-upstream／review_required | 按视频时长、来源和问答类型建 profile；固定媒体哈希和字幕协议；风险：当前卡片无统一许可；YouTube／学术视频与 GPT-4o 条款；媒体下载漂移 | [官方来源](https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K) |
| `videochat_flash_training` | text, image, video | sft／optional | video_instruction_samples；长上下文视频指令混合包；当前 API 未提供统一切分行数 | Apache-2.0 + mixed-upstream／review_required | 长视频指令补集；固定子目录、媒体清单和帧预算；风险：上游视频与教师条款；长视频存储、抽帧和时间标注成本 | [官方来源](https://huggingface.co/datasets/OpenGVLab/VideoChat-Flash-Training-Data) |
| `molmo2_videotrack` | text, image, video | sft／optional | video_track_samples；default/train；当前 API 未提供固定行数 | ODC-By／allowed_with_obligations | 视频跟踪补集；固定 2fps／原始时间戳协议并验证轨迹；风险：视频上游权利和轨迹标注噪声；时间戳与帧率绑定 | [官方来源](https://huggingface.co/datasets/allenai/Molmo2-VideoTrack) |
| `molmo2_videopoint` | text, image, video | sft／core | 658,340 train_samples；default/train 精确行数；其他类别 config 不与其直接相加 | ODC-By／allowed_with_obligations | 时空指向主候选；固定 default/train，过滤 unsure 并验证点／时间戳；风险：default 与类别 config 可能重复；标注 unsure、时间戳和坐标验证；视频上游权利 | [官方来源](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint) |

### vision_grounding

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `pixmo_points` | text, image | sft／core | 2,376,222 samples；default/train 精确行数；每行可含多个点，行数不等于点数 | ODC-By／allowed_with_obligations | 定位与计数主候选；固定坐标归一化和点／样本两种配比；风险：坐标系、图像缩放和无效 URL；集合标签许可不替代图像权利审查 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-points) |
| `pixmo_point_explanations` | text, image | sft／optional | 79,551 samples；default/train 精确行数；含解析点与文本解释 | ODC-By／allowed_with_obligations | 可解释指向补集；分别监督文本和点坐标并做解析校验；风险：文本中的点需与 parsed_response 一致；图像 URL 和隐私审查 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-point-explanations) |
| `pixmo_count_train` | text, image | sft／core | 36,916 train_samples；train 36,916；validation/test 各 540，独立资产隔离 | ODC-By／allowed_with_obligations | 计数训练主候选；只用 train，并按图像 SHA 对测试集去污；风险：点与计数必须一致；同图跨 split 泄漏检查 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-count) |

### vision_sft

| ID | 模态 | 阶段／层级 | 规模与版本口径 | 许可／商用状态 | 建议与主要风险 | 来源 |
|---|---|---|---|---|---|---|
| `llava_instruct_150k` | text, image | sft／research_only | 157,710 instruction_samples；当前 FineVision 同名子集也为 157,710；不得与 558K 特征对齐集混写 | CC-BY-4.0 + GPT-4/upstream-terms／noncommercial | 仅作研究视觉指令基线；与 FineVision、LLaVA-1.5、Mantis 按来源去重；风险：GPT-4 输出与原始图像上游条款；LLaVA 项目研究／非商用约束 | [官方来源](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K) |
| `llava15_mix665k` | text, image | sft／research_only | 665,000 samples_approx；学术任务与 GPT 生成指令混合；558K 是特征对齐预训练，不属于本资产 | research/noncommercial + mixed-upstream／noncommercial | 研究隔离的经典视觉 SFT 配方基线，不进入商用默认；风险：非商用；多上游图像和教师条款；与 Mantis、FineVision、OneVision 大量重叠 | [官方来源](https://github.com/haotian-liu/LLaVA) |
| `llava_onevision15_instruct_22m` | text, image | sft／optional | 22,000,000 samples_approx；22M 官方口径、124 类；part-* 与完整 config 可能重复，不能对全部 config 行数求和 | Apache-2.0 + mixed-upstream／review_required | 按 config 建立配方，不做全包无差别训练；固定 22M 版本并逐来源签署；风险：多上游许可和 GPT 教师输出；含医学等范围外 config，必须逐 config 选择；与 PixMo、FineVision、文本数学／代码数据重叠 | [官方来源](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data) |
| `finevision` | text, image | sft／optional | 24,000,000 samples_approx；约 24M；200+ config 含完整集与分片，禁止直接汇总所有 config | no-unified-license-in-card + mixed-upstream／review_required | 作为大规模待审混合池；逐 config 审许可、媒体权利和评测污染；风险：当前卡片无统一许可字段；含 LLaVA、GUI、医学等异质来源；与 OneVision 合并必须去重 | [官方来源](https://huggingface.co/datasets/HuggingFaceM4/FineVision) |
| `pixmo_ask_model_anything` | text, image | sft／core | 161,737 samples；default/train 精确行数；图像通过 URL＋SHA 引用 | ODC-By／allowed_with_obligations | 开放视觉指令主候选；下载时核对 image_sha256、可用率和隐私；风险：图像 URL 失效、隐私与上游图像权利；答案开放域质量需抽检 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-ask-model-anything) |
| `pixmo_cap_qa` | text, image | sft／optional | 271,714 samples；default/train 精确行数；caption-conditioned QA | ODC-By／allowed_with_obligations | 细粒度视觉问答补集；抽检问题是否真正需要图像；风险：依赖图像描述可能引入二阶错误；图像 URL 与文本质量 | [官方来源](https://huggingface.co/datasets/allenai/pixmo-cap-qa) |

## 6. 关键去重与隔离关系

- Aya Collection 内含 `dataset_name=Aya-Dataset` 记录，**Aya Dataset + Aya Collection 不得直接相加**；M2Lingual 也由 Aya 种子演化，需跨集谱系去重。
- Infinity-Instruct 含 OpenHermes、FLAN、BELLE、COIG-CQIA、WildChat 等上游，必须做来源级去重和继承许可审查。
- OpenMathInstruct-2 基于 GSM8K/MATH 母题增广；OpenCodeInstruct/OpenCodeReasoning/TACO/CodeContests/APPS 等按母题谱系去重，不能只按文本哈希。
- ToolMind 与 xLAM、Glaive、ToolACE、When2Call、APIGen-MT、τ-bench 等有来源级重叠；τ-bench 2.0 的公开评测任务绝不能因轨迹增广进入训练。
- PRM800K 与 PathFinder-PRM 继承 MATH 切分风险；MATH-500、Omni-MATH、ProcessBench、PRMBench、RewardBench、LiveCodeBench、BFCL、SWE-bench Verified 全部严禁训练。
- LongForm、FalseReject、Enigmata、WebLINX、Mind2Web 的训练与测试必须按版本和切分隔离；同一 HF repo 不代表可以混用。
- Arena、Tulu Preference、RewardBench 2 同时含用户提示与不同供应商模型输出；合集或提示的许可不自动覆盖模型输出。

## 7. 尚未闭合的真实缺口

1. **中文精确指令与多语言人类偏好仍偏弱**：IFEval-like、M2Lingual 和中文 R1 蒸馏以合成数据为主，不能替代中文人工约束数据和多语言人工偏好。
2. **长输出已有结构补集，但全局一致性未闭合**：LongForm 可训练长回答，仍需事实一致性、跨章节依赖、多文档冲突和真实业务长文私有评测。
3. **开放式通用推理缺少可靠自动奖励**：Enigmata 闭合的是规则谜题 RLVR，不代表开放问答、科学推理和通用写作都可验证。
4. **浏览 Agent 只有非商用静态研究轨迹**：WebLINX＋Mind2Web 补上了结构空缺，但可商用训练物料、动态网站环境、账号安全和在线回放仍未闭合。
5. **Agent 安全与业务边界必须由自有数据闭合**：AgentHarm/AgentDojo 只做评测；真实工具返回注入、数据外泄、危险动作、中文正常请求防过拒和私有时间外评测仍需本地建设。
6. **本清单未下载全量数据、未固定所有 revision、未执行样本级验证**；这些是训练前必做步骤，不在静态调研中冒充完成。

## 8. 训练前门禁

- [ ] 固定 repo revision、文件哈希和实际 split
- [ ] 按精确/近重复/语义/母题/仓库/网站/媒体内容谱系去重去污
- [ ] 许可、上游媒体、肖像／声音同意、教师服务条款和访问条件分别签署
- [ ] 按有效 token、独立提示、媒体时长、任务和轨迹分别配比
- [ ] 数学/代码/工具/坐标/时空/音频验证器实际重跑
- [ ] 固定图像尺寸、视频抽帧、音频采样率、codec 和 processor
- [ ] eval_only 和私有时间外评测绝不进入训练

机器校验：`python validate_datasets_list.py datasets-list.yaml`。
