# 数据集自动更新与分类说明

参考 [awesome-visual-reasoning](https://github.com/isLinXu/awesome-visual-reasoning/) 的配置化分类、状态外置、自动去重和报告生成方式，但针对训练数据增加许可与评测隔离门禁。

## 1. 数据流

```text
config/dataset-taxonomy.yaml
        │ 分类关键词、查询、权重、屏蔽名单
        ▼
datasets-list.yaml ──► scripts/update_datasets_catalog.py
        │                     │
        │                     ├─► data/dataset-catalog-state.json
        │                     │   已知仓库快照、变更历史、候选状态
        │                     │
        │                     ├─► datasets-catalog.md
        │                     │   按类别、阶段、能力生成的已收录目录
        │                     │
        │                     ├─► datasets-candidates.yaml
        │                     │   自动发现的待审核候选，禁止直接训练
        │                     │
        │                     └─► datasets-update-report.md
        │                         刷新结果、变化、错误与新增候选
        ▼
validate_datasets_list.py
```

核心原则：**canonical 总表由人工维护，自动发现只进入候选区。** API 中的许可字段只用于提醒，不会自动修改 `commercial_status`，也不会把 `review_required` 自动改成可商用。

## 2. 常用命令

```bash
# 刷新已收录的 Hugging Face 来源元数据，并重建分类视图
python scripts/update_datasets_catalog.py

# 同时执行完整的新数据发现与自动分类
python scripts/update_datasets_catalog.py --discover

# 小批量调试发现链路
python scripts/update_datasets_catalog.py --discover --discovery-limit 5 --max-queries 5

# 离线重建，不访问网络
python scripts/update_datasets_catalog.py --offline

# 试跑，不写文件
python scripts/update_datasets_catalog.py --discover --dry-run

# 严格模式：任一刷新失败即返回非零状态
python scripts/update_datasets_catalog.py --strict

# 测试与 canonical 校验
python -m unittest scripts/test_update_datasets_catalog.py -v
python validate_datasets_list.py datasets-list.yaml --expect-total 114
```

如环境需要 Hugging Face 凭证，可通过 `HF_TOKEN` 环境变量提供；不要把令牌写入配置或生成文件。

## 3. 修改分类与发现规则

编辑 `config/dataset-taxonomy.yaml`：

- `queries`：新增或调整 Hugging Face 搜索查询。
- `categories`：维护类别名称及 strong／medium／weak 关键词。
- `automation.weights`：调整标题与正文命中的权重。
- `automation.min_score`：调整候选进入阈值。
- `negative`：排除明显非文本后训练的数据。
- `blocklist`：人工确认离题后精确屏蔽仓库，避免自动化反复召回。

分数只表示关键词相关度，不代表数据质量、许可状态或训练价值。

## 4. 候选审核与晋升

所有新候选默认：

```yaml
status: pending_review
auto_training_allowed: false
```

晋升到训练清单前必须完成：

1. 确认文本模态、训练阶段、实际 split 和能力标签。
2. 固定不可变 revision、文件哈希与规模口径。
3. 审查许可、上游内容、访问条件和教师服务条款。
4. 做精确／近重复／语义／母题去污及样本级抽检。
5. 人工加入 `datasets-list.yaml`，再通过完整性与评测隔离校验。

候选被人工收入 canonical 后，更新器会自动把候选状态同步为 `accepted`；加入 `blocklist` 后会同步为 `rejected`。不要只修改生成版 `datasets-candidates.yaml` 来冒充审核完成。

## 5. 定时更新

`.github/workflows/update-datasets-catalog.yml` 已配置：

- 每天 **17:17 UTC**，即北京时间次日 **01:17**。
- 支持手动触发。
- 先运行测试，再刷新与发现，最后校验 canonical 总表。
- 只提交四个自动产物，不自动修改训练总表。

该工作流只有在目录进入 GitHub 仓库并启用 Actions 后才会运行；当前没有在本机启用定时任务。

## 6. 当前边界

- 已收录资产中，只有 `source.provider=huggingface` 且带 `repo_id` 的来源会自动刷新；其他官方项目仍显示 `not_tracked`。
- 当前自动发现覆盖 Hugging Face，不声称覆盖所有 arXiv、GitHub 或内部数据源。
- 元数据刷新成功不等于数据内容、许可和样本质量验证完成。
- `eval_only`、API-Bank 的评测部分以及私有／时间外评测必须继续隔离，严禁训练。
