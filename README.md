# Awesome LLM Post-Training Datasets

面向**文本 Base 模型**的指令、SFT、偏好／DPO、RLVR、PRM、Agent 与独立评测数据物料库。包含人工维护的 canonical 总表、自动分类与更新流程，以及“商用默认／研究隔离”两套可机读训练配方。

> 当前快照：2026-11-09。共 **114 项资产、26 项能力、10 个训练 profile、16 个配方唯一数据来源**。这里的“完整”指能力、阶段和治理覆盖闭合，不代表穷尽所有公开数据集，也不代表所有条目已获训练或商用批准。

## 快速入口

| 内容 | 文件 | 用途 |
|---|---|---|
| 完整分类数据清单 | [datasets-list.md](datasets-list.md) | 阅读 114 项资产的规模、许可、风险与官方来源 |
| Canonical YAML | [datasets-list.yaml](datasets-list.yaml) | 程序读取的唯一资产总表 |
| 自动分类目录 | [datasets-catalog.md](datasets-catalog.md) | 按类别、阶段、能力和外部刷新状态浏览 |
| 基础调研报告 | [llm-post-training-datasets-zh.md](llm-post-training-datasets-zh.md) | 理解 Instruction、SFT、偏好、RL、PRM 与 Agent 数据差异 |
| Awesome 差分复核 | [awesome-datasets-gap-review.md](awesome-datasets-gap-review.md) | 查看 GitHub awesome 清单召回、纠错和补齐过程 |
| 两套训练配方 | [training-recipes.md](training-recipes.md) | 查看逐项 revision、config／split、配比与开训门禁 |
| ERNIE 5.5 训练计划 | [ernie55-training-plan.md](ernie55-training-plan.md) | 查看当前 Base 的实验顺序、模板与硬件边界 |
| 自动更新说明 | [DATASET-AUTOMATION.md](DATASET-AUTOMATION.md) | 配置发现、分类、候选审核与定时更新 |

## 数据全景

| 维度 | 数量 | 说明 |
|---|---:|---|
| Canonical 资产 | 114 | 旧 42 项全部保留 |
| Core | 23 | 首轮配方候选，不等于许可已签署 |
| Optional | 37 | 按目标和消融结果加入 |
| Research only | 18 | 非商用或许可待审，隔离使用 |
| Eval only | 31 | 严禁进入训练 |
| Local required | 5 | 公共数据无法替代的业务物料 |
| 必需能力 | 26 | 均有训练候选与独立评测引用 |
| 待审核自动候选 | 11 | 不会自动晋升到训练总表 |

### 训练配方快照

| 配方 | 数据项 | Profile | 覆盖内容 |
|---|---:|---:|---|
| 商用默认 | 8 | 5 | 通用 SFT、代码 SFT、长文 SFT、DPO、数学 RLVR |
| 研究隔离 | 10 | 5 | 推理 SFT、浏览 SFT、防过拒 SFT、偏好 DPO、Enigmata RLVR |

两套配方共享 Tulu 3 SFT 与 OpenMathReasoning，因此共有 **16 个唯一来源**。所有启用项均固定 40 位数据 revision、config、split 和采样权重；采样权重不是样本行数占比或有效 token 占比。

**当前配方仍未获得开训授权。** 数据质量、许可、上游与教师条款、去污、模板／label mask、RLVR 验证器和训练环境门禁仍须完成。

## 本地使用

需要 Python 3.10+。

```bash
python -m pip install -r requirements.txt

# 校验 canonical 总表
python validate_datasets_list.py datasets-list.yaml --expect-total 114

# 校验全部 10 个 profile、40 位 revision、权重与路径隔离
python validate_training_recipes.py

# 校验 ERNIE 计划中的数据引用
python validate_ernie55_training_plan.py config/ernie55-training-plan.yaml

# 运行自动化单元测试与仓库卫生检查
python -m unittest scripts/test_update_datasets_catalog.py -v
python scripts/check_repository.py
```

离线重建自动目录：

```bash
python scripts/update_datasets_catalog.py --offline
```

在线刷新已跟踪来源并发现新候选：

```bash
python scripts/update_datasets_catalog.py --discover
```

自动发现结果只进入 `datasets-candidates.yaml`，默认 `pending_review` 且 `auto_training_allowed=false`。API 返回的许可字段只用于变更提醒，不会自动修改人工许可结论。

## 仓库结构

```text
.
├── datasets-list.yaml                 # 人工维护的 canonical 总表
├── datasets-list.md                   # 完整可读清单
├── datasets-catalog.md                # 自动分类视图
├── datasets-candidates.yaml           # 待审核候选，禁止自动训练
├── commercial-default-manifest.yaml   # 商用默认配方
├── research-isolated-manifest.yaml    # 研究隔离配方
├── config/                            # 分类规则与 ERNIE 实验计划
├── data/                              # 外部仓库快照和变更历史
├── research/                          # 差分复核、官方卡片快照与图表
├── scripts/                           # 更新、测试与仓库检查
└── .github/workflows/                 # PR 校验与定时更新
```

## 数据治理原则

1. **Canonical 由人工审核，自动化只负责召回和刷新。**
2. **训练、研究和评测严格分层。** `eval_only` 不得转成提示、蒸馏输入、偏好对或奖励数据。
3. **固定不可变版本。** 正式配方不能使用浮动的 `main`。
4. **许可状态不等于法律批准。** 上游内容、访问条件和教师模型服务条款需要独立审查。
5. **记录真实训练口径。** 实际样本数、row tokens、supervised tokens、长度分桶和过滤失败率应进入运行记录。
6. **研究资产晋升商用必须重新建项和完整重审。** 不得只修改状态字段或复用研究输出。

贡献新数据集或修正条目，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可说明

本仓库只登记外部数据集的元数据、官方链接和训练配方，不再分发其样本内容。各数据集、模型、论文和代码仍遵循其自身许可证与访问条款。

仓库自身代码与文档的开源许可证尚未指定；公开仓库前应由所有者添加 `LICENSE`。详见 [LICENSE-NOTICE.md](LICENSE-NOTICE.md)。
