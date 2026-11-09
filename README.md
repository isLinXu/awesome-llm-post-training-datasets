# Awesome LLM Post-Training Datasets

面向**文本与多模态 Base 模型**的指令、SFT、偏好／DPO、RLVR、PRM、Agent 与独立评测数据物料库。覆盖文本、图像、视频、音频，包含人工维护的 canonical 总表、自动分类与更新流程，以及 ERNIE 文本模型专用的“商用默认／研究隔离”两套可机读训练配方。

> 当前快照：2026-11-09。共 **175 项资产、38 项能力、10 个文本训练 profile、16 个文本配方唯一数据来源**。原 **114 项文本资产全部保留**，新增 **61 项多模态资产**。这里的“完整”指能力、阶段和治理覆盖闭合，不代表穷尽所有公开数据集，也不代表所有条目已获训练或商用批准。

## 快速入口

| 内容 | 文件 | 用途 |
|---|---|---|
| 完整分类数据清单 | [datasets-list.md](datasets-list.md) | 阅读 175 项资产的模态、规模、许可、风险与官方来源 |
| Canonical YAML | [datasets-list.yaml](datasets-list.yaml) | 程序读取的唯一资产总表 |
| 多模态扩展 YAML | [datasets-multimodal.yaml](datasets-multimodal.yaml) | 单独审阅 61 项多模态扩展及其范围边界 |
| 多模态调研报告 | [multimodal-post-training-datasets-zh.md](multimodal-post-training-datasets-zh.md) | 图像、视频、音频、GUI、偏好／RLVR、安全和评测结论 |
| 自动分类目录 | [datasets-catalog.md](datasets-catalog.md) | 按类别、模态、阶段、能力和外部刷新状态浏览 |
| 基础文本调研报告 | [llm-post-training-datasets-zh.md](llm-post-training-datasets-zh.md) | 理解 Instruction、SFT、偏好、RL、PRM 与 Agent 数据差异 |
| 文本 Awesome 差分复核 | [awesome-datasets-gap-review.md](awesome-datasets-gap-review.md) | 查看历史文本总表从 78 到 114 项的补齐过程 |
| 两套文本训练配方 | [training-recipes.md](training-recipes.md) | 查看逐项 revision、config／split、配比与开训门禁 |
| ERNIE 5.5 文本训练计划 | [ernie55-training-plan.md](ernie55-training-plan.md) | 查看当前文本 Base 的实验顺序、模板与硬件边界 |
| 自动更新说明 | [DATASET-AUTOMATION.md](DATASET-AUTOMATION.md) | 配置发现、分类、候选审核与定时更新 |

## 数据全景

| 维度 | 数量 | 说明 |
|---|---:|---|
| Canonical 资产 | 175 | 原 114 项文本资产全部保留 |
| 多模态扩展 | 61 | 32 项训练／研究／本地物料＋29 项独立评测 |
| Core | 30 | 首轮候选，不等于许可已签署 |
| Optional | 51 | 按目标和消融结果加入 |
| Research only | 26 | 非商用或许可待审，隔离使用 |
| Eval only | 60 | 严禁进入训练 |
| Local required | 8 | 公共数据无法替代的业务物料 |
| 必需能力 | 38 | 均有训练候选与独立评测引用 |

模态字段采用集合计数：一项资产可同时包含文本、图像、视频和音频。GUI 是 Agent 任务类型，不作为模态。

### 多模态覆盖

- **图像指令与文档**：LLaVA、PixMo、LLaVA-OneVision-1.5、FineVision，区分 SFT 与特征对齐预训练。
- **多图与视频**：Mantis、LLaVA-Video、VideoChat-Flash、Molmo2 时空指向，区分视频数、问答数、帧数和时长。
- **偏好与 RLVR**：人类修正、AI 反馈、构造负例分 profile；数学、分类、检测、坐标和时空验证器分开。
- **音频**：VoiceAssistant、VoiceBench、MMAU、AudioBench、AIR-Bench；公开音频偏好／RLVR 缺口由本地物料补齐。
- **GUI Agent**：OS-Atlas action、GUIOdyssey、AndroidControl，以及 ScreenSpot、OSWorld、AndroidWorld 独立评测。
- **中文与安全**：CMMMU、CMMU、MMBench-CN 仅作评测；VLGuard、SPA-VL、SafeVid 与本地动作安全分层管理。

### 文本训练配方快照

| 配方 | 数据项 | Profile | 覆盖内容 |
|---|---:|---:|---|
| 商用默认 | 8 | 5 | 通用 SFT、代码 SFT、长文 SFT、DPO、数学 RLVR |
| 研究隔离 | 10 | 5 | 推理 SFT、浏览 SFT、防过拒 SFT、偏好 DPO、Enigmata RLVR |

两套配方共享 Tulu 3 SFT 与 OpenMathReasoning，因此共有 **16 个唯一来源**。所有启用项均固定 40 位数据 revision、config、split 和采样权重；采样权重不是样本行数占比或有效 token 占比。

**两套现有配方仍是 ERNIE 文本专用，且尚未获得开训授权。** 多模态资产不会自动进入配方。选择多模态 Base 后，必须另行确认模型 ID、processor、图像／视频／音频输入契约和硬件，再建立独立配方；本仓库不虚构多模态启动配置。

## 本地使用

需要 Python 3.10+。

```bash
python -m pip install -r requirements.txt

# 确定性重建 canonical 与多模态扩展
python build_multimodal_datasets.py
python build_datasets_list.py

# 校验 canonical 总表
python validate_datasets_list.py datasets-list.yaml --expect-total 175

# 校验全部 10 个文本 profile、40 位 revision、权重与路径隔离
python validate_training_recipes.py

# 校验 ERNIE 文本计划中的数据引用
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
├── datasets-list.yaml                 # 由人工审核定义构建的 canonical 总表
├── datasets-list.md                   # 完整可读清单
├── datasets-multimodal.yaml           # 多模态扩展子表
├── multimodal-post-training-datasets-zh.md
├── datasets-catalog.md                # 自动分类视图
├── datasets-candidates.yaml           # 待审核候选，禁止自动训练
├── commercial-default-manifest.yaml   # ERNIE 文本商用默认配方
├── research-isolated-manifest.yaml    # ERNIE 文本研究隔离配方
├── build_multimodal_datasets.py       # 多模态扩展定义
├── build_datasets_list.py             # 合并文本与多模态总表
├── config/                            # 分类规则与 ERNIE 实验计划
├── data/                              # 外部仓库快照和变更历史
├── research/                          # 官方卡片快照、差分复核与图表
├── scripts/                           # 更新、测试与仓库检查
└── .github/workflows/                 # PR 校验与定时更新
```

## 数据治理原则

1. **Canonical 由人工审核，自动化只负责召回和刷新。**
2. **训练、研究和评测严格分层。** `eval_only` 不得转成提示、蒸馏输入、偏好对或奖励数据。
3. **固定不可变版本。** 正式配方不能使用浮动的 `main`；同时固定 config、split、媒体文件和处理器版本。
4. **许可状态不等于法律批准。** 上游内容、媒体权利、肖像／声音同意、访问条件和教师模型服务条款需要独立审查。
5. **记录真实训练口径。** 样本数、row／supervised tokens、媒体时长、帧数、独立提示、任务、轨迹和过滤失败率不可混计。
6. **研究资产晋升商用必须重新建项和完整重审。** 不得只修改状态字段或复用研究输出。
7. **媒体生成不纳入当前范围。** text-to-image、视频生成、音乐／声音生成及专门的医学影像、遥感数据继续隔离。

贡献新数据集或修正条目，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可说明

本仓库只登记外部数据集的元数据、官方链接和训练配方，不再分发其样本内容。各数据集、模型、论文和代码仍遵循其自身许可证与访问条款。

仓库自身代码与文档的开源许可证尚未指定；公开仓库前应由所有者添加 `LICENSE`。详见 [LICENSE-NOTICE.md](LICENSE-NOTICE.md)。
