#!/usr/bin/env python3

'''Test out some comparison of mobile data results with opensim.'''

import json
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

def calc_joint_angle(initial_side: dict, vertex: dict, terminal_side: dict):
    v1 = (vertex['x'] - initial_side['x'], vertex['y'] - initial_side['y'])
    v2 = (vertex['x'] - terminal_side['x'], vertex['y'] - terminal_side['y'])

    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle_radians = math.acos(cos_angle)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def sigmoid(x: float) -> float:
    '''
    Apply the sigmoid function to x (used for converting presence and
    visibility values from mobile data to percentages).

    Returns:
      Result of applying sigmoid function to x (float between 0 and 1).
    '''
    return 1 / (1 + math.exp(-x))

PRES = 0.95
VIS = 0.90

filepath = 'data/opensim_ik_results/20240904/stsstruggle_result.mot'

ik = pd.read_csv(filepath, delim_whitespace=True, skiprows=10)
lab_knee_angles = ik['knee_angle_r']

with open('data/opensim_ik_results/20240904/uncalibrated_side_cam_stsstruggle.json') as f:
    poses = json.load(f)

mobile_knee_angles = []
for pose in poses:
    pose = {kp['name']: kp for kp in pose['keypoints']}

    try:
        hip = pose['left_hip']
        knee = pose['left_knee']
        ankle = pose['left_ankle']
        print(sigmoid(hip['visibility']), sigmoid(hip['presence']), sigmoid(knee['visibility']), sigmoid(knee['presence']), sigmoid(ankle['visibility']), sigmoid(ankle['presence']))
        if (sigmoid(hip['visibility']) < VIS or sigmoid(hip['presence']) < PRES
            or sigmoid(knee['visibility']) < VIS or sigmoid(knee['presence']) < PRES
            or sigmoid(ankle['visibility']) < VIS or sigmoid(ankle['presence']) < PRES):
            continue
        mobile_knee_angles.append(calc_joint_angle(ankle, knee, hip))
    except:
        continue

time_lab = np.linspace(0, 1, len(lab_knee_angles))
time_mobile = np.linspace(0, 1, len(mobile_knee_angles))

interpolator = PchipInterpolator(time_mobile, mobile_knee_angles)
interpolated_mobile_knee_angles = interpolator(time_lab)

plt.plot(time_lab, lab_knee_angles, label='opensim')
plt.plot(time_lab, interpolated_mobile_knee_angles, label='pose_estimation')
plt.xlabel('Relative Time')
plt.ylabel('Knee Flexion Angle')
plt.title('opensim vs pose estimation (uncalibrated)')
plt.legend()
plt.show()

