# Stores and retrieves the transcription
_transcript = []

def append_note(text):
    _transcript.append(text)
    with open("live_notepad.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def get_transcript():
    return "\n".join(_transcript)
