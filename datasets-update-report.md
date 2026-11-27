# 数据目录更新报告

> 运行时间：2026-11-27T01:02:03Z；模式：metadata+discovery。

## 本次概览

| 指标 | 数量 |
|---|---:|
| canonical 资产 | 175 |
| 已跟踪 Hugging Face 仓库 | 101 |
| 本次成功刷新 | 101 |
| 刷新失败 | 0 |
| 元数据变化 | 6 |
| 本次新候选 | 1 |
| 累计待审核候选 | 180 |
| 执行发现查询 | 35 |

## 元数据变化

| 仓库 | 关联资产 | 变化字段 |
|---|---|---|
| [`Anthropic/hh-rlhf`](https://huggingface.co/datasets/Anthropic/hh-rlhf) | [`hh_rlhf`](https://huggingface.co/datasets/Anthropic/hh-rlhf) | `likes` |
| [`Idavidrein/gpqa`](https://huggingface.co/datasets/Idavidrein/gpqa) | [`gpqa_diamond`](https://huggingface.co/datasets/Idavidrein/gpqa) | `likes` |
| [`Salesforce/xlam-function-calling-60k`](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) | [`xlam_function_calling`](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k) | `likes` |
| [`longvideobench/LongVideoBench`](https://huggingface.co/datasets/longvideobench/LongVideoBench) | [`longvideobench`](https://huggingface.co/datasets/longvideobench/LongVideoBench) | `likes` |
| [`nvidia/Aegis-AI-Content-Safety-Dataset-2.0`](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) | [`aegis_content_safety_2`](https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0) | `likes` |
| [`openai/gsm8k`](https://huggingface.co/datasets/openai/gsm8k) | [`gsm8k_test`](https://huggingface.co/datasets/openai/gsm8k) | `likes` |

## 新发现候选（仅待审核）

| 仓库 | 建议分类 | 分数 | 状态 |
|---|---|---:|---|
| [`nvidia/Nemotron-SFT-Instruction-Following-Chat-v4`](https://huggingface.co/datasets/nvidia/Nemotron-SFT-Instruction-Following-Chat-v4) | `general_sft` | 13.5 | pending_review |

## 错误与限制

_本次没有刷新错误。_

- 外部 API 元数据不等于数据内容审计；许可变化、revision 固定和样本级验证仍需人工完成。
- 自动分类分数表示关键词相关度，不代表数据质量或训练适用性。
- 更新器不会修改原有 42 项保留关系，也不会把候选资产自动写入训练清单。
