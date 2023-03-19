from typing import Tuple

from Controller import Controller
from plugins.BasePlugin import BasePlugin
from plugins.ControllerMode import ControllerMode


class NoConfirmMode(BasePlugin):
    def __init__(self):
        super().__init__(
            "no_confirm_mode",
            "generate chatbot response without having to confirm text",
        )

    def exec(self, controller: Controller, text: str) -> Tuple[bool, bool]:
        if controller.currentMode != ControllerMode.NO_CONFIRM:
            return False, False
        controller.chatbot_gen_response(text)
        return True, False
