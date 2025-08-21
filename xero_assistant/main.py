from xero import XEROAssistant
from av_input import AVInput
from av_output import speak, start_speech_thread, stop_speech_thread
import threading

def handle_ai_reply(xero, cmd):
    reply = xero.ask(cmd)
    print(f"XERO: {reply}")
    speak(reply)

def main():
    start_speech_thread()
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
            print("XERO: Didn't catch that. Please speak again.")
            continue

        print(f"You said: {cmd}")

        if "exit" in cmd:
            avio.running = False
            speak("Goodbye! XERO is shutting down.")
            break

        elif "capture" in cmd:
            filename = avio.save_frame()
            if filename:
                speak("Image frame has been captured.")
            continue

        print("XERO is thinking...")

        reply_thread = threading.Thread(target=handle_ai_reply, args=(xero, cmd))
        reply_thread.start()

    video_thread.join()
    audio_thread.join()
    stop_speech_thread()

if __name__ == "__main__":
    main()
