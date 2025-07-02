# utils/hand_tracker.py

import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def get_landmarks(self, frame, draw=True):
        landmarks = []
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                single_hand = []
                for lm in hand.landmark:
                    single_hand.extend([lm.x, lm.y])
                landmarks.append(single_hand)
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
        return frame, landmarks
