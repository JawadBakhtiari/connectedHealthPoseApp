#!/usr/bin/env python3

'''A script for playing around with different ideas'''

'''Currently testing out calculating when a 360 degree spin has been executed'''

import json
import heapq

def same_sign(a, b):
    return a * b > 0

with open('../be_pose_estimation/data/results/20240904/uncalibrated_360_spin_test_thunder.json') as f:
    poses = json.load(f)

NUM_SHOULDER_WIDTHS = 10
SHOULDER_WIDTH_DIFF_TOLERANCE = 0.01

last_shoulder_dist = None
pose_index = 0
shoulder_dists = []


# loop for getting shoulder width before first turn
while pose_index < len(poses):
    pose = {kp['name']: kp for kp in poses[pose_index]['keypoints']}
    shoulder_dist = pose['left_shoulder']['x'] - pose['right_shoulder']['x']

    if last_shoulder_dist != None and not same_sign(shoulder_dist, last_shoulder_dist):
        # turning point
        break

    if len(shoulder_dists) < NUM_SHOULDER_WIDTHS:
        heapq.heappush(shoulder_dists, shoulder_dist)
    elif shoulder_dist > shoulder_dists[0]:
        heapq.heapreplace(shoulder_dists, shoulder_dist)

    last_shoulder_dist = shoulder_dist
    pose_index += 1


shoulder_width = shoulder_dists[NUM_SHOULDER_WIDTHS // 2]


while pose_index < len(poses):
    pose = {kp['name']: kp for kp in poses[pose_index]['keypoints']}
    shoulder_dist = pose['left_shoulder']['x'] - pose['right_shoulder']['x']
    if abs(shoulder_dist - shoulder_width) <= SHOULDER_WIDTH_DIFF_TOLERANCE:
        print(f'time taken to complete turn -> {poses[pose_index]['time_since_start']:.2f} seconds')
        break
    last_shoulder_dist = shoulder_dist
    pose_index += 1


