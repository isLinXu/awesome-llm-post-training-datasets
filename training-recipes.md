# 商用默认／研究隔离训练配方

> 数据源刷新时间：`2026-11-10T01:37:56Z`。两套 Manifest 已固定 ERNIE BF16、数据 revision、config、split 和采样权重；`signoff=false` 是有意保留的开训门禁。

## 1. 使用边界

- **商用默认**：所有数据均为 `allowed_with_obligations`，不含 NC、`research_only` 或 `review_required`；仍需完成实际上游、教师条款、质量和去污签署。
- **研究隔离**：包含非商用和许可待审数据，`commercial_use=false`；原始数据、缓存、处理结果和输出目录均与商用配方分离。
- `enabled=true` 表示配方引用完整，不表示已获许可或质量批准。未下载全量数据、未执行样本级转换和训练冒烟前，不得称为已经开训就绪。
- 采样权重不是行数或有效 token 占比；训练时必须记录实际采样量、row tokens 和 supervised tokens。

- Base：`baidu/ERNIE-5.5-Flash-Base-BF16`
- Model revision：`dfab899dadcff8f4d08af24b75a26c6d4d2e0b09`
- Bridge／模板 revision：`08035723e7a86f94fc54a7f4473bd0519f2ac941`

## 2. 商用默认配方

Manifest：`commercial-default-manifest.yaml`；默认 profile：`commercial_general_sft`；输出：`./runs/commercial-default`。

### `commercial_general_sft`

商用默认通用／多语言／数学／精确指令 SFT；不包含 NC 或 review_required 数据

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | `allenai/tulu-3-sft-mixture` | `b14afda60f1bbebe55d5d2fa1e4df5042f97f8be` | `default` | `train` | 65% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`aya_dataset`](https://huggingface.co/datasets/CohereLabs/aya_dataset) | `CohereLabs/aya_dataset` | `f9ea04583f02a8f86404ff6c58bf75fe637df8a2` | `default` | `train` | 10% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`openmath_reasoning`](https://huggingface.co/datasets/nvidia/OpenMathReasoning) | `nvidia/OpenMathReasoning` | `d3d08664755704f422af97d43a7ff0ded4bd95df` | `default` | `cot` | 15% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`tulu3_persona_if`](https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following) | `allenai/tulu-3-sft-personas-instruction-following` | `fe0c7d350c9b4542b8d829a6f1daa1c259f0ba0e` | `default` | `train` | 10% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_seq_len": 8192, "packing": false, "assistant_only_loss": true, "row_token_budget": 250000000}`

### `commercial_code_sft`

商用默认代码专项；通用回放与代码主集分开计量

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | `allenai/tulu-3-sft-mixture` | `b14afda60f1bbebe55d5d2fa1e4df5042f97f8be` | `default` | `train` | 20% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`opencodeinstruct`](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) | `nvidia/OpenCodeInstruct` | `8f3ba5bafe4d6e8db46082cf7ae6741bc370604d` | `train` | `train` | 80% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_seq_len": 8192, "packing": false, "assistant_only_loss": true, "row_token_budget": 250000000}`

### `commercial_long_sft`

商用默认长文引用专项；长输入单独验收

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | `allenai/tulu-3-sft-mixture` | `b14afda60f1bbebe55d5d2fa1e4df5042f97f8be` | `default` | `train` | 60% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`longcite_45k`](https://huggingface.co/datasets/zai-org/LongCite-45k) | `zai-org/LongCite-45k` | `b776b01faf6e132a3d9cc373de1b46cd6630d772` | `default` | `train` | 40% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_seq_len": 32768, "packing": false, "assistant_only_loss": true, "row_token_budget": 200000000}`

### `commercial_preference_dpo`

最佳商用 SFT 之后的偏好实验；固定 preference config

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`helpsteer3_preference`](https://huggingface.co/datasets/nvidia/HelpSteer3) | `nvidia/HelpSteer3` | `f6d145777bcbde96137596340fab89793acd1031` | `preference` | `train` | 100% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_prompt_len": 4096, "max_response_len": 4096}`

### `commercial_math_rlvr`

商用默认数学 RLVR；Math-Verify 版本和奖励一致性签署后启动

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`dapo_math_17k`](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) | `BytedTsinghua-SIA/DAPO-Math-17k` | `65877096c24ffa7abc4e4fa5edb95cf3413a5674` | `default` | `train` | 100% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署；固定 Math-Verify 版本；验证器签署 |

覆盖参数：`{"max_prompt_len": 4096, "max_response_len": 8192, "rollouts_per_prompt": 8, "temperature": 0.7, "curriculum": "base_model_pass_rate_buckets"}`

## 3. 研究隔离配方

Manifest：`research-isolated-manifest.yaml`；默认 profile：`research_reasoning_sft`；输出：`./runs/research-isolated`。

### `research_reasoning_sft`

研究隔离推理、多语言、中文蒸馏与长输出 SFT；包含 NC／待审数据

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`openmath_reasoning`](https://huggingface.co/datasets/nvidia/OpenMathReasoning) | `nvidia/OpenMathReasoning` | `d3d08664755704f422af97d43a7ff0ded4bd95df` | `default` | `cot` | 30% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`opencode_reasoning`](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) | `nvidia/OpenCodeReasoning` | `20a1ca19c0d050fe9057fc08339d6b370ec1c67a` | `split_0` | `split_0` | 25% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`chinese_r1_distill_110k`](https://huggingface.co/datasets/Congliu/Chinese-DeepSeek-R1-Distill-data-110k) | `Congliu/Chinese-DeepSeek-R1-Distill-data-110k` | `8520b649430617c2be4490f424d251d09d835ed3` | `default` | `train` | 15% | `review_required` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`m2lingual`](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual) | `ServiceNow-AI/M2Lingual` | `e02c0901ccabb711e3dc27ccebaf001e23ee92a4` | `full_data` | `train` | 10% | `noncommercial` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`longform`](https://huggingface.co/datasets/akoksal/LongForm) | `akoksal/LongForm` | `c4d2836f581bf1b7ad4ba1243af81b6b1b8626f1` | `default` | `train` | 10% | `review_required` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | `allenai/tulu-3-sft-mixture` | `b14afda60f1bbebe55d5d2fa1e4df5042f97f8be` | `default` | `train` | 10% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_seq_len": 16384, "packing": false, "assistant_only_loss": true, "row_token_budget": 250000000}`

### `research_browser_sft`

WebLINX 1.0 chat 静态轨迹研究；不得视为动态浏览环境训练

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`weblinx`](https://huggingface.co/datasets/McGill-NLP/WebLINX) | `McGill-NLP/WebLINX` | `a30ff2cbecb75f2d04fac75a2b92721c6c9e3f13` | `chat` | `train` | 80% | `noncommercial` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | `allenai/tulu-3-sft-mixture` | `b14afda60f1bbebe55d5d2fa1e4df5042f97f8be` | `default` | `train` | 20% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_seq_len": 16384, "packing": false, "assistant_only_loss": true, "mask_tool_outputs": true, "row_token_budget": 200000000}`

### `research_overrefusal_sft`

FalseReject Instruct 防过拒研究；test 独立隔离，不使用 CoT 字段复制样本

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`falsereject_train`](https://huggingface.co/datasets/AmazonScience/FalseReject) | `AmazonScience/FalseReject` | `493ba967714ea54c6f01067e1f61e389cc2c9b3e` | `default` | `train` | 60% | `noncommercial` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |
| [`tulu3_sft_mixture`](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) | `allenai/tulu-3-sft-mixture` | `b14afda60f1bbebe55d5d2fa1e4df5042f97f8be` | `default` | `train` | 40% | `allowed_with_obligations` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_seq_len": 8192, "packing": false, "assistant_only_loss": true, "row_token_budget": 200000000}`

### `research_preference_dpo`

Tulu 3 整包偏好研究基线；含非商小子集，禁止晋升商用

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`tulu3_preference_mixture`](https://huggingface.co/datasets/allenai/llama-3.1-tulu-3-8b-preference-mixture) | `allenai/llama-3.1-tulu-3-8b-preference-mixture` | `78a6f00785946cd24276c5dd075f83a143a3b1e6` | `default` | `train` | 100% | `noncommercial` | 上游许可审查；教师条款审查；数据质量签署；去污签署 |

覆盖参数：`{"max_prompt_len": 4096, "max_response_len": 4096}`

### `research_enigmata_rlvr`

Enigmata 非商用规则验证 RL；固定全部任务验证器和 Eval 实例去污后启动

| 数据集 | HF repo | revision | config | split | 权重 | 许可状态 | 该项待签署门禁 |
|---|---|---|---|---|---:|---|---|
| [`enigmata_data`](https://huggingface.co/datasets/BytedTsinghua-SIA/Enigmata-Data) | `BytedTsinghua-SIA/Enigmata-Data` | `95f6920c2428c762ba6a6a2038af7dbe15eb7c75` | `default` | `train` | 100% | `noncommercial` | 上游许可审查；教师条款审查；数据质量签署；去污签署；固定 Enigmata Git commit；验证器签署 |

覆盖参数：`{"max_prompt_len": 16384, "max_response_len": 4096, "rollouts_per_prompt": 8, "temperature": 0.7, "curriculum": "task_and_pass_rate_buckets"}`

## 4. 待签署门禁

| 门禁 | 商用默认 | 研究隔离 | 完成标准 |
|---|---|---|---|
| 模型与数据不可变 revision | 已固定 | 已固定 | 物化时复核 SHA 与文件清单 |
| config／split／配比 | 已固定 | 已固定 | 转换报告中保持相同口径 |
| 数据质量 | 待签署 | 待签署 | 字段、角色、长度、事实、代码执行、偏好对和失败率报告 |
| 数据许可、上游与教师条款 | 待签署 | 待签署；NC 不晋升商用 | 审查后将对应 review flag 置 false，并签署 `signoff.license` |
| 母题／语义／翻译去污 | 待签署 | 待签署 | 对所有公开评测和私有／时间外评测出报告 |
| ERNIE 模型许可 | 待签署 | 待签署 | 地域、商业通知／授权、衍生模型与蒸馏边界 |
| 模板与 label mask | 待验证 | 待验证 | BOS、assistant-only、think 标签、工具输出 mask、训练推理一致 |
| 数据转换器 | 待冒烟 | 待冒烟 | 每个 adapter 跑真实样本并验证 schema、空回答和截断率 |
| RLVR 验证器 | Math-Verify 版本待固定 | Enigmata Git commit 待固定 | 奖励一致性、任务覆盖、攻击测试与 `signoff.verifier` |
| 训练环境与导出 | 待验证 | 待验证 | GPU／互联／存储、2–10 step、保存恢复、HF 导出对比 |
| 本地业务与私有评测 | 生产前必需 | 按研究目标补充 | 业务中文、正常请求、防过拒、不调用负例和私有／时间外评测 |
| 更小 Base 模型 | 待提供 ID／revision | 待提供 ID／revision | 不直接复制 ERNIE 的 Muon、并行和学习率 |

## 5. 校验与切换 profile

```bash
python build_training_recipes.py
python validate_training_recipes.py  # 一次校验全部 10 个 profile 与路径隔离
python validate_post_training_manifest.py commercial-default-manifest.yaml --profile commercial_math_rlvr --allow-placeholders
python validate_post_training_manifest.py research-isolated-manifest.yaml --profile research_enigmata_rlvr --allow-placeholders
# 完成真实审查后，去掉 --allow-placeholders 运行严格模式
python validate_post_training_manifest.py commercial-default-manifest.yaml
python validate_post_training_manifest.py research-isolated-manifest.yaml
```

`--allow-placeholders` 只证明结构、权重和引用有效，**不是开训凭证**。完成真实审查后移除该参数；严格模式通过才允许进入具体训练框架配置生成。

研究数据要进入商用配方时，必须新建商用 Manifest 项并重新完成许可、上游、教师、质量和去污审查；禁止只改 `commercial_status` 或复用研究输出目录。
