---
license: apache-2.0
configs:
- config_name: test
  data_files:
  - split: graph_syn_datasets
    path: graph_syn_datasets/*
  - split: open_datasets
    path: open_datasets/*
    
task_categories:
- text-generation
language:
- en
tags:
- function-calling
- tool-calling
- synthetic
arxiv: 2511.15718
paper: https://arxiv.org/abs/2511.15718
pretty_name: ToolMind
---


# ToolMind: A Large-Scale, Reasoning-Enhanced Tool-Use Dataset

ToolMind is a large-scale, high-quality tool-agentic dataset with 160k synthetic data instances generated using over 20k tools and 200k augmented open-source data instances.
Our data synthesis pipeline first constructs a function graph based on parameter correlations and then uses a multi-agent framework to simulate realistic user–assistant–tool interactions.
Beyond trajectory-level validation, we employ fine-grained turn-level filtering to remove erroneous or suboptimal steps, ensuring that only high-quality reasoning traces are retained.
* Technical Report - https://arxiv.org/abs/2511.15718

<img src="./figures/toolmind_performance.png" width="800"/>

# Synthesis pipeline

<img src="./figures/ToolMind.png" width="600"/>

* Graph Construction and Function Chain Sampling

  * We construct a directed graph over the collected functions to model their input–output compatibility, and then sample function chains via random walks for trajectory synthesis. 

* Multi-Agent Multi-Turn Trajectory Synthesis

  * We synthesize user intents to represent realistic user goals. And then the trajectories are created through a multi-agent simulation that involves three distinct agents.

* Quality Filtering

  * To ensure that the synthesized interactions provide reliable learning signals, we apply a two-stage quality filtering process: trajectory-level filtering that maintains goal alignment and coherence, followed by turn-level filtering that removes erroneous or misaligned steps. 

* Hybrid Training with Augmented Open-Source Data
  * We also incorporat a large amount of processed open-source data, including [xlam-function-calling-60k](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k), [When2Call](https://huggingface.co/datasets/nvidia/When2Call), [glaive-function-calling-v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2), [ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE), [BUTTONInstruct](https://github.com/PKU-Baichuan-MLSystemLab/BUTTON), [APIGen-MT-5k](https://huggingface.co/datasets/Salesforce/APIGen-MT-5k), [Tau-bench training set](https://github.com/sierra-research/tau-bench/tree/main). The processing steps involved quality filtering and response reconstruction. 
  * All open-source multi-turn datasets are subjected to the same split and quality-filtering procedures as the synthesised data.


# Dataset Statistic

* We split each trajectory into multiple samples using the turns that passed the turn-level quality filter and analyze both trajectories (orange) and post-split samples (blue).

<img src="./figures/combined_analysis.png" width="800"/>

* Domain Statistics

<img src="./figures/domain_pie.png" width="500"/>

# Overall Performance

* BFCL-v4 2510

| Model                         | Overall | Single Turn (Non-live AST) | Single Turn (Live AST) | Multi Turn | Agentic (Search) | Agentic (Memory) |
|-------------------------------|---------|-----------------------------|------------------------|------------|------------------|------------------|
| DeepSeek-v3 (FC)              | 45.20   | 88.77                       | 79.94                  | 33.00      | 32.50            | 22.37            |
| DeepSeek-R1-0528 (FC)         | 48.97   | 75.73                       | 80.90                  | 44.50      | 63.00            | 0.00             |
| Qwen3-235-instruct (FC)       | 54.37   | 88.10                       | **82.61**              | 44.50      | 49.00            | 29.25            |
| Kimi-K2-Instruct (FC)         | 56.07   | 84.02                       | 77.57                  | **48.75**  | 59.00            | 25.16            |
| GPT-4o-2024-11-20 (FC)        | 50.27   | 83.88                       | 70.54                  | 42.50      | 40.50            | 28.82            |
| GPT5-2025-0807 (FC)           | **59.22** | 72.92                     | 58.25                  | 28.50      | **84.50**        | **57.63**        |
| Gemini2.5-Pro (Prompt)        | 54.14   | **89.54**                   | 76.83                  | 30.62      | 66.50            | 31.61            |
|                               |         |                             |                        |            |                  |                  |
| Qwen3-8b (FC)                 | 42.21   | **88.27**                   | 80.83                  | 38.88      | 10.00            | 18.71            |
| ↳ with ToolMind               | **46.92** (+4.69%) | 88.06            | **81.42**              | **46.62**  | **21.50**        | **20.43**        |
| Qwen3-14b (FC)                | 45.14   | **90.10**                   | **80.90**              | 44.12      | 12.50            | **21.29**        |
| ↳ with ToolMind               | **50.54** (+5.40%) | 89.00           | 80.83                  | **51.00**  | **35.50**        | 17.85            |


* τ-bench and τ²-bench (*For τ²-bench evaluation, we use gpt-4o to act as the user*)

| Model              | τ-bench Avg | τ-bench retail | τ-bench airline | τ²-bench Avg | τ²-bench retail | τ²-bench airline | τ²-bench telecom |
|--------------------|-------------|----------------|-----------------|--------------|------------------|------------------|------------------|
| qwen3-8b (FC)      | 35.83       | 35.65          | 36.00           | 34.67        | 43.86             |   32.00           | 28.07             |
| ↳ with ToolMind    | **46.70** (+10.87%) | **57.39** | **36.00** | **46.40** (+11.77%) | **59.65** | **48.0** | **31.6** |
| qwen3-14b (FC)     | 38.78       | 49.56          | 28.00           | 40.63        | 52.63            |  36.00            | **33.33**         |
| ↳ with ToolMind    | **53.00** (+14.22%) | **60.00** | **46.00** | **49.07** (+8.43%) | **59.65** | **56.00** | 31.58 |


# Ablation Study
| Model                                      | τ-bench Avg | τ-bench retail | τ-bench airline | τ²-bench Avg | τ²-bench retail | τ²-bench airline | τ²-bench telecom | BFCL-v4 overall |
|--------------------------------------------|-------------|----------------|-----------------|--------------|------------------|------------------|------------------|-----------------|
| Qwen3-8B (FC)                              | 35.83       | 35.65          | 36.00           | 34.64        | 43.86             | 32.00             | 28.07             | 42.21           |
| ↳ with (a) synthesized data                | 42.31       | 42.61          | 42.00           | 38.85        | 42.98             | 42.00             | **31.58**         | 46.87           |
| ↳ with (b) no turn-level filtering         | 35.31       | 42.61          | 28.00           | 41.73        | 47.37             | 48.00             | 29.82             | 44.11           |
| ↳ with (c) augmented open-source data      | **48.65**   | 51.30          | **46.00**       | 42.16        | 57.89             | 44.00             | 24.56             | 45.88           |
| ↳ with ToolMind                            | 46.70       | **57.39**      | 36.00           | **46.41**    | **59.65**         | **48.00**         | **31.58**         | **46.92**       |


# Limitations

While we place great emphasis on the safety of the model during the training process, striving to ensure that its outputs align with ethical and legal requirements, it may not completely avoid generating unexpected outputs due to the model's size and probabilistic nature. These outputs may include harmful content such as bias or discrimination. Please don't propagate such content. We do not assume any responsibility for the consequences resulting from the dissemination of inappropriate information.

# Citation
If you find our verifiers useful or want to use it in your projects, please kindly cite this Huggingface project.

<pre><code>
@misc{yang2025toolmindtechnicalreportlargescale,
      title={ToolMind Technical Report: A Large-Scale, Reasoning-Enhanced Tool-Use Dataset}, 
      author={Chen Yang and Ran Le and Yun Xing and Zhenwei An and Zongchao Chen and Wayne Xin Zhao and Yang Song and Tao Zhang},
      year={2025},
      eprint={2511.15718},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2511.15718}, 
}
</code></pre>


# Other Information
If you have any questions, please raise an issue or contact us at nanbeige@126.com.