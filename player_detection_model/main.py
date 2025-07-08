import os
import cv2
from src.detect import detect_players
from src.features import extract_features
from src.matcher import match_players
from src.assign_ids import assign_ids
from src.utils import draw_boxes

TACTICAM_PATH = 'data/tacticam.mp4'
BROADCAST_PATH = 'data/broadcast.mp4'
MODEL_PATH = 'models/best.pt'
OUTPUT_PATH = 'outputs/tacticam_matched.jpg'

print("\n[INFO] Detecting players in both videos...")
broadcast_frames, broadcast_detections = detect_players(BROADCAST_PATH, MODEL_PATH)
tacticam_frames, tacticam_detections = detect_players(TACTICAM_PATH, MODEL_PATH)

print("[INFO] Extracting features from the middle frame...")
mid_idx = min(len(broadcast_frames), len(tacticam_frames)) // 2

broad_frame = broadcast_frames[mid_idx]
tac_frame = tacticam_frames[mid_idx]
broad_boxes = broadcast_detections[mid_idx]
tac_boxes = tacticam_detections[mid_idx]

broadcast_feats = extract_features(broad_frame, broad_boxes)
tacticam_feats = extract_features(tac_frame, tac_boxes)

print("[INFO] Matching players using visual + spatial features...")
matches = match_players(tacticam_feats, broadcast_feats)
id_map = assign_ids(tacticam_feats, broadcast_feats, matches)

print("[INFO] Drawing player IDs on tacticam frame...")
tac_frame_annotated = draw_boxes(tac_frame.copy(), tacticam_feats, id_map)

os.makedirs("outputs", exist_ok=True)
cv2.imwrite(OUTPUT_PATH, tac_frame_annotated)
print(f"[INFO] Saved output to {OUTPUT_PATH}")
