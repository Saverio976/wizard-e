import mic
import causal
import to_speech
import threading

def get_response(text: str):
    print(f"Understood: {text}")
    rep = causal.get_response(text)
    print(f"Response: {rep}")
    if rep == "" or rep is None:
        return
    to_speech.to_speech(rep)

def func(text: str):
    threading.Thread(target=get_response, args=(text,)).run()

stop_listening = mic.setup_mic(func)

try:
    input("Press Enter to stop listening...")
except KeyboardInterrupt:
    print("Stopping...")

stop_listening(True)
