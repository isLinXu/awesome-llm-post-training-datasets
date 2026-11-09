---
language:
- en
license: other
size_categories:
- 1K<n<10K
task_categories:
- text-generation
pretty_name: IFEval Like Data
license_name: qwen
license_link: https://huggingface.co/Qwen/Qwen2.5-72B-Instruct/blob/main/LICENSE
dataset_info:
- config_name: default
  features:
  - name: instruction
    dtype: string
  - name: response
    dtype: string
  - name: model_name
    dtype: string
  - name: instruction_id_list
    sequence: string
  - name: distilabel_metadata
    struct:
    - name: raw_input_i_f_eval_kwargs_assignator_0
      list:
      - name: content
        dtype: string
      - name: role
        dtype: string
    - name: raw_output_i_f_eval_kwargs_assignator_0
      dtype: string
  - name: kwargs
    dtype: string
  splits:
  - name: train
    num_bytes: 4946738037
    num_examples: 550000
  download_size: 590155799
  dataset_size: 4946738037
- config_name: filtered
  features:
  - name: key
    dtype: int64
  - name: prompt
    dtype: string
  - name: response
    dtype: string
  - name: instruction_id_list
    sequence: string
  - name: kwargs
    dtype: string
  - name: prompt_level_strict_acc
    dtype: bool
  - name: inst_level_strict_acc
    sequence: bool
  - name: prompt_level_loose_acc
    dtype: bool
  - name: inst_level_loose_acc
    sequence: bool
  splits:
  - name: train
    num_bytes: 83762994.47804716
    num_examples: 56339
  download_size: 31864315
  dataset_size: 83762994.47804716
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
- config_name: filtered
  data_files:
  - split: train
    path: filtered/train-*
tags:
- synthetic
- distilabel
- rlaif
---

<p align="left">
  <a href="https://github.com/argilla-io/distilabel">
    <img src="https://raw.githubusercontent.com/argilla-io/distilabel/main/docs/assets/distilabel-badge-light.png" alt="Built with Distilabel" width="200" height="32"/>
  </a>
</p>

# IFEval Like Data

This dataset contains instruction-response pairs synthetically generated using [Qwen/Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) following the style of [google/IFEval](https://huggingface.co/datasets/google/IFEval) dataset and verified for correctness with [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness). The dataset contains two subsets:

- `default`: which contains 550k unfiltered rows synthetically generated with Qwen2.5-72B-Instruct, a few system prompts and MagPie prompting technique. The `prompt`s can contain [conflicting instructions as defined in the IFEval benchmark](https://github.com/EleutherAI/lm-evaluation-harness/blob/15ffb0dafa9c869c7436ba9a3cf3067ac4c9d846/lm_eval/tasks/ifeval/instructions_registry.py#L76-L150) and incorrect `response`s.
- `filtered`: contains filtered rows i.e. their `IFEval` metric `prompt_level_strict_acc` is equal to `True`. Suitable for fine-tuning.


The pipeline script was uploaded to easily reproduce the dataset:
[ifeval_like_dataset.py](https://huggingface.co/datasets/argilla-warehouse/ifeval-like-data/raw/main/ifeval_like_dataset.py).

It can be run directly using the CLI:

```console
distilabel pipeline run --script "https://huggingface.co/datasets/argilla-warehouse/ifeval-like-data/raw/main/ifeval_like_dataset.py"
```

The resulting dataset can be filtered using the [`filter_ifval_data.py`](https://huggingface.co/datasets/argilla/ifeval-like-data/blob/main/filter_ifeval_data.py) script.

## Dataset Summary

This dataset contains a `pipeline.yaml` which can be used to reproduce the pipeline that generated it in distilabel using the `distilabel` CLI:

```console
distilabel pipeline run --config "https://huggingface.co/datasets/argilla-warehouse/ifeval-like-data/raw/main/pipeline.yaml"
```

or explore the configuration:

```console
distilabel pipeline info --config "https://huggingface.co/datasets/argilla-warehouse/ifeval-like-data/raw/main/pipeline.yaml"
```

## Dataset structure

The examples have the following structure per configuration:


<details><summary> Configuration: default </summary><hr>

```json
{
    "distilabel_metadata": {
        "raw_input_i_f_eval_kwargs_assignator_0": [
            {
                "content": "You will receive a list of constraints and an instruction. The instruction contains constraints. Your task is to generate the appropriate arguments for each constraint type.\n\n## Constraint types, descriptions, and arguments\n\n1. keywords:existence - Checks if specific keywords are present in the response.\n   - keywords: List[str]\n\n2. keywords:frequency - Verifies if a keyword appears a certain number of times in the response.\n   - keyword: str\n   - frequency: int\n   - relation: str\n\n3. keywords:forbidden_words - Ensures that specified words are not used in the response.\n   - forbidden_words: List[str]\n\n4. keywords:letter_frequency - Checks if a particular letter appears a certain number of times in the response.\n   - letter: str (single letter)\n   - let_frequency: int\n   - let_relation: str\n\n5. language:response_language - Verifies that the entire response is in a specified language.\n   - language: str (ISO 639-1 language code)\n\n6. length_constraints:number_sentences - Checks if the response contains a specific number of sentences.\n   - num_sentences: int\n   - relation: str\n\n7. length_constraints:number_paragraphs - Verifies that the response has a particular number of paragraphs.\n   - num_paragraphs: int\n\n8. length_constraints:number_words - Ensures the response contains a specified number of words.\n   - num_words: int\n   - relation: str\n\n9. length_constraints:nth_paragraph_first_word - Checks if a specific paragraph starts with a particular word.\n   - num_paragraphs: int\n   - nth_paragraph: int\n   - first_word: str\n\n10. detectable_content:number_placeholders - Verifies that the response includes a certain number of placeholders (e.g., [placeholder]).\n    - num_placeholders: int\n\n11. detectable_content:postscript - Checks if the response includes a postscript section.\n    - postscript_marker: str\n\n12. detectable_format:number_bullet_lists - Ensures the response contains a specific number of bullet point lists.\n    - num_bullets: int\n\n13. detectable_format:constrained_response - Verifies that the response matches one of a set of predefined options.\n    - (No additional arguments required)\n\n14. detectable_format:number_highlighted_sections - Checks if the response includes a certain number of highlighted sections.\n    - num_highlights: int\n\n15. detectable_format:multiple_sections - Ensures the response is divided into a specified number of sections.\n    - section_spliter: str\n    - num_sections: int\n\n16. detectable_format:json_format - Verifies that the entire response is in valid JSON format.\n    - (No additional arguments required)\n\n17. detectable_format:title - Checks if the response includes a title wrapped in double angular brackets.\n    - (No additional arguments required)\n\n18. combination:two_responses - Ensures that two distinct responses are provided, separated by asterisks.\n    - (No additional arguments required)\n\n19. combination:repeat_prompt - Verifies that the original prompt is repeated before the answer is given.\n    - prompt_to_repeat: str\n\n20. startend:end_checker - Checks if the response ends with a specific phrase.\n    - end_phrase: str\n\n21. change_case:capital_word_frequency - Verifies that a certain number of words are in all capital letters.\n    - capital_frequency: int\n    - capital_relation: str\n\n22. change_case:english_capital - Ensures the entire response is in English and uses all capital letters.\n    - (No additional arguments required)\n\n23. change_case:english_lowercase - Checks that the entire response is in English and uses all lowercase letters.\n    - (No additional arguments required)\n\n24. punctuation:no_comma - Verifies that the response does not contain any commas.\n    - (No additional arguments required)\n\n25. startend:quotation - Ensures the entire response is wrapped in double quotation marks.\n    - (No additional arguments required)\n\nAll the arguments are optional.\n\n## Instructions\n\n1. Analyze the provided list of constraints and the given instruction carefully.\n2. For each constraint in the list, identify the relevant parameters from the instruction text.\n3. If a constraint type is not in the list of constraints then all its arguments should be `null`.\n4. Use appropriate data types for the kwargs (strings, integers, booleans, lists, etc.).\n5. If an argument is not relevant, then its value must be `null`.\n6. Be precise and avoid adding unnecessary or speculative kwargs.\n7. For `*_relation` arguments, only provide a non-null value if the corresponding main argument is also non-null.\n\n## Output format:\n\n```\n{{\n    \"keywords\": [...],\n    \"keyword\": ...,\n    \"frequency\": ...,\n    \"relation\": ...,\n    \"forbidden_words\": [...],\n    \"letter\": ...,\n    \"let_frequency\": ...,\n    \"let_relation\": ...,\n    \"language\": \"...\",\n    \"num_sentences\": ...,\n    \"num_paragraphs\": ...,\n    \"num_words\": ...,\n    \"nth_paragraph\": ...,\n    \"first_word\": ...,\n    \"num_placeholders\": ...,\n    \"postscript_marker\": ...,\n    \"num_bullets\": ...,\n    \"num_highlights\": ...,\n    \"section_spliter\": ...,\n    \"num_sections\": ...,\n    \"prompt_to_repeat\": ...,\n    \"end_phrase\": ...,\n    \"capital_frequency\": ...,\n    \"capital_relation\": ...\n}}\n```\n",
                "role": "system"
            },
            {
                "content": "## Instruction\n\nYour ENTIRE response should be in en language, no other language is allowed. Your response should contain at least 3 sentences. The response must contain at least 2 placeholders represented by square brackets, such as [address]. Your answer must contain exactly 2 bullet points. Use the markdown bullet points such as: * This is point 1. Highlight at least 2 sections in your answer with markdown, i.e. *highlighted section*. Your response must have 2 sections. Mark the beginning of each section with SECTION X, such as: SECTION 1. At the end of your response, please explicitly add a postscript starting with P.S.\n\nPlease provide the details for the [event] taking place at [address]. I need to know the time and the entry requirements.\n## Instruction ID List\n\nlanguage:response_language\nlength_constraints:number_sentences\ndetectable_content:number_placeholders\ndetectable_format:number_bullet_lists\ndetectable_format:number_highlighted_sections\ndetectable_format:multiple_sections\ndetectable_content:postscript",
                "role": "user"
            }
        ],
        "raw_output_i_f_eval_kwargs_assignator_0": "{ \"language\": \"en\", \"num_sentences\": 3, \"relation\": \"at least\", \"num_placeholders\": 2, \"num_bullets\": 2, \"starter\": \"*\", \"num_highlights\": 2, \"section_spliter\": \"SECTION\", \"num_sections\": 2, \"num_paragraphs\": null, \"postscript_marker\": \"P.S.\" , \"original_message\": null, \"keywords\": [], \"keyword\": null, \"frequency\": null, \"num_words\": null, \"nth_paragraph\": null, \"first_word\": null, \"key_sentences\": null, \"forbidden_words\": null, \"original_paragraph\": null, \"low\": null, \"high\": null, \"prompt_to_repeat\": null, \"end_phrase\": null, \"letter\": null, \"let_frequency\": null, \"let_relation\": \"at least\", \"capital_frequency\": null, \"capital_relation\": \"at least\" }"
    },
    "instruction": "Your ENTIRE response should be in en language, no other language is allowed. Your response should contain at least 3 sentences. The response must contain at least 2 placeholders represented by square brackets, such as [address]. Your answer must contain exactly 2 bullet points. Use the markdown bullet points such as: * This is point 1. Highlight at least 2 sections in your answer with markdown, i.e. *highlighted section*. Your response must have 2 sections. Mark the beginning of each section with SECTION X, such as: SECTION 1. At the end of your response, please explicitly add a postscript starting with P.S.\n\nPlease provide the details for the [event] taking place at [address]. I need to know the time and the entry requirements.\n",
    "instruction_id_list": [
        "language:response_language",
        "length_constraints:number_sentences",
        "detectable_content:number_placeholders",
        "detectable_format:number_bullet_lists",
        "detectable_format:number_highlighted_sections",
        "detectable_format:multiple_sections",
        "detectable_content:postscript"
    ],
    "kwargs": "{ \"language\": \"en\", \"num_sentences\": 3, \"relation\": \"at least\", \"num_placeholders\": 2, \"num_bullets\": 2, \"starter\": \"*\", \"num_highlights\": 2, \"section_spliter\": \"SECTION\", \"num_sections\": 2, \"num_paragraphs\": null, \"postscript_marker\": \"P.S.\" , \"original_message\": null, \"keywords\": [], \"keyword\": null, \"frequency\": null, \"num_words\": null, \"nth_paragraph\": null, \"first_word\": null, \"key_sentences\": null, \"forbidden_words\": null, \"original_paragraph\": null, \"low\": null, \"high\": null, \"prompt_to_repeat\": null, \"end_phrase\": null, \"letter\": null, \"let_frequency\": null, \"let_relation\": \"at least\", \"capital_frequency\": null, \"capital_relation\": \"at least\" }",
    "model_name": "Qwen/Qwen2.5-72B-Instruct",
    "response": "SECTION 1\n*highlighted section* The [event] is scheduled to take place at [address] on the specified date. Here are the details you requested:\n\n* The event will commence at 7:00 PM sharp.\n* Entry requirements include a valid ticket and a photo ID for verification.\n\nSECTION 2\n*highlighted section* Please ensure you arrive at least 30 minutes early to allow time for check-in and seating. If you have any additional questions or need further assistance, feel free to reach out.\n\nP.S. Enjoy the event and have a wonderful time!"
}
```

This subset can be loaded as:

```python
from datasets import load_dataset

ds = load_dataset("argilla-warehouse/ifeval-like-data", "default")
```

Or simply as it follows, since there's only one configuration and is named `default`: 

```python
from datasets import load_dataset

ds = load_dataset("argilla-warehouse/ifeval-like-data")
```


</details>





## References


```
@misc{xu2024magpiealignmentdatasynthesis,
    title={Magpie: Alignment Data Synthesis from Scratch by Prompting Aligned LLMs with Nothing},
    author={Zhangchen Xu and Fengqing Jiang and Luyao Niu and Yuntian Deng and Radha Poovendran and Yejin Choi and Bill Yuchen Lin},
    year={2024},
    eprint={2406.08464},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2406.08464},
}
```