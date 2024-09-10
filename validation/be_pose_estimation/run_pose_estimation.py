#!/usr/bin/env python3

'''
    Run pose estimation model on backend side. Run on both calibrated and uncalibrated videos.

    For calibrated videom use predetermined camera parameters (camera matrix and distortion
    coefficients) to undistort images from video capture before running pose estimation.

    Save calculated poses to an output file for later use in validation.
'''

import cv2
import numpy as np
import tensorflow as tf
import json
from pose_model import format_pose

######################################################################
############################# CONSTANTS ##############################
######################### change as needed ############################
######################################################################
VIDEO_PATH = 'data/videos/20240904/side_cam_stsstruggle_trimmed.avi'
MODEL_PATH = 'data/pose_estimation_model.tflite'
CALIBRATED_OUT_FILE_PATH = 'data/results/20240904/calibrated_side_cam_stsstruggle.json'
UNCALIBRATED_OUT_FILE_PATH = 'data/results/20240904/uncalibrated_side_cam_stsstruggle.json'
CAM_PARAMS = np.load('data/camera_parameters/20240904/side_cam.npz')
######################################################################
######################################################################


######################################################################
########################## HELPER FUNCTIONS ##########################
######################################################################
def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image = cv2.resize(image, (256, 256))
    return np.expand_dims(image, axis=0)

def run_model(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])
######################################################################
######################################################################


######################################################################
############################ RUN SCRIPT ##############################
######################################################################
cap = cv2.VideoCapture(VIDEO_PATH)
interpreter = load_model(MODEL_PATH)
print(interpreter.get_input_details())
undstcammtx = None
calibrated_video_poses = []
uncalibrated_video_poses = []

while cap.isOpened():
    ret, dst_img = cap.read()
    if not ret:
        break

    print(f'processing {dst_img} ...')

    time_since_start = cap.get(cv2.CAP_PROP_POS_MSEC)
    h, w = dst_img.shape[:2]
    undstcammtx, _ = cv2.getOptimalNewCameraMatrix(CAM_PARAMS['mtx'], CAM_PARAMS['dst'], (w,h), 1, (w,h))

    # Undistort image and run pose estimation model
    undst_img = cv2.undistort(dst_img, CAM_PARAMS['mtx'], CAM_PARAMS['dst'], None, undstcammtx)
    image = preprocess_image(undst_img)

    uncalibrated_image_pose = run_model(interpreter, preprocess_image(dst_img))
    calibrated_image_pose = run_model(interpreter, preprocess_image(undst_img))
    calibrated_video_poses.append({
        'time_since_start': time_since_start,
        'keypoints': format_pose(calibrated_image_pose.tolist()[0])
    })
    uncalibrated_video_poses.append({
        'time_since_start': time_since_start,
        'keypoints': format_pose(uncalibrated_image_pose.tolist()[0])
    })
cap.release()
cv2.destroyAllWindows()

# Save results of pose estimation
with open(CALIBRATED_OUT_FILE_PATH, 'w') as json_file:
    json.dump(calibrated_video_poses, json_file, indent=4)
with open(UNCALIBRATED_OUT_FILE_PATH, 'w') as json_file:
    json.dump(uncalibrated_video_poses, json_file, indent=4)
######################################################################
######################################################################

