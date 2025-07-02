import cv2
import os
import pandas as pd
from utils.hand_tracker import HandTracker

# Setup
tracker = HandTracker()
data_path = "data/sign_data.csv"
os.makedirs("data", exist_ok=True)

# Initialize CSV with headers if not present
if not os.path.exists(data_path):
    columns = ["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)]
    pd.DataFrame(columns=columns).to_csv(data_path, index=False)

print("\n🖐️ Press 's' to save hand sign data, 'q' to quit.\n")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    frame, landmarks = tracker.get_landmarks(frame)

    cv2.imshow("Collect Hand Sign Data", frame)
    key = cv2.waitKey(1)

    if key == ord('s') and landmarks:
        label = input("Enter label for this sign: ").strip()
        if label:
            row = [label] + landmarks[0]
            df = pd.read_csv(data_path)
            df.loc[len(df)] = row
            df.to_csv(data_path, index=False)
            print(f"[+] Saved sign: {label}")
        else:
            print("⚠️ Label cannot be empty.")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
