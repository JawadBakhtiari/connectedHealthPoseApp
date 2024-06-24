#!/usr/bin/env python3
from functools import reduce
import numpy as np

'''Trying out some different methods for validation.'''

FACTOR = 10

mobile_ys = [
  98.73078761334244,
  64.96097916316998,
  71.87025256282408,
  97.77277611396866,
  64.99816076243849,
  98.62037189373348,
  68.36240226025112,
  73.52253692486524,
  97.39269258228084,
]

inverted_mobile_ys = [
  98.73078761334244,
  132.5005960635149,
  125.59132266386081,
  99.68879911271623,
  132.4634144642464,
  98.84120333295141,
  129.09917296643377,
  123.93903830181965,
  100.06888264440404,
]

lab_ys = [
  1006.177063,
  1393.190063,
  1282.140869,
  1028.449463,
  1392.183228,
  1016.626709,
  1325.929932,
  1319.566772,
  1027.943359,
]


def scale_mobile_ys(mobile_ys: list, factor: float) -> list:
  '''Scale up mobile data y values so values are in a similar range to lab data.'''
  return list(map(lambda y : y * factor, mobile_ys))


def calc_percentage_diff(first: float, second: float) -> float:
  return abs(((first - second) / first) * 100)


def calc_percentage_changes(data: list):
  '''
    Calculate the percentage change from each point to the next in each system.
    Return these values as a list.
  '''
  return [calc_percentage_diff(data[i], data[i+1]) for i in range(len(data) - 1)]


def compare_percentage_change(mobile_percentage_changes: list, lab_percentage_changes: list) -> float:
  '''
    Find the difference in percentage change at each point between lab and mobile data.
    Return the average of these differences.
  '''
  diffs = [abs(m - l) for m, l in zip(mobile_percentage_changes, lab_percentage_changes)]
  return {
      'median' : sorted(diffs)[len(diffs) // 2],
      'average': sum(diffs) / len(diffs)
    }

def compare_absolute_differences(mobile_ys: list, lab_ys: list) -> float:
  mobile_ys = scale_mobile_ys(mobile_ys, FACTOR)
  last = None
  diffs = []
  for my, ly in list(zip(mobile_ys, lab_ys)):
    if last:
      last_my, last_ly = last
      diff_lab = abs(last_ly - ly)
      diff_mobile = abs(last_my - my)
      diffs.append(abs(diff_lab - diff_mobile))
    last = (my, ly)
  return reduce(lambda a, b: a + b, diffs) / len(diffs) 


def huber_loss(y_true, y_pred, delta):
    residual = y_true - y_pred
    loss = np.where(np.abs(residual) < delta, 0.5 * residual**2, delta * (np.abs(residual) - 0.5 * delta))
    return np.mean(loss)


def find_median_scale_factor(mobile_ys: list, lab_ys: list) -> float:
  factors = sorted([l / m for m, l in zip(mobile_ys, lab_ys)])
  return factors[len(factors) // 2]

def find_median_distance_scale_factor(mobile_distances: list, lab_distances: list) -> float:
  distance_factors = sorted([l / m for m, l in zip(mobile_distances, lab_distances)])
  return distance_factors[len(distance_factors) // 2]

def compare_absolute_differences_v2(mobile_ys: list, lab_ys: list) -> float:
  '''
    This version uses the mobile data after inversion (this is easier to work with
    as now it has the same shape as the lab data).
    This version also calculates a median scale factor across the data set, to reduce
    the risk of outliers skewing results.
  '''
  scale_factor = find_median_scale_factor(mobile_ys, lab_ys)
  diffs = [abs(m * scale_factor - l) for m, l in zip(mobile_ys, lab_ys)]
  return {
    'median' : sorted(diffs)[len(diffs) // 2],
    'average': sum(diffs) / len(diffs)
  }

def percentage_error(mobile_val: float, lab_val: float) -> float:
  return abs(mobile_val - lab_val) / lab_val * 100

def compare_differences_in_distance(mobile_ys: list, lab_ys: list) -> float:
  '''
    Calculate the median and average percentage error in distances between each keypoint
    computed by the mobile app vs the lab motion capture.
  '''
  mobile_distances = [abs(mobile_ys[i] - mobile_ys[i + 1]) for i in range(len(mobile_ys) - 1)]
  lab_distances = [abs(lab_ys[i] - lab_ys[i + 1]) for i in range(len(lab_ys) - 1)]
  distance_scale_factor = find_median_distance_scale_factor(mobile_distances, lab_distances)
  # point_scale_factor = find_median_scale_factor(mobile_ys, lab_ys)
  diffs = [percentage_error(md * distance_scale_factor, ld) for md, ld in zip(mobile_distances, lab_distances)]
  return {
    'median' : sorted(diffs)[len(diffs) // 2],
    'average': sum(diffs) / len(diffs)
  } 


#####################################################################################################
###########################################VALIDATION################################################
#####################################################################################################
mobile_percentage_changes = calc_percentage_changes(mobile_ys) 
lab_percentage_changes = calc_percentage_changes(lab_ys)
# delta = 0.6 # for huber loss

absolute_diff_v2 = compare_absolute_differences_v2(inverted_mobile_ys, lab_ys)
keypoint_percentage_diffs = compare_percentage_change(mobile_percentage_changes, lab_percentage_changes)
# hl = huber_loss(np.array(lab_percentage_changes), np.array(mobile_percentage_changes), delta)
distance_percentage_diffs = compare_differences_in_distance(inverted_mobile_ys, lab_ys)

print("========================================")
print("================RESULTS=================")
print("========================================")
print("average absolute diff (keypoints) v2:", f"\t{absolute_diff_v2.get('average'):.2f}cm")
print("median absolute diff (keypoints) v2:", f"\t{absolute_diff_v2.get('median'):.2f}cm")
print("average percentage error (keypoints):", f"\t{keypoint_percentage_diffs.get('average'):.2f}%")
print("median percentage error (keypoints):", f"\t{keypoint_percentage_diffs.get('median'):.2f}%")
print("median percentage error (distance):", f"\t{distance_percentage_diffs.get('median'):.2f}%")
print("average percentage error (distance):", f"\t{distance_percentage_diffs.get('average'):.2f}%")
print("========================================")

#####################################################################################################
#####################################################################################################
