from typing import Optional, Tuple

from Controller import Controller
from plugins.BasePlugin import BasePlugin
from plugins.ControllerMode import ControllerMode


class ChangeMode(BasePlugin):
    def __init__(self):
        super().__init__(
            "change_current_mode",
            "Change the current mode of the controller",
        )
        self.in_confirmation = False
        self.mode_to_switch = ControllerMode.CONFIRM_BEFORE
        self.mode_before = ControllerMode.CONFIRM_BEFORE

    def action_in_confirmation(
        self, controller: Controller, text: str
    ) -> Tuple[bool, bool]:
        texts = text.lower().strip().replace(".,;?!:", " ").split()
        if "yes" in texts:
            self.in_confirmation = False
            self.mode_before = controller.currentMode
            controller.currentMode = self.mode_to_switch
            controller.speak_voice_off(f"Switched to mode {self.mode_to_switch.name}")
            return True, False
        elif "no" in texts:
            self.in_confirmation = False
            controller.speak_voice_off("Cancelled")
            return True, False
        else:
            controller.speak_voice_off("Please say 'yes' or 'no'")
            return True, True

    def find_mode_to_switch(
        self, text: str, controller: Controller
    ) -> Tuple[str, Optional[ControllerMode]]:
        texts = text.lower().strip().replace(".,;?!:", " ").split()
        if "mode" not in texts:
            return "", None
        texts = texts[texts.index("mode") + 1 :]
        possibilities = {
            "no confirm": [0.0, ControllerMode.NO_CONFIRM],
            "confirm before": [0.0, ControllerMode.CONFIRM_BEFORE],
            "sleep": [0.0, ControllerMode.SLEEP],
        }
        text = " ".join(texts)
        for key in possibilities.keys():
            possibilities[key][0] = controller.comparator.estimate_correlation(
                key, text
            )
        max_correlation = max(
            possibilities.keys(), key=lambda key: possibilities[key][0]
        )
        return max_correlation, possibilities[max_correlation][1]

    def exec(self, controller: Controller, text: str) -> Tuple[bool, bool]:
        if controller.currentMode == ControllerMode.SLEEP:
            text = text.lower().strip().replace(",?;.:/!", " ")
            if (
                "sleep disable" in text
                or "sleep off" in text
                or "sleep mode disable" in text
                or "sleep mode off" in text
            ):
                controller.currentMode = self.mode_before
                controller.speak_voice_off("Sleep mode disabled")
                return True, False
            return False, False
        if self.in_confirmation:
            return self.action_in_confirmation(controller, text)
        change_mode_sentence = "change mode"
        if controller.comparator.estimate_correlation(text, change_mode_sentence) > 0.8:
            mode_text, mode_value = self.find_mode_to_switch(text, controller)
            if mode_value is None:
                controller.speak_voice_off("I don't understand mode")
                return True, False
            self.in_confirmation = True
            self.mode_to_switch = mode_value
            controller.speak_voice_off(f"mode to switch to: {mode_text}")
            controller.speak_voice_off(f"Is this correct? Respond with 'yes' or 'no'")
            return True, True
        return False, False
