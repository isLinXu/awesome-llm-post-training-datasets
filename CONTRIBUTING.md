# 贡献指南

感谢补充或修正 Base LLM 后训练数据物料。优先提交官方数据卡、论文或项目页能够支持的内容，不要只复制二手 awesome 清单中的规模与许可结论。

## 新增或修改 canonical 资产

1. 编辑 `datasets-list.yaml`，保持唯一、小写的 canonical `id`。
2. 明确训练阶段、能力、`usage_tier`、规模口径和官方来源。
3. 核对真实 config／split；独立评测必须标记 `usage_tier: eval_only` 和 `train_prohibited: true`。
4. 填写许可、访问条件、上游与教师条款风险。无法确认时使用 `review_required`，不要猜测为可商用。
5. 如进入正式配方，固定 40 位不可变 revision，并更新对应 Manifest 与配比。
6. 运行完整校验后再提交 PR。

```bash
python -m pip install -r requirements.txt
python -m unittest scripts/test_update_datasets_catalog.py -v
python validate_datasets_list.py datasets-list.yaml --expect-total 114
python validate_training_recipes.py
python validate_ernie55_training_plan.py config/ernie55-training-plan.yaml
python scripts/check_repository.py
```

若资产总数发生变化，应同步更新校验命令、README 快照和相关报告，而不是为了通过旧计数检查保留错误数字。

## 自动产物

以下文件由更新器生成，不建议手工修改：

- `datasets-catalog.md`
- `datasets-candidates.yaml`
- `datasets-update-report.md`
- `data/dataset-catalog-state.json`

以下文件由配方生成器重建：

- `commercial-default-manifest.yaml`
- `research-isolated-manifest.yaml`
- `training-recipes.md`

修改配方时优先编辑 `build_training_recipes.py`，再运行：

```bash
python build_training_recipes.py
python validate_training_recipes.py
```

差分报告由 `research/build_gap_review.py` 生成。分类与发现规则位于 `config/dataset-taxonomy.yaml`。

## 候选晋升门禁

自动发现候选默认禁止训练。晋升前至少完成：

- 文本模态、训练阶段、真实字段和 split 确认；
- 不可变 revision 与规模口径确认；
- 许可、上游内容、访问条件和教师条款审查；
- 精确／近重复／语义／母题去污与样本级抽检；
- 独立评测隔离；
- canonical 和配方校验通过。

## Pull Request 要求

PR 中请说明：

- 变更的数据 ID 与官方来源；
- 修改的是 canonical、自动规则、文档还是训练配方；
- 是否改变资产数、能力覆盖或许可分层；
- 已运行的校验命令及结果；
- 尚未完成的审查和验证。

不要提交原始数据、模型权重、训练输出、访问令牌或本地缓存。
