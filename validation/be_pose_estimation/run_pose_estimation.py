#!/usr/bin/env python3

'''
    Run pose estimation model on backend side. Use predetermined camera parameters (camera matrix and
    distortion coefficients) to undistort images from video capture before running pose estimation.

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
VIDEO_PATH = 'data/videos/20240904/side_cam_stsstruggle.avi'
MODEL_PATH = 'data/pose_estimation_model.tflite'
OUT_FILE_PATH = 'data/results/20240904/side_cam_stsstruggle.json'
RECORDING_START_TIME = 78593275
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
poses = []

while cap.isOpened():
    ret, dst_img = cap.read()
    if not ret:
        break

    print(f'processing {dst_img} ...')

    # Get the timestamp of the current frame
    time_since_start = cap.get(cv2.CAP_PROP_POS_MSEC)
    timestamp = RECORDING_START_TIME + time_since_start

    h, w = dst_img.shape[:2]
    undstcammtx, _ = cv2.getOptimalNewCameraMatrix(CAM_PARAMS['mtx'], CAM_PARAMS['dst'], (w,h), 1, (w,h))

    # Undistort image and run pose estimation model
    undst_img = cv2.undistort(dst_img, CAM_PARAMS['mtx'], CAM_PARAMS['dst'], None, undstcammtx)
    image = preprocess_image(undst_img)

    pose = run_model(interpreter, image)
    poses.append({
        'timestamp': timestamp,
        'keypoints': format_pose(pose.tolist()[0])
    })

cap.release()
cv2.destroyAllWindows()

# Save results of pose estimation to json file
with open(OUT_FILE_PATH, 'w') as json_file:
    json.dump(poses, json_file, indent=4)
######################################################################
######################################################################

