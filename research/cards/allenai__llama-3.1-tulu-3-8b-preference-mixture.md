---
dataset_info:
  features:
  - name: id
    dtype: string
  - name: source
    dtype: string
  - name: prompt
    dtype: string
  - name: chosen
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: rejected
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  splits:
  - name: train
    num_bytes: 1793139112
    num_examples: 272898
  download_size: 940908959
  dataset_size: 1793139112
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
license: odc-by
---



<img src="https://huggingface.co/datasets/allenai/blog-images/resolve/main/tulu-3/Tulu3-logo.png" alt="Tulu3 banner" width="400" style="margin-left:'auto' margin-right:'auto' display:'block'"/>

# Tulu 3 8B Preference Mixture

*Note that this collection is licensed under ODC-BY-1.0 license; different licenses apply to subsets of the data. Some portions of the dataset are non-commercial. We present the mixture as a research artifact.*

This mix is made up from the following preference datasets:

- https://huggingface.co/datasets/allenai/tulu-3-sft-reused-off-policy
- https://huggingface.co/datasets/allenai/tulu-3-sft-reused-on-policy-8b
- https://huggingface.co/datasets/allenai/tulu-3-wildchat-if-on-policy-8b
- https://huggingface.co/datasets/allenai/tulu-3-IF-augmented-on-policy-8b
- https://huggingface.co/datasets/allenai/tulu-3-sft-personas-instruction-following
- https://huggingface.co/datasets/allenai/tulu-3-wildchat-reused-on-policy-8b
- https://huggingface.co/datasets/allenai/tulu-3-ultrafeedback-cleaned-on-policy-8b

This preference mixture used for DPO on our the [Llama 3.1 Tulu 3 8B SFT](https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B-SFT) checkpoint to obtain [Llama 3.1 Tulu 3 8B DPO](https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B-DPO).

It contains 272,898 generation pairs obtained using the following models:
- [Mistral 7B Instruct v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) (Apache 2.0)
- [Mistral Nemo Instruct 2407](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407) (Apache 2.0)
- [Tulu 2 7B](https://huggingface.co/allenai/tulu-2-7b) (Ai2 ImpACT Low Risk License)
- [Tulu 2 13B](https://huggingface.co/allenai/tulu-2-13b) (Ai2 ImpACT Low Risk License)
- [Yi-34B-Chat](https://huggingface.co/01-ai/Yi-34B-Chat) (Apache 2.0)
- [Yi-6B-Chat](https://huggingface.co/01-ai/Yi-6B-Chat) (Apache 2.0)
- [MPT 30B Chat](https://huggingface.co/mosaicml/mpt-30b-chat) (CC-BY-SA-4.0)
- [MPT 7B 8k Chat](https://huggingface.co/mosaicml/mpt-7b-8k-chat) (CC-BY-SA-4.0)
- [Google Gemma 2 27B it](https://huggingface.co/google/gemma-2-27b-it) (Gemma is provided under and subject to the Gemma Terms of Use found at [ai.google.dev/gemma/terms](https://ai.google.dev/gemma/terms))
- [Google Gemma 2 9B it](https://huggingface.co/google/gemma-2-9b-it) (Gemma is provided under and subject to the Gemma Terms of Use found at [ai.google.dev/gemma/terms](https://ai.google.dev/gemma/terms))
- [InternLM2.5 20B](https://huggingface.co/internlm/internlm2_5-20b-chat) (InternLM weights are fully open for academic research and also allow free commercial usage. A commercial license can be obtained as instructed in the model card.)
- [InternLM2.5 7B](https://huggingface.co/internlm/internlm2_5-7b-chat) (InternLM weights are fully open for academic research and also allow free commercial usage. A commercial license can be obtained as instructed in the model card.)
- [InternLM2.5 1.8B](https://huggingface.co/internlm/internlm2_5-1_8b-chat) (InternLM weights are fully open for academic research and also allow free commercial usage. A commercial license can be obtained as instructed in the model card.)
- [Falcon 7B](https://huggingface.co/tiiuae/falcon-7b-instruct) (Apache 2.0)
- [Qwen2.5 72B Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) (Qwen is licensed under the Qwen LICENSE AGREEMENT, Copyright (c) Alibaba Cloud. All Rights Reserved.)
- [Qwen2.5 32B Instruct](https://huggingface.co/Qwen/Qwen2.5-32B-Instruct) (Apache 2.0)
- [Qwen2.5 14B Instruct](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct) (Apache 2.0)
- [Qwen2.5 7B Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) (Apache 2.0)
- [Llama 3.1 8B Instruct ](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) (this dataset was partially "Built with Llama" and is thus subject to the Llama 3.1 License)
- [Llama 3.1 70B Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) (this dataset was partially "Built with Llama" and is thus subject to the Llama 3.1 License)
- [Llama 3 8B Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B) (this dataset was partially "Built with Meta Llama 3"  and is thus subject to the Llama 3 License)
- [GPT-4 Turbo](https://openai.com/index/new-models-and-developer-products-announced-at-devday/) and [GPT-4o](https://openai.com/index/hello-gpt-4o/) (Outputs produced by GPT-4 are subject to OpenAI's [terms of use](https://openai.com/policies/row-terms-of-use))
- [Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet) (Outputs produced by Claude are subject to Anthropic [terms of service](https://www.anthropic.com/legal/commercial-terms) and [usage policy](https://www.anthropic.com/legal/aup))

### Model Family

| **Stage**           | **Llama 3.1 8B**                                                                                          | **Llama 3.1 70B**                                                                                         |
|----------------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **Base Model**       | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B)                                | [meta-llama/Llama-3.1-70B](https://huggingface.co/meta-llama/Llama-3.1-70B)                              |
| **SFT**              | [allenai/Llama-3.1-Tulu-3-8B-SFT](https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B-SFT)                | [allenai/Llama-3.1-Tulu-3-70B-SFT](https://huggingface.co/allenai/Llama-3.1-Tulu-3-70B-SFT)              |
| **DPO**              | [allenai/Llama-3.1-Tulu-3-8B-DPO](https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B-DPO)                | [allenai/Llama-3.1-Tulu-3-70B-DPO](https://huggingface.co/allenai/Llama-3.1-Tulu-3-70B-DPO)              |
| **Final Models (RLVR)**     | [allenai/Llama-3.1-Tulu-3-8B](https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B)                        | [allenai/Llama-3.1-Tulu-3-70B](https://huggingface.co/allenai/Llama-3.1-Tulu-3-70B)                      |
| **Reward Model (RM)**| [allenai/Llama-3.1-Tulu-3-8B-RM](https://huggingface.co/allenai/Llama-3.1-Tulu-3-8B-RM)                                                     | (Same as 8B)                                                     |


## License
This dataset is licensed under ODC-BY. It is intended for research and educational use in accordance with Ai2's [Responsible Use Guidelines](https://allenai.org/responsible-use). This dataset includes output data generated from third party models that are subject to separate terms governing their use.

## Citation

If Tülu3 or any of the related materials were helpful to your work, please cite:
```
@article{lambert2024tulu3,
  title = {Tülu 3: Pushing Frontiers in Open Language Model Post-Training},
  author = {
    Nathan Lambert and 
    Jacob Morrison and 
    Valentina Pyatkin and 
    Shengyi Huang and 
    Hamish Ivison and 
    Faeze Brahman and 
    Lester James V. Miranda and 
    Alisa Liu and 
    Nouha Dziri and 
    Shane Lyu and 
    Yuling Gu and 
    Saumya Malik and 
    Victoria Graf and 
    Jena D. Hwang and 
    Jiangjiang Yang and
    Ronan Le Bras and
    Oyvind Tafjord and
    Chris Wilhelm and
    Luca Soldaini and 
    Noah A. Smith and 
    Yizhong Wang and 
    Pradeep Dasigi and 
    Hannaneh Hajishirzi
  },
  year = {2024},
  email = {tulu@allenai.org}
}
```
