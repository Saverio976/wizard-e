# https://github.com/mallorbc/whisper_mic
# (without functions that are no used for my purpose)
# you can access the true file (and the licence) in __pypackage__/whisper_mic/ (git update --recursive --init)

import whisper
import speech_recognition as sr
import queue
import torch
import numpy as np

def record_audio(audio_queue: queue.Queue, energy: int, pause: float, dynamic_energy: bool):
    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone() as source:
        print('Microphone ready to listen')
        i = 0
        while record_audio.__is_recording:
            print("You can speak now")
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio

            audio_queue.put_nowait(audio_data)
            i += 1

record_audio.__is_recording = True


def transcribe_forever(audio_queue: queue.Queue, result_queue: queue.Queue, audio_model: whisper.Whisper):
    #load the speech recognizer and set the initial energy threshold and pause threshold
    print("Starting speech recognition")
    while transcribe_forever.__is_transcribing:
        audio_data = audio_queue.get()
        result = audio_model.transcribe(audio_data, fp16=False)
        result_queue.put_nowait(result)

transcribe_forever.__is_transcribing = True

def end_mic():
    transcribe_forever.__is_transcribing = False
    record_audio.__is_recording = False
