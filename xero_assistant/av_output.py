import pyttsx3
import threading
from queue import Queue

_speech_queue = Queue()
_speech_thread = None
_speech_engine = pyttsx3.init()

def _speech_worker():
    while True:
        text = _speech_queue.get()
        if text is None:
            break  # Sentinel to exit the loop
        print("XERO (speaking):", text)
        _speech_engine.say(text)
        _speech_engine.runAndWait()
        _speech_queue.task_done()

def speak(text):
    _speech_queue.put(text)

def start_speech_thread():
    global _speech_thread
    if _speech_thread is None:
        _speech_thread = threading.Thread(target=_speech_worker, daemon=True)
        _speech_thread.start()

def stop_speech_thread():
    _speech_queue.put(None)  # Signal thread to exit
    if _speech_thread is not None:
        _speech_thread.join()
