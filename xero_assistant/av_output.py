import pyttsx3

def speak(text):
    print("XERO (speaking):", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
