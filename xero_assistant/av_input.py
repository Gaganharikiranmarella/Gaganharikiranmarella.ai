import speech_recognition as sr
import cv2

def listen_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("XERO is listening... (Speak now)")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You (voice detected):", text)
        return text
    except Exception:
        print("Sorry, XERO could not recognize your voice.")
        return ""

def capture_image(filename="captured_image.jpg"):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera")
        return None
    print("Press SPACE to capture, ESC to close camera window.")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            break
        cv2.imshow("XERO Camera", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC KEY
            break
        elif key == 32:  # SPACE KEY
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as {filename}")
            cam.release()
            cv2.destroyAllWindows()
            return filename
    cam.release()
    cv2.destroyAllWindows()
    return None
