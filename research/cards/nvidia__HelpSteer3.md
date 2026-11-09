---
license: cc-by-4.0
language:
- en
- zh
- ko
- fr
- es
- ru
- ja
- de
- it
- pt
- pl
- id
- nl
- vi
pretty_name: HelpSteer3
size_categories:
- 10K<n<100K
tags:
- human-feedback
- reinforcement-learning
configs:
- config_name: preference
  default: true
  data_files:
  - split: train
    path: preference/train.jsonl.gz
  - split: validation
    path: preference/validation.jsonl.gz
- config_name: feedback
  data_files:
  - split: train
    path: feedback/train.jsonl.gz
  - split: validation
    path: feedback/validation.jsonl.gz
- config_name: edit
  data_files:
  - split: train
    path: edit/train.jsonl.gz
  - split: validation
    path: edit/validation.jsonl.gz
- config_name: edit_quality
  data_files:
  - split: train
    path: edit_quality/train.jsonl.gz
  - split: validation
    path: edit_quality/validation.jsonl.gz
- config_name: principle
  data_files:
  - split: train
    path: principle/train.jsonl.gz
  - split: validation
    path: principle/validation.jsonl.gz
---
# HelpSteer3

HelpSteer3 is an open-source dataset (CC-BY-4.0) that supports aligning models to become more helpful in responding to user prompts.

HelpSteer3-Preference can be used to train [Llama 3.3 Nemotron Super 49B v1](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1) (for Generative RMs) and [Llama 3.3 70B Instruct Models](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) (for Bradley-Terry RMs) to produce Reward Models that score as high as 85.5% on [RM-Bench](https://arxiv.org/abs/2410.16184) and 78.6% on [JudgeBench](https://huggingface.co/spaces/ScalerLab/JudgeBench), which substantially surpass existing Reward Models on these benchmarks.

HelpSteer3-Feedback and Edit can be used to train [Llama 3.3 70B Instruct Models](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) to perform a novel approach to Inference Time Scaling (ITS) for open-ended, general-domain tasks, we achieve as high as 93.4% on [Arena Hard](https://github.com/lmarena/arena-hard-auto), which makes it No. 1 on the benchmark as of 18 Mar 2025.

See details on HelpSteer3-Preference at [https://arxiv.org/abs/2505.11475](https://arxiv.org/abs/2505.11475) and HelpSteer3-Feedback and Edit at [https://arxiv.org/abs/2503.04378](https://arxiv.org/abs/2503.04378).

Models were trained using the open-source [NeMo Aligner](https://github.com/NVIDIA/NeMo-Aligner).

HelpSteer3 is a follow-up to the [HelpSteer](https://huggingface.co/datasets/nvidia/HelpSteer) and [HelpSteer2](https://huggingface.co/datasets/nvidia/HelpSteer2) datasets.

## RM-Bench LeaderBoard

As of 24 Sep 2025, our reward models trained with HelpSteer3 are among top performing reward models on [RM-Bench](https://arxiv.org/abs/2410.16184), an improved variant of RewardBench for evaluating Reward Models in Chat, Math, Code and Safety.

**Generative RMs** 

Thinking RMs that require hundreds/thousands of generated tokens (>10 seconds/sample)

| Model  |  Chat | Math | Code | Safety | Easy | Normal | Hard | Overall RM-Bench|
|:-----------------------------|:------|:------|:------|:------|:------|:------|:------|:------|
|**[Qwen3-Nemotron-32B-GenRM-Principle](https://huggingface.co/nvidia/Qwen3-Nemotron-32B-GenRM-Principle)** | 80.4 | 92.0 | 77.0 | 95.5 | 88.9 | 86.4 | 83.4 |**86.2** | 
|[Llama-3_3-Nemotron-Super-49B-GenRM](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-GenRM) | 73.7 |	91.4 |	75.0 |	90.6 |	91.2 |	85.7 |	71.2 |	82.7 | 
|[RewardAnything-8B-v1](https://huggingface.co/WisdomShell/RewardAnything-8B-v1) | 76.7 | 90.3 | 75.2 | 90.2 | 85.6 | 82.2 | 81.5 | 83.1 | 
|[RM-R1-DeepSeek-Distilled-Qwen-32B](https://huggingface.co/gaotang/RM-R1-DeepSeek-Distilled-Qwen-32B) | 74.2 | 	91.8 | 74.1 | 95.4 | 89.5 | 85.4 | 76.7 | 83.9 |
|[R3-QWEN3-14B-LORA-4K](https://huggingface.co/rubricreward/R3-Qwen3-14B-LoRA-4k) | 76.5 | 92.4 | 78.7 | 91.9 | 91.4 |  86.2 | 77.1 | 84.9 |

**Scalar RMs**

Fast RMs that require 1 generated token worth of compute (<0.1 second/sample)

| Model  |  Chat | Math | Code | Safety | Easy | Normal | Hard | Overall RM-Bench|
|:-----------------------------|:------|:------|:------|:------|:------|:------|:------|:------|
| **[Llama-3.3-Nemotron-70B-Reward-Principle](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Reward-Principle/)**  | 85.3 | 81.9 | **70.4** | **96.9** | 85.5 | **84.9** | **80.5**	| **83.6** |
| **[Llama-3.3-Nemotron-70B-Reward-Multilingual](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Reward-Multilingual/)**  | **86.2** | 82.4 | 66.8 | 94.1 | 86.5 | 85.4 | 80.0	| 82.4 |
| **[Llama-3.3-Nemotron-70B-Reward](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Reward)**  |75.4 | **84.5** | 69.3 | 90.4 | 92.1 | **85.7** |71.1 | 79.9|
| [Llama-3.1-Nemotron-70B-Reward](https://huggingface.co/nvidia/Llama-3.1-Nemotron-70B-Reward) | 70.7 | 64.3 | 57.4 | 90.3 | **92.2** | 76.8 | 48.0 | 70.7 |
| [Skywork-Reward-Gemma-2-27B](https://huggingface.co/Skywork/Skywork-Reward-Gemma-2-27B) | 71.8 | 59.2 | 56.6 | 94.3 | 89.6 | 75.4 | 50.0 | 70.5 |
| [Skywork-Reward-Llama-3.1-8B](https://huggingface.co/Skywork/Skywork-Reward-Llama-3.1-8B)  | 69.5 | 60.6 |  54.5 |95.7 | 89.0 | 74.7 | 46.6 | 70.1 | 


*Note that Skywork-Reward-Llama-3.1-8B was the best performing reward model reported on RM-Bench and we evaluated all other models. * 

## JudgeBench LeaderBoard

As of 24 Sep 2025, reward models trained with HelpSteer3 are the top performing models on [JudgeBench](https://huggingface.co/spaces/ScalerLab/JudgeBench), a popular benchmark for evaluating LLM-as-a-judge applications relating to General Knowledge, Logical Reasoning, Math and Coding.

**Generative RMs**

Thinking RMs that require hundreds/thousands of generated tokens (>10 seconds/sample)

| Model  |  Knowl.| Reason.| Math | Code | Overall JudgeBench |
|:-----------------------------|:------|:------|:------|:------|:------|
| **[Qwen3-Nemotron-32B-GenRM-Principle](https://huggingface.co/nvidia/Qwen3-Nemotron-32B-GenRM-Principle)** | 74.6 | 85.7 | 85.7 | 90.5 | **81.4** |
| [Llama-3_3-Nemotron-Super-49B-GenRM](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-GenRM) | 71.4 |	73.5 |	87.5	| 76.2 |	75.1 |
| [RewardAnything-8B-v1](https://huggingface.co/WisdomShell/RewardAnything-8B-v1) | 61.0 |  57.1 | 73.2 | 66.7 | 62.6 |
| [RM-R1-DeepSeek-Distilled-Qwen-32B](https://huggingface.co/gaotang/RM-R1-DeepSeek-Distilled-Qwen-32B) | 56.5 | 66.3 | 85.7 | 73.8 | 66.0|
| [R3-QWEN3-14B-LORA-4K](https://huggingface.co/rubricreward/R3-Qwen3-14B-LoRA-4k) | 50.0 | 64.3 | 76.8 | 71.4 | 60.9 | 

**Scalar RMs**

Fast RMs that require 1 generated token worth of compute (<0.1 second/sample)

| Model  |  Knowl.| Reason.| Math | Code | Overall JudgeBench |
|:-----------------------------|:------|:------|:------|:------|:------|
| **[Llama-3.3-Nemotron-70B-Reward-Principle](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Reward-Principle)**  |**74.0** |74.5 | 82.1 | **81.0** |**76.3** |
| **[Llama-3.3-Nemotron-70B-Reward](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Reward)**  | 70.8 |**76.5** | 82.1 | **66.7** |73.7 |
| **[Llama-3.3-Nemotron-70B-Reward-Multilingual](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Reward-Multilingual)**  |66.2 | 71.4 | 82.1 |59.5 | 69.4|
| [Llama-3.1-Nemotron-70B-Reward](https://huggingface.co/nvidia/Llama-3.1-Nemotron-70B-Reward) |62.3 | 72.5 | 76.8 | 57.1 | 66.9 |
| [Skywork-Reward-Gemma-2-27B](https://huggingface.co/Skywork/Skywork-Reward-Gemma-2-27B) |  59.7 | 66.3 | **83.9** | 50.0	| 64.3 |
| [Skywork-Reward-Llama-3.1-8B](https://huggingface.co/Skywork/Skywork-Reward-Llama-3.1-8B) | 59.1 | 64.3 |  76.8 | 50.0 | 62.3 |


*Note that Skywork-Reward-Llama-3.1-27B was the best performing reward model reported on JudgeBench and we evaluated all other numbers.* 

## Arena Hard LeaderBoard

As of 18 Mar 2025, augmenting models with the Feedback-Edit Inference Time Scaling (ITS) approach leads to the highest performance on Arena Hard.

The Feedback-Edit Inference Time Scaling system comprise of the following models:

1. [Llama-3.3-Nemotron-70B-Feedback](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Feedback)
2. [Llama-3.3-Nemotron-70B-Edit](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Edit)
3. [Llama-3.3-Nemotron-70B-Select](https://huggingface.co/nvidia/Llama-3.3-Nemotron-70B-Select)


| Model  | Arena Hard (95% CI) |
|:-----------------------------|:----------------|
| [Llama 3.3 Nemotron Super 49B v1](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1) + **Feedback-Edit ITS** | **93.4 (-1.1, 1.0)** |
| [Llama-3.1-Nemotron-70B-Instruct](https://huggingface.co/nvidia/Llama-3.1-Nemotron-70B-Instruct) + **Feedback-Edit ITS** | 92.7 (-1.2, 0.9) |
| o1-mini-2024-09-12          | 92.0 (-1.2, 1.0)  |
| o1-preview-2024-09-12         | 90.4 (-1.1, 1.3)  |
| [Llama 3.3 Nemotron Super 49B v1](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1) | 88.3 (-1.6, 1.6) |
| claude-3-5-sonnet-20241022     | 85.2 (-1.4, 1.6) |
| [Llama-3.1-Nemotron-70B-Instruct](https://huggingface.co/nvidia/Llama-3.1-Nemotron-70B-Instruct) | 84.9 (-1.7, 1.8) |


## Preference

HelpSteer3 contains 40,476 preference samples, each containing a domain, language, context, two responses, an overall preference score between the responses as well as individual preferences from up to 3 annotators. Each individual preference contains a preference score in addition to a concise reasoning for their preference in 1-2 sentences. Data is split into 95% train and 5% validation.

**Domain** In HelpSteer3, we collected data spanning four domains: General, STEM, Code and Multilingual. The first three domains were annotated by Scale AI while the last domain was annotated by Translated.

**Language** For Code domain, language refers to the programming language while for the Multilingual domain, it refers to the natural language. In other domains, this field will be English. Please note that the Code domain only includes prompts in English while the Multilingual domain does not contain any Code prompts.

**Context** Many of the samples in HelpSteer3 contain multi-turn prompts, hence the context field which is in a form that is compatible with the OpenAI ChatCompletion Message object.

**Preference Score** Integer from -3 to 3, corresponding to:

-3: Response 1 is much better than Response 2

-2: Response 1 is better than Response 2

-1: Response 1 is slightly better than Response 2

0: Response 1 is about the same as Response 2

1: Response 2 is slightly better than Response 1

2: Response 2 is better than Response 1

3: Response 2 is much better than Response 1


**Single-Turn Example**

```json
{
    "domain": "code",
    "language": "javascript_html_css",
    "context": [
        {
            "role": "user",
            "content": "Write a JavaScript program that reads a string of text from the keyboard and performs some very basic encryption on this string. First, the order of the words in the string should be reversed. Second, the order of the letters within each word should be reversed. Finally, the first letter of each word should be inserted between each pair of letters to generate the output string.\nWhen the encryption processing has been completed for the entire input string, the program should print the whole encrypted string back to the user on the screen.\nYou can assume that the maximum number of words in the input stream will be 20.\nAfter the encrypted string has been printed to screen, the program should stop."
        }
    ],
    "response1": "Here's a JavaScript program that meets your requirements. This program uses the `readline-sync` module to read input from the keyboard. Make sure to install it by running `npm install readline-sync` before executing the code.\n\n```javascript\nconst readlineSync = require('readline-sync');\n\nfunction encryptString(inputString) {\n const words = inputString.split(' ').reverse();\n let encryptedString = '';\n\n for (let i = 0; i < words.length; i++) {\n    const word = words[i];\n    const reversedWord = word.split('').reverse().join('');\n\n    for (let j = 0; j < reversedWord.length - 1; j++) {\n      encryptedString += reversedWord[j] + reversedWord[0];\n    }\n\n    encryptedString += reversedWord[reversedWord.length - 1];\n\n    if (i < words.length - 1) {\n      encryptedString += ' ';\n    }\n  }\n\n  return encryptedString;\n}\n\nconst inputString = readlineSync.question('Please enter a string of text (max 20 words): ');\n\nif (inputString.split(' ').length > 20) {\n console.log('Error: The input string contains more than 20 words.');\n process.exit(1);\n}\n\nconst encryptedString = encryptString(inputString);\nconsole.log(`Encrypted string: ${encryptedString}`);\n```\n\nThis program reads a string from the keyboard, checks if it has more than 20 words, and then encrypts the string according to the specified rules. Finally, it prints the encrypted string to the screen.",
    "response2": "```javascript\nconst readline = require('readline');\n\nconst rl = readline.createInterface({\n  input: process.stdin,\n  output: process.stdout\n});\n\nrl.question('Enter a string of text: ', (inputString) => {\n  const words = inputString.split(' ');\n  const reversedWords = words.reverse();\n  const encryptedWords = reversedWords.map(word => word.split('').reverse().join(''));\n  let encryptedString = '';\n\n  for (let i = 0; i < encryptedWords.length; i++) {\n    encryptedString += encryptedWords[i].charAt(0) + encryptedWords[i].substring(1);\n    if (i < encryptedWords.length - 1) {\n      encryptedString += ' ';\n    }\n  }\n\n  console.log('Encrypted string:', encryptedString);\n  rl.close();\n});\n```\n\n**Explanation:**\n\n1. **Input:**\n   - The code uses the `readline` module to read input from the user.\n   - `rl.question()` prompts the user to enter a string and stores it in the `inputString` variable.\n\n2. **Word Reversal:**\n   - `inputString.split(' ')` splits the input string into an array of words based on spaces.\n   - `words.reverse()` reverses the order of words in the array.\n\n3. **Letter Reversal:**\n   - `reversedWords.map(word => ...)` iterates through each word in the reversed array and applies a function to transform it.\n   - Inside the function:\n     - `word.split('')` splits each word into an array of individual letters.\n     - `reverse()` reverses the order of letters in the array.\n     - `join('')` joins the reversed letters back into a string.\n\n4. **Encryption:**\n   - `encryptedString` is initialized as an empty string to store the encrypted result.\n   - The code iterates through the `encryptedWords` array.\n   - For each word:\n     - `encryptedWords[i].charAt(0)` gets the first letter of the word.\n     - `encryptedWords[i].substring(1)` gets the rest of the letters in the word.\n     - These are concatenated and added to `encryptedString`.\n     - A space is added after each word except the last one.\n\n5. **Output:**\n   - `console.log('Encrypted string:', encryptedString)` prints the final encrypted string to the console.\n   - `rl.close()` closes the readline interface, ending the program.\n\n\n\nLet me know if you have any other questions.",
    "overall_preference": -2,
    "individual_preference": [
        {
            "score": -1,
            "reasoning": "@Response 1 is slightly better than @Response 2. @Response 1 needs some improvements but is closer to the expected result than @Response 2. "
        },
        {
            "score": -3,
            "reasoning": "@Response 1 is much better than @Response 2 because it accurately and thoroughly followed the instruction, providing a complete solution for encrypting a string."
        },
        {
            "score": -2,
            "reasoning": "@Response 1 is better than @Response 2 because the former fully addressed the prompt's requirements with a possibility of minor improvements, whereas @Response 2 missed a part in the requirement of the prompt."
        }
    ]
}
```

**Multi-Turn Example**

```json
{
    "domain": "code",
    "language": "python",
    "context": [
        {
            "role": "user",
            "content": "lets do python coding"
        },
        {
            "role": "assistant",
            "content": " def greet(name):\n      return f\"Hello, {name}!\"\n\nprint(greet(\"Alice\"))\n# Output: Hello, Alice!\n\ndef add(a, b):\n    return a + b\n\nprint(add(3, 4))\n# Output: 7\n\ndef is_even(number):\n    return number % 2 == 0\n\nprint(is_even(5))\n# Output: False\n\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n\nprint(factorial(5))\n# Output: 120\n```"
        },
        {
            "role": "user",
            "content": "First of all, in this scenario, two programmers are collaborating. Programmer A can do as much work as a per day, and programmer B can do as much work as b. Two programmers always finish n (=a+b) jobs a day. The first input given are three numbers, n a b respectively, separated by spaces. So make the code that gets the three inputs.\n"
        },
        {
            "role": "assistant",
            "content": "7 2\n\nHere's the Python code that solves the problem:\n\n```python\ndef work_rate(a, b):\n    return a / (a + b)\n\ndef jobs_per_day(work_rate):\n    return 1 / work_rate\n\ndef main():\n    n, a, b = map(int, input().split())\n    \n    work_rate_ab = work_rate(a, b)\n    jobs_per_day_ab = jobs_per_day(work_rate_ab)\n    \n    print(jobs_per_day_ab)\n\nmain()\n```\n\nThis code first defines a function `work_rate(a, b)` that calculates the combined work rate of programmers A and B. Then, it defines a function `jobs_per_day(work_rate)` that calculates the number of jobs they can complete in a day based on their combined work rate.\n\nIn the `main()` function, we read the input values `n`, `a`, and `b` from the user, and then calculate and print the number of jobs that can be completed in a day by both programmers working together."
        },
        {
            "role": "user",
            "content": "Continuing the above, the work we've received has a level of complexity. Since programmer A likes to perform complex tasks, and programmer B likes to perform simple tasks, they divide the tasks by setting the appropriate integer x. If the complexity is greater than x, then that work will be given to A. And if the complexity is less than x, then that work will be given to B. The program has to find the possible number of x that allows each person to perform exactly the number of tasks of a and b.\nFor an example, if a=2 and b=3, and the complexity of work is 1,1,1,4,4, then the possible x is 2 or 3. So the output will be 2. \nFor another example, if n=5, a=2 and b=3, and the complexity of work is 6,2,3,100,1, then the possible x is 4 or 5. So the output will be 2."
        },
        {
            "role": "assistant",
            "content": "5\n\nHere's the Python code that solves the problem:\n\n```python\ndef find_possible_x(n, a, b, complexities):\n    count = 0\n    for x in range(1, n+1):\n        a_count = sum(1 for c in complexities if c > x)\n        b_count = sum(1 for c in complexities if c <= x)\n        if a_count == a and b_count == b:\n            count += 1\n    return count\n\nn, a, b = map(int, input().split())\ncomplexities = list(map(int, input().split()))\n\nprint(find_possible_x(n, a, b, complexities))\n```\n\nThis code defines a function `find_possible_x(n, a, b, complexities)` that takes the input values `n`, `a`, `b`, and a list of `complexities`. It then iterates through all possible values of `x` from 1 to `n`, and for each value of `x`, it counts the number of tasks that can be assigned to programmer A and programmer B based on the given complexities.\n\nFinally, the code reads the input values `n`, `a`, `b`, and `complexities` from the user, and then calculates and prints the number of possible values of `x` that satisfy the given conditions."
        },
        {
            "role": "user",
            "content": "At the \"tasks_B = [task for task in tasks if task &lt;= x]\", can you fix &lt;= sign to &lt; ?"
        }
    ],
    "response1": "Yes, you are correct. The correct comparison operator should be `<` instead of `<=`. Here's the corrected code:\n\n```python\ndef find_possible_x(n, a, b, complexities):\n    count = 0\n    for x in range(1, n+1):\n        a_count = sum(1 for c in complexities if c > x)\n        b_count = sum(1 for c in complexities if c < x)\n        if a_count == a and b_count == b:\n            count += 1\n    return count\n\nn, a, b = map(int, input().split())\ncomplexities = list(map(int, input().split()))\n\nprint(find_possible_x(n, a, b, complexities))\n```\n\nThank you for pointing out the mistake.",
    "response2": "Sure! Here's the updated line of code with `<` instead of `<=`:\n\n```python\ntasks_B = [task for task in tasks if task < x]\n```\n\nThis change means that tasks with a complexity equal to `x` will no longer be assigned to programmer B.",
    "overall_preference": -2,
    "individual_preference": [
        {
            "score": -2,
            "reasoning": "@Response 1 is better than @Response 2 because @Response 1 provides a full code example, integrating the required change directly into the main function, making it immediately usable for the user. @Response 2, while technically correct, only addresses part of the problem by showing a single line change without embedding it into the overall code, leaving more work for the user to complete the solution."
        },
        {
            "score": -2,
            "reasoning": "@Response 1 is better than @Response 2. This is because it provides the complete corrected code and addresses the main idea of the prompt, even though it mistakenly apologizes for saying the comparison should be '<' instead of '<='.  In comparison, @Response 2 only shows one line of code and does not modify the original code to fit what the user wants, making it less helpful for understanding the complete code."
        },
        {
            "score": -2,
            "reasoning": "@Response 1 is better than @Response 2 because it was able to address the prompt's request accurately and the code was working as expected to output value as stated in the prompt."
        }
    ]
}
```



## Feedback

HelpSteer3-Feedback contains 40,821 samples, each containing a domain, language, context, and two responses (see Preference section for details). In addition, each response was annotated with up to 3 instances of feedback elaborating upon the overall helpfulness of the response. Annotators are asked to provide feedback of 2-10 sentences (50 - 250 words) that starts with 'The response is \{not / slightly / partially / mostly / perfectly\} helpful'. Data is split into 95% train and 5% validation.

While annotators are generally free to write any feedback regarding the helpfulness of responses, we reminded the annotators of a few specific aspects that are important but possibly missed. For Multilingual data, we specifically encourage the annotators to provide feedback if the response language is not the same as the prompt language or the language the user expects the output in (e.g. for translation/language-learning tasks). For Coding data, we encourage the annotators to provide feedback on whether there are sufficient comments to describe the code and whether code follows best practices recommended by [Google Style Guides](https://google.github.io/styleguide/).


**Example**

```json
{
    "domain": "code",
    "language": "javascript_html_css",
    "context": [
        {
            "role": "user",
            "content": "Write a JavaScript program that reads a string of text from the keyboard and performs some very basic encryption on this string. First, the order of the words in the string should be reversed. Second, the order of the letters within each word should be reversed. Finally, the first letter of each word should be inserted between each