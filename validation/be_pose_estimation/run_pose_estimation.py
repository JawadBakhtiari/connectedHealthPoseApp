#!/usr/bin/env python3

import cv2
import numpy as np
import tensorflow as tf
import json

VIDEO_PATH = 'data/front.avi'
MODEL_PATH = 'data/pose_estimation_model.tflite'
OUT_FILE_PATH = 'results.json'
RECORDING_START_TIME = 78593275

# Calibration coefficients for the camera that was used.
CALIBRATION_COEFFICIENTS = {
    "ret": 0.37792383159926235,
    "mtx": [
        [
            1668.9209764199638,
            0.0,
            937.2442689208088
        ],
        [
            0.0,
            1665.774625676352,
            570.1815548280978
        ],
        [
            0.0,
            0.0,
            1.0
        ]
    ],
    "dst": [
        [
            0.18438871449170227,
            -0.4560320771008444,
            0.009597708193139959,
            -0.0037874684297786003,
            0.47972763283947006
        ]
    ]
}

def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.expand_dims(image, axis=0)
    return image

def run_inference(interpreter, image):
    # Run inference on the image
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    # Get output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

def process_video(
        video_path: str,
        model_path: str,
        recording_start_time: int,
        calco: dict,
        output_json_path: str
    ) -> None:
    cap = cv2.VideoCapture(video_path)
    interpreter = load_model(model_path)
    undstcammtx = None
    results_list = []

    while cap.isOpened():
        ret, dst_img = cap.read()
        if not ret:
            break

        # Get the timestamp of the current frame
        time_since_start = cap.get(cv2.CAP_PROP_POS_MSEC)
        timestamp = recording_start_time + time_since_start

        if not undstcammtx:
            h, w = dst_img.shape[:2]
            undstcammtx, _ = cv2.getOptimalNewCameraMatrix(calco['mtx'], dst_img, (w,h), 1, (w,h))

        undst_img = cv2.undistort(dst_img, calco['mtx'], calco['dst'], None, undstcammtx)
        image = preprocess_image(undst_img)
        output_data = run_inference(interpreter, image)
        results_list.append({
            'timestamp': timestamp,
            'output': output_data.tolist()
        })

    cap.release()
    cv2.destroyAllWindows()

    # Save results to JSON
    with open(output_json_path, 'w') as json_file:
        json.dump(results_list, json_file, indent=4)

process_video(VIDEO_PATH, MODEL_PATH, RECORDING_START_TIME, CALIBRATION_COEFFICIENTS, OUT_FILE_PATH)
