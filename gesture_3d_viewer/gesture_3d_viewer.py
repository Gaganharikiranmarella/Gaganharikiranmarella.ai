import cv2
import mediapipe as mp
import open3d as o3d
import numpy as np
import math

def create_hexagon_prism(radius=1.0, height=0.5):
    vertices = []
    for i in range(6):
        angle = 2 * np.pi * i / 6
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append([x, y, -height / 2])
    for i in range(6):
        angle = 2 * np.pi * i / 6
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append([x, y, height / 2])

    triangles = []
    for i in range(6):
        j = (i + 1) % 6
        triangles += [[i, j, i + 6], [j, j + 6, i + 6]]
    for i in range(1, 5):
        triangles.append([0, i, i + 1])
        triangles.append([6, 6 + i + 1, 6 + i])

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    mesh.paint_uniform_color([0, 0, 1])  
    mesh.compute_vertex_normals()
    return mesh

color_map = {
    1: [0, 0, 1],    
    2: [1, 0, 0],    
    3: [0, 1, 0],    
    4: [1, 1, 0],    
    5: [0, 0, 0],    
}

mesh = create_hexagon_prism()
vis = o3d.visualization.Visualizer()
vis.create_window("3D Viewer", width=800, height=600)
vis.add_geometry(mesh)
ctr = vis.get_view_control()
zoom = 1.0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_right_pos = None

current_color = [0, 0, 1]
last_finger_count = 0
color_locked = True

def count_fingers(lm):
    finger_ids = [4, 8, 12, 16, 20]
    open_fingers = 0
    
    if lm[4].x < lm[3].x:
        open_fingers += 1
 
    if lm[8].y < lm[6].y: open_fingers += 1
    if lm[12].y < lm[10].y: open_fingers += 1
    if lm[16].y < lm[14].y: open_fingers += 1
    if lm[20].y < lm[18].y: open_fingers += 1
    return open_fingers

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_handedness in enumerate(results.multi_handedness):
            label = hand_handedness.classification[0].label
            handLms = results.multi_hand_landmarks[idx]
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            lm = handLms.landmark

            if label == 'Right':
                palm_open = lm[8].y < lm[6].y and lm[12].y < lm[10].y
                x0 = int(lm[0].x * w)
                y0 = int(lm[0].y * h)
                curr_pos = (x0, y0)

                if palm_open:
                    if last_right_pos is not None:
                        dx = curr_pos[0] - last_right_pos[0]
                        dy = curr_pos[1] - last_right_pos[1]
                        angle_y = np.radians(-dx * 0.5)
                        angle_x = np.radians(-dy * 0.5)
                        R = mesh.get_rotation_matrix_from_xyz((angle_x, angle_y, 0))
                        mesh.rotate(R, center=mesh.get_center())
                        vis.update_geometry(mesh)
                    last_right_pos = curr_pos
                else:
                    last_right_pos = None

            elif label == 'Left':
                finger_count = count_fingers(lm)

                if finger_count == 0:
                    color_locked = True

                elif 1 <= finger_count <= 5:
                    color = color_map.get(finger_count)
                    if not color_locked or color != current_color:
                        mesh.paint_uniform_color(color)
                        vis.update_geometry(mesh)
                        current_color = color
                        color_locked = False

    cv2.imshow("Gesture Control", frame)
    vis.poll_events()
    vis.update_renderer()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
vis.destroy_window()
