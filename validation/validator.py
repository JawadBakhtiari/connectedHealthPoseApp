import os
import json
import math
from typing import List, Tuple
import const

class Validator():
  '''
  Process mobile data and validate it against data captured from optitrack
  lab motion capture system.
  '''

  def __init__(self, filepath: str, lab_data: list, exercise_start: float, exercise_end: float):
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file '{filepath}' does not exist")
    self.lab_data = lab_data

    with open(filepath) as f:
      mobile_data = json.load(f)
    self.mobile_data = Validator.__preprocess(mobile_data, exercise_start, exercise_end)

  @staticmethod
  def __sigmoid(x) -> float:
    '''
    Apply the sigmoid function to x (used for converting presence and
    visibility values from mobile data to percentages).

    Returns:
      Result of applying sigmoid function to x (float between 0 and 1).
    '''
    return 1 / (1 + math.exp(-x))

  @staticmethod
  def __preprocess(raw_mobile_data: list, exercise_start: float, exercise_end:float) -> list:
    '''
    Filter out undesired values from mobile data.

    Returns:
      A list representing the filtered mobile data.
    '''
    # Only retain poses between the start and end of exercise recording.
    in_exercise = lambda p: p['timestamp'] > exercise_start and p['timestamp'] < exercise_end
    exercise_mobile_data = list(filter(in_exercise, raw_mobile_data))

    def filter_keypoints(pose: dict) -> dict:
      '''
      Only keep keypoints for each pose that meet a threshold for
      visibility and presence values.

      Note that this means for any given pose in the mobile data,
      any keypoint may not have a value.
      '''
      pose['keypoints'] = [
        kp for kp in pose['keypoints']
        if (Validator.__sigmoid(kp['visibility']) >= const.VIS_THRESHOLD and
            Validator.__sigmoid(kp['presence']) >= const.PRES_THRESHOLD)
      ]
      return pose

    return list(map(filter_keypoints, exercise_mobile_data))

  def zip(self) -> List[Tuple[dict, dict]]:
    '''
    Zip poses from lab and mobile data together with their closest match
    (temporally) within a set threshold.

    Returns:
      A list of matches in the form [(lab_pose), (mobile_pose)].
    '''
    j = 0
    zipped = []
    for mpose in self.mobile_data:
      best_pair = None
      best_time_diff = None
      while j < len(self.lab_data):
        lpose = self.lab_data[j]
        time_diff = abs(mpose.get('timestamp') - lpose.get('timestamp'))
        if time_diff < const.TIME_DIFF_THRESHOLD:
          if not best_time_diff or time_diff < best_time_diff:
            # best match for this mkp so far.
            best_time_diff = time_diff
            best_pair = (lpose, mpose)
          if lpose.get('timestamp') > mpose.get('timestamp'):
            # no better matches to be found after this point
            if best_pair:
              zipped.append(best_pair)
            if best_time_diff == time_diff:
              # move to next lab pose if this one was used
              j += 1
            break
        elif lpose.get('timestamp') > mpose.get('timestamp'):
          break
        j += 1

    # record length for logging + return zipped list
    self.zipped_length = len(zipped)
    return zipped

  def log(self) -> None:
    '''Print logging information collected during validation process'''
    print('\nVALIDATION LOG')
    print('==============')
    print(f'{self.zipped_length} mobile data poses matched from a potential {len(self.mobile_data)} ({int(self.zipped_length / len(self.mobile_data) * 100)}%)')
    print('==============\n')

  def validate(self) -> None:
    self.log()

