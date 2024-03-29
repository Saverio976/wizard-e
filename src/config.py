DEBUG = True

# CAUSAL_MODEL_USED = "microsoft/GODEL-v1_1-large-seq2seq"
CAUSAL_MODEL_USED_SEQ2SEQ = "microsoft/GODEL-v1_1-base-seq2seq"
CHATBOT_DEFAULT_INSTRUCTION = (
    "Instruction: given a dialog context, you need to response empathically."
)
CHATBOT_DEFAULT_KNOWLEDGE = ""
CHATBOT_DEFAULT_DIALOG = []

CAUSAL_MODEL_USED_GPT = "togethercomputer/GPT-NeoXT-Chat-Base-20B"

CAUSAL_MODEL_PARAMS = {
    "cache_dir": "./cache",
    "resume_download": True
}

# https://github.com/openai/whisper/blob/main/model-card.md
OPENAI_MODEL_RECOGNIZER = "small.en"

OPENAI_LANGUAGE_MODEL = "english"

TTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
TTS_LOGS_OPEN = ".tts.log"

from plugins.ControllerMode import ControllerMode

CONTROLER_START_MODE = ControllerMode.NO_CONFIRM  # respond directly to user input
# CONTROLER_START_MODE = ControllerMode.CONFIRM_BEFORE # ask user to confirm before respond

SENTENCE_COMPARE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SENTENCE_COMPARE_CACHE_FOLDER = "./cache"
