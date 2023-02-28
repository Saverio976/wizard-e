from TTS.api import TTS
import sounddevice

def to_speech(text: str, tts: TTS, speaker: str = "female-en-5"):
    if tts.speakers is None or tts.languages is None:
        print("Model have not speakers or/and language")
        return
    if "en" not in tts.languages:
        print("Model have not english language")
        return
    if speaker not in tts.speakers:
        print(f"Model have not {speaker} speaker")
        print(f"Available speakers: {tts.speakers}")
        return
    wav = tts.tts(text=text, speaker=speaker, language="en")
    sounddevice.play(
        wav,
        blocking=True,
        samplerate=19000
    )
