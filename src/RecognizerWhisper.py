import io

import numpy as np
import soundfile as sf
import speech_recognition as sr
import torch
from whispercpp import Whisper


class RecognizerWhisperCPP(sr.Recognizer):
    def __init__(self):
        super().__init__()

    # modification from https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py#L1460
    # use Whisper from whispercpp and not openai-whisper
    def recognize_whisper(
        self,
        audio_data,
        model="base",
        show_dict=False,
        load_options=None,
        language=None,
        translate=False,
        **transcribe_options
    ):
        """
        Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using Whisper.
        The recognition language is determined by ``language``, an uncapitalized full language name like "english" or "chinese". See the full language list at https://github.com/openai/whisper/blob/main/whisper/tokenizer.py
        model can be any of tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en. See https://github.com/openai/whisper for more details.
        If show_dict is true, returns the full dict response from Whisper, including the detected language. Otherwise returns only the transcription.
        You can translate the result to english with Whisper by passing translate=True
        Other values are passed directly to whisper. See https://github.com/openai/whisper/blob/main/whisper/transcribe.py for all options
        """

        assert isinstance(audio_data, sr.AudioData), "Data must be audio data"

        if (
            load_options
            or not hasattr(self, "whisper_model")
            or self.whisper_model.get(model) is None
        ):
            self.whisper_model = getattr(self, "whisper_model", {})
            self.whisper_model[model] = Whisper.from_pretrained(
                model, **load_options or {}
            )

        # 16 kHz https://github.com/openai/whisper/blob/28769fcfe50755a817ab922a7bc83483159600a9/whisper/audio.py#L98-L99
        wav_bytes = audio_data.get_wav_data(convert_rate=16000)
        wav_stream = io.BytesIO(wav_bytes)
        audio_array, _ = sf.read(wav_stream)
        audio_array = audio_array.astype(np.float32)

        result = self.whisper_model[model].transcribe(
            audio_array,
            language=language,
            task="translate" if translate else None,
            fp16=torch.cuda.is_available(),
            **transcribe_options
        )

        if show_dict:
            return result
        else:
            return result["text"]
