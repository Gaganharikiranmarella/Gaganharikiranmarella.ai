from xero import XEROAssistant
from av_input import AVInput
from av_output import speak
import threading

def main():
    xero = XEROAssistant()
    avio = AVInput()
    print("\n==== XERO: Real-Time AV Conversational Assistant ====")
    print("Speak to XERO naturally. Say 'exit' to quit.\n")

    video_thread = threading.Thread(target=avio.video_stream)
    video_thread.start()
    audio_thread = threading.Thread(target=avio.listen_audio)
    audio_thread.start()

    while avio.running:
        avio.command_detected.wait()
        cmd = avio.voice_command
        avio.command_detected.clear()

        if not cmd:
            speak("Sorry, I didn't catch that. Could you say it again?")
            continue

        print("You said:", cmd)

        if "exit" in cmd:
            avio.running = False
            speak("Goodbye! XERO is shutting down.")
            break

        elif "capture" in cmd:
            filename = avio.save_frame()
            if filename:
                speak("Image frame has been captured.")
            continue

        # XERO responds to ALL other input!
        reply = xero.ask(cmd)
        speak(reply)

    video_thread.join()
    audio_thread.join()

if __name__ == "__main__":
    main()
