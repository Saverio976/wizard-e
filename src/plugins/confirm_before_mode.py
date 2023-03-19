from typing import Tuple

from Controller import Controller
from plugins.BasePlugin import BasePlugin
from plugins.ControllerMode import ControllerMode


class ConfirmBeforeMode(BasePlugin):
    def __init__(self):
        super().__init__(
            "confirm_before_mode",
            "generate chatbot response after the user confirm text",
        )
        self.in_confirmation = False

    def action_in_confirmation(
        self, controller: Controller, text: str
    ) -> Tuple[bool, bool]:
        texts = text.lower().strip().replace(".,;?!:", " ").split()
        if "yes" in texts:
            self.in_confirmation = False
            controller.chatbot_gen_response(controller.savedResponses[-1])
            return True, False
        elif "no" in texts:
            self.in_confirmation = False
            controller.speak_voice_off("Cancelled")
            return True, False
        else:
            controller.speak_voice_off("Please say 'yes' or 'no'")
            return True, True

    def action_not_in_confirmation(
        self, controller: Controller, text: str
    ) -> Tuple[bool, bool]:
        self.in_confirmation = True
        controller.speak_voice_off(f"Understood text: {text}")
        controller.speak_voice_off(f"Is this correct? Respond with 'yes' or 'no'")
        return True, True

    def exec(self, controller: Controller, text: str) -> Tuple[bool, bool]:
        if controller.currentMode != ControllerMode.CONFIRM_BEFORE:
            return False, False
        if self.in_confirmation:
            return self.action_in_confirmation(controller, text)
        return self.action_not_in_confirmation(controller, text)
