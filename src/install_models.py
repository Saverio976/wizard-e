from TTS.api import TTS
import whisper
from transformers import AutoModelForCausalLM, AutoTokenizer

import config

def install_models():
    _ = AutoTokenizer.from_pretrained(
        config.CAUSAL_MODEL_USED
    )
    _ = AutoModelForCausalLM.from_pretrained(
        config.CAUSAL_MODEL_USED
    )
    _ = whisper.load_model(
        config.OPENAI_MODEL_RECOGNIZER
    )
    if config.TTS_MODEL not in TTS.list_models():
        print("ERROR: TTS model not found")
        tts = None
    else:
        tts = TTS(config.TTS_MODEL, progress_bar=True)
    return tts
