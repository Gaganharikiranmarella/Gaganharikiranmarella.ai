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
            if cv2.waitKey(1) & 0xFF == 27:  # ESC quits
                self.running = False
                break
        self.cam.release()
        cv2.destroyAllWindows()

    def listen_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            failure_count = 0
            while self.running:
                print("XERO is listening for command...")
                try:
                    audio = recognizer.listen(source, phrase_time_limit=10)
                    text = recognizer.recognize_google(audio)
                    print("Heard:", text)
                    self.voice_command = text.lower()
                    self.command_detected.set()
                    failure_count = 0
                    if "exit" in text.lower():
                        self.running = False
                        break
                except sr.UnknownValueError:
                    failure_count += 1
                    self.voice_command = ""
                    self.command_detected.set()
                    if failure_count >= 2:
                        print("XERO: Didn't catch that. Please speak again.")
                    continue
                except sr.RequestError as e:
                    print(f"Recognition error: {e}")
                    self.voice_command = ""
                    self.command_detected.set()
                    continue

    def save_frame(self, filename="captured_frame.jpg"):
        if self.last_frame is not None:
            cv2.imwrite(filename, self.last_frame)
            print(f"Frame saved as {filename}")
            return filename
        return None
