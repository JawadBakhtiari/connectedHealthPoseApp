'''Visualise a set of poses over a video capture'''

import json
import cv2
from time import sleep
from be_pose_estimation.models.movenet_thunder import MovenetThunder as model

with open('be_pose_estimation/data/results/20240904/uncalibrated_stsnorm_thunder.json') as f:
    POSES = json.load(f)

CAP = cv2.VideoCapture('be_pose_estimation/data/videos/20240904/front_cam_stsnorm.avi')

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
        cv2.circle(overlay_image, kp, radius=2, color=(0, 0, 255), thickness=7)

    for joint1, joint2 in model.joint_connections():
        pt1 = keypoints[joint1]
        pt2 = keypoints[joint2]
        cv2.line(overlay_image, pt1, pt2, (0, 0, 255), 2)

    cv2.imshow('Pose Estimation', overlay_image)
    sleep(0.05)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

