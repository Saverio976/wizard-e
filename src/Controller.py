import causal
import to_speech
import config

from TTS.api import TTS

AVAILABLE_MODE = ["live", "confirm-before", "in-confirm-before"]

class Controller:
    def __init__(self, tts: TTS):
        self._tts = tts
        self._currentMode = AVAILABLE_MODE[0]
        self._savedResponse = ""

        self._actions = [
            self.action__change_mode,
        ]

    def speak(self, text: str):
        to_speech.to_speech(text, self._tts)

    def chatbot(self, text: str):
        rep = causal.get_response(text)
        if config.DEBUG:
            print(f"Response: {rep}")
        if rep == "" or rep is None:
            return
        self.speak(rep)

    def get_response(self, text: str):
        if config.DEBUG:
            print(f"Understood: {text}")
        for action in self._actions:
            if action(text) == True:
                return
        if self._currentMode == "live":
            self.chatbot(text)
        elif self._currentMode == "confirm-before":
            self.speak(f"Understood: {text}.")
            self.speak("Is this correct? Respond with 'yes' or 'no'.")
            self._currentMode = "in-confirm-before"
            self._savedResponse = text
        elif self._currentMode == "in-confirm-before":
            if "yes" in text.lower().strip().split():
                self.speak("Okay. Processing...")
                self.chatbot(self._savedResponse)
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
                self.speak("Live mode activated.")
                return True
            elif "confirm before" in text.lower().strip():
                self._currentMode = "confirm-before"
                self.speak("Confirm before mode activated.")
                return True
            else:
                self.speak("I don't understand the mode to switch in.")
                self.speak("Possibilities: 'live', 'confirm before'")
                return True
        if "change mode" in text.lower().strip() or \
            "switch mode" in text.lower().strip():
            self._currentMode = "in-change-mode"
            return True
        return False
