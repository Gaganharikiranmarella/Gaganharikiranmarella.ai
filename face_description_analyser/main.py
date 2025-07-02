import cv2
import numpy as np
import mediapipe as mp
from fer import FER
from utils.description_utils import build_description

# Load emotion detector
emotion_detector = FER(mtcnn=True)

# Load age and gender models
age_net = cv2.dnn.readNetFromCaffe(
    "models/age_deploy.prototxt", "models/age_net.caffemodel")
gender_net = cv2.dnn.readNetFromCaffe(
    "models/gender_deploy.prototxt", "models/gender_net.caffemodel")

age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']

# Setup Mediapipe face mesh
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False)

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    face_box = None
    emotion = "Unknown"
    gender = "Unknown"
    age = "Unknown"
    head_pose = "Unknown"

    # Detect emotion and estimate face box
    emotion_results = emotion_detector.detect_emotions(frame)

    if emotion_results:
        emotion = emotion_detector.top_emotion(frame)[0]

        x, y, w_box, h_box = emotion_results[0]['box']

        # Clamp bounding box within frame bounds
        x = max(0, x)
        y = max(0, y)
        x2 = min(frame.shape[1], x + w_box)
        y2 = min(frame.shape[0], y + h_box)

        face_box = frame[y:y2, x:x2]

        if face_box.size > 0:
            blob = cv2.dnn.blobFromImage(face_box, 1.0, (227, 227), [104, 117, 123], swapRB=False)

            gender_net.setInput(blob)
            gender = gender_list[gender_net.forward().argmax()]

            age_net.setInput(blob)
            age = age_list[age_net.forward().argmax()]

            # Draw rectangle and labels
            cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{gender}, {age}, {emotion}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Estimate head pose using MediaPipe
    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0]
        nose_tip = landmarks.landmark[1]  # Approx. nose tip
        head_pose = "Facing Forward" if nose_tip.z < -0.1 else "Head Tilted"

    # Build natural language description
    description = build_description(gender, age, emotion, head_pose)

    # Create a white canvas (200x900) for description
    desc_canvas = np.ones((200, 900, 3), dtype=np.uint8) * 255  # white background

    # Put the description text on it (black text)
    cv2.putText(desc_canvas, description, (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Show it in a separate window
    cv2.imshow("Description", desc_canvas)

    # Show the main webcam feed
    cv2.imshow("Facial Description Analyzer", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
