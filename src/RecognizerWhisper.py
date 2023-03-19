import io

import numpy as np
import soundfile as sf
import speech_recognition as sr
from transformers.utils.logging import sys
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

        if show_dict is not False:
            print("WARNING[Special recognize_whisper function, dont use `show_dict` parameter]", file=sys.stderr)
        if language is not None:
            print("WARNING[Special recognize_whisper function, dont use `language` parameter]", file=sys.stderr)
        if translate is not False:
            print("WARNING[Special recognize_whisper function, dont use `translate` parameter]", file=sys.stderr)
        if len(transcribe_options.keys()) != 0:
            print("WARNING[Special recognize_whisper function, dont use kwargs parameters]", file=sys.stderr)

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

        w: Whisper = self.whisper_model[model]
        result = w.transcribe(
            audio_array,
        )
        return str(result)
