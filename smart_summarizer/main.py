from speech_recorder import start_transcription
from notepad import append_note, get_transcript
from summarizer import summarize_transcript
import threading

def update_summary_periodically(interval=30):
    import time
    while True:
        transcript = get_transcript()
        summary = summarize_transcript(transcript)
        print("\nSummary Bullets:\n" + summary)
        time.sleep(interval)

if __name__ == "__main__":
    # Start transcription in a background thread
    t1 = threading.Thread(target=start_transcription, daemon=True)
    t1.start()

    # Periodically fetch updated summary
    update_summary_periodically()
