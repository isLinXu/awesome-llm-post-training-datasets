# ERNIE 5.5 Flash Base 与更小 Base 模型后训练方案

> 状态：首轮实验计划，不是开训授权。机器版本为 `config/ernie55-training-plan.yaml`， canonical 数据引用仍为 `datasets-list.yaml`。

## 1. 模型结论与训练含义

ERNIE-5.5-Flash-Base 是纯文本稀疏 MoE Base，总参数 280B、每 token 激活 14B，预训练 33.5T tokens；预训练上下文最高 128K，官方声明微调与推理支持 1M。它是预训练结束检查点，没有经过 mid-/post-training。[ModelScope 官方模型卡](https://www.modelscope.cn/models/baidu/ERNIE-5.5-Flash-Base)

这意味着：

1. **不做重复通用 CPT 作为首轮任务。** 先补指令行为、中文业务分布、偏好、安全和可验证能力；代码仓库理解与长上下文已经有很强预训练投入。
2. **不能把它当普通 14B 稠密模型。** 14B 是激活参数，权重存储、专家并行、路由和检查点仍按 280B MoE 处理。
3. **使用 BF16 权重作为首个 SFT 来源。** 官方 Bridge 配方是 BF16 全量 SFT；FP8 部署权重不与训练权重混为同一入口。
4. **1M 不是首轮默认训练长度。** 首轮 8K，长输出／引用分支 32K；通过长度外推、引用与长上下文回归后，再扩 128K／256K。

已固定 BF16 模型 revision：`dfab899dadcff8f4d08af24b75a26c6d4d2e0b09`。该 revision 来自当前 Hugging Face 官方模型 API；正式物化时仍需核对文件清单和哈希。[Hugging Face 官方 API](https://huggingface.co/api/models/baidu/ERNIE-5.5-Flash-Base-BF16)

## 2. 框架、模板与硬件边界

NVIDIA Megatron Bridge 已提供 ERNIE 5.5 的 HF 权重导入、SFT、HF 导出和专用聊天模板。官方参考配方为 `ernie55_sft_64gpu_gb300_bf16_config`：16 节点×4 张 GB300，TP1／PP1／CP64／EP64，行长 262,144，global batch 为 2 行。组件支持 SM90，但官方明确 Hopper 完整配方尚未验证。[Megatron Bridge 官方示例](https://github.com/NVIDIA-NeMo/Megatron-Bridge/blob/main/examples/models/ernie55/README.md)

| 项目 | 本方案处理 |
|---|---|
| Bridge | 固定 commit `08035723e7a86f94fc54a7f4473bd0519f2ac941` |
| Megatron-Core | 官方要求 dev 分支 `f78809f6d` 或之后；开训前解析并记录完整 commit |
| 聊天模板 | 使用 Bridge 的 `ernie55_chat_template.jinja`，训练、离线转换和推理使用同一固定版本 |
| Base tokenizer | 官方 `tokenizer_config.json` 未包含 chat template，不能依赖 `apply_chat_template` 自动获得正确模板。[官方 tokenizer 配置](https://huggingface.co/baidu/ERNIE-5.5-Flash-Base/raw/main/tokenizer_config.json) |
| 特殊 token | 保留 BOS，文本 tokenization 使用 `add_special_tokens=True`。[ERNIE 官方技术博客](https://ernie.baidu.com/release/ernie-5-5-flash-base/) |
| loss | assistant-only；历史 assistant 可单独关闭 loss；工具输出默认 mask |
| reasoning | 统一转换为 `<ernie:think>…</ernie:think>`，不能把其他模板的 think 标签原样混入 |
| 优化器 | ERNIE 官方参考为 `dist_muon`，学习率 2e-5→2e-6，103 warmup steps，默认 2065 steps |
| 首轮改造 | 8K／32K 属于新配置，必须重新做两步冒烟、数值、路由、保存和导出验证，不能视为官方已验证配置 |

### 大模型开训前的最小冒烟

- 2–10 steps：确认 loss、grad norm、router／expert load、MTP 与 DSA indexer 指标有限且可解释。
- 保存→恢复→再训练一步：确认 checkpoint 不是只“能写不能读”。
- 导出 HF：比较固定提示下导出前后 logits／生成，记录容差。
- 模板对称性：同一 messages 经离线与在线路径得到相同 input IDs 和 label mask。
- 长度分桶：8K、32K、128K 分开记录吞吐、显存、有效 supervised tokens 与丢弃率。
- Hopper 集群：先验证 kernels、CP／EP 和通信，不以“组件支持 SM90”推断整训可用。

## 3. 训练顺序：主 run 与专项 branch

**不要从 Base 开始依次把所有阶段串联。** 通用主 run 选出最佳 SFT 后，专项能力从该检查点分支；每个 branch 都带通用回放并做 Base 能力回归。

```text
Base 评测与模板验证
├─ general_public_sft ─┬─ precise_if_sft
│                      ├─ long_output_sft
│                      ├─ code_sft ──────── code_rlvr
│                      └─ tool_sft
├─ general_domain_sft ─── safety_sft
└─ 最佳 SFT ────────────┬─ preference_dpo
                        └─ math_rlvr
```

| 实验 | 数据配比（采样权重） | 初始预算／长度 | 主要验收 |
|---|---|---|---|
| `general_public_sft` | Dolci 80%＋[COIG-PC-Lite](https://huggingface.co/datasets/BAAI/COIG-PC-Lite) 10%＋[OpenMathReasoning](https://huggingface.co/datasets/nvidia/OpenMathReasoning) CoT 10% | 250M tokens／8K | 通用、多轮、IF、数学与 Base 回归 |
| `general_domain_sft` | Dolci 70%＋COIG 10%＋OpenMath 10%＋真实业务中文 10% | 250M tokens／8K | 私有业务集优先，不看公开榜代替业务效果 |
| `precise_if_sft` | 通用回放 50%＋Tulu Persona IF 30%＋[IFEval-like filtered](https://huggingface.co/datasets/argilla/ifeval-like-data) 20% | 200M tokens／8K | 程序约束通过率；[IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval) 严格只评测 |
| `long_output_sft` | 通用回放 60%＋[LongForm](https://huggingface.co/datasets/akoksal/LongForm) train 20%＋LongCite 20% | 200M tokens／32K | 长度、任务完成、事实、引用和一致性 |
| `code_sft` | 通用回放 20%＋[OpenCodeInstruct](https://huggingface.co/datasets/nvidia/OpenCodeInstruct) 80% | 250M tokens／8K | 沙箱、母题去污、LiveCodeBench／BigCodeBench |
| `tool_sft` | [xLAM](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) 55%＋[ToolACE](https://arxiv.org/html/2409.00917v1) 25%＋本地不调用负例 20% | 200M tokens／8K | Schema、实际执行、多轮并行与无需调用 |
| `safety_sft` | 通用回放 60%＋领域政策 20%＋防过拒 20% | 200M tokens／8K | 攻击成功率、过拒率和任务效用 |
| `preference_dpo` | [HelpSteer3 Preference](https://huggingface.co/datasets/nvidia/HelpSteer3) 100%；[HelpSteer2](https://huggingface.co/datasets/nvidia/HelpSteer2) 做独立替代 run | 从最佳 SFT 启动 | [RewardBench 2](https://huggingface.co/datasets/allenai/reward-bench-2)＋通用／私有偏好验收 |
| `math_rlvr` | [DAPO-Math-17k](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k) 100% | 从最佳 SFT；先 pass-rate 分桶 | 答案等价验证＋数学时间外评测 |
| `code_rlvr` | [AceCode-87K](https://arxiv.org/html/2502.01718v4) 100% | 从 code_sft；沙箱签署后启动 | 隐藏测试、fail closed、防奖励攻击 |

说明：

- 配比是**首轮消融起点**，不是最优结论；权重不是样本行数或有效 token 占比。
- Dolci 与 Tulu 3 大全集不在首轮叠加；OpenCodeInstruct 与 OpenCodeReasoning 也做替代 run，不直接相加。
- Aegis 2.0 可用于安全分类器和政策处理，不把危险原文直接转换成普通聊天回答训练。
- 公开评测、`longform_test` 和私有／时间外评测均禁止进入训练。

## 4. 更小 Base 模型的代理实验协议

小模型的作用是用较低成本淘汰错误模板、差配比、低质量过滤器和失效验证器，不是证明大模型一定同比提升。

| 项目 | 统一要求 |
|---|---|
| 模型登记 | 用户提供模型 ID、不可变 revision、架构、参数量、上下文和许可 |
| 对照口径 | 同一数据 revision、配比、过滤、去污、聊天行为和评测版本 |
| 主实验 | Base 行为对齐优先 full SFT；LoRA 可作为工程或筛选项，但不与 full SFT 混为缩放结论 |
| 首轮长度 | 8K；长输出专项 32K；根据模型自身上下文和显存缩小，不强求与 ERNIE 相同 |
| 冒烟预算 | 20M row tokens，先检查损失、模板、长度分布和训练稳定性 |
| 代理预算 | 250M row tokens；有效 supervised tokens 单独记录 |
| 扩展预算 | 最多先做 1B row tokens 的首轮完整实验，不通过增加 epoch 掩盖数据不足 |
| 超参迁移 | 不把 ERNIE 的 Muon、CP64／EP64 或学习率直接复制到其他架构 |
| 晋级规则 | 小模型只淘汰差配方；最终候选仍需在 ERNIE 上做小规模复验 |

建议每个小模型至少运行：

1. `base_regression`；
2. `general_public_sft`；
3. 一个目标专项 branch；
4. 必要时 `preference_dpo` 或对应 RLVR。

不建议所有小模型都跑全部 11 个实验，这会失去代理实验降低成本的意义。

## 5. 评测与晋级门禁

### 每个 run 都记录

- 模型、数据、模板、框架和容器不可变版本。
- 原始行数、过滤后行数、row tokens、supervised tokens、长度分桶和各来源实际采样量。
- train loss、grad norm、吞吐、显存；ERNIE 额外记录 router／expert load、MTP 和 DSA indexer。
- 公开评测与私有／时间外评测分开报告；固定 judge、提示、解码和系统提示。
- 通用能力回归：MMLU-Pro、BBH、MT-Bench、RULER、代码与业务私有集按实验选择。

### 晋级条件

- 模板／mask／BOS 测试通过。
- 数据 revision、质量、许可和去污签署完成。
- 主 run 相比 Base 有目标能力提升，且关键 Base 能力没有不可接受回退。
- 专项 branch 同时通过专项指标和通用回放指标。
- RLVR 必须先通过验证器、奖励一致性、隐藏测试和奖励攻击审计。

## 6. 模型许可对训练方案的约束

ERNIE 5.5 使用自定义模型许可，不是 Apache-2.0。许可地域不包括欧盟、英国和韩国；商业相关产品或服务年收入不超过 5,000 万美元时，需要一次性使用通知并展示 `Powered by ERNIE`，超过该门槛须事先取得书面商业授权。[ERNIE 官方 LICENSE](https://www.modelscope.cn/models/baidu/ERNIE-5.5-Flash-Base/resolve/master/LICENSE)

尤其需要注意第 5.5 条：**不得使用模型、衍生模型或其输出改进非 ERNIE 模型／系统。** 因此：

- 不用 ERNIE 5.5 给其他非 ERNIE 小模型生成蒸馏数据或奖励标签。
- 小模型使用现有公共／自有数据独立训练，不把它当作 ERNIE 的衍生模型，除非谱系和法律审查明确支持。
- 数据自身的教师条款仍需单独审查；ERNIE 模型许可不会替代数据许可。
- 分发衍生模型时保留许可、修改记录和适用的署名／商业义务。

## 7. 当前已固定与仍待提供

已固定：

- ERNIE BF16 模型 ID 与 revision。
- Bridge commit、官方 recipe、模板名称和数据实验依赖关系。
- 11 个实验的训练／评测引用、阶段、权重和 eval-only 隔离校验。

仍需项目侧提供：

1. 更小 Base 的准确模型 ID／revision。
2. GPU 类型、数量、节点互联、共享存储和可用训练时长。
3. 首个目标优先级：通用中文、推理、代码、长输出、工具还是安全。
4. 商用地域、相关产品收入区间，以及是否需要对外分发衍生模型。
5. 本地业务中文、无需工具负例、防过拒和私有评测是否已存在。

在这些信息齐全前，可以执行数据物化和代理协议设计，但不应生成声称“可直接全量开训”的启动配置。
