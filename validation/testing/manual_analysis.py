#!/usr/bin/env python3

'''
Inspecting angles manually, to get an idea of accuracy before
any real effort is put into automating the process

To run this script, cd into teleRehab directory and use command:
  python3 -m validation.testing.manual_analysis
'''
import sys
import os
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from validation.format.labdataformatter import LabDataFormatter
from validation.validator import Validator

lab_filepath = 'validation/example_data/second_sample_sit_to_stand/sit_to_stand_1.csv'
mobile_filepath = 'validation/example_data/second_sample_sit_to_stand/sit_to_stand_1.json'

def calc_angle(kp1, kp2, kp3):
  v1 = (kp2['x'] - kp1['x'], kp2['y'] - kp1['y'])
  v2 = (kp2['x'] - kp3['x'], kp2['y'] - kp3['y'])

  dot_product = v1[0] * v2[0] + v1[1] * v2[1]
  magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
  magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

  cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
  angle_radians = math.acos(cos_angle)
  angle_degrees = math.degrees(angle_radians)
  return angle_degrees

def run():
  ldf = LabDataFormatter(lab_filepath)
  lab_data = ldf.format()
  start, end = ldf.get_exercise_start_end()
  validator = Validator(mobile_filepath, lab_data, start, end)
  zipped_data = validator.zip()
  chunk_size = len(zipped_data) // 10

  num_success = 0
  diffs = []
  for i in range(len(zipped_data)):
    try:
      pose = zipped_data[chunk_size * i]
      lab_kps = [kp for kp in pose[0]['keypoints'] if kp['name'] in ['left_elbow', 'left_shoulder', 'left_hip']]
      mobile_kps = [kp for kp in pose[1]['keypoints'] if kp['name'] in ['left_elbow', 'left_shoulder', 'left_hip']]
      ma = calc_angle(mobile_kps[1], mobile_kps[0], mobile_kps[2])
      la = calc_angle(lab_kps[1], lab_kps[0], lab_kps[2])
      print(ma)
      print(la)
      print()
      diffs.append(abs(ma - la))
      num_success += 1
    except:
      continue
    if num_success >= 9:
      break
  print(f'median diff: {sorted(diffs)[len(diffs) // 2]}')
  print(f'average diff: {sum(diffs) / len(diffs)}')

if __name__ == "__main__":
  run()

