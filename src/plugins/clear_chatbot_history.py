from typing import Tuple
from plugins.BasePlugin import BasePlugin
from Controller import Controller

class ClearChatbotHistory(BasePlugin):
    def __init__(self):
        super().__init__(
            "clear_chatbot_history",
            "clear chatbot history and saved response of controller"
        )
        self.in_confirmation = False

    def action_in_confirmation(self, controller: Controller, text: str) -> Tuple[bool, bool]:
        texts = text.lower().strip().replace(".,;?!:", " ").split()
        if "yes" in texts:
            self.in_confirmation = False
            controller.chatbot.clear_history()
            controller.savedResponses = []
            controller.speak_voice_off("Chatbot history cleared")
            return True, False
        elif "no" in texts:
            self.in_confirmation = False
            controller.speak_voice_off("Cancelled")
            return True, False
        else:
            controller.speak_voice_off("Please say 'yes' or 'no'")
            return True, True

    def action_not_in_confirmation(self, controller: Controller, text: str) -> Tuple[bool, bool]:
        self.in_confirmation = True
        controller.speak_voice_off(f"Understood text: {text}")
        controller.speak_voice_off(f"Is this correct? Respond with 'yes' or 'no'")
        return True, True

    def exec(self, controller: Controller, text: str) -> Tuple[bool, bool]:
        if self.in_confirmation:
            return self.action_in_confirmation(controller, text)
        if controller.comparator.estimate_correlation(text, "clear chatbot history") > 0.85:
            return self.action_not_in_confirmation(controller, text)
        return False, False
