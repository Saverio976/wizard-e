from typing import Union, Optional, List
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import config

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Chatbot:
    def __init__(self, instruction: Optional[str] = None, knowledge: Optional[str] = None, dialog: Optional[List[str]] = None):
        self._tokenizer = AutoTokenizer.from_pretrained(config.CAUSAL_MODEL_USED)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(config.CAUSAL_MODEL_USED)
        if instruction is None:
            instruction = config.CHATBOT_DEFAULT_INSTRUCTION
        self._instruction = instruction
        if knowledge is None:
            knowledge = config.CHATBOT_DEFAULT_KNOWLEDGE
        self._knowledge = knowledge
        if dialog is None:
            dialog = config.CHATBOT_DEFAULT_DIALOG
        self._dialog = dialog

    def __generate(self):
        if self._knowledge != '':
            knowledge = '[KNOWLEDGE] ' + self._knowledge
        else:
            knowledge = ""
        dialog = ' EOS '.join(self._dialog)
        query = f"{self._instruction} [CONTEXT] {dialog} {knowledge}"
        input_ids = self._tokenizer(f"{query}", return_tensors="pt").input_ids
        outputs = self._model.generate(
            input_ids,
            max_length=128,
            min_length=8,
            top_p=0.9,
            do_sample=True
        )
        output = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return output

    def get_response(self, text: str) -> Union[str, None]:
        self._dialog.append(f"Your friend: {text}")
        response = self.__generate()
        if response == "" or response is None:
            self._dialog.append(f"You: ...")
            return None
        self._dialog.append(f"You: {response}")
        return str(response)

    def clear_history(self):
        self._dialog = []
