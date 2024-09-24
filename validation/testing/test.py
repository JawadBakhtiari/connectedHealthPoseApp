#!/usr/bin/env python3

'''A script for playing around with different ideas'''

'''Currently testing out calculating when a 360 degree spin has been executed'''

# import json
import heapq
import math

def same_sign(a, b):
    return a * b > 0

# with open('../be_pose_estimation/data/results/20240904/uncalibrated_360_spin_test_thunder.json') as f:
#     poses = json.load(f)

def run_360_check(poses) -> float:
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
            return poses[pose_index]['time_since_start']
        last_shoulder_dist = shoulder_dist
        pose_index += 1

    return poses[pose_index]['time_since_start'] + 1

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

def sts_check(poses, target) -> float:
    check_seated = True
    count = -1
    for pose in poses:
        time_since_start = pose['time_since_start']
        pose = {kp['name']: kp for kp in pose['keypoints']}
        wrist_height = pose['left_wrist']['y']
        hip_height = pose['left_hip']['y']
        if (wrist_height > hip_height):
            # Hands must be on shoulders throughout exercise.
            # This seems backwards, but this check is checking that hands are above hips
            # or else the rep count is reset.
            count = -1
            check_seated = True
        knee_flexion = calc_joint_angle(pose['left_ankle'], pose['left_knee'], pose['left_hip'])
        if check_seated:
            if knee_flexion <= 90:
                check_seated = False
                count += 1
            if count == target:
                return time_since_start
        elif knee_flexion >= 145:
            check_seated = True
        print(count)
    return poses[-1]['time_since_start'] + 1

def run_single_sts_check(poses) -> float:
    return sts_check(poses, 1)

def run_five_sts_check(poses) -> float:
    return sts_check(poses, 5)

