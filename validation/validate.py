#!/usr/bin/env python3
from functools import reduce
import numpy as np

'''Trying out some different methods for validation.'''

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


def scale_mobile_ys(mobile_ys: list) -> list:
  '''Scale up mobile data y values so values are in a similar range to lab data.'''
  return list(map(lambda y : y * 10, mobile_ys))


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
  percentage_differences = [abs(m - l) for m, l in zip(mobile_percentage_changes, lab_percentage_changes)]
  average_difference = reduce(lambda a, b: a + b, percentage_differences) / len(percentage_differences)
  return average_difference


def huber_loss(y_true, y_pred, delta):
    residual = y_true - y_pred
    loss = np.where(np.abs(residual) < delta, 0.5 * residual**2, delta * (np.abs(residual) - 0.5 * delta))
    return np.mean(loss)



#####################################################################################################
###########################################VALIDATION################################################
#####################################################################################################
mobile_percentage_changes = calc_percentage_changes(mobile_ys) 
lab_percentage_changes = calc_percentage_changes(lab_ys)
delta = 0.6 # for huber loss

average_percentage_diff = compare_percentage_change(mobile_percentage_changes, lab_percentage_changes)
hl = huber_loss(np.array(lab_percentage_changes), np.array(mobile_percentage_changes), delta)

print("==========================")
print("====PERCENTAGE CHANGES====")
print("==========================")
print("mobile percentage changes:", mobile_percentage_changes)
print("lab percentage changes:", lab_percentage_changes)
print("==========================\n")

print("==========================")
print("=========RESULTS==========")
print("==========================")
print("average diff:", average_percentage_diff)
print("huber loss:", hl)
print("==========================")

#####################################################################################################
#####################################################################################################
