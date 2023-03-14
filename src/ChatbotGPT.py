import os
from typing import Union

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from transformers import AutoModelForCausalLM, AutoTokenizer

import config


class Chatbot:
    def __init__(self):
        self._tokenizer = AutoTokenizer.from_pretrained(config.CAUSAL_MODEL_USED_GPT, cache_dir="./cache", resume_download=True)
        self._model = AutoModelForCausalLM.from_pretrained(config.CAUSAL_MODEL_USED_GPT)
        self._dialog = []

    def __generate(self):
        dialog = "\n".join(self._dialog)
        query = f"{dialog}\n<bot>: "
        input_ids = self._tokenizer(f"{query}", return_tensors="pt").input_ids
        outputs = self._model.generate(
            input_ids, max_length=128, min_length=8, top_p=0.9, do_sample=True
        )
        output = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return output

    def get_response(self, text: str) -> Union[str, None]:
        self._dialog.append(f"<human>: {text}")
        response = self.__generate()
        if response == "" or response is None:
            self._dialog.append(f"<bot>: ...")
            return None
        self._dialog.append(f"<bot>: {response}")
        return str(response)

    def clear_history(self):
        self._dialog = []
