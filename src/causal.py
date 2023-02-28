from typing import Union
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import config

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

TOKENIZER = AutoTokenizer.from_pretrained(config.CAUSAL_MODEL_USED)
MODEL = AutoModelForSeq2SeqLM.from_pretrained(config.CAUSAL_MODEL_USED)

def generate(instruction, knowledge, dialog):
    if knowledge != '':
        knowledge = '[KNOWLEDGE] ' + knowledge
    dialog = ' EOS '.join(dialog)
    query = f"{instruction} [CONTEXT] {dialog} {knowledge}"
    input_ids = TOKENIZER(f"{query}", return_tensors="pt").input_ids
    outputs = MODEL.generate(
        input_ids,
        max_length=128,
        min_length=8,
        top_p=0.9,
        do_sample=True
    )
    output = TOKENIZER.decode(outputs[0], skip_special_tokens=True)
    return output

# Instruction for a chitchat task
INSTRUCTION = 'Instruction: given a dialogue between you and your friend, respond empathically. Be kind to your friend. Don\'t say your name each time you respond.'
# Leave the knowldge empty
KNOWLEDGE = 'My name is Wizard-e'
DIALOG = []

def get_response(text: str) -> Union[str, None]:
    global DIALOG
    DIALOG.append(text)
    response = generate(INSTRUCTION, KNOWLEDGE, DIALOG)
    if response == "" or response is None:
        DIALOG.append("...")
        return None
    DIALOG.append(str(response))
    return str(response)

def clear_history():
    global DIALOG
    DIALOG = []
