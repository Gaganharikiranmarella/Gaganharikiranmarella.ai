import torchvision.transforms as T
from torchvision.models import resnet50
import torch.nn as nn
import torch
import cv2
import numpy as np

resnet = resnet50(pretrained=True)
resnet.fc = nn.Identity()
resnet.eval()
transform = T.Compose([T.ToPILImage(), T.Resize((224, 224)), T.ToTensor()])

def extract_features(frame, boxes):
    features = []
    for box in boxes:
        x1, y1, x2, y2, conf, cls = map(int, box)
        crop = frame[y1:y2, x1:x2]
        if crop.size == 0: continue

        crop_tensor = transform(crop).unsqueeze(0)
        with torch.no_grad():
            embedding = resnet(crop_tensor).squeeze().numpy()

        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        features.append({
            "bbox": (x1, y1, x2, y2),
            "center": center,
            "embedding": embedding,
            "player_id": None
        })

    return features
