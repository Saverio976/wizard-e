import sys

import Controller
import install_models
import mic
from plugins import (change_mode, clear_chatbot_history, confirm_before_mode,
                     no_confirm_mode)

if __name__ == "__main__":
    engine, chatbot, comparator = install_models.install_models()
    if engine is None:
        print("ERROR[TTS error]")
        sys.exit(1)

    controller = Controller.Controller(engine, chatbot, comparator)

    controller.register_plugin(change_mode.ChangeMode())
    controller.register_plugin(clear_chatbot_history.ClearChatbotHistory())
    controller.register_plugin(confirm_before_mode.ConfirmBeforeMode())
    controller.register_plugin(no_confirm_mode.NoConfirmMode())

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
