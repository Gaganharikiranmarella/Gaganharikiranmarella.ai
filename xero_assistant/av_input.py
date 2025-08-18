import speech_recognition as sr
import cv2
import threading

class AVInput:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.last_frame = None
        self.running = True
        self.voice_command = ""
        self.command_detected = threading.Event()

    def video_stream(self):
        while self.running:
            ret, frame = self.cam.read()
            if not ret:
                continue
            self.last_frame = frame
            cv2.imshow("XERO Live Video", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC closes window
                self.running = False
                break
        self.cam.release()
        cv2.destroyAllWindows()

    def listen_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            while self.running:
                print("XERO is listening for command...")
                audio = recognizer.listen(source, phrase_time_limit=5)
                try:
                    text = recognizer.recognize_google(audio)
                    print("Heard:", text)
                    # Here, any trigger word can be used, e.g. "capture"
                    if "capture" in text.lower() or "analyze" in text.lower() or "exit" in text.lower():
                        self.voice_command = text.lower()
                        self.command_detected.set()
                        if "exit" in text.lower():
                            self.running = False
                            break
                except Exception:
                    print("Didn't catch that. Listening again...")

    def save_frame(self, filename="captured_frame.jpg"):
        if self.last_frame is not None:
            cv2.imwrite(filename, self.last_frame)
            print(f"Frame saved as {filename}")
            return filename
        return None
