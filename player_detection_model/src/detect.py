import cv2
from ultralytics import YOLO

def detect_players(video_path, model_path):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    frames = []
    all_detections = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, verbose=False)[0]
        boxes = results.boxes.data

        if boxes is not None and len(boxes) > 0:
            boxes = boxes.cpu().numpy()
            players = [box for box in boxes if int(box[5]) == 0]
        else:
            players = []

        frames.append(frame)
        all_detections.append(players)

    cap.release()
    return frames, all_detections
