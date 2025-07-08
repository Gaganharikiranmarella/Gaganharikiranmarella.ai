import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Set up the matplotlib window
fig = plt.figure("Dual 6DOF Robot Hands")
ax = fig.add_subplot(111, projection='3d')
plt.ion()
fig.show()

# Finger link lengths (3 segments per finger)
link_lengths = [1.0, 0.7, 0.5]

def draw_robot_hand(base_x, base_y, joint_angles, hand_color='blue'):
    """
    Draw a single robotic hand with given base position and joint angles.
    base_x, base_y: base palm position for left/right hand
    joint_angles: List of 5 fingers × 3 segments = 15 angles
    """
    fingers_base = [
        [base_x, base_y, 0],
        [base_x + 1.0, base_y, 0],
        [base_x + 2.0, base_y, 0],
        [base_x + 3.0, base_y, 0],
        [base_x + 4.0, base_y, 0]
    ]

    for i, base in enumerate(fingers_base):
        x, y, z = base
        theta = 0  # Starting orientation
        for j in range(3):  # 3 segments per finger
            angle_deg = joint_angles[i * 3 + j]
            theta += np.radians(angle_deg)
            dx = link_lengths[j] * np.cos(theta)
            dz = link_lengths[j] * np.sin(theta)
            x_new = x + dx
            z_new = z + dz
            ax.plot([x, x_new], [y, y], [z, z_new], color=hand_color, linewidth=4)
            x, z = x_new, z_new  # update position

def simulate_dual_robot_hands(left_angles, right_angles):
    """
    Draw both left and right robot hands in the same figure.
    left_angles and right_angles: 15 angles (5 fingers × 3 joints) each
    """
    ax.clear()
    ax.set_title("Dual 6DOF Robot Hands")
    ax.set_xlim(0, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(0, 5)

    # Draw left and right hands
    draw_robot_hand(1, -5, left_angles, hand_color='blue')
    draw_robot_hand(1, +5, right_angles, hand_color='red')

    plt.draw()
    plt.pause(0.001)
