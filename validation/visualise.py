'''Visualise a set of poses over a video capture'''

import json
import cv2
from time import sleep
from be_pose_estimation.movenet_model import MovenetModel as model

with open('be_pose_estimation/data/results/20240904/uncalibrated_stsstruggle_thunder.json') as f:
    POSES = json.load(f)

CAP = cv2.VideoCapture('be_pose_estimation/data/videos/20240904/side_cam_stsstruggle_trimmed.avi')

# KP_CONNS = [
#     (0, 4), (0, 1), (4, 5), (5, 6), (6, 8), (1, 2), (2, 3), (3, 7),
#     (10, 9), (12, 11), (12, 14), (14, 16), (16, 22), (16, 20), (16, 18), (18, 20),
#     (11, 13), (13, 15), (15, 21), (15, 19), (15, 17), (17, 19), (12, 24),
#     (11, 23), (24, 23), (24, 26), (23, 25), (26, 28), (25, 27), (28, 32), 
#     (28, 30), (30, 32), (27, 29), (27, 31), (29, 31)
# ]
KP_CONNS = []

for pose in POSES:
    ret, frame_image = CAP.read()
    if not ret:
        break

    frame_height, frame_width, _ = frame_image.shape
    frame_dims = (frame_width, frame_height)
    overlay_image = frame_image.copy()

    keypoints = [model.get_pixel_coordinate((kp['x'], kp['y']), frame_dims) for kp in pose['keypoints']]

    # Visualize the keypoints and connections
    for kp in keypoints:
        cv2.circle(overlay_image, kp, radius=2, color=(0, 255, 0), thickness=-1)

    for joint1, joint2 in KP_CONNS:
        pt1 = keypoints[joint1]
        pt2 = keypoints[joint2]
        cv2.line(overlay_image, pt1, pt2, (0, 255, 0), 1)

    cv2.imshow('Pose Estimation', overlay_image)
    sleep(0.05)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

