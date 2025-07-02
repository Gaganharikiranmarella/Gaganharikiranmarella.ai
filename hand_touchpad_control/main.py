import cv2
import mediapipe as mp
import pyautogui
import keyboard
import time
import numpy as np

# Setup
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Cursor starts at screen center
cursor_x, cursor_y = screen_w // 2, screen_h // 2
prev_index_x, prev_index_y = None, None

gesture_delay = 1
last_gesture_time = 0
scroll_threshold = 40
drag_active = False
prev_y_scroll = None
prev_x_switch = None
prev_zoom_dist = None

def get_finger_states(lm):
    fingers = []
    fingers.append(lm[4].x < lm[3].x)  # Thumb
    for tip_id in [8, 12, 16, 20]:
        fingers.append(lm[tip_id].y < lm[tip_id - 2].y)
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
            hand_label = results.multi_handedness[i].classification[0].label
            lm = hand_landmarks.landmark
            fingers = get_finger_states(lm)
            total_up = fingers.count(True)

            # Screen coords of index finger
            index_screen_x = int(lm[8].x * screen_w)
            index_screen_y = int(lm[8].y * screen_h)

            if hand_label == "Right":
                if prev_index_x is not None:
                    dx = index_screen_x - prev_index_x
                    dy = index_screen_y - prev_index_y
                    cursor_x = max(0, min(cursor_x + dx, screen_w))
                    cursor_y = max(0, min(cursor_y + dy, screen_h))
                    pyautogui.moveTo(cursor_x, cursor_y)
                prev_index_x = index_screen_x
                prev_index_y = index_screen_y

                # Scroll
                if total_up == 2 and fingers[1] and fingers[2]:
                    if prev_y_scroll is not None:
                        dy = index_screen_y - prev_y_scroll
                        if abs(dy) > scroll_threshold:
                            pyautogui.scroll(-30 if dy > 0 else 30)
                    prev_y_scroll = index_screen_y
                else:
                    prev_y_scroll = None

                # 3-finger gestures
                if total_up == 3 and all(fingers[1:4]):
                    if prev_y_scroll is not None and now - last_gesture_time > gesture_delay:
                        dy = index_screen_y - prev_y_scroll
                        if dy < -40:
                            keyboard.send("windows+tab")
                            last_gesture_time = now
                        elif dy > 40:
                            keyboard.send("windows+d")
                            last_gesture_time = now
                    prev_y_scroll = index_screen_y

                # 4-finger desktop switch
                if total_up == 4 and all(fingers[1:5]):
                    if prev_x_switch is not None and now - last_gesture_time > gesture_delay:
                        dx = index_screen_x - prev_x_switch
                        if dx < -40:
                            keyboard.send("windows+ctrl+left")
                            last_gesture_time = now
                        elif dx > 40:
                            keyboard.send("windows+ctrl+right")
                            last_gesture_time = now
                    prev_x_switch = index_screen_x
                else:
                    prev_x_switch = None

                # Clicks
                if fingers[1] and fingers[0]:
                    pyautogui.click()
                    time.sleep(0.3)
                if fingers[2] and fingers[0]:
                    pyautogui.click(button='right')
                    time.sleep(0.3)

            elif hand_label == "Left":
                # Zoom
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

                # Drag
                if fingers[1] and fingers[0]:
                    if not drag_active:
                        pyautogui.mouseDown()
                        drag_active = True
                else:
                    if drag_active:
                        pyautogui.mouseUp()
                        drag_active = False

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Draw floating '+' cursor (blue)
    cx_disp = int(cursor_x * w / screen_w)
    cy_disp = int(cursor_y * h / screen_h)
    draw_cursor(frame, cx_disp, cy_disp, (255, 0, 0))

    cv2.imshow("Floating Cursor Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
