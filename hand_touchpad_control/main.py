import cv2
import mediapipe as mp
import pyautogui
import keyboard
import time
import numpy as np

# Initialize screen size and MediaPipe
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Gesture memory
gesture_delay = 1
last_gesture_time = 0
scroll_threshold = 40
drag_active = False
prev_y_scroll = None
prev_x_switch = None
prev_zoom_dist = None

def get_finger_states(hand_landmarks):
    fingers = []
    fingers.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)  # Thumb
    for tip_id in [8, 12, 16, 20]:
        fingers.append(hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y)
    return fingers

def draw_cursor(frame, x, y, color):
    cv2.line(frame, (x - 10, y), (x + 10, y), color, 2)
    cv2.line(frame, (x, y - 10), (x, y + 10), color, 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    now = time.time()

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i].classification[0].label
            lm = hand_landmarks.landmark
            index_finger = lm[8]
            thumb = lm[4]

            cx, cy = int(index_finger.x * w), int(index_finger.y * h)
            screen_x, screen_y = int(index_finger.x * screen_w), int(index_finger.y * screen_h)
            fingers = get_finger_states(hand_landmarks)
            total_up = fingers.count(True)

            # Draw cursor
            if handedness == "Right":
                draw_cursor(frame, cx, cy, (255, 0, 0))  # Blue for Right Hand

                # Cursor movement
                if total_up == 1 and fingers[1]:
                    pyautogui.moveTo(screen_x, screen_y)

                # Scroll
                if total_up == 2 and fingers[1] and fingers[2]:
                    if prev_y_scroll is not None:
                        dy = cy - prev_y_scroll
                        if abs(dy) > scroll_threshold:
                            pyautogui.scroll(-30 if dy > 0 else 30)
                    prev_y_scroll = cy
                else:
                    prev_y_scroll = None

                # App switch / minimize
                if total_up == 3 and all(fingers[1:4]) and not fingers[0] and not fingers[4]:
                    if prev_y_scroll is not None and now - last_gesture_time > gesture_delay:
                        dy = cy - prev_y_scroll
                        if dy < -40:
                            keyboard.send("windows+tab")
                            last_gesture_time = now
                        elif dy > 40:
                            keyboard.send("windows+d")
                            last_gesture_time = now
                    prev_y_scroll = cy

                # Desktop switch
                if total_up == 4 and all(fingers[1:5]) and not fingers[0]:
                    if prev_x_switch is not None and now - last_gesture_time > gesture_delay:
                        dx = cx - prev_x_switch
                        if dx < -40:
                            keyboard.send("windows+ctrl+left")
                            last_gesture_time = now
                        elif dx > 40:
                            keyboard.send("windows+ctrl+right")
                            last_gesture_time = now
                    prev_x_switch = cx
                else:
                    prev_x_switch = None

                # Left click (index + thumb)
                if fingers[1] and fingers[0]:
                    pyautogui.click()
                    time.sleep(0.3)

                # Right click (middle + thumb)
                if fingers[2] and fingers[0]:
                    pyautogui.click(button='right')
                    time.sleep(0.3)

            elif handedness == "Left":
                draw_cursor(frame, cx, cy, (0, 255, 0))  # Green for Left Hand

                # Zoom in/out
                index_pos = (int(lm[8].x * w), int(lm[8].y * h))
                thumb_pos = (int(lm[4].x * w), int(lm[4].y * h))
                dist = np.linalg.norm(np.array(index_pos) - np.array(thumb_pos))

                if prev_zoom_dist is not None and now - last_gesture_time > 0.3:
                    if dist - prev_zoom_dist > 15:
                        pyautogui.keyDown('ctrl')
                        pyautogui.scroll(50)
                        pyautogui.keyUp('ctrl')
                        last_gesture_time = now
                    elif prev_zoom_dist - dist > 15:
                        pyautogui.keyDown('ctrl')
                        pyautogui.scroll(-50)
                        pyautogui.keyUp('ctrl')
                        last_gesture_time = now
                prev_zoom_dist = dist

                # Drag (pinch and hold)
                if fingers[1] and fingers[0]:  # Thumb + Index
                    if not drag_active:
                        pyautogui.mouseDown()
                        drag_active = True
                else:
                    if drag_active:
                        pyautogui.mouseUp()
                        drag_active = False

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Dual Hand Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
