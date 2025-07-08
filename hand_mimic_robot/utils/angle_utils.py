import numpy as np

def vector_angle(a, b, c):
    ab = np.array(a) - np.array(b)
    cb = np.array(c) - np.array(b)
    dot_product = np.dot(ab, cb)
    norm_product = np.linalg.norm(ab) * np.linalg.norm(cb)
    if norm_product == 0:
        return 0
    cos_angle = np.clip(dot_product / norm_product, -1.0, 1.0)
    angle_rad = np.arccos(cos_angle)
    return np.degrees(angle_rad)

def extract_finger_angles(landmarks):
    """
    Extracts 15 angles (3 per finger) from MediaPipe landmarks.
    Returns list of 15 joint angles (degrees).
    """
    def pt(i):
        return [landmarks.landmark[i].x,
                landmarks.landmark[i].y,
                landmarks.landmark[i].z]

    angles = []

    # Define joints for each finger
    finger_joints = [
        (1, 2, 3), (2, 3, 4),      # Thumb
        (5, 6, 7), (6, 7, 8),      # Index
        (9, 10, 11), (10, 11, 12), # Middle
        (13, 14, 15), (14, 15, 16),# Ring
        (17, 18, 19), (18, 19, 20) # Pinky
    ]

    for a, b, c in finger_joints:
        angle = vector_angle(pt(a), pt(b), pt(c))
        angles.append(angle)

    # Add 1 extra dummy joint per finger (to make 15 total)
    while len(angles) < 15:
        angles.append(0)

    return angles
