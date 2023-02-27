import whisper
from transformers import AutoModelForCausalLM, AutoTokenizer

import config

_ = AutoTokenizer.from_pretrained(
    config.CAUSAL_MODEL_USED
)
_ = AutoModelForCausalLM.from_pretrained(
    config.CAUSAL_MODEL_USED
)

_ = whisper.load_model(
    config.OPENAI_MODEL_RECOGNIZER
)
