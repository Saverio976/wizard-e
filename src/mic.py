from typing import Callable

import speech_recognition as sr

import config

def _callback(recognizer: sr.Recognizer, audio):
    try:
        if config.DEBUG:
            print("LOG[Starts recognizer]")
        text = recognizer.recognize_whisper(
            audio,
            model=config.OPENAI_MODEL_RECOGNIZER,
            language=config.OPENAI_LANGUAGE_MODEL
        )
        if config.DEBUG:
            print("LOG[Finished recognizer]")
    except Exception as esc:
        print(f"ERROR[Failed recognizer: {esc}]")
        text = ""
    _callback.__func_callback(text)
    return text

def setup_mic(func_to_call: Callable[[str], None]) -> Callable[[bool], None]:
    mic = sr.Microphone()
    rec = sr.Recognizer()
    with mic as source:
        rec.adjust_for_ambient_noise(source)
    _callback.__func_callback = func_to_call
    if config.DEBUG:
        print("LOG[Launch listen in background]")
    stop_listening = rec.listen_in_background(mic, _callback, phrase_time_limit=30)
    return stop_listening
