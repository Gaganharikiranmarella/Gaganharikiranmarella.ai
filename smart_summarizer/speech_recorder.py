import speech_recognition as sr
from notepad import append_note

def start_transcription():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("Listening... (Ctrl+C to stop)")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print("Recognized:", text)
                append_note(text)
            except Exception:
                print("Could not recognize audio.")
