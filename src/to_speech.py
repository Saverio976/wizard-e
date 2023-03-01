from TTS.api import TTS
import sounddevice

import sys

import config

def to_speech(text: str, tts: TTS, speaker: str = "female-en-5"):
    if tts.speakers is None or tts.languages is None:
        print("ERROR[Model have not speakers or/and language]")
        return
    if "en" not in tts.languages:
        print("ERROR[Model have not english language]")
        print("ERROR[Available languages: {tts.languages}]")
        return
    if speaker not in tts.speakers:
        print(f"ERROR[Model have not {speaker} speaker]")
        print(f"ERROR[Available speakers: {tts.speakers}]")
        return
    if config.DEBUG:
        print(f"LOG[Speaker: {speaker} | Text: {text}]")
    with open(config.TTS_LOGS_OPEN, "a") as sys.stdout:
        wav = tts.tts(text=text, speaker=speaker, language="en")
    sys.stdout = sys.__stdout__
    if config.DEBUG:
        print(f"LOG[Starting to play to audio]")
    sounddevice.play(
        wav,
        blocking=True,
        samplerate=19000
    )
    if config.DEBUG:
        print(f"LOG[Finished to play to audio]")
