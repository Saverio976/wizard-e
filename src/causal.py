from typing import Union
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import config

# def wraper_model_generate(inputs):
#     return TRANSFORMERS_MODEL.generate(
#         inputs,
#         max_length=1000,
#         do_sample=True,
#         top_p=0.95,
#         top_k=100,
#         temperature=0.75,
#         pad_token_id=TRANSFORMERS_TOKENIZER.eos_token_id,
#     )

TOKENIZER = AutoTokenizer.from_pretrained(config.CAUSAL_MODEL_USED)
MODEL = AutoModelForCausalLM.from_pretrained(config.CAUSAL_MODEL_USED)

CHAT_HISTORY_IDS = None

def get_response(text: str) -> Union[str, None]:
    global chat_history_ids
    response = ""
    new_user_input_ids = TOKENIZER.encode(
        text + TOKENIZER.eos_token,
        return_tensors='pt'
    )
    if CHAT_HISTORY_IDS is None:
        bot_input_ids = new_user_input_ids
    else:
        bot_input_ids = torch.cat(
            [CHAT_HISTORY_IDS, new_user_input_ids], dim=-1
        )
    chat_history_ids = MODEL.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=TOKENIZER.eos_token_id
    )
    response = str(TOKENIZER.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    ))
    if len(str(response)) < 1:
        return None
    return str(response)
