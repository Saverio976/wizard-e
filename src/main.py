import threading
import queue

import whisper
import mic

# record ambient audio
audio_queue = queue.Queue()
thread_recorder = threading.Thread(
    target=mic.record_audio,
    kwargs={
        'audio_queue': audio_queue,
        'energy': 300,
        'pause': 0.8,
        'dynamic_energy': True,
    },
)

# transcribe audio recorded
result_queue = queue.Queue()
audio_model = whisper.load_model("small")
thread_transcriber = threading.Thread(
    target=mic.transcribe_forever, 
    kwargs={
        'audio_queue': audio_queue, 
        'result_queue': result_queue,
        'audio_model': audio_model,
    },
)

thread_recorder.start()
thread_transcriber.start()

print("Waiting for transcription...")
try:
    while True:
        result = result_queue.get()
        print(result["text"])
except KeyboardInterrupt:
    mic.end_mic()

thread_recorder.join()
thread_transcriber.join()
