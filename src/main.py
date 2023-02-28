import install_models
import mic
import Controller


if __name__ == "__main__":
    tts = install_models.install_models()
    controller = Controller.Controller(tts)
    stop_listening = mic.setup_mic(controller.get_response)

    try:
        input("Press Enter to stop listening...\n")
    except KeyboardInterrupt:
        print("Stopping...")

    stop_listening(True)
