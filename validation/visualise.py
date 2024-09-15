#!/usr/bin/env python3

'''Helper script to visualise a set of poses over a video capture'''

import cv2
import mediapipe as mp
import json

with open('be_pose_estimation/data/results/20240904/stsstruggletrimmed_1.json') as f:
  POSES = json.load(f)

CAP = cv2.VideoCapture('be_pose_estimation/data/videos/20240904/side_cam_stsstruggle_trimmed.avi')
KP_CONNS = [
    (0, 4), (0, 1), (4, 5), (5, 6), (6, 8), (1, 2), (2, 3), (3, 7),
    (10, 9), (12, 11), (12, 14), (14, 16), (16, 22), (16, 20), (16, 18), (18, 20),
    (11, 13), (13, 15), (15, 21), (15, 19), (15, 17), (17, 19), (12, 24),
    (11, 23), (24, 23), (24, 26), (23, 25), (26, 28), (25, 27), (28, 32), 
    (28, 30), (30, 32), (27, 29), (27, 31), (29, 31)
]

mp_pose = mp.solutions.pose
frames = []

with mp_pose.Pose(
  static_image_mode=True,
  model_complexity=0,
  enable_segmentation=True,
  min_detection_confidence=0.5) as pose:

  for _ in POSES:
    ret, frame_image = CAP.read()
    if not ret:
      # video has reached the end
      break

    frame_height, frame_width, _ = frame_image.shape

    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB))

    # Create a copy of the frame for overlaying keypoints
    overlay_image = frame_image.copy()

    if results.pose_landmarks:
      # Overlay each keypoint onto the image for this frame
      keypoints = [(int(lm.x * frame_width), int(lm.y * frame_height)) for lm in results.pose_landmarks.landmark]
      for kp in keypoints:
        cv2.circle(overlay_image, kp, radius=2, color=(0, 255, 0), thickness=-1)

      # Connect the dots - draw lines between joints to form a human stick-figure shape
      for joint1, joint2 in KP_CONNS:
        pt1 = keypoints[joint1]
        pt2 = keypoints[joint2]
        cv2.line(overlay_image, pt1, pt2, (0, 255, 0), 1)

    cv2.imshow('Pose Estimation', overlay_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

