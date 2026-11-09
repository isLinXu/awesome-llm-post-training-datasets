---
license: cc-by-nc-sa-4.0
dataset_info:
- config_name: seed_data
  splits:
  - name: train
    num_examples: 13686
- config_name: seed_evol_data
  splits:
  - name: train
    num_examples: 102423
- config_name: full_data
  splits:
  - name: train
    num_examples: 173672
configs:
- config_name: seed_data
  data_files: "seed_data.parquet"
- config_name: seed_evol_data
  data_files: "seed_evol_data.parquet"
- config_name: full_data
  data_files: "full_data.parquet"
language:
- zh
- ne
- uk
- ja
- zu
- ku
- ig
- mg
- fi
- si
- id
- sw
- ar
- sv
- ru
- yo
- en
- ht
- kn
- ta
- te
- sq
- mr
- am
- wo
- it
- tr
- ha
- pl
- el
- lt
- ms
- jv
- sn
- ml
- ps
- ky
- es
- ga
- gu
- ko
- vi
- sd
- fa
- nl
- hu
- so
- pa
- bn
- pt
- da
- hi
- eu
- de
- ur
- su
- xh
- fr
---

# M2Lingual
A _**M**ulti-turn_ _**M**ultilingual_ dataset for Instruction Fine-tuning LLMs - [Link](https://arxiv.org/pdf/2406.16783)

## Dataset Summary
The M2Lingual dataset is a comprehensive multi-turn multilingual resource designed to facilitate research and development in conversational AI. It encompasses a wide range of conversation scenarios across multiple languages, making it an invaluable asset for training, evaluating, and benchmarking conversational models. The dataset includes  diverse tasks such as question answering, task completion, summarization and more. Each entry is annotated with information about the conversation's evolution, including task Evol type, multi-turn Evol type, prompts, and the number of turns. The M2Lingual dataset aims to bridge the gap in multi-turn multilingual conversational data, providing a robust foundation for building more inclusive and effective AI systems that can understand and engage in human-like conversations across languages. 

Here is a walkthrough example conversation, the first step involves selecting seeds, the second step evolves the seed sample, and the third step sets a multi-turn evolution which leads to a diverse multi-turn multilingual dataset: 
![Walkthrough for dataset creation](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual/resolve/main/walkthrough-fig.jpg)

## Dataset Instances
Here is an example conversation:
``` 
{ 

    "id": 8605, 

    "conversation": [ 

        { 

            "role": "user", 

            "content": "Formulate an answer to this elaborate question: Identify the base location of the regional airline for which Jim French served as the former chairman and CEO, and explain the significance of this location in the context of the airline's regional operations." 

        }, 

        { 

            "role": "assistant", 

            "content": "Jim French served as the former chairman and CEO of Flybe, a British regional airline. The base location of Flybe was Exeter International Airport in Devon, England. \n\nThe significance of Exeter International Airport as the base location for Flybe lies in its strategic positioning within the United Kingdom. Exeter is situated in the southwest region of England, which allowed Flybe to efficiently connect various regional destinations across the UK and Europe. This location provided a central hub for operations, facilitating shorter flight routes and quick turnaround times, which are essential for regional airlines aiming to offer frequent and reliable services. Additionally, having a base in Exeter helped Flybe tap into a market with fewer competing airlines, allowing it to establish a strong regional presence and foster economic growth within the southwest of England by improving connectivity and accessibility." 

        }, 

        { 

            "role": "user", 

            "content": "Please adjust the output to provide the answer in a concise text-only format." 

        }, 

        { 

            "role": "assistant", 

            "content": "Jim French served as the former chairman and CEO of Flybe, a British regional airline based at Exeter International Airport in Devon, England. The significance of this location lies in its strategic positioning in the southwest of England, enabling efficient regional connectivity across the UK and Europe and fostering economic growth in the region." 

        }, 

        { 

            "role": "user", 

            "content": "Now, rephrase your response as if you were an enthusiastic travel blogger sharing fascinating details with your readers." 

        }, 

        { 

            "role": "assistant", 

            "content": "Hey travel enthusiasts! Did you know that Jim French, the former chairman and CEO of Flybe, once led this fantastic British regional airline based at Exeter International Airport in beautiful Devon, England? It's such a cool spot! Nestled in the southwest of England, Exeter\u2019s prime location made it perfect for Flybe to connect countless regional destinations across the UK and Europe. This strategic hub wasn\u2019t just about convenience; it played a crucial role in boosting regional connectivity and economic growth. So, next time you\u2019re flying through Exeter, remember the incredible role it played in the world of regional air travel! \ud83c\udf0d\u2708\ufe0f" 

        } 

    ], 

    "language": "English", 

    "task": "hotpotqa", 

    "no_of_turns": 2, 

    "evolved_multiturn_prompt": [ 

        "Please adjust the output to provide the answer in a concise text-only format.", 

        "Now, rephrase your response as if you were an enthusiastic travel blogger sharing fascinating details with your readers." 

    ], 

    "multiturn_evol_type": [ 

        "ADJUST_OUTPUT_FORMAT", 

        "PERSONA_REWRITING_FOLLOW_UP" 

    ], 

    "multiturn_evol_prompt": [ 

        { 

            "ADJUST_OUTPUT_FORMAT": "- The follow-up instruction must ask to adjust the output format as users may request specific formats for the output, such as text-only, summarized results, or structured data formats." 

        }, 

        { 

            "PERSONA_REWRITING_FOLLOW_UP": "- The follow-up instruction must request a change in the persona of the response to the previous instruction." 

        } 

    ], 

    "evolved_user_prompt": "Formulate an answer to this elaborate question: Identify the base location of the regional airline for which Jim French served as the former chairman and CEO, and explain the significance of this location in the context of the airline's regional operations.", 

    "output_assistant_reply": "Jim French served as the former chairman and CEO of Flybe, a British regional airline. The base location of Flybe was Exeter International Airport in Devon, England. \n\nThe significance of Exeter International Airport as the base location for Flybe lies in its strategic positioning within the United Kingdom. Exeter is situated in the southwest region of England, which allowed Flybe to efficiently connect various regional destinations across the UK and Europe. This location provided a central hub for operations, facilitating shorter flight routes and quick turnaround times, which are essential for regional airlines aiming to offer frequent and reliable services. Additionally, having a base in Exeter helped Flybe tap into a market with fewer competing airlines, allowing it to establish a strong regional presence and foster economic growth within the southwest of England by improving connectivity and accessibility.", 

    "seed_prompt": "Formulate an answer to this elaborate question: Where is the regional airline based that Jim French is the former chairman and CEO of?", 

    "task_evol_prompt": "Given a prompt #Given Prompt# based upon the #Given Prompt# create a #New Prompt# in the same language by combining multiple facts thus making the question more complex and requiring combining multiple facts to answer correctly.\n#Given Prompt#:\nFormulate an answer to this elaborate question: Where is the regional airline based that Jim French is the former chairman and CEO of?", 

    "task_evol_type": "COMBINE_FACTS" 

}  
```

## Data Fields
“id”: Sample ID. 

“conversation”: The full conversation with user and assistant turns. 

“evolved_multiturn_prompt”: The generated user turns from GPT-4 after using its corresponding multiturn _Evol_. 

“evolved_user_prompt”: The generated instruction from GPT-4 after using its corresponding evol. 

“language”: Language of the conversation. 

“multiturn_evol_type”: The type of multiturn _Evol_ used to prompt GPT-4. 

“multiturn_evol_prompt”: Multiturn _Evol_ prompt to GPT-4. 

“no_of_turns”: Number of turns in the conversation. 

“output_assistant_reply”: GPT-4 output 

“sample_type”: Reflects whether the row is a seed sample, _Evol_ sample or a conversation. 

“seed_prompt”: The seed prompt from which the conversation was generated. 

“task_evol_prompt”: _Evol_ prompt to GPT-4. 

“task_evol_type”: The type of _Evol_ used to prompt GPT-4. 

“task”: The NLP task category of the seed prompt. 

## Statistics
The total number of data points is 182K IR pairs. The table shows more details, with Avg Inst and Response showing the average no of tokens: 
| **Dataset**      | **Seed**  | **Evoled**  | **Multi-turn**  |
|------------------|:---------:|:-----------:|:---------------:|
| Aya Dataset      |   7000    |    37803    |      36969      |
| Aya Collection   |   7140    |    57145    |      34426      |
| Total IR pairs   |   14140   |    94948    |      71395      |
| Avg Instruction  |   49.6    |   107.71    |     356.81      |
| Avg Response     |   56.79   |    62.16    |      87.6       |

## Load with Datasets
To load this dataset with Datasets, you'll need to install Datasets as pip install datasets --upgrade and then use the following code: 

```py

from datasets import load_dataset 
 
dataset = load_dataset("ServiceNow-AI/M2Lingual", "full_data") 

``` 
In the above code snippet, "full_data" refers to the complete dataset, including seeds, evols and multi-turn conversations. You can load other subsets by specifying the name ('seed_data', 'seed_evol_data' or 'full_data') at the time of loading the dataset. Please adhere to the licenses specified for this dataset.

## Additional Information
### Authorship
Publishing Organization: ServiceNow AI 

Industry Type: Tech 

Contact Details: https://www.servicenow.com/now-platform/generative-ai.html

### Intended use and License
Our dataset is licensed through CC-by-NC-SA-4.0 license. More details on the license terms can be found here: [CC BY-NC-SA 4.0 Deed](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)

The dataset is intended to be used to improve model performance towards multilingual natural language understanding. 

Portions of the dataset pertaining to seeds from the Aya collection are licensed under the Apache License, Version 2.0. You may obtain a copy of the License at [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html). This portion contains some files that have been modified. You may not use this file except in compliance with the License. 

### Dataset Version and Maintenance 

Maintenance Status: Actively Maintained 

Version Details: 

   Current version: 1.0 

   Last Update: 06/2024 

   First Release: 06/2024 

### Citation Info

M2Lingual - [Paper link](https://arxiv.org/pdf/2406.16783)


```
@misc{maheshwary2024m2lingual, 

      title={M2Lingual: Enhancing Multilingual, Multi-Turn Instruction Alignment in Large Language Models},  

      author={Rishabh Maheshwary and Vikas Yadav and Hoang Nguyen and Khyati Mahajan and Sathwik Tejaswi Madhusudhan}, 

      year={2024}, 

      eprint={2406.16783}, 

      archivePrefix={arXiv}, 

}
```