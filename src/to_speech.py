from TTS.api import TTS
import sounddevice

model_name = TTS.list_models()[0]
tts = TTS(model_name, progress_bar=True)

def to_speech(text: str):
    if tts.speakers is None or tts.languages is None:
        return
    wav = tts.tts(text=text, speaker=tts.speakers[0], language=tts.languages[0])
    sounddevice.play(
        wav,
        blocking=True,
        samplerate=19000
    )
