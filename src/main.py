import sys

import Controller
import install_models
import mic

if __name__ == "__main__":
    tts, chatbot, comparator = install_models.install_models()
    if tts is None:
        print("ERROR[TTS error]")
        sys.exit(1)

    controller = Controller.Controller(tts, chatbot, comparator)
    stop_listening = mic.setup_mic(controller.get_response)

    print(
        "Write '!!QUIT' or Ctrl+C to exit. Else write your sentences that you don't want to say out loud\n"
    )
    try:
        while True:
            sentence = input(">> ")
            if sentence == "!!QUIT":
                print("LOG[Quitting...]")
                break
            controller.get_response(sentence, out_loud=False)
    except KeyboardInterrupt:
        print("LOG[Stopping...]")

    stop_listening(True)
