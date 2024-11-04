#!/usr/bin/env python3

'''A script for playing around with different ideas'''

import json

with open('../example_data/20241023/dartboard.json') as f:
    poses = json.load(f)

for pose in poses:
    for kp in pose['keypoints']:
        if kp['name'] == 'right_ankle':
            print(pose['time_since_start'])

