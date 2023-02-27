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
    model_name = TTS.list_models()[0]
    _ = TTS(model_name, progress_bar=True)
