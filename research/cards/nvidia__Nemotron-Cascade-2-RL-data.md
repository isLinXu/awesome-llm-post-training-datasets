---
license: odc-by
language:
  - en
configs:
  - config_name: MOPD
    data_files:
      - split: train
        path: MOPD/train.jsonl
  - config_name: multi-domain-RL
    data_files:
      - split: train
        path: multi-domain-RL/train.jsonl
  - config_name: IF-RL
    data_files:
      - split: train
        path: IF-RL/train.jsonl
  - config_name: SWE-RL
    data_files:
      - split: train
        path: SWE-RL/train.jsonl
---

## Dataset Description:

The Nemotron-Cascade-2-RL dataset is a curated reinforcement learning (RL) dataset blend used to train Nemotron-Cascade-2-30B-A3B model. It includes instruction-following RL, multi-domain RL, on-policy distillation, and software engineering RL (SWE-RL) data.

This dataset is ready for commercial use.

The dataset contains the following subset:

### IF-RL

Contains 45,879 training samples for instruction-following RL. Our curation process mainly resolves formatting inconsistencies within the keyword arguments for certain instruction types (e.g., `count_increment_word`). 

This sub dataset is from [nvidia/Nemotron-RL-instruction_following](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following).

### Multi-domain-RL

Contains 18,147 training samples spanning multi-domain tasks, including Multi-choice Question Answering (MCQA), workplace assistant, and structured output for instruction following.

The datasets are from:
- [nvidia/Nemotron-RL-knowledge-mcqa](https://huggingface.co/datasets/nvidia/Nemotron-RL-knowledge-mcqa) (55%)
- [nvidia/Nemotron-RL-agent-workplace_assistant](https://huggingface.co/datasets/nvidia/Nemotron-RL-agent-workplace_assistant) (30%)
- [nvidia/Nemotron-RL-instruction_following-structured_outputs](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following-structured_outputs) (15%)

### Multi-domain on-policy distillation

Contains **6171** data instances, covering data sources from AceReason-Math, instruction following, structured outputs, stem MCQA, and Workplace assistant.

| Data Source            | Count |
|------------------------|------:|
| AceReason-Math         | 1853  |
| Instruction Following  | 1854  |
| Workplace              | 610   |
| STEM                   | 927   |
| Structured Outputs     | 927   | 

The datasets are from:
- [nvidia/AceReason-Math](https://huggingface.co/datasets/nvidia/AceReason-Math)
- [nvidia/Nemotron-RL-instruction_following](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following)
- [nvidia/Nemotron-RL-knowledge-mcqa](https://huggingface.co/datasets/nvidia/Nemotron-RL-knowledge-mcqa) 
- [nvidia/Nemotron-RL-agent-workplace_assistant](https://huggingface.co/datasets/nvidia/Nemotron-RL-agent-workplace_assistant)
- [nvidia/Nemotron-RL-instruction_following-structured_outputs](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following-structured_outputs)

### SWE-RL

Contains 3,612 training samples for software engineering RL workflows.

The datasets are from:
- [SWE-Gym/SWE-Gym](https://huggingface.co/datasets/SWE-Gym/SWE-Gym) (20%)
- [R2E-Gym/R2E-Gym-Subset](https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset) (80%)


## Dataset Creation Date:

Created on: Mar 19, 2026

## License/Terms of Use:

The dataset is governed by the [Open Data Commons Attribution License (ODC-By) v1.0](https://opendatacommons.org/licenses/by/1-0/).

## Intended Usage:

This dataset is intended to be used by the community to train and evaluate RL and instruction-following models. The data may be freely used to train and evaluate.

## Dataset Characterization

**Data Collection Method**  
Hybrid: Human, Synthetic, Automated

**Labeling Method**  
Hybrid: Human, Synthetic, Automated

## Dataset Format

Modality: Text  
Format: JSONL  
Structure: Text + Metadata  

**Columns:**

- Core columns (all subsets):
  - `responses_create_params`: Input payload and generation settings
  - `agent_ref`: Agent metadata used for generation/evaluation
  - `dataset`: Dataset/source identifier (available in subsets that include dataset-level tags)
- Common additional columns (subset-dependent):
  - `prompt`, `instruction_id_list`, `kwargs`, `id`, `category`, `environment_name`, `ground_truth`
  - `pass_rate`, `pass_rate_total`, `pass_rate_passed`
  - `metadata`, `model`, `temperature` (under `responses_create_params`)

## Dataset Quantification


| Subset          | Samples |
| --------------- | ------- |
| MOPD            | 6,171   |
| multi-domain-RL | 18,147  |
| IF-RL           | 45,879  |
| SWE-RL          | 3,612   |
| Total           | 73,809  |


Total Disk Size: ~2.73 GB

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal developer teams to ensure this dataset meets requirements for the relevant industry and use case and addresses unforeseen product misuse.  
Please report quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).