import sounddevice

import config

def to_speech(text: str, tts):
    if tts.speakers is None or tts.languages is None:
        print("Model have not speakers or/and language")
        return
    if "en" not in tts.languages:
        print("Model have not english language")
        return
    if "female-en-5" not in tts.speakers:
        print("Model have not female-en-5 speaker")
        return
    wav = tts.tts(text=text, speaker="female-en-5", language="en")
    sounddevice.play(
        wav,
        blocking=True,
        samplerate=19000
    )
