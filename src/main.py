import mic
import causal

def func(text: str):
    print(f"Understood: {text}")
    rep = causal.get_response(text)
    print(f"Response: {rep}")

stop_listening = mic.setup_mic(func)

try:
    input("Press Enter to stop listening...")
except KeyboardInterrupt:
    pass

stop_listening(True)
causal.end_session()
