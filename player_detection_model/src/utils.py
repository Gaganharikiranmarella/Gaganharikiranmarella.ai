import cv2

def draw_boxes(frame, features, id_map=None):  # Add 3rd argument
    for idx, feat in enumerate(features):
        x1, y1, x2, y2 = feat["bbox"]
        player_id = id_map.get(idx, f"?{idx}") if id_map else f"?{idx}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, player_id, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame

def save_output(frames, output_path, fps=30):
    if not frames: return
    h, w, _ = frames[0].shape
    writer = cv2.VideoWriter(output_path,
                             cv2.VideoWriter_fourcc(*'mp4v'),
                             fps, (w, h))
    for f in frames:
        writer.write(f)
    writer.release()
