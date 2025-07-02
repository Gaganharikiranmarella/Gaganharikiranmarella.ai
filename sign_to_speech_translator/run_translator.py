import cv2
import pickle
import pyttsx3
from utils.hand_tracker import HandTracker
import numpy as np
import pandas as pd

# Load trained model
with open("models/trained_model.pkl", "rb") as f:
    model = pickle.load(f)

# Init text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Init hand tracker
tracker = HandTracker()

# Define column names for consistency with training
columns = [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)]

# Track previous prediction to avoid repeats
prev_pred = None
delay_frames = 15
frame_counter = 0

cap = cv2.VideoCapture(0)
print("[🖐️] Starting live translator... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    frame, landmarks = tracker.get_landmarks(frame)

    if landmarks:
        # Convert to DataFrame with proper feature names to avoid warning
        input_df = pd.DataFrame([landmarks[0]], columns=columns)
        prediction = model.predict(input_df)[0]

        # Prevent repeating same prediction continuously
        if prediction != prev_pred or frame_counter > delay_frames:
            print(f"[📢] Recognized: {prediction}")
            engine.say(prediction)
            engine.runAndWait()
            prev_pred = prediction
            frame_counter = 0
        else:
            frame_counter += 1

        cv2.putText(frame, f"Sign: {prediction}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Sign to Speech Translator", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
