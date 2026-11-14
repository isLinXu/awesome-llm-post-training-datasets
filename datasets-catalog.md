# Base 与多模态模型后训练数据自动目录

> 自动更新：2026-11-14T21:33:04Z；canonical 输入：`datasets-list.yaml`。本文件只生成视图，不改写人工许可和训练分层。
> 共 175 项已收录资产；待审核候选 161 项。候选数据不会自动进入训练配方。

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
| `general_chat` | [`dolci_instruct_sft`](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT), [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture), [`dolly_15k`](https://huggingface.co/datasets/databricks/databricks-dolly-15k), [`longform`](https://huggingface.co/datasets/akoksal/LongForm), [`nemotron_cascade_2_sft`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data), [`smoltalk2`](https://huggingface.co/blog/smollm3), [`no_robots`](https://huggingface.co/datasets/HuggingFaceH4/no_robots), [`oasst2`](https://arxiv.org/html/2304.07327v3), [`lima`](https://arxiv.org/html/2305.11206v4), [`wildchat`](https://arxiv.org/html/2405.01470v3), [`openhermes_2_5`](https://huggingface.co/datasets/teknium/OpenHermes-2.5), [`infinity_instruct`](https://huggingface.co/datasets/BAAI/Infinity-Instruct), `local_domain_zh_sft` | [`mt_bench`](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts), `local_private_time_eval` |
| `knowledge_recall` | [`dolci_instruct_sft`](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT), [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture), [`nemotron_cascade_2_sft`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data), [`smoltalk2`](https://huggingface.co/blog/smollm3), [`aya_collection`](https://huggingface.co/datasets/CohereLabs/aya_collection), [`natural_reasoning`](https://huggingface.co/datasets/facebook/natural_reasoning) | [`mmlu_pro`](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro), [`gpqa_diamond`](https://huggingface.co/datasets/Idavidrein/gpqa), `local_private_time_eval` |
| `multilingual` | [`aya_dataset`](https://huggingface.co/datasets/CohereLabs/aya_dataset), [`aya_collection`](https://huggingface.co/datasets/CohereLabs/aya_collection), [`m2lingual`](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual), [`helpsteer3_preference`](https://huggingface.co/datasets/nvidia/HelpSteer3), [`oasst2`](https://arxiv.org/html/2304.07327v3), [`dolci_instruct_sft`](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT), [`wildchat`](https://arxiv.org/html/2405.01470v3) | [`mgsm`](https://arxiv.org/abs/2210.03057), [`sorry_bench_202503`](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503), [`tau_bench_2_text`](https://github.com/sierra-research/tau2-bench), `local_private_time_eval` |
| `chinese` | [`coig_pc_lite`](https://huggingface.co/datasets/BAAI/COIG-PC-Lite), [`coig_cqia`](https://arxiv.org/html/2403.18058v2), [`belle`](https://github.com/LianjiaTech/BELLE), [`firefly`](https://github.com/yangjianxin1/Firefly), [`chinese_r1_distill_110k`](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k), [`dolci_instruct_sft`](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT), [`longcite_45k`](https://huggingface.co/datasets/zai-org/LongCite-45k), `local_domain_zh_sft` | `local_private_time_eval` |
| `multiturn` | [`no_robots`](https://huggingface.co/datasets/HuggingFaceH4/no_robots), [`oasst2`](https://arxiv.org/html/2304.07327v3), [`wildchat`](https://arxiv.org/html/2405.01470v3), [`smoltalk2`](https://huggingface.co/blog/smollm3), [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture), [`helpsteer3_preference`](https://huggingface.co/datasets/nvidia/HelpSteer3), [`toolmind`](https://huggingface.co/datasets/Nanbeige/ToolMind), [`m2lingual`](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual), [`weblinx`](https://huggingface.co/datasets/McGill-NLP/WebLINX), [`toolace`](https://arxiv.org/html/2409.00917v1) | [`mt_bench`](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts), [`tau_bench_2_text`](https://github.com/sierra-research/tau2-bench), `local_private_time_eval` |
| `precise_if` | [`tulu3_persona_if`](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following), [`ifeval_like_filtered`](https://huggingface.co/datasets/argilla/ifeval-like-data), [`verinstruct`](https://aclanthology.org/2025.emnlp-main.1542/), [`nemotron_cascade_2_rl`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data), [`dolci_instruct_sft`](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT), [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | [`ifeval`](https://github.com/google-research/google-research/tree/master/instruction_following_eval), [`rewardbench2`](https://huggingface.co/datasets/allenai/reward-bench-2), `local_private_time_eval` |
| `long_context` | [`longalign_10k`](https://huggingface.co/datasets/zai-org/LongAlign-10k), [`longcite_45k`](https://huggingface.co/datasets/zai-org/LongCite-45k), [`nemotron_cascade_2_sft`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) | [`longbench_chat`](https://github.com/THUDM/LongAlign), [`longbench_cite`](https://github.com/THUDM/LongCite), [`ruler`](https://github.com/NVIDIA/RULER), `local_private_time_eval` |
| `grounded_citation` | [`longcite_45k`](https://huggingface.co/datasets/zai-org/LongCite-45k), [`webgpt_comparisons`](https://huggingface.co/datasets/openai/webgpt_comparisons), `local_domain_zh_sft` | [`longbench_cite`](https://github.com/THUDM/LongCite), `local_private_time_eval` |
| `general_reasoning` | [`openthoughts3`](https://arxiv.org/html/2506.04178v1), [`natural_reasoning`](https://huggingface.co/datasets/facebook/natural_reasoning), [`mixture_of_thoughts`](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts), [`openmathinstruct2`](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2), [`enigmata_data`](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data), [`nemotron_cascade_2_rl`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data), [`chinese_r1_distill_110k`](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k), [`s1k`](https://arxiv.org/html/2501.19393v1), [`limo`](https://arxiv.org/html/2502.03387v1), [`openmath_reasoning`](https://huggingface.co/datasets/nvidia/OpenMathReasoning), [`numina_math_cot`](https://github.com/project-numina/aimo-progress-prize) | [`bbh`](https://huggingface.co/datasets/lukaemon/bbh), [`mmlu_pro`](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro), [`omni_math`](https://huggingface.co/datasets/KbsdJames/Omni-MATH), [`gpqa_diamond`](https://huggingface.co/datasets/Idavidrein/gpqa), [`enigmata_eval`](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval), `local_private_time_eval` |
| `math_sft` | [`numina_math_cot`](https://github.com/project-numina/aimo-progress-prize), [`openmath_reasoning`](https://huggingface.co/datasets/nvidia/OpenMathReasoning), [`openmathinstruct2`](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2), [`chinese_r1_distill_110k`](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k), [`openthoughts3`](https://arxiv.org/html/2506.04178v1), [`mixture_of_thoughts`](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts) | [`math_500`](https://huggingface.co/datasets/HuggingFaceH4/MATH-500), [`gsm8k_test`](https://huggingface.co/datasets/openai/gsm8k), [`omni_math`](https://huggingface.co/datasets/KbsdJames/Omni-MATH), [`mgsm`](https://arxiv.org/abs/2210.03057), `local_private_time_eval` |
| `math_rlvr` | [`dapo_math_17k`](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k), [`deepscaler_preview`](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset), [`deepmath_103k`](https://arxiv.org/html/2504.11456v2), [`big_math_rl_verified`](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified), [`skywork_or1_rl`](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) | [`math_500`](https://huggingface.co/datasets/HuggingFaceH4/MATH-500), [`gsm8k_test`](https://huggingface.co/datasets/openai/gsm8k), [`omni_math`](https://huggingface.co/datasets/KbsdJames/Omni-MATH), [`mgsm`](https://arxiv.org/abs/2210.03057), `local_private_time_eval` |
| `code_sft` | [`kodcode`](https://arxiv.org/html/2503.02951), [`magicoder`](https://arxiv.org/html/2312.02120v2), [`opencode_reasoning`](https://huggingface.co/datasets/nvidia/OpenCodeReasoning), [`opencodeinstruct`](https://huggingface.co/datasets/nvidia/OpenCodeInstruct), [`codefeedback_filtered`](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction), [`mixture_of_thoughts`](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts), [`taco`](https://huggingface.co/datasets/BAAI/TACO), [`codecontests`](https://huggingface.co/datasets/deepmind/code_contests) | [`livecodebench_v6`](https://github.com/LiveCodeBench/LiveCodeBench), [`bigcodebench`](https://github.com/bigcode-project/bigcodebench), `local_private_time_eval` |
| `code_rlvr` | [`acecode_87k`](https://arxiv.org/html/2502.01718v4), [`kodcode`](https://arxiv.org/html/2503.02951), [`taco`](https://huggingface.co/datasets/BAAI/TACO), [`codecontests`](https://huggingface.co/datasets/deepmind/code_contests), [`skywork_or1_rl`](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) | [`livecodebench_v6`](https://github.com/LiveCodeBench/LiveCodeBench), [`bigcodebench`](https://github.com/bigcode-project/bigcodebench), `local_private_time_eval` |
| `tool_calling` | [`xlam_function_calling`](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k), [`toolace`](https://arxiv.org/html/2409.00917v1), [`toolmind`](https://huggingface.co/datasets/Nanbeige/ToolMind), [`glaive_function_calling_v2`](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2), [`api_bank`](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank), [`toolbench`](https://github.com/OpenBMB/ToolBench), `local_no_tool_negative` | [`bfcl`](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard), [`agentdojo`](https://github.com/ethz-spylab/agentdojo), `local_private_time_eval` |
| `multistep_tool` | [`toolbench`](https://github.com/OpenBMB/ToolBench), [`api_bank`](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank), [`toolace`](https://arxiv.org/html/2409.00917v1), [`toolmind`](https://huggingface.co/datasets/Nanbeige/ToolMind), [`weblinx`](https://huggingface.co/datasets/McGill-NLP/WebLINX), `local_no_tool_negative` | [`bfcl`](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard), [`tau_bench_2_text`](https://github.com/sierra-research/tau2-bench), [`agentdojo`](https://github.com/ethz-spylab/agentdojo), [`mind2web_test`](https://github.com/OSU-NLP-Group/Mind2Web), [`agentharm`](https://huggingface.co/datasets/ai-safety-institute/AgentHarm), `local_private_time_eval` |
| `preference_rm` | [`helpsteer2`](https://huggingface.co/datasets/nvidia/HelpSteer2), [`helpsteer3_preference`](https://huggingface.co/datasets/nvidia/HelpSteer3), [`tulu3_preference_mixture`](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture), [`webgpt_comparisons`](https://huggingface.co/datasets/openai/webgpt_comparisons), [`summarize_from_feedback`](https://huggingface.co/datasets/openai/summarize_from_feedback), [`hh_rlhf`](https://huggingface.co/datasets/Anthropic/hh-rlhf), [`shp`](https://huggingface.co/datasets/stanfordnlp/SHP), [`helpsteer`](https://arxiv.org/html/2406.08673v1), [`ultrafeedback`](https://huggingface.co/datasets/openbmb/UltraFeedback), [`nectar`](https://huggingface.co/datasets/berkeley-nest/Nectar), [`arena_human_preference_140k`](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k), [`skywork_reward_preference_80k`](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2), `local_domain_zh_sft` | [`rewardbench`](https://huggingface.co/datasets/allenai/reward-bench), [`rewardbench2`](https://huggingface.co/datasets/allenai/reward-bench-2), `local_private_time_eval` |
| `safety_moderation` | [`aegis_content_safety_2`](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0), [`wildguardmix_tulu3`](https://arxiv.org/html/2411.15124v2), [`pku_saferlhf`](https://github.com/PKU-Alignment/beavertails), `local_domain_safety` | [`xstest`](https://github.com/paul-rottger/exaggerated-safety), [`harmbench`](https://github.com/centerforaisafety/HarmBench), [`strongreject`](https://github.com/dsbowen/strong_reject), [`sorry_bench_202503`](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503), `local_private_time_eval` |
| `safe_refusal` | [`pku_saferlhf`](https://github.com/PKU-Alignment/beavertails), [`aegis_content_safety_2`](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0), [`wildguardmix_tulu3`](https://arxiv.org/html/2411.15124v2), [`falsereject_train`](https://huggingface.co/datasets/AmazonScience/FalseReject), [`hh_rlhf`](https://huggingface.co/datasets/Anthropic/hh-rlhf), `local_domain_safety` | [`xstest`](https://github.com/paul-rottger/exaggerated-safety), [`falsereject_test`](https://huggingface.co/datasets/AmazonScience/FalseReject), [`harmbench`](https://github.com/centerforaisafety/HarmBench), [`strongreject`](https://github.com/dsbowen/strong_reject), [`sorry_bench_202503`](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503), [`agentharm`](https://huggingface.co/datasets/ai-safety-institute/AgentHarm), `local_private_time_eval` |
| `overrefusal` | `local_overrefusal`, [`wildguardmix_tulu3`](https://arxiv.org/html/2411.15124v2), [`falsereject_train`](https://huggingface.co/datasets/AmazonScience/FalseReject) | [`xstest`](https://github.com/paul-rottger/exaggerated-safety), [`falsereject_test`](https://huggingface.co/datasets/AmazonScience/FalseReject), [`rewardbench`](https://huggingface.co/datasets/allenai/reward-bench), `local_private_time_eval` |
| `process_reward` | [`prm800k`](https://github.com/openai/prm800k), [`math_shepherd`](https://arxiv.org/abs/2312.08935), [`pathfinder_prm`](https://github.com/declare-lab/PathFinder-PRM) | [`processbench`](https://huggingface.co/datasets/Qwen/ProcessBench), [`prmbench`](https://github.com/ssmisya/PRMBench), `local_private_time_eval` |
| `search_agent` | [`search_r1`](https://github.com/PeterGriffinJin/Search-R1), [`webgpt_comparisons`](https://huggingface.co/datasets/openai/webgpt_comparisons) | `local_private_time_eval` |
| `swe_agent` | [`swe_gym`](https://arxiv.org/abs/2412.21139), [`swe_smith`](https://github.com/SWE-bench/SWE-smith), [`r2e_gym`](https://r2e-gym.github.io/), [`nemotron_cascade_2_rl`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) | [`swebench_verified`](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified), `local_private_time_eval` |
| `domain_adaptation` | `local_domain_zh_sft`, `local_no_tool_negative`, `local_overrefusal`, `local_domain_safety` | `local_private_time_eval` |
| `long_output` | [`longform`](https://huggingface.co/datasets/akoksal/LongForm) | [`longform_test`](https://huggingface.co/datasets/akoksal/LongForm), `local_private_time_eval` |
| `browser_agent` | [`weblinx`](https://huggingface.co/datasets/McGill-NLP/WebLINX) | [`mind2web_test`](https://github.com/OSU-NLP-Group/Mind2Web), `local_private_time_eval` |
| `agent_safety` | `local_domain_safety` | [`agentharm`](https://huggingface.co/datasets/ai-safety-institute/AgentHarm), [`agentdojo`](https://github.com/ethz-spylab/agentdojo), `local_private_time_eval` |
| `visual_instruction` | [`pixmo_ask_model_anything`](https://huggingface.co/datasets/allenai/pixmo-ask-model-anything), [`pixmo_cap_qa`](https://huggingface.co/datasets/allenai/pixmo-cap-qa), [`llava_onevision15_instruct_22m`](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data), [`finevision`](https://huggingface.co/datasets/HuggingFaceM4/FineVision), [`llava_instruct_150k`](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K), [`llava15_mix665k`](https://github.com/haotian-liu/LLaVA), `local_multimodal_sft` | [`mmmu_validation`](https://huggingface.co/datasets/MMMU/MMMU), [`mmstar`](https://github.com/MMStar-Benchmark/MMStar), [`mmbench_cn`](https://github.com/open-compass/MMBench), `local_private_time_eval` |
| `visual_grounding` | [`pixmo_points`](https://huggingface.co/datasets/allenai/pixmo-points), [`pixmo_point_explanations`](https://huggingface.co/datasets/allenai/pixmo-point-explanations), [`molmo2_videopoint`](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint), [`os_atlas_action_sft`](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data), [`visual_rft_tasks`](https://arxiv.org/html/2503.01785v1) | [`screenspot_v2`](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2), [`pixmo_count_test`](https://huggingface.co/datasets/allenai/pixmo-count), `local_private_time_eval` |
| `visual_counting` | [`pixmo_count_train`](https://huggingface.co/datasets/allenai/pixmo-count), [`pixmo_points`](https://huggingface.co/datasets/allenai/pixmo-points), [`molmo2_videopoint`](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint), [`llava_onevision15_instruct_22m`](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data) | [`pixmo_count_test`](https://huggingface.co/datasets/allenai/pixmo-count), `local_private_time_eval` |
| `document_chart_ocr` | [`pixmo_docs`](https://huggingface.co/datasets/allenai/pixmo-docs), [`pixmo_cap_qa`](https://huggingface.co/datasets/allenai/pixmo-cap-qa), [`llava_onevision15_instruct_22m`](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data), [`finevision`](https://huggingface.co/datasets/HuggingFaceM4/FineVision), [`mantis_instruct`](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct), `local_multimodal_sft` | [`docvqa_validation`](https://huggingface.co/datasets/lmms-lab/DocVQA), [`chartqa_test`](https://huggingface.co/datasets/lmms-lab/ChartQA), [`ocrbench`](https://github.com/Yuliang-Liu/MultimodalOCR), [`mathvista_testmini`](https://huggingface.co/datasets/AI4Math/MathVista), `local_private_time_eval` |
| `multiimage_video` | [`mantis_instruct`](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct), [`llava_video_178k`](https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K), [`videochat_flash_training`](https://huggingface.co/datasets/OpenGVLab/VideoChat-Flash-Training-Data), [`molmo2_videotrack`](https://huggingface.co/datasets/allenai/Molmo2-VideoTrack), [`molmo2_videopoint`](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint), `local_multimodal_sft` | [`mantis_eval`](https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval), [`video_mme`](https://huggingface.co/datasets/lmms-lab/Video-MME), [`mlvu`](https://github.com/JUNJIE99/MLVU), [`longvideobench`](https://huggingface.co/datasets/longvideobench/LongVideoBench), `local_private_time_eval` |
| `visual_reasoning_rlvr` | [`r1_onevision`](https://huggingface.co/datasets/Fancy-MLLM/R1-Onevision), [`visual_rft_tasks`](https://arxiv.org/html/2503.01785v1), [`llava_onevision15_instruct_22m`](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data) | [`mmmu_pro_standard10`](https://huggingface.co/datasets/MMMU/MMMU_Pro), [`mathvista_testmini`](https://huggingface.co/datasets/AI4Math/MathVista), [`mathvision_test`](https://huggingface.co/datasets/MathLLMs/MathVision), [`chartqa_test`](https://huggingface.co/datasets/lmms-lab/ChartQA), [`cmmmu_test`](https://github.com/CMMMU-Benchmark/CMMMU), `local_private_time_eval` |
| `visual_preference_rm` | [`llava_human_preference_10k`](https://huggingface.co/datasets/zhiqings/LLaVA-Human-Preference-10K), [`rlhf_v`](https://github.com/rlhf-v/rlhf-v), [`rlaif_v`](https://huggingface.co/datasets/openbmb/RLAIF-V-Dataset), [`vlfeedback`](https://huggingface.co/datasets/MMInstruction/VLFeedback), [`povid`](https://huggingface.co/datasets/YiyangAiLab/POVID_preference_data_for_VLLMs), [`spa_vl_train`](https://sqrtizhang.github.io/SPA-VL/), `local_multimodal_preference` | [`vl_rewardbench`](https://huggingface.co/datasets/MMInstruction/VL-RewardBench), [`mmhal_bench`](https://github.com/open-compass/MMHal-Bench), `local_private_time_eval` |
| `audio_instruction` | [`voice_assistant_400k`](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K), `local_multimodal_sft` | [`voicebench`](https://huggingface.co/datasets/hlt-lab/voicebench), [`mmau`](https://sakshi113.github.io/mmau_homepage/), [`audiobench`](https://github.com/AudioLLMs/AudioBench), [`air_bench`](https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset), `local_private_time_eval` |
| `audio_preference_rl` | `local_multimodal_preference` | [`voicebench`](https://huggingface.co/datasets/hlt-lab/voicebench), `local_private_time_eval` |
| `gui_agent` | [`os_atlas_action_sft`](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data), [`gui_odyssey_train`](https://huggingface.co/datasets/hflqf88888/GUIOdyssey), [`android_control_train`](https://github.com/google-research/google-research/tree/master/android_control), `local_gui_action_safety` | [`screenspot_v2`](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2), [`gui_odyssey_test`](https://huggingface.co/datasets/hflqf88888/GUIOdyssey), [`osworld_verified`](https://github.com/xlang-ai/OSWorld), [`androidworld`](https://github.com/google-research/android_world), `local_private_time_eval` |
| `multimodal_safety` | [`vlguard_train`](https://huggingface.co/datasets/ys-zong/VLGuard), [`spa_vl_train`](https://sqrtizhang.github.io/SPA-VL/), [`safe_vid_350k`](https://huggingface.co/datasets/yxwang/SafeVid-350K), `local_multimodal_preference`, `local_gui_action_safety` | [`mm_safetybench`](https://github.com/isXinLiu/MM-SafetyBench), [`figstep`](https://github.com/ThuCCSLab/FigStep), [`safevidbench`](https://huggingface.co/datasets/yxwang/SafeVid-350K), [`voicebench`](https://huggingface.co/datasets/hlt-lab/voicebench), [`mmhal_bench`](https://github.com/open-compass/MMHal-Bench), `local_private_time_eval` |
| `multilingual_multimodal` | [`llava_onevision15_instruct_22m`](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data), [`finevision`](https://huggingface.co/datasets/HuggingFaceM4/FineVision), `local_multimodal_sft` | [`cmmmu_test`](https://github.com/CMMMU-Benchmark/CMMMU), [`cmmu`](https://github.com/FlagOpen/CMMU), [`mmbench_cn`](https://github.com/open-compass/MMBench), [`audiobench`](https://github.com/AudioLLMs/AudioBench), `local_private_time_eval` |

## 分类目录

### 浏览与网页导航 Agent（`agent_browser`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [WebLINX 1.0 chat train](https://huggingface.co/datasets/McGill-NLP/WebLINX)<br>[`weblinx`](https://huggingface.co/datasets/McGill-NLP/WebLINX) | text | agent_sft | research_only | noncommercial | ok | 2024-12-07T04:23:40.000Z | [来源](https://huggingface.co/datasets/McGill-NLP/WebLINX) |

### 搜索与浏览 Agent（`agent_search`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Search-R1](https://github.com/PeterGriffinJin/Search-R1)<br>[`search_r1`](https://github.com/PeterGriffinJin/Search-R1) | text | agent_rl | optional | review_required | not_tracked | — | [来源](https://github.com/PeterGriffinJin/Search-R1) |

### 软件工程 Agent（`agent_swe`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [R2E-Gym](https://r2e-gym.github.io/)<br>[`r2e_gym`](https://r2e-gym.github.io/) | text | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://r2e-gym.github.io/) |
| [SWE-Gym](https://arxiv.org/abs/2412.21139)<br>[`swe_gym`](https://arxiv.org/abs/2412.21139) | text | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://arxiv.org/abs/2412.21139) |
| [SWE-smith](https://github.com/SWE-bench/SWE-smith)<br>[`swe_smith`](https://github.com/SWE-bench/SWE-smith) | text | agent_sft, agent_rl | optional | review_required | not_tracked | — | [来源](https://github.com/SWE-bench/SWE-smith) |

### 音频与语音指令（`audio_sft`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [VoiceAssistant-400K](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K)<br>[`voice_assistant_400k`](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K) | text, audio | sft | optional | review_required | ok | 2024-09-13T12:01:42.000Z | [来源](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K) |

### 中文指令与领域数据（`chinese`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [BELLE](https://github.com/LianjiaTech/BELLE)<br>[`belle`](https://github.com/LianjiaTech/BELLE) | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/LianjiaTech/BELLE) |
| [Chinese DeepSeek R1 Distill 110K](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k)<br>[`chinese_r1_distill_110k`](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k) | text | sft | optional | review_required | ok | 2025-02-21T02:18:08.000Z | [来源](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k) |
| [COIG-CQIA](https://arxiv.org/html/2403.18058v2)<br>[`coig_cqia`](https://arxiv.org/html/2403.18058v2) | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://arxiv.org/html/2403.18058v2) |
| [COIG-PC-Lite](https://huggingface.co/datasets/BAAI/COIG-PC-Lite)<br>[`coig_pc_lite`](https://huggingface.co/datasets/BAAI/COIG-PC-Lite) | text | sft | core | review_required | ok | 2024-06-14T01:18:23.000Z | [来源](https://huggingface.co/datasets/BAAI/COIG-PC-Lite) |
| [Firefly](https://github.com/yangjianxin1/Firefly)<br>[`firefly`](https://github.com/yangjianxin1/Firefly) | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/yangjianxin1/Firefly) |

### 代码 SFT 与推理（`code`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [CodeContests](https://huggingface.co/datasets/deepmind/code_contests)<br>[`codecontests`](https://huggingface.co/datasets/deepmind/code_contests) | text | sft, rlvr | core | allowed_with_obligations | ok | 2023-06-11T12:22:30.000Z | [来源](https://huggingface.co/datasets/deepmind/code_contests) |
| [CodeFeedback-Filtered-Instruction](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction)<br>[`codefeedback_filtered`](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction) | text | sft | optional | review_required | ok | 2024-02-26T09:25:26.000Z | [来源](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction) |
| [KodCode-V1](https://arxiv.org/html/2503.02951)<br>[`kodcode`](https://arxiv.org/html/2503.02951) | text | sft, rlvr | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2503.02951) |
| [Magicoder OSS-Instruct / Self-OSS-Instruct](https://arxiv.org/html/2312.02120v2)<br>[`magicoder`](https://arxiv.org/html/2312.02120v2) | text | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2312.02120v2) |
| [OpenCodeReasoning](https://huggingface.co/datasets/nvidia/OpenCodeReasoning)<br>[`opencode_reasoning`](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) | text | sft | core | allowed_with_obligations | ok | 2025-05-04T23:54:22.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) |
| [OpenCodeInstruct](https://huggingface.co/datasets/nvidia/OpenCodeInstruct)<br>[`opencodeinstruct`](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) | text | sft | core | allowed_with_obligations | ok | 2025-04-28T19:08:02.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) |
| [TACO](https://huggingface.co/datasets/BAAI/TACO)<br>[`taco`](https://huggingface.co/datasets/BAAI/TACO) | text | sft, rlvr | core | review_required | ok | 2024-06-19T09:16:49.000Z | [来源](https://huggingface.co/datasets/BAAI/TACO) |

### 文档、图表与 OCR（`document_sft`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [PixMo-Docs](https://huggingface.co/datasets/allenai/pixmo-docs)<br>[`pixmo_docs`](https://huggingface.co/datasets/allenai/pixmo-docs) | text, image | sft | core | allowed_with_obligations | ok | 2025-02-24T17:25:46.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-docs) |

### 独立评测（`evaluation`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [AgentDojo](https://github.com/ethz-spylab/agentdojo)<br>[`agentdojo`](https://github.com/ethz-spylab/agentdojo) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ethz-spylab/agentdojo) |
| [AgentHarm public test](https://huggingface.co/datasets/ai-safety-institute/AgentHarm)<br>[`agentharm`](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) | text | evaluation | eval_only | eval_only | ok | 2024-12-19T13:27:30.000Z | [来源](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) |
| [AIR-Bench](https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset)<br>[`air_bench`](https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset) | text, audio | evaluation | eval_only | eval_only | ok | 2024-05-12T08:45:15.000Z | [来源](https://huggingface.co/datasets/qyang1021/AIR-Bench-Dataset) |
| [AndroidWorld](https://github.com/google-research/android_world)<br>[`androidworld`](https://github.com/google-research/android_world) | text, image, video | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/google-research/android_world) |
| [AudioBench suite](https://github.com/AudioLLMs/AudioBench)<br>[`audiobench`](https://github.com/AudioLLMs/AudioBench) | text, audio | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/AudioLLMs/AudioBench) |
| [BIG-bench Hard](https://huggingface.co/datasets/lukaemon/bbh)<br>[`bbh`](https://huggingface.co/datasets/lukaemon/bbh) | text | evaluation | eval_only | eval_only | ok | 2025-07-11T17:27:58.000Z | [来源](https://huggingface.co/datasets/lukaemon/bbh) |
| [Berkeley Function Calling Leaderboard](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard)<br>[`bfcl`](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) |
| [BigCodeBench Full / Hard](https://github.com/bigcode-project/bigcodebench)<br>[`bigcodebench`](https://github.com/bigcode-project/bigcodebench) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/bigcode-project/bigcodebench) |
| [ChartQA test](https://huggingface.co/datasets/lmms-lab/ChartQA)<br>[`chartqa_test`](https://huggingface.co/datasets/lmms-lab/ChartQA) | text, image | evaluation | eval_only | eval_only | ok | 2024-03-08T05:04:43.000Z | [来源](https://huggingface.co/datasets/lmms-lab/ChartQA) |
| [CMMMU test](https://github.com/CMMMU-Benchmark/CMMMU)<br>[`cmmmu_test`](https://github.com/CMMMU-Benchmark/CMMMU) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/CMMMU-Benchmark/CMMMU) |
| [CMMU validation / hosted test](https://github.com/FlagOpen/CMMU)<br>[`cmmu`](https://github.com/FlagOpen/CMMU) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/FlagOpen/CMMU) |
| [DocVQA validation](https://huggingface.co/datasets/lmms-lab/DocVQA)<br>[`docvqa_validation`](https://huggingface.co/datasets/lmms-lab/DocVQA) | text, image | evaluation | eval_only | eval_only | ok | 2024-04-18T05:14:35.000Z | [来源](https://huggingface.co/datasets/lmms-lab/DocVQA) |
| [Enigmata-Eval](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval)<br>[`enigmata_eval`](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval) | text | evaluation | eval_only | eval_only | ok | 2025-05-27T08:14:17.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Eval) |
| [FalseReject test](https://huggingface.co/datasets/AmazonScience/FalseReject)<br>[`falsereject_test`](https://huggingface.co/datasets/AmazonScience/FalseReject) | text | evaluation | eval_only | eval_only | ok | 2025-05-14T19:16:44.000Z | [来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| [FigStep](https://github.com/ThuCCSLab/FigStep)<br>[`figstep`](https://github.com/ThuCCSLab/FigStep) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ThuCCSLab/FigStep) |
| [GPQA Diamond](https://huggingface.co/datasets/Idavidrein/gpqa)<br>[`gpqa_diamond`](https://huggingface.co/datasets/Idavidrein/gpqa) | text | evaluation | eval_only | eval_only | ok | 2026-09-21T22:29:06.000Z | [来源](https://huggingface.co/datasets/Idavidrein/gpqa) |
| [GSM8K test](https://huggingface.co/datasets/openai/gsm8k)<br>[`gsm8k_test`](https://huggingface.co/datasets/openai/gsm8k) | text | evaluation | eval_only | eval_only | ok | 2026-03-23T10:18:13.000Z | [来源](https://huggingface.co/datasets/openai/gsm8k) |
| [GUIOdyssey test splits](https://huggingface.co/datasets/hflqf88888/GUIOdyssey)<br>[`gui_odyssey_test`](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) | text, image | evaluation | eval_only | eval_only | ok | 2025-08-04T02:22:43.000Z | [来源](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) |
| [HarmBench](https://github.com/centerforaisafety/HarmBench)<br>[`harmbench`](https://github.com/centerforaisafety/HarmBench) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/centerforaisafety/HarmBench) |
| [IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval)<br>[`ifeval`](https://github.com/google-research/google-research/tree/master/instruction_following_eval) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/google-research/google-research/tree/master/instruction_following_eval) |
| [LiveCodeBench release_v6](https://github.com/LiveCodeBench/LiveCodeBench)<br>[`livecodebench_v6`](https://github.com/LiveCodeBench/LiveCodeBench) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/LiveCodeBench/LiveCodeBench) |
| [LongBench-Chat](https://github.com/THUDM/LongAlign)<br>[`longbench_chat`](https://github.com/THUDM/LongAlign) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/THUDM/LongAlign) |
| [LongBench-Cite](https://github.com/THUDM/LongCite)<br>[`longbench_cite`](https://github.com/THUDM/LongCite) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/THUDM/LongCite) |
| [LongForm test](https://huggingface.co/datasets/akoksal/LongForm)<br>[`longform_test`](https://huggingface.co/datasets/akoksal/LongForm) | text | evaluation | eval_only | eval_only | ok | 2024-03-05T15:20:00.000Z | [来源](https://huggingface.co/datasets/akoksal/LongForm) |
| [LongVideoBench](https://huggingface.co/datasets/longvideobench/LongVideoBench)<br>[`longvideobench`](https://huggingface.co/datasets/longvideobench/LongVideoBench) | text, image, video | evaluation | eval_only | eval_only | ok | 2024-10-14T05:43:04.000Z | [来源](https://huggingface.co/datasets/longvideobench/LongVideoBench) |
| [Mantis-Eval](https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval)<br>[`mantis_eval`](https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval) | text, image, video | evaluation | eval_only | eval_only | ok | 2024-11-15T06:43:06.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/Mantis-Eval) |
| [MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500)<br>[`math_500`](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) | text | evaluation | eval_only | eval_only | ok | 2025-12-15T11:01:40.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) |
| [MathVision test](https://huggingface.co/datasets/MathLLMs/MathVision)<br>[`mathvision_test`](https://huggingface.co/datasets/MathLLMs/MathVision) | text, image | evaluation | eval_only | eval_only | ok | 2026-06-10T07:04:16.000Z | [来源](https://huggingface.co/datasets/MathLLMs/MathVision) |
| [MathVista testmini](https://huggingface.co/datasets/AI4Math/MathVista)<br>[`mathvista_testmini`](https://huggingface.co/datasets/AI4Math/MathVista) | text, image | evaluation | eval_only | eval_only | ok | 2024-02-11T23:09:05.000Z | [来源](https://huggingface.co/datasets/AI4Math/MathVista) |
| [MGSM](https://arxiv.org/abs/2210.03057)<br>[`mgsm`](https://arxiv.org/abs/2210.03057) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://arxiv.org/abs/2210.03057) |
| [Mind2Web test](https://github.com/OSU-NLP-Group/Mind2Web)<br>[`mind2web_test`](https://github.com/OSU-NLP-Group/Mind2Web) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/OSU-NLP-Group/Mind2Web) |
| [MLVU](https://github.com/JUNJIE99/MLVU)<br>[`mlvu`](https://github.com/JUNJIE99/MLVU) | text, image, video | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/JUNJIE99/MLVU) |
| [MM-SafetyBench](https://github.com/isXinLiu/MM-SafetyBench)<br>[`mm_safetybench`](https://github.com/isXinLiu/MM-SafetyBench) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/isXinLiu/MM-SafetyBench) |
| [MMAU](https://sakshi113.github.io/mmau_homepage/)<br>[`mmau`](https://sakshi113.github.io/mmau_homepage/) | text, audio | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://sakshi113.github.io/mmau_homepage/) |
| [MMBench-CN](https://github.com/open-compass/MMBench)<br>[`mmbench_cn`](https://github.com/open-compass/MMBench) | text, image | evaluation | eval_only | eval_only | ok | 2023-09-13T02:11:05.000Z | [来源](https://github.com/open-compass/MMBench) |
| [MMHal-Bench](https://github.com/open-compass/MMHal-Bench)<br>[`mmhal_bench`](https://github.com/open-compass/MMHal-Bench) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/open-compass/MMHal-Bench) |
| [MMLU-Pro](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro)<br>[`mmlu_pro`](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro) | text | evaluation | eval_only | eval_only | ok | 2026-05-02T06:26:05.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro) |
| [MMMU-Pro standard 10 options](https://huggingface.co/datasets/MMMU/MMMU_Pro)<br>[`mmmu_pro_standard10`](https://huggingface.co/datasets/MMMU/MMMU_Pro) | text, image | evaluation | eval_only | eval_only | ok | 2026-10-05T01:55:47.000Z | [来源](https://huggingface.co/datasets/MMMU/MMMU_Pro) |
| [MMMU validation](https://huggingface.co/datasets/MMMU/MMMU)<br>[`mmmu_validation`](https://huggingface.co/datasets/MMMU/MMMU) | text, image | evaluation | eval_only | eval_only | ok | 2026-10-05T02:04:29.000Z | [来源](https://huggingface.co/datasets/MMMU/MMMU) |
| [MMStar](https://github.com/MMStar-Benchmark/MMStar)<br>[`mmstar`](https://github.com/MMStar-Benchmark/MMStar) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/MMStar-Benchmark/MMStar) |
| [MT-Bench](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts)<br>[`mt_bench`](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts) | text | evaluation | eval_only | eval_only | ok | 2023-07-03T20:52:34.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts) |
| [OCRBench](https://github.com/Yuliang-Liu/MultimodalOCR)<br>[`ocrbench`](https://github.com/Yuliang-Liu/MultimodalOCR) | text, image | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/Yuliang-Liu/MultimodalOCR) |
| [Omni-MATH](https://huggingface.co/datasets/KbsdJames/Omni-MATH)<br>[`omni_math`](https://huggingface.co/datasets/KbsdJames/Omni-MATH) | text | evaluation | eval_only | eval_only | ok | 2024-10-12T09:02:05.000Z | [来源](https://huggingface.co/datasets/KbsdJames/Omni-MATH) |
| [OSWorld Verified](https://github.com/xlang-ai/OSWorld)<br>[`osworld_verified`](https://github.com/xlang-ai/OSWorld) | text, image, video | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/xlang-ai/OSWorld) |
| [PixMo-Count test](https://huggingface.co/datasets/allenai/pixmo-count)<br>[`pixmo_count_test`](https://huggingface.co/datasets/allenai/pixmo-count) | text, image | evaluation | eval_only | eval_only | ok | 2024-11-30T04:08:58.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-count) |
| [PRMBench](https://github.com/ssmisya/PRMBench)<br>[`prmbench`](https://github.com/ssmisya/PRMBench) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/ssmisya/PRMBench) |
| [ProcessBench](https://huggingface.co/datasets/Qwen/ProcessBench)<br>[`processbench`](https://huggingface.co/datasets/Qwen/ProcessBench) | text | evaluation | eval_only | eval_only | ok | 2024-12-27T14:05:30.000Z | [来源](https://huggingface.co/datasets/Qwen/ProcessBench) |
| [RewardBench filtered](https://huggingface.co/datasets/allenai/reward-bench)<br>[`rewardbench`](https://huggingface.co/datasets/allenai/reward-bench) | text | evaluation | eval_only | eval_only | ok | 2024-09-09T16:11:45.000Z | [来源](https://huggingface.co/datasets/allenai/reward-bench) |
| [RewardBench 2](https://huggingface.co/datasets/allenai/reward-bench-2)<br>[`rewardbench2`](https://huggingface.co/datasets/allenai/reward-bench-2) | text | evaluation | eval_only | eval_only | ok | 2025-06-04T08:53:38.000Z | [来源](https://huggingface.co/datasets/allenai/reward-bench-2) |
| [RULER](https://github.com/NVIDIA/RULER)<br>[`ruler`](https://github.com/NVIDIA/RULER) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/NVIDIA/RULER) |
| [SafeVidBench](https://huggingface.co/datasets/yxwang/SafeVid-350K)<br>[`safevidbench`](https://huggingface.co/datasets/yxwang/SafeVid-350K) | text, image, video | evaluation | eval_only | eval_only | ok | 2025-11-27T11:30:31.000Z | [来源](https://huggingface.co/datasets/yxwang/SafeVid-350K) |
| [ScreenSpot-v2](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2)<br>[`screenspot_v2`](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2) | text, image | evaluation | eval_only | eval_only | ok | 2025-02-10T11:15:38.000Z | [来源](https://huggingface.co/datasets/OS-Copilot/ScreenSpot-v2) |
| [SORRY-Bench 2025/03](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503)<br>[`sorry_bench_202503`](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503) | text | evaluation | eval_only | eval_only | ok | 2025-02-28T21:58:59.000Z | [来源](https://huggingface.co/datasets/sorry-bench/sorry-bench-202503) |
| [StrongREJECT](https://github.com/dsbowen/strong_reject)<br>[`strongreject`](https://github.com/dsbowen/strong_reject) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/dsbowen/strong_reject) |
| [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified)<br>[`swebench_verified`](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) | text | evaluation | eval_only | eval_only | ok | 2025-02-18T23:48:55.000Z | [来源](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) |
| [τ-bench 2.0 text-v1](https://github.com/sierra-research/tau2-bench)<br>[`tau_bench_2_text`](https://github.com/sierra-research/tau2-bench) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/sierra-research/tau2-bench) |
| [Video-MME](https://huggingface.co/datasets/lmms-lab/Video-MME)<br>[`video_mme`](https://huggingface.co/datasets/lmms-lab/Video-MME) | text, image, video, audio | evaluation | eval_only | eval_only | ok | 2024-07-04T08:14:20.000Z | [来源](https://huggingface.co/datasets/lmms-lab/Video-MME) |
| [VL-RewardBench](https://huggingface.co/datasets/MMInstruction/VL-RewardBench)<br>[`vl_rewardbench`](https://huggingface.co/datasets/MMInstruction/VL-RewardBench) | text, image | evaluation | eval_only | eval_only | ok | 2025-05-19T10:50:44.000Z | [来源](https://huggingface.co/datasets/MMInstruction/VL-RewardBench) |
| [VoiceBench](https://huggingface.co/datasets/hlt-lab/voicebench)<br>[`voicebench`](https://huggingface.co/datasets/hlt-lab/voicebench) | text, audio | evaluation | eval_only | eval_only | ok | 2025-04-19T16:49:38.000Z | [来源](https://huggingface.co/datasets/hlt-lab/voicebench) |
| [XSTest](https://github.com/paul-rottger/exaggerated-safety)<br>[`xstest`](https://github.com/paul-rottger/exaggerated-safety) | text | evaluation | eval_only | eval_only | not_tracked | — | [来源](https://github.com/paul-rottger/exaggerated-safety) |

### 通用指令与 SFT（`general_sft`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Dolci-Instruct-SFT](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT)<br>[`dolci_instruct_sft`](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT) | text | sft | core | allowed_with_obligations | ok | 2026-02-03T00:08:38.000Z | [来源](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT) |
| [Databricks Dolly 15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k)<br>[`dolly_15k`](https://huggingface.co/datasets/databricks/databricks-dolly-15k) | text | sft | core | allowed_with_obligations | ok | 2023-06-30T18:34:13.000Z | [来源](https://huggingface.co/datasets/databricks/databricks-dolly-15k) |
| [Infinity-Instruct](https://huggingface.co/datasets/BAAI/Infinity-Instruct)<br>[`infinity_instruct`](https://huggingface.co/datasets/BAAI/Infinity-Instruct) | text | sft | optional | review_required | ok | 2025-12-04T07:56:39.000Z | [来源](https://huggingface.co/datasets/BAAI/Infinity-Instruct) |
| [LIMA](https://arxiv.org/html/2305.11206v4)<br>[`lima`](https://arxiv.org/html/2305.11206v4) | text | sft | research_only | noncommercial | not_tracked | — | [来源](https://arxiv.org/html/2305.11206v4) |
| [Nemotron-Cascade-2-SFT-Data](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data)<br>[`nemotron_cascade_2_sft`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) | text | sft | optional | review_required | ok | 2026-03-19T23:57:48.000Z | [来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data) |
| [No Robots](https://huggingface.co/datasets/HuggingFaceH4/no_robots)<br>[`no_robots`](https://huggingface.co/datasets/HuggingFaceH4/no_robots) | text | sft | research_only | noncommercial | ok | 2024-04-18T08:40:39.000Z | [来源](https://huggingface.co/datasets/HuggingFaceH4/no_robots) |
| [OpenHermes-2.5](https://huggingface.co/datasets/teknium/OpenHermes-2.5)<br>[`openhermes_2_5`](https://huggingface.co/datasets/teknium/OpenHermes-2.5) | text | sft | optional | review_required | ok | 2024-04-15T08:18:12.000Z | [来源](https://huggingface.co/datasets/teknium/OpenHermes-2.5) |
| [SmolTalk2](https://huggingface.co/blog/smollm3)<br>[`smoltalk2`](https://huggingface.co/blog/smollm3) | text | sft | optional | review_required | not_tracked | — | [来源](https://huggingface.co/blog/smollm3) |
| [Tulu 3 SFT Mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture)<br>[`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | text | sft | core | allowed_with_obligations | ok | 2024-12-02T19:48:33.000Z | [来源](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) |
| [WildChat](https://arxiv.org/html/2405.01470v3)<br>[`wildchat`](https://arxiv.org/html/2405.01470v3) | text | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2405.01470v3) |

### GUI Agent 与动作轨迹（`gui_agent`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [AndroidControl train](https://github.com/google-research/google-research/tree/master/android_control)<br>[`android_control_train`](https://github.com/google-research/google-research/tree/master/android_control) | text, image | agent_sft | research_only | review_required | not_tracked | — | [来源](https://github.com/google-research/google-research/tree/master/android_control) |
| [GUIOdyssey train splits](https://huggingface.co/datasets/hflqf88888/GUIOdyssey)<br>[`gui_odyssey_train`](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) | text, image | agent_sft | core | allowed_with_obligations | ok | 2025-08-04T02:22:43.000Z | [来源](https://huggingface.co/datasets/hflqf88888/GUIOdyssey) |
| [OS-Atlas action fine-tuning data](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data)<br>[`os_atlas_action_sft`](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data) | text, image | agent_sft | core | allowed_with_obligations | ok | 2024-12-04T10:26:47.000Z | [来源](https://huggingface.co/datasets/OS-Copilot/OS-Atlas-Data) |

### 精确指令遵循（`instruction_following`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [IFEval-like Data filtered](https://huggingface.co/datasets/argilla/ifeval-like-data)<br>[`ifeval_like_filtered`](https://huggingface.co/datasets/argilla/ifeval-like-data) | text | sft | optional | review_required | ok | 2024-10-17T09:43:39.000Z | [来源](https://huggingface.co/datasets/argilla/ifeval-like-data) |
| [Tulu 3 Persona Instruction Following](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following)<br>[`tulu3_persona_if`](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following) | text | sft | core | allowed_with_obligations | ok | 2024-11-21T15:57:21.000Z | [来源](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following) |

### 本地必需物料（`local_required`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| 领域安全与政策样本<br>`local_domain_safety` | text | sft, preference, reward_model, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 真实业务中文与领域 SFT<br>`local_domain_zh_sft` | text | sft | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 本地 GUI 动作与危险操作安全数据<br>`local_gui_action_safety` | text, image, video | agent_sft, agent_rl, preference, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 多模态人类偏好与音频 RL 物料<br>`local_multimodal_preference` | text, image, video, audio | preference, reward_model, rlvr | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 真实业务多模态与中文指令 SFT<br>`local_multimodal_sft` | text, image, video, audio | sft | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 无需工具调用负例<br>`local_no_tool_negative` | text | sft, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 正常请求防过拒数据<br>`local_overrefusal` | text | sft, preference, evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |
| 私有与时间外综合评测<br>`local_private_time_eval` | text, image, video, audio | evaluation | local_required | internal_review_required | not_tracked | — | 内部登记项 |

### 长上下文与引用（`long_context`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [LongAlign-10k](https://huggingface.co/datasets/zai-org/LongAlign-10k)<br>[`longalign_10k`](https://huggingface.co/datasets/zai-org/LongAlign-10k) | text | sft | optional | review_required | ok | 2024-02-22T11:39:00.000Z | [来源](https://huggingface.co/datasets/zai-org/LongAlign-10k) |
| [LongCite-45k](https://huggingface.co/datasets/zai-org/LongCite-45k)<br>[`longcite_45k`](https://huggingface.co/datasets/zai-org/LongCite-45k) | text | sft | core | allowed_with_obligations | ok | 2024-10-18T09:59:40.000Z | [来源](https://huggingface.co/datasets/zai-org/LongCite-45k) |

### 长输出生成（`long_output`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [LongForm](https://huggingface.co/datasets/akoksal/LongForm)<br>[`longform`](https://huggingface.co/datasets/akoksal/LongForm) | text | sft | optional | review_required | ok | 2024-03-05T15:20:00.000Z | [来源](https://huggingface.co/datasets/akoksal/LongForm) |

### 数学 SFT（`math`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [NuminaMath-CoT](https://github.com/project-numina/aimo-progress-prize)<br>[`numina_math_cot`](https://github.com/project-numina/aimo-progress-prize) | text | sft | optional | review_required | not_tracked | — | [来源](https://github.com/project-numina/aimo-progress-prize) |
| [OpenMathReasoning](https://huggingface.co/datasets/nvidia/OpenMathReasoning)<br>[`openmath_reasoning`](https://huggingface.co/datasets/nvidia/OpenMathReasoning) | text | sft | core | allowed_with_obligations | ok | 2025-05-27T18:43:44.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenMathReasoning) |
| [OpenMathInstruct-2](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2)<br>[`openmathinstruct2`](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) | text | sft | core | allowed_with_obligations | ok | 2024-11-25T20:07:28.000Z | [来源](https://huggingface.co/datasets/nvidia/OpenMathInstruct-2) |

### 多图交错指令（`multiimage_sft`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Mantis-Instruct](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct)<br>[`mantis_instruct`](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct) | text, image | sft | optional | review_required | ok | 2024-12-25T01:43:11.000Z | [来源](https://huggingface.co/datasets/TIGER-Lab/Mantis-Instruct) |

### 多语言指令数据（`multilingual`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Aya Collection](https://huggingface.co/datasets/CohereLabs/aya_collection)<br>[`aya_collection`](https://huggingface.co/datasets/CohereLabs/aya_collection) | text | sft | optional | allowed_with_obligations | ok | 2025-04-15T08:52:39.000Z | [来源](https://huggingface.co/datasets/CohereLabs/aya_collection) |
| [Aya Dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset)<br>[`aya_dataset`](https://huggingface.co/datasets/CohereLabs/aya_dataset) | text | sft | core | allowed_with_obligations | ok | 2025-04-15T08:51:55.000Z | [来源](https://huggingface.co/datasets/CohereLabs/aya_dataset) |
| [M2Lingual full_data](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual)<br>[`m2lingual`](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual) | text | sft | research_only | noncommercial | ok | 2024-08-13T19:01:43.000Z | [来源](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual) |
| [OpenAssistant OASST2](https://arxiv.org/html/2304.07327v3)<br>[`oasst2`](https://arxiv.org/html/2304.07327v3) | text | sft, preference | optional | allowed_with_obligations | not_tracked | — | [来源](https://arxiv.org/html/2304.07327v3) |

### 多模态偏好与奖励模型（`multimodal_preference`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [LLaVA-Human-Preference-10K](https://huggingface.co/datasets/zhiqings/LLaVA-Human-Preference-10K)<br>[`llava_human_preference_10k`](https://huggingface.co/datasets/zhiqings/LLaVA-Human-Preference-10K) | text, image | preference, reward_model | optional | review_required | ok | 2023-09-27T01:03:58.000Z | [来源](https://huggingface.co/datasets/zhiqings/LLaVA-Human-Preference-10K) |
| [POVID preference data](https://huggingface.co/datasets/YiyangAiLab/POVID_preference_data_for_VLLMs)<br>[`povid`](https://huggingface.co/datasets/YiyangAiLab/POVID_preference_data_for_VLLMs) | text, image | preference, reward_model | optional | review_required | ok | 2024-04-01T08:56:50.000Z | [来源](https://huggingface.co/datasets/YiyangAiLab/POVID_preference_data_for_VLLMs) |
| [RLAIF-V-Dataset](https://huggingface.co/datasets/openbmb/RLAIF-V-Dataset)<br>[`rlaif_v`](https://huggingface.co/datasets/openbmb/RLAIF-V-Dataset) | text, image | preference, reward_model | research_only | noncommercial | ok | 2025-10-14T08:35:37.000Z | [来源](https://huggingface.co/datasets/openbmb/RLAIF-V-Dataset) |
| [RLHF-V](https://github.com/rlhf-v/rlhf-v)<br>[`rlhf_v`](https://github.com/rlhf-v/rlhf-v) | text, image | preference, reward_model | research_only | noncommercial | not_tracked | — | [来源](https://github.com/rlhf-v/rlhf-v) |
| [VLFeedback](https://huggingface.co/datasets/MMInstruction/VLFeedback)<br>[`vlfeedback`](https://huggingface.co/datasets/MMInstruction/VLFeedback) | text, image | preference, reward_model | optional | review_required | ok | 2024-10-17T05:40:23.000Z | [来源](https://huggingface.co/datasets/MMInstruction/VLFeedback) |

### 多模态推理蒸馏（`multimodal_reasoning`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [R1-Onevision](https://huggingface.co/datasets/Fancy-MLLM/R1-Onevision)<br>[`r1_onevision`](https://huggingface.co/datasets/Fancy-MLLM/R1-Onevision) | text, image | sft, rlvr | optional | review_required | ok | 2025-03-18T15:25:45.000Z | [来源](https://huggingface.co/datasets/Fancy-MLLM/R1-Onevision) |

### 多模态 RLVR（`multimodal_rlvr`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Visual-RFT task data](https://arxiv.org/html/2503.01785v1)<br>[`visual_rft_tasks`](https://arxiv.org/html/2503.01785v1) | text, image | rlvr | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2503.01785v1) |

### 多模态安全与幻觉（`multimodal_safety`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [SafeVid-350K](https://huggingface.co/datasets/yxwang/SafeVid-350K)<br>[`safe_vid_350k`](https://huggingface.co/datasets/yxwang/SafeVid-350K) | text, image, video | preference, reward_model | research_only | noncommercial | ok | 2025-11-27T11:30:31.000Z | [来源](https://huggingface.co/datasets/yxwang/SafeVid-350K) |
| [SPA-VL train](https://sqrtizhang.github.io/SPA-VL/)<br>[`spa_vl_train`](https://sqrtizhang.github.io/SPA-VL/) | text, image | preference, reward_model | research_only | review_required | not_tracked | — | [来源](https://sqrtizhang.github.io/SPA-VL/) |
| [VLGuard train](https://huggingface.co/datasets/ys-zong/VLGuard)<br>[`vlguard_train`](https://huggingface.co/datasets/ys-zong/VLGuard) | text, image | sft | optional | review_required | ok | 2025-01-19T00:32:34.000Z | [来源](https://huggingface.co/datasets/ys-zong/VLGuard) |

### 偏好与奖励模型（`preference`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Arena Human Preference 140K](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k)<br>[`arena_human_preference_140k`](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k) | text | preference, reward_model | optional | review_required | ok | 2025-08-01T05:03:39.000Z | [来源](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k) |
| [HelpSteer](https://arxiv.org/html/2406.08673v1)<br>[`helpsteer`](https://arxiv.org/html/2406.08673v1) | text | reward_model, preference | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2406.08673v1) |
| [HelpSteer2](https://huggingface.co/datasets/nvidia/HelpSteer2)<br>[`helpsteer2`](https://huggingface.co/datasets/nvidia/HelpSteer2) | text | preference, reward_model | core | allowed_with_obligations | ok | 2024-12-18T21:06:57.000Z | [来源](https://huggingface.co/datasets/nvidia/HelpSteer2) |
| [HelpSteer3 Preference](https://huggingface.co/datasets/nvidia/HelpSteer3)<br>[`helpsteer3_preference`](https://huggingface.co/datasets/nvidia/HelpSteer3) | text | preference, reward_model | core | allowed_with_obligations | ok | 2025-11-16T07:18:00.000Z | [来源](https://huggingface.co/datasets/nvidia/HelpSteer3) |
| [HH-RLHF](https://huggingface.co/datasets/Anthropic/hh-rlhf)<br>[`hh_rlhf`](https://huggingface.co/datasets/Anthropic/hh-rlhf) | text | preference, reward_model | optional | allowed_with_obligations | ok | 2023-05-26T18:47:34.000Z | [来源](https://huggingface.co/datasets/Anthropic/hh-rlhf) |
| [Nectar](https://huggingface.co/datasets/berkeley-nest/Nectar)<br>[`nectar`](https://huggingface.co/datasets/berkeley-nest/Nectar) | text | preference, reward_model | optional | review_required | ok | 2024-03-20T04:17:46.000Z | [来源](https://huggingface.co/datasets/berkeley-nest/Nectar) |
| [SHP](https://huggingface.co/datasets/stanfordnlp/SHP)<br>[`shp`](https://huggingface.co/datasets/stanfordnlp/SHP) | text | preference, reward_model | optional | review_required | ok | 2023-10-10T23:35:57.000Z | [来源](https://huggingface.co/datasets/stanfordnlp/SHP) |
| [Skywork-Reward-Preference-80K-v0.2](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2)<br>[`skywork_reward_preference_80k`](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2) | text | preference, reward_model | optional | review_required | ok | 2024-10-25T01:58:25.000Z | [来源](https://huggingface.co/datasets/Skywork/Skywork-Reward-Preference-80K-v0.2) |
| [Summarize from Feedback](https://huggingface.co/datasets/openai/summarize_from_feedback)<br>[`summarize_from_feedback`](https://huggingface.co/datasets/openai/summarize_from_feedback) | text | preference, reward_model | research_only | review_required | ok | 2023-01-03T16:55:41.000Z | [来源](https://huggingface.co/datasets/openai/summarize_from_feedback) |
| [Tulu 3 8B Preference Mixture](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture)<br>[`tulu3_preference_mixture`](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture) | text | preference, reward_model | research_only | noncommercial | ok | 2025-02-04T00:21:47.000Z | [来源](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture) |
| [UltraFeedback](https://huggingface.co/datasets/openbmb/UltraFeedback)<br>[`ultrafeedback`](https://huggingface.co/datasets/openbmb/UltraFeedback) | text | preference, reward_model | optional | review_required | ok | 2023-12-29T14:11:19.000Z | [来源](https://huggingface.co/datasets/openbmb/UltraFeedback) |
| [WebGPT Comparisons](https://huggingface.co/datasets/openai/webgpt_comparisons)<br>[`webgpt_comparisons`](https://huggingface.co/datasets/openai/webgpt_comparisons) | text | preference, reward_model | research_only | review_required | ok | 2022-12-19T17:55:29.000Z | [来源](https://huggingface.co/datasets/openai/webgpt_comparisons) |

### 过程奖励与步级监督（`process_reward`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Math-Shepherd](https://arxiv.org/abs/2312.08935)<br>[`math_shepherd`](https://arxiv.org/abs/2312.08935) | text | prm | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/abs/2312.08935) |
| [PathFinder-PRM 400K](https://github.com/declare-lab/PathFinder-PRM)<br>[`pathfinder_prm`](https://github.com/declare-lab/PathFinder-PRM) | text | prm | research_only | review_required | not_tracked | — | [来源](https://github.com/declare-lab/PathFinder-PRM) |
| [PRM800K](https://github.com/openai/prm800k)<br>[`prm800k`](https://github.com/openai/prm800k) | text | prm | optional | allowed_with_obligations | not_tracked | — | [来源](https://github.com/openai/prm800k) |

### 通用与蒸馏推理（`reasoning`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [LIMO](https://arxiv.org/html/2502.03387v1)<br>[`limo`](https://arxiv.org/html/2502.03387v1) | text | sft | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2502.03387v1) |
| [open-r1 Mixture-of-Thoughts](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts)<br>[`mixture_of_thoughts`](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts) | text | sft | optional | review_required | ok | 2025-05-26T15:25:56.000Z | [来源](https://huggingface.co/datasets/open-r1/Mixture-of-Thoughts) |
| [NaturalReasoning](https://huggingface.co/datasets/facebook/natural_reasoning)<br>[`natural_reasoning`](https://huggingface.co/datasets/facebook/natural_reasoning) | text | sft | research_only | noncommercial | ok | 2025-02-21T06:02:40.000Z | [来源](https://huggingface.co/datasets/facebook/natural_reasoning) |
| [OpenThoughts3](https://arxiv.org/html/2506.04178v1)<br>[`openthoughts3`](https://arxiv.org/html/2506.04178v1) | text | sft | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2506.04178v1) |
| [s1K](https://arxiv.org/html/2501.19393v1)<br>[`s1k`](https://arxiv.org/html/2501.19393v1) | text | sft | research_only | review_required | not_tracked | — | [来源](https://arxiv.org/html/2501.19393v1) |

### 代码 RLVR（`rlvr_code`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [AceCode-87K](https://arxiv.org/html/2502.01718v4)<br>[`acecode_87k`](https://arxiv.org/html/2502.01718v4) | text | rlvr | core | review_required | not_tracked | — | [来源](https://arxiv.org/html/2502.01718v4) |

### rlvr_general（`rlvr_general`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Enigmata-Data](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data)<br>[`enigmata_data`](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data) | text | rlvr | research_only | noncommercial | ok | 2025-08-13T09:00:27.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data) |
| [Nemotron-Cascade-2-RL-data](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data)<br>[`nemotron_cascade_2_rl`](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) | text | rlvr, agent_rl, sft | optional | allowed_with_obligations | ok | 2026-03-20T03:38:20.000Z | [来源](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data) |

### 指令遵循 RLVR（`rlvr_if`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [VerInstruct](https://aclanthology.org/2025.emnlp-main.1542/)<br>[`verinstruct`](https://aclanthology.org/2025.emnlp-main.1542/) | text | rlvr | core | review_required | not_tracked | — | [来源](https://aclanthology.org/2025.emnlp-main.1542/) |

### 数学 RLVR（`rlvr_math`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Big-Math-RL-Verified](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified)<br>[`big_math_rl_verified`](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) | text | rlvr | core | allowed_with_obligations | ok | 2025-03-25T15:33:48.000Z | [来源](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) |
| [DAPO-Math-17k](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k)<br>[`dapo_math_17k`](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) | text | rlvr | core | allowed_with_obligations | ok | 2025-04-18T11:20:51.000Z | [来源](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) |
| [DeepMath-103K](https://arxiv.org/html/2504.11456v2)<br>[`deepmath_103k`](https://arxiv.org/html/2504.11456v2) | text | rlvr | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2504.11456v2) |
| [DeepScaleR-Preview-Dataset](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset)<br>[`deepscaler_preview`](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset) | text | rlvr | core | allowed_with_obligations | ok | 2025-02-10T09:51:18.000Z | [来源](https://huggingface.co/datasets/agentica-org/DeepScaleR-Preview-Dataset) |
| [Skywork-OR1-RL-Data](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data)<br>[`skywork_or1_rl`](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) | text | rlvr | optional | review_required | ok | 2025-05-29T02:27:10.000Z | [来源](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data) |

### 安全、拒答与防过拒（`safety`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [Nemotron Content Safety Dataset V2 / Aegis 2.0](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0)<br>[`aegis_content_safety_2`](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) | text | sft, reward_model | core | allowed_with_obligations | ok | 2025-06-09T19:15:56.000Z | [来源](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) |
| [FalseReject train](https://huggingface.co/datasets/AmazonScience/FalseReject)<br>[`falsereject_train`](https://huggingface.co/datasets/AmazonScience/FalseReject) | text | sft | research_only | noncommercial | ok | 2025-05-14T19:16:44.000Z | [来源](https://huggingface.co/datasets/AmazonScience/FalseReject) |
| [PKU-SafeRLHF / BeaverTails](https://github.com/PKU-Alignment/beavertails)<br>[`pku_saferlhf`](https://github.com/PKU-Alignment/beavertails) | text | preference, reward_model, sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/PKU-Alignment/beavertails) |
| [Tulu 3 WildGuardMix fixed subset](https://arxiv.org/html/2411.15124v2)<br>[`wildguardmix_tulu3`](https://arxiv.org/html/2411.15124v2) | text | sft, preference | optional | review_required | not_tracked | — | [来源](https://arxiv.org/html/2411.15124v2) |

### 工具与函数调用（`tool`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [API-Bank](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank)<br>[`api_bank`](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) | text | sft, evaluation | optional | review_required | not_tracked | — | [来源](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank) |
| [Glaive-function-calling-v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2)<br>[`glaive_function_calling_v2`](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2) | text | sft | optional | allowed_with_obligations | ok | 2023-09-27T18:04:08.000Z | [来源](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2) |
| [ToolACE](https://arxiv.org/html/2409.00917v1)<br>[`toolace`](https://arxiv.org/html/2409.00917v1) | text | sft | core | review_required | not_tracked | — | [来源](https://arxiv.org/html/2409.00917v1) |
| [ToolBench](https://github.com/OpenBMB/ToolBench)<br>[`toolbench`](https://github.com/OpenBMB/ToolBench) | text | sft, agent_sft | optional | review_required | not_tracked | — | [来源](https://github.com/OpenBMB/ToolBench) |
| [ToolMind](https://huggingface.co/datasets/Nanbeige/ToolMind)<br>[`toolmind`](https://huggingface.co/datasets/Nanbeige/ToolMind) | text | sft, agent_sft | optional | allowed_with_obligations | ok | 2026-01-09T02:23:42.000Z | [来源](https://huggingface.co/datasets/Nanbeige/ToolMind) |
| [xLAM / APIGen](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k)<br>[`xlam_function_calling`](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) | text | sft | core | review_required | ok | 2025-01-24T19:25:58.000Z | [来源](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) |

### 视频指令与时空理解（`video_sft`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [LLaVA-Video-178K](https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K)<br>[`llava_video_178k`](https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K) | text, image, video | sft | optional | review_required | ok | 2024-10-11T04:59:25.000Z | [来源](https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K) |
| [Molmo2-VideoPoint default](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint)<br>[`molmo2_videopoint`](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint) | text, image, video | sft | core | allowed_with_obligations | ok | 2026-03-16T01:32:31.000Z | [来源](https://huggingface.co/datasets/allenai/Molmo2-VideoPoint) |
| [Molmo2-VideoTrack](https://huggingface.co/datasets/allenai/Molmo2-VideoTrack)<br>[`molmo2_videotrack`](https://huggingface.co/datasets/allenai/Molmo2-VideoTrack) | text, image, video | sft | optional | allowed_with_obligations | ok | 2025-12-16T15:37:13.000Z | [来源](https://huggingface.co/datasets/allenai/Molmo2-VideoTrack) |
| [VideoChat-Flash-Training-Data](https://huggingface.co/datasets/OpenGVLab/VideoChat-Flash-Training-Data)<br>[`videochat_flash_training`](https://huggingface.co/datasets/OpenGVLab/VideoChat-Flash-Training-Data) | text, image, video | sft | optional | review_required | ok | 2025-06-24T07:51:17.000Z | [来源](https://huggingface.co/datasets/OpenGVLab/VideoChat-Flash-Training-Data) |

### vision_grounding（`vision_grounding`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [PixMo-Count train](https://huggingface.co/datasets/allenai/pixmo-count)<br>[`pixmo_count_train`](https://huggingface.co/datasets/allenai/pixmo-count) | text, image | sft | core | allowed_with_obligations | ok | 2024-11-30T04:08:58.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-count) |
| [PixMo-Point-Explanations](https://huggingface.co/datasets/allenai/pixmo-point-explanations)<br>[`pixmo_point_explanations`](https://huggingface.co/datasets/allenai/pixmo-point-explanations) | text, image | sft | optional | allowed_with_obligations | ok | 2024-12-05T18:45:24.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-point-explanations) |
| [PixMo-Points](https://huggingface.co/datasets/allenai/pixmo-points)<br>[`pixmo_points`](https://huggingface.co/datasets/allenai/pixmo-points) | text, image | sft | core | allowed_with_obligations | ok | 2024-11-27T22:12:24.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-points) |

### 视觉指令与 SFT（`vision_sft`）

| 数据集／ID | 模态 | 阶段 | 层级 | 商用状态 | 外部元数据 | 最近修改 | 来源 |
|---|---|---|---|---|---|---|---|
| [FineVision](https://huggingface.co/datasets/HuggingFaceM4/FineVision)<br>[`finevision`](https://huggingface.co/datasets/HuggingFaceM4/FineVision) | text, image | sft | optional | review_required | ok | 2025-10-21T10:12:56.000Z | [来源](https://huggingface.co/datasets/HuggingFaceM4/FineVision) |
| [LLaVA-1.5 Mix665K](https://github.com/haotian-liu/LLaVA)<br>[`llava15_mix665k`](https://github.com/haotian-liu/LLaVA) | text, image | sft | research_only | noncommercial | not_tracked | — | [来源](https://github.com/haotian-liu/LLaVA) |
| [LLaVA-Instruct-150K](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K)<br>[`llava_instruct_150k`](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K) | text, image | sft | research_only | noncommercial | ok | 2024-01-03T01:59:20.000Z | [来源](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K) |
| [LLaVA-OneVision-1.5-Instruct-Data](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data)<br>[`llava_onevision15_instruct_22m`](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data) | text, image | sft | optional | review_required | ok | 2026-07-16T16:14:35.000Z | [来源](https://huggingface.co/datasets/mvp-lab/LLaVA-OneVision-1.5-Instruct-Data) |
| [PixMo-Ask-Model-Anything](https://huggingface.co/datasets/allenai/pixmo-ask-model-anything)<br>[`pixmo_ask_model_anything`](https://huggingface.co/datasets/allenai/pixmo-ask-model-anything) | text, image | sft | core | allowed_with_obligations | ok | 2024-12-05T18:45:02.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-ask-model-anything) |
| [PixMo-Cap-QA](https://huggingface.co/datasets/allenai/pixmo-cap-qa)<br>[`pixmo_cap_qa`](https://huggingface.co/datasets/allenai/pixmo-cap-qa) | text, image | sft | optional | allowed_with_obligations | ok | 2024-12-05T18:49:29.000Z | [来源](https://huggingface.co/datasets/allenai/pixmo-cap-qa) |

## 自动化边界

- 分类、模态、规模、许可和 `usage_tier` 以人工维护的 canonical 总表为准。
- API 返回的许可仅用于变更提醒，不会自动把 `review_required` 改成可商用。
- 新发现数据只进入 `datasets-candidates.yaml`，必须人工审核后才能加入 canonical 总表。
- 多模态资产不会自动进入现有 ERNIE 文本配方；`eval_only` 与私有／时间外评测始终禁止训练。
