DEBUG = True

CAUSAL_MODEL_USED = "microsoft/GODEL-v1_1-base-seq2seq"
CHATBOT_DEFAULT_INSTRUCTION = "Instruction: given a dialog context, you need to response empathically without repeting yourself"
CHATBOT_DEFAULT_KNOWLEDGE = ""
CHATBOT_DEFAULT_DIALOG = []

# https://github.com/openai/whisper/blob/main/model-card.md
OPENAI_MODEL_RECOGNIZER = "small.en"

OPENAI_LANGUAGE_MODEL = "english"

TTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
TTS_LOGS_OPEN = ".tts.log"

CONTROLER_START_MODE = "live"  # respond directly to user input
# CONTROLER_START_MODE = "confirm-before" # ask user to confirm before respond

SENTENCE_COMPARE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
