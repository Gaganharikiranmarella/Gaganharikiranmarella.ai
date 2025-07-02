import cv2
import mediapipe as mp
import numpy as np
from robot_controller import simulate_dual_robot_hands
from utils.angle_utils import extract_finger_angles

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Webcam feed
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        left_angles = [0] * 15
        right_angles = [0] * 15

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[idx].classification[0].label
                angles = extract_finger_angles(hand_landmarks)

                if hand_label == "Left":
                    left_angles = angles
                elif hand_label == "Right":
                    right_angles = angles

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Update dual robot simulation
        simulate_dual_robot_hands(left_angles, right_angles)

        # Display webcam
        cv2.imshow("Dual Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
