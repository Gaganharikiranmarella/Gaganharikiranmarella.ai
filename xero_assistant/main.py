from xero import XEROAssistant
from av_input import listen_audio, capture_image
from av_output import speak

def main():
    xero = XEROAssistant()
    print("\n==== XERO: Your AV Personal Assistant ====")
    print("Say 'capture image' to take a photo with your webcam.")
    print("Say 'exit' or 'quit' to stop.\n")
    while True:
        user_text = listen_audio()
        if not user_text:
            continue
        if user_text.lower() in ("exit", "quit"):
            speak("Goodbye! XERO will be waiting for your next question.")
            break
        elif "capture image" in user_text.lower():
            filename = capture_image()
            if filename:
                speak("Image captured. If you want, I can analyze it or include it in our conversation.")
            continue
        reply = xero.ask(user_text)
        speak(reply)

if __name__ == "__main__":
    main()
