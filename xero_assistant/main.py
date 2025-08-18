from xero import XEROAssistant
from av_input import AVInput
from av_output import speak
import threading

def main():
    xero = XEROAssistant()
    avio = AVInput()
    print("\n==== XERO: Real-Time AV Assistant ====")
    print("Say 'capture' to save a frame. Say 'exit' to quit.\n")

    # Start video in a thread
    video_thread = threading.Thread(target=avio.video_stream)
    video_thread.start()
    # Start audio listening in this thread (or another)
    audio_thread = threading.Thread(target=avio.listen_audio)
    audio_thread.start()

    while avio.running:
        # Wait for a command to be detected
        avio.command_detected.wait()
        cmd = avio.voice_command
        avio.command_detected.clear()
        if "capture" in cmd:
            filename = avio.save_frame()
            if filename:
                speak("Image frame has been captured.")
        elif "analyze" in cmd:
            # You can add image analysis logic here, send it to XERO/AI, etc.
            speak("Image analysis not yet implemented.")
        elif "exit" in cmd:
            avio.running = False
            speak("Goodbye! XERO is shutting down.")
    video_thread.join()
    audio_thread.join()

if __name__ == "__main__":
    main()
