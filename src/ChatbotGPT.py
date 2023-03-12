import os
from typing import List, Optional, Union

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from transformers import pipeline

import config


class Chatbot:
    def __init__(self, dialog: Optional[List[str]] = None):
        self._pipe = pipeline(model=config.CAUSAL_MODEL_USED_GPT)
        if dialog is None:
            dialog = config.CHATBOT_DEFAULT_DIALOG
        self._dialog = dialog

    def __generate(self):
        dialog = "\n".join(self._dialog) + "\n<bot>:"
        text = self._pipe(dialog)
        print(text)
        return None

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
