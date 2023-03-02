import sys

import whisper
from TTS.api import TTS

import Chatbot
import config


def install_models():
    if config.DEBUG:
        print("LOG[Start launching Chatbot model]")
    chatbot = Chatbot.Chatbot()
    if config.DEBUG:
        print("LOG[Finished launching Chatbot model]")
    if config.DEBUG:
        print("LOG[Start launching voice understanding model]")
    _ = whisper.load_model(config.OPENAI_MODEL_RECOGNIZER)
    if config.DEBUG:
        print("LOG[Finished launching voice understanding model]")
    if config.TTS_MODEL not in TTS.list_models():
        print("ERROR[TTS model not found]")
        tts = None
    else:
        if config.DEBUG:
            print("LOG[Start launching TTS model]")
        with open(config.TTS_LOGS_OPEN, "w") as sys.stdout:
            tts = TTS(config.TTS_MODEL, progress_bar=False)
        sys.stdout = sys.__stdout__
        if config.DEBUG:
            print("LOG[Finished launching TTS model]")
    return tts, chatbot
