'''Visualise a set of poses over a video capture'''

import json
import cv2
from time import sleep
from be_pose_estimation.models.movenet_thunder import MovenetThunder as model
from exercises.grid_steps import GridSteps as Exercise

POSE_COLOR = (0, 165, 255)
SUCCESS_COLOR = (0, 255, 0)
FAIL_COLOR = (0, 0, 255)
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TIME_POS = (20, 100)
REPS_POS = (400, 100)
TIME_AFTER_SUCCESS_POS = (20, 200)
TEXT_SCALE = 2
TEXT_COLOR = (255, 255, 255)
TEXT_THICKNESS = 3
TEXT_LINE_TYPE = cv2.LINE_AA
CAP = cv2.VideoCapture('be_pose_estimation/data/videos/20241023/grid_steps.mp4')
with open('be_pose_estimation/data/results/20241023/grid_steps_thunder.json') as f:
    POSES = json.load(f)

# tandem_walk_end = 1665
# tandem_walk_end = 1800
exercise = Exercise(10)
EXERCISE_COMPLETED_TIME = exercise.run_check(POSES)

for pose in POSES:
    ret, frame_image = CAP.read()
    if not ret:
        break

    frame_height, frame_width, _ = frame_image.shape
    frame_dims = (frame_width, frame_height)
    overlay_image = frame_image.copy()

    time_since_start = CAP.get(cv2.CAP_PROP_POS_MSEC) / 1000
    reps = exercise.num_reps_completed(time_since_start)
    cv2.putText(
        overlay_image,
        f'REPS: {reps}',
        REPS_POS,
        TEXT_FONT,
        TEXT_SCALE,
        TEXT_COLOR,
        TEXT_THICKNESS,
        TEXT_LINE_TYPE
    )

    if time_since_start >= EXERCISE_COMPLETED_TIME:
        cv2.putText(
            overlay_image,
            f'{EXERCISE_COMPLETED_TIME:.2f}',
            TIME_POS,
            TEXT_FONT,
            TEXT_SCALE,
            SUCCESS_COLOR,
            TEXT_THICKNESS,
            TEXT_LINE_TYPE
        )
        cv2.putText(overlay_image,
            f'{time_since_start:.2f}',
            TIME_AFTER_SUCCESS_POS,
            TEXT_FONT,
            TEXT_SCALE,
            TEXT_COLOR,
            TEXT_THICKNESS,
            TEXT_LINE_TYPE
        )
    else:
        cv2.putText(
            overlay_image,
            f'{time_since_start:.2f}',
            TIME_POS,
            TEXT_FONT,
            TEXT_SCALE,
            TEXT_COLOR,
            TEXT_THICKNESS,
            TEXT_LINE_TYPE
        )

    keypoints = [(kp['x'], kp['y']) for kp in pose['keypoints']]

    pose_color = POSE_COLOR
    if time_since_start >= EXERCISE_COMPLETED_TIME:
        pose_color = SUCCESS_COLOR
    elif exercise.is_failing_interval(time_since_start):
        pose_color = FAIL_COLOR

    # Visualize the keypoints and connections
    for kp in keypoints:
        cv2.circle(overlay_image, kp, radius=2, color=pose_color, thickness=7)

    for joint1, joint2 in model.joint_connections():
        pt1 = keypoints[joint1]
        pt2 = keypoints[joint2]
        cv2.line(overlay_image, pt1, pt2, pose_color, 2)

    cv2.imshow('Pose Estimation', overlay_image)
    sleep(0.04)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

