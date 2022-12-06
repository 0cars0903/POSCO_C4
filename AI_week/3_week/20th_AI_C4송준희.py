#!/usr/bin/env python
# coding: utf-8

# ## 20기 AI/Bigdata 아카데미 자연어처리 과목의 실습을 위한 견본 코드입니다.
# 
# Kaggle 링크: https://www.kaggle.com/t/beb77bf068f64c44a1fe2bccabb9ca47
# 
# 하단의 코드 블럭을 실행하여 데이터셋을 불러옵니다.
# 

# In[1]:


# 하단의 코드에서 주석(#)을 해제하고, Colab 인스턴스에 transformers 와 datasets 라이브러리를 설치합니다. PyTorch는 Colab 인스턴스에 이미 설치되어 있습니다.
get_ipython().system(' pip install datasets transformers')


# In[2]:


# 설치된 Transformers lib의 버전이 최소 4.11.0 이상인지 확인합니다.
import transformers
print(transformers.__version__)


# In[3]:


# CUDA GPU가 사용 가능한지 확인합니다.
import torch
print(torch.cuda.is_available())
device = 'cuda' if torch.cuda.is_available() else 'cpu'


# In[4]:


# Huggingface Dataset 레포지토리에서 KLUE-Ynat 데이터를 로드합니다.
from datasets import load_dataset
train_dataset = load_dataset("glue", "sst2", split="train")
val_dataset = load_dataset("glue", "sst2", split="validation")


# In[5]:


# train_dataset과 val_dataset의 크기를 확인합니다.
print(len(train_dataset))
print(len(val_dataset))


# In[6]:


# train_dataset과 val_dataset의 첫 번째 샘플을 출력합니다.
print(train_dataset[0])
print(val_dataset[0])


# Casual Language Modeling 학습을 위해 일정 길이로 나눠진 Text Chunk (텍스트 조각)이 필요합니다. 이를 위해서, 데이터셋의 모든 Text를 Tokenize 한 후 하나로 합칩니다.
# 전부 다 이어붙인 Text를 미리 정해진 길이로 나눕니다. 편집 완료된 데이터의 예시는 아래와 같습니다:
# ```
# part of text 1
# ```
# or
# ```
# end of text 1 [BOS_TOKEN] beginning of text 2
# ```
# 
# 텍스트 데이터 별로 학습시키는 것도 가능하지만, 여기서는 batch 관리를 편하게 하기 위해 일렬로 나열한 후 일정 길이 마다 잘라서 사용합니다.
# 
# 두 경우 모두 각 Token에 대해 다음 순번의 Token을 예측하는 것을 Objective Function으로 설정합니다.
# 
# 예시 코드에서는 '[bert-base-uncased](https://huggingface.co/bert-base-uncased)' 모델을 사용합니다.
# [Repository](https://huggingface.co/models?filter=causal-lm)에서 다양한 모델을 찾을 수 있습니다. 적절한 모델을 찾아 시도해보세요.

# In[7]:


model_checkpoint = 'bert-base-uncased'


# tokenizer와 model을 초기화 합니다.

# In[8]:


from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint).to(device)


# 이제 불러온 모든 Text에 대해 Tokenizer를 적용할 수 있습니다. Huggingface Datasets 라이브러리의 [`map`](https://huggingface.co/docs/datasets/package_reference/main_classes.html#datasets.Dataset.map) 메서드를 통해 데이터에 일괄적으로 전처리 함수를 적용할 수 있습니다.
# 
# 여기서는 tokenizer로 입력된 Text를 Tokenize하는 전처리 함수를 정의합니다:

# In[9]:


def tokenize_function(examples):
    new_data = [s.replace('.','') for s in examples['sentence']]
    return tokenizer(new_data)


# 그리고, 해당 전처리 함수를 `datasets` object의 모든 데이터에 적용합니다. `batched=True`로 설정하고 process를 4로 설정함으로써 처리 속도를 향상시킬 수 있습니다.
# 
# 이 과정에서 에러가 발생할 경우 process 수를 줄이거나 `batched=False`로 설정해서 다시 해보세요.
# 
# Tokenize 이후에 제출 데이터 제작을 위한 guid를 제외한 텍스트는 필요하지 않으므로, `remove_columns=['sentence','idx','label']`옵션을 통해 해당 Column을 제거합니다.

# In[10]:


tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True, num_proc=1, remove_columns=['sentence','idx','label'])
tokenized_val_dataset = val_dataset.map(tokenize_function, batched=True, num_proc=1, remove_columns=['sentence','idx','label'])
val_dataset_token_count_list = [len(t['input_ids']) for t in tokenized_val_dataset]
len(val_dataset_token_count_list)


# In[11]:


tokenized_train_dataset[0]


# In[12]:


tokenized_val_dataset[0]


# Tokenize를 끝냈으면, 텍스트를 모두 하나로 이어 이를 `block_size` 만큼의 조각으로 나눕니다. 이를 위해 `batched=True`를 활성화 한 `map` method를 한번 더 활용합니다.
# 
# `batched=True` 옵션은 입력과 출력 데이터의 개수를 다르게 지정할 수 있습니다. 이를 통해 새로운 batch dataset을 생성할 수도 있습니다.
# 
# `block_size`를 `tokenizer.model_max_length`로 설정하는 것이 일반적이나(BERT의 경우 512), GPU 자원의 한계로 인해 이를 모두 활용하지 못할 수도 있습니다. (Colab 노트북에서는 `tokenizer.model_max_length`로 설정하면 메모리가 부족할 가능성이 매우 높습니다.)
# 
# GPU 메모리 이슈가 발생할 경우, `block_size`를 128이나 더 작은 값으로 설정하고 다시 해보세요.

# In[13]:


#block_size = tokenizer.model_max_length
block_size = 128


# Batch 생성 함수를 아래와 같이 작성합니다:

# In[14]:


def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples['input_ids'])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result


# `map` 메서드의 `batch_size` 파라미터의 기본값은 1,000입니다. 즉 1,000 데이터마다 정해진 `block_size`에 맞지 않는 조그마한 데이터가 버려집니다.
# 필요에 따라 `batch_size`를 변경하는 것이 가능합니다.
# 

# In[15]:


lm_train_dataset = tokenized_train_dataset.map(
    group_texts,
    batched=True,
    batch_size=1000,
    num_proc=1,
)


# In[16]:


lm_val_dataset = tokenized_val_dataset.map(
    group_texts,
    batched=True,
    batch_size=1000,
    num_proc=1,
)


# HyperParameter를 초기화 합니다. 여기서 값을 다양하게 바꾸거나, 다양한 세팅을 시도해 보세요.
# 하단의 코드 블럭에 명시된 파라미터를 컨트롤 하여 실험하는 것으로도 충분하긴 하나, 다른 파라미터를 도입하는 것도 가능합니다.
# 
# 가능한 파라미터의 목록은 [API 문서](https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments) 를 참조하실 수 있습니다.

# In[41]:


from transformers import Trainer, TrainingArguments
model_name = model_checkpoint.split("/")[-1]
training_args = TrainingArguments(
    f"{model_name}-finetuned-gluesst2",
    evaluation_strategy = "epoch",
    learning_rate=1e-4,
    weight_decay=0.1,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    push_to_hub=False,
)


# In[42]:


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=lm_train_dataset,
    eval_dataset=lm_val_dataset,
)


# In[43]:


trainer.train()


# 학습이 끝난 Language Model을 평가합니다.

# In[44]:


import math
eval_results = trainer.evaluate()
print(f"Perplexity: {math.exp(eval_results['eval_loss']):.10f}")


# Kaggle System에 제출할 파일을 생성합니다.

# In[45]:


predicted = []
label = []
from tqdm import tqdm

torch.cuda.empty_cache()
with torch.no_grad():
    dataset_count = len(tokenized_val_dataset)
    sentence_count = 0
    idx = 1
    predicted_cache = []
    for datum in tqdm(tokenized_val_dataset):
        input_vec = torch.Tensor(datum['input_ids']).to('cuda',dtype=torch.long).unsqueeze(0)
        output = model(input_ids=input_vec)
        logits = output.logits[0]
        len_vec = len(input_vec[0])
        for i in range(len_vec-1):
            l = torch.softmax(logits[i],dim=-1)[datum['input_ids'][i+1]].item()
            predicted_cache.append(l)
        if idx < dataset_count:
            predicted_cache.append(torch.softmax(logits[-1],dim=-1)[tokenized_val_dataset[idx]['input_ids'][0]].item())
            idx += 1
        predicted.append(sum(predicted_cache)/len(predicted_cache))
        label.append(1)

        # label.append(tokenizer.decode(datum['input_ids'],skip_special_tokens=True))
        # input_vec = torch.Tensor(datum['input_ids'][:-2]).to('cuda',dtype=torch.int32).unsqueeze(0)
        # generated = model.generate(input_vec,max_length=len(input_vec[0])+1,
        #                            no_repeat_ngram_size=2)
        # predicted_word.append(tokenizer.decode(generated[0],skip_special_tokens=True))
import numpy as np
MSE = np.square(np.subtract(predicted, label)).mean()
print("MSE:{}".format(MSE))


# In[46]:


#export generated text to .csv file
import pandas

prw_df = pandas.DataFrame({"prob":predicted})
prw_df.to_csv("./result.csv",index_label='index')

l_df = pandas.DataFrame({"prob":label})
l_df.to_csv("./gold.csv",index_label='index')


# In[ ]:





# In[ ]:




