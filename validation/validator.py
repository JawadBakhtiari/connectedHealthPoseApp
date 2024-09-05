import os
import json
import math
from typing import List, Tuple
from collections import defaultdict
from statistics import mean, median
import const
from format.labdataformatter import LabDataFormatter

class Validator():
  '''
  Process mobile data and validate it against data captured from optitrack
  lab motion capture system.
  '''

  def __init__(
    self,
    mobile_data_filepath: str,
    lab_data_filepath: str,
  ) -> None:
    if not os.path.exists(mobile_data_filepath):
      raise FileNotFoundError(f"file '{mobile_data_filepath}' does not exist")
    if not os.path.exists(lab_data_filepath):
      raise FileNotFoundError(f"file '{lab_data_filepath}' does not exist")

    self.filtered_out_keypoints = defaultdict(int)
    self.joint_angles = defaultdict(lambda: {'lab': [], 'mobile': []})

    # Format lab data
    ldf = LabDataFormatter(lab_data_filepath)
    self.lab_data = ldf.format()
    start, end = ldf.get_exercise_start_end()

    with open(mobile_data_filepath) as f:
      mobile_data = json.load(f)
    self.mobile_data = self.__preprocess(mobile_data, start, end)


  @staticmethod
  def __sigmoid(x) -> float:
    '''
    Apply the sigmoid function to x (used for converting presence and
    visibility values from mobile data to percentages).

    Returns:
      Result of applying sigmoid function to x (float between 0 and 1).
    '''
    return 1 / (1 + math.exp(-x))


  def filter_keypoints(self, pose: dict) -> dict:
    '''
    Only keep keypoints for each pose that meet a threshold for
    visibility and presence values.

    Note that this means for any given pose in the mobile data,
    any keypoint may not have a value.

    Returns:
      A dict representing the passed in pose containing only
      keypoints with visibility and presence above a defined
      threshold.
    '''
    filtered_keypoints = []
    for kp in pose['keypoints']:
      if (Validator.__sigmoid(kp['visibility']) >= const.VIS_THRESHOLD and
          Validator.__sigmoid(kp['presence']) >= const.PRES_THRESHOLD):
        filtered_keypoints.append(kp)
      else:
        # Add filtered out keypoints to collection for logging.
        self.filtered_out_keypoints[kp['name']] += 1
    pose['keypoints'] = filtered_keypoints
    return pose


  def __preprocess(
    self,
    raw_mobile_data: list,
    exercise_start: float,
    exercise_end:float
  ) -> list:
    '''
    Filter out undesired values from mobile data.

    Returns:
      A list representing the filtered mobile data.
    '''
    # Only retain poses between the start and end of exercise recording.
    in_exercise = (lambda p:
      p['timestamp'] > exercise_start and
      p['timestamp'] < exercise_end
    )
    exercise_mobile_data = list(filter(in_exercise, raw_mobile_data))

    return list(map(self.filter_keypoints, exercise_mobile_data))


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
            # best match for this mpose so far.
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


  @staticmethod
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


  def validate(self, angles: list) -> None:
    # todo -> finish this function
    matches = self.zip()
    for lpose, mpose in matches:
      # NOTE -> this is hacky and inefficient, should keypoint data structure be changed??
      #      -> (making this change could affect visualisation etc.)
      lkps = {kp['name']: kp for kp in lpose['keypoints']}
      mkps = {kp['name']: kp for kp in mpose['keypoints']}
      for angle in angles:
        try:
          # could fail if keypoint not in this pose, skip if this happens
          lab_angle = Validator.calc_joint_angle(
            lkps[angle['initial_side']],
            lkps[angle['vertex']],
            lkps[angle['terminal_side']]
          )
          mobile_angle = Validator.calc_joint_angle(
            mkps[angle['initial_side']],
            mkps[angle['vertex']],
            mkps[angle['terminal_side']]
          )
          self.joint_angles[angle['name']]['lab'].append(lab_angle)
          self.joint_angles[angle['name']]['mobile'].append(mobile_angle)
        except KeyError:
          continue
    self.log()


  def log(self) -> None:
    '''Print logging information collected during validation process'''
    percent_poses_matched = int(self.zipped_length / len(self.mobile_data) * 100)
    print('\nVALIDATION LOG')
    print('==============')
    print(
      f'{self.zipped_length} mobile data poses matched to lab poses ' \
      f'from a potential {len(self.mobile_data)} ({percent_poses_matched}%)'
    )
    print('\n------------------------------------')
    print('-- mobile data keypoint filtering --')
    print('--    on presence & visibility    --')
    print('------------------------------------')
    sorted_keypoints = dict(
      sorted(
        self.filtered_out_keypoints.items(),
        key=lambda i: i[1],
        reverse=True
      )
    )
    for kp, num_filtered in sorted_keypoints.items():
      percent_filtered = int((num_filtered / len(self.mobile_data)) * 100)
      print(f'{kp} \t -> filtered out {num_filtered:>3} times ({percent_filtered}%)')
    print('----------------------------------')
    print('\n------------------------------------')
    print('------- joint angle results -------')
    print('------------------------------------')
    for joint, angles in self.joint_angles.items():
      diffs = [abs(lab - mobile) for lab, mobile in zip(angles['lab'], angles['mobile'])]
      print(f' + {joint}:')
      print(f'\taverage difference (degrees) -> {mean(diffs):.2f}')
      print(f'\tmedian difference  (degrees) -> {median(diffs):.2f}')
    print('----------------------------------')
    print('==============\n')


