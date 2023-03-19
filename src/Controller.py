# from TTS.api import TTS
from typing import Dict, Optional

import pyttsx3

import config
import to_speech
from ChatbotGPT import Chatbot
from plugins.ControllerMode import ControllerMode
from SentenceCompare import SentenceCompare


class Controller:
    def __init__(
        self,
        engine: pyttsx3.engine.Engine,
        chatbot: Chatbot,
        comparator: SentenceCompare,
    ):
        # self.__tts = tts
        self.__engine = engine
        self.chatbot = chatbot
        self.comparator = comparator
        self.currentMode: ControllerMode = config.CONTROLER_START_MODE
        self.savedResponses = []
        self._out_loud = True

        self._plugins: Dict[str, "BasePlugin"] = {}
        self._pluginsNexts: Optional["BasePlugin"] = None

    def speak(self, text: str):
        # Speak with the voice of 'Wizard-e'
        if self._out_loud:
            to_speech.to_speech(text, self.__engine)
        else:
            print(f"Wizard-e: {text}")

    def speak_voice_off(self, text: str):
        # Speak with the voice of not 'Wizard-e'
        if self._out_loud:
            to_speech.to_speech(text, self.__engine, speaker="male-en-2")
        else:
            print(f"Assistant: {text}")

    def chatbot_gen_response(self, text: str):
        rep = self.chatbot.get_response(text)
        if config.DEBUG:
            print(f"LOG[Response: {rep}]")
        if rep == "" or rep is None:
            return
        self.speak(rep)

    def get_response(self, text: str, out_loud=True):
        self._out_loud = out_loud
        if config.DEBUG:
            print(f"LOG[Understood: {text}]")
        if self.currentMode == ControllerMode.SLEEP:
            plugin = self._plugins["change_current_mode"]
            if plugin is None:
                print("ERROR[Can't find plugin for change mode]")
                return
            plugin.exec(self, text)
            return
        if self._pluginsNexts is not None:
            is_picked, need_next = self._pluginsNexts.exec(self, text)
            if is_picked:
                print(
                    f"LOG[plugin picked (because of need_next): {self._pluginsNexts.name}]"
                )
            if need_next:
                print(f"LOG[plugin need next: {self._pluginsNexts.name}]")
                return
            else:
                self._plugsNexts = None
        for plugin in self._plugins.values():
            is_picked, need_next = plugin.exec(self, text)
            if is_picked:
                print(f"LOG[plugin picked: {plugin.name}]")
            if need_next:
                print(f"LOG[plugin need next: {plugin.name}]")
                self._pluginsNexts = plugin
                break

    def register_plugin(self, plugin) -> bool:
        # plugin: BasePlugin
        if plugin.name in self._plugins.keys():
            return False
        self._plugins[plugin.name] = plugin
        return True

from plugins.BasePlugin import BasePlugin
