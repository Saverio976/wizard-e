import causal
import to_speech
import config

from TTS.api import TTS

AVAILABLE_MODE = ["live", "confirm-before", "in-confirm-before", "sleep"]

class Controller:
    def __init__(self, tts: TTS):
        self._tts = tts
        self._currentMode = AVAILABLE_MODE[0]
        self._savedResponse = ""

        self._actions = [
            self.action__change_mode,
            self.action__clear_chatbot,
        ]

    def speak(self, text: str):
        to_speech.to_speech(text, self._tts)

    def speak_voice_off(self, text: str):
        to_speech.to_speech(text, self._tts, speaker="male-en-2")

    def chatbot_gen_response(self, text: str):
        rep = causal.get_response(text)
        if config.DEBUG:
            print(f"Response: {rep}")
        if rep == "" or rep is None:
            return
        self.speak(rep)

    def chatbot_clear_msg_history(self):
        causal.clear_history()

    def get_response(self, text: str):
        if config.DEBUG:
            print(f"Understood: {text}")
        if self._currentMode == "sleep":
            self.action__sleep_mode(text)
            return
        for action in self._actions:
            if action(text) == True:
                return
        if self._currentMode == "live":
            self.chatbot_gen_response(text)
        elif self._currentMode == "confirm-before":
            self.speak(f"Understood: {text}.")
            self.speak("Is this correct? Respond with 'yes' or 'no'.")
            self._currentMode = "in-confirm-before"
            self._savedResponse = text
        elif self._currentMode == "in-confirm-before":
            if "yes" in text.lower().strip().split():
                self.speak("Okay. Processing...")
                self.chatbot_gen_response(self._savedResponse)
                self._savedResponse = ""
            elif text.lower() == "no":
                self.speak("Okay. You can ask again.")
                self._currentMode = "confirm-before"
            else:
                self.speak("I don't understand.")
                self._currentMode = "confirm-before"
                self._savedResponse = ""

    def action__change_mode(self, text: str) -> bool:
        if self._currentMode == "in-change-mode":
            if "live" in text.lower().strip().split():
                self._currentMode = "live"
                self.speak_voice_off("Live mode activated.")
                return True
            elif "confirm before" in text.lower().strip():
                self._currentMode = "confirm-before"
                self.speak_voice_off("Confirm before mode activated.")
                return True
            else:
                self.speak_voice_off("I don't understand the mode to switch in.")
                self.speak_voice_off("Possibilities: 'live', 'confirm before'")
                return True
        if self._currentMode not in ["live", "confirm-before"]:
            return False
        if "change mode" in text.lower().strip() or \
            "switch mode" in text.lower().strip():
            self._currentMode = "in-change-mode"
            self.speak_voice_off("You can select one of this two mode: 'live' or 'confirm before'.")
            return True
        return False

    def action__clear_chatbot(self, text: str) -> bool:
        if self._currentMode == "in-change-mode":
            if "yes" in text.lower().strip().replace(".,", "").split():
                self.chatbot_clear_msg_history()
                self._currentMode = self._oldMode
                self.speak_voice_off("Chatbot message history cleared.")
                return True
            elif "no" in text.lower().strip().replace(".,", "").split():
                self.speak_voice_off("Requests cancelled.")
                self._currentMode = self._oldMode
                return True
            else:
                self.speak_voice_off("Do you want to clear history of chat? Respond with 'yes' or 'no'.")
                return True
        if self._currentMode not in ["live", "confirm-before"]:
            return False
        if "clear history" in text.lower().strip():
            self._oldMode = self._currentMode
            self._currentMode = "in-clear-history"
            self.speak_voice_off("Do you want to clear history of chat? Respond with 'yes' or 'no'.")
            return True
        return False

    def action__sleep_mode(self, text: str) -> bool:
        if self._currentMode == "sleep":
            if "sleep disabled" in text.lower().strip().replace(".,", "") or \
                "sleep mode disabled" in text.lower().strip().replace(".,", "") or \
                "sleep disable" in text.lower().strip().replace(".,", "") or \
                "sleep mode disable" in text.lower().strip().replace(".,", ""):
                self._currentMode = self._oldMode
                self.speak_voice_off(f"Sleep mode disabled. {self._currentMode} mode activated.")
                return True
            return True
        if self._currentMode == "in-sleep":
            if "yes" in text.lower().strip().replace(".,", "").split():
                self._currentMode = "sleep"
                self.speak_voice_off("Sleep mode activated.")
                return True
            elif "no" in text.lower().strip().replace(".,", "").split():
                self._currentMode = self._oldMode
                self.speak_voice_off("Requests cancelled.")
                return True
            else:
                self.speak_voice_off("Do you want to enable sleep mode? Respond with 'yes' or 'no'.")
                return True
        if self._currentMode not in ["live", "confirm-before"]:
            return False
        if "sleep enabled" in text.lower().strip().replace(".,", "") or \
            "sleep mode enabled" in text.lower().strip().replace(".,", "") or \
            "sleep enable" in text.lower().strip().replace(".,", "") or \
            "sleep mode enable" in text.lower().strip().replace(".,", ""):
            self._oldMode = self._currentMode
            self._currentMode = "in-sleep"
            self.speak_voice_off("Do you want to enable sleep mode? Respond with 'yes' or 'no'.")
            return True
        return False
