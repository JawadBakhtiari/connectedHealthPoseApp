'''Visualise a set of poses over a video capture'''

import json
import cv2
from time import sleep
from be_pose_estimation.models.movenet_thunder import MovenetThunder as model
from testing.test import run_single_sts_check

POSE_COLOR = (0, 0, 255)
SUCCESS_COLOR = (0, 255, 0)
TIME_FONT = cv2.FONT_HERSHEY_SIMPLEX
TIME_POS = (20, 100)
TIME_AFTER_SUCCESS_POS = (20, 200)
TIME_SCALE = 3
TIME_COLOR = (255, 255, 255)
TIME_THICKNESS = 3
TIME_LINE_TYPE = cv2.LINE_AA
CAP = cv2.VideoCapture('example_data/random/sts_fail.MOV')
with open('be_pose_estimation/data/results/20240904/uncalibrated_sts_fail_thunder.json') as f:
    POSES = json.load(f)
EXERCISE_COMPLETED_TIME = run_single_sts_check(POSES)

for pose in POSES:
    ret, frame_image = CAP.read()
    if not ret:
        break

    frame_height, frame_width, _ = frame_image.shape
    frame_dims = (frame_width, frame_height)
    overlay_image = frame_image.copy()

    time_since_start = CAP.get(cv2.CAP_PROP_POS_MSEC) / 1000
    if time_since_start >= EXERCISE_COMPLETED_TIME:
        POSE_COLOR = SUCCESS_COLOR
        cv2.putText(overlay_image, f'{EXERCISE_COMPLETED_TIME:.2f}', TIME_POS, TIME_FONT, TIME_SCALE, SUCCESS_COLOR, TIME_THICKNESS, TIME_LINE_TYPE)
        cv2.putText(overlay_image, f'{time_since_start:.2f}', TIME_AFTER_SUCCESS_POS, TIME_FONT, TIME_SCALE, TIME_COLOR, TIME_THICKNESS, TIME_LINE_TYPE)
    else:
        cv2.putText(overlay_image, f'{time_since_start:.2f}', TIME_POS, TIME_FONT, TIME_SCALE, TIME_COLOR, TIME_THICKNESS, TIME_LINE_TYPE)

    keypoints = [model.get_pixel_coordinate((kp['x'], kp['y']), frame_dims) for kp in pose['keypoints']]

    # Visualize the keypoints and connections
    for kp in keypoints:
        cv2.circle(overlay_image, kp, radius=2, color=POSE_COLOR, thickness=7)

    # Display time since start of video

    for joint1, joint2 in model.joint_connections():
        pt1 = keypoints[joint1]
        pt2 = keypoints[joint2]
        cv2.line(overlay_image, pt1, pt2, POSE_COLOR, 2)

    cv2.imshow('Pose Estimation', overlay_image)
    sleep(0.05)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

