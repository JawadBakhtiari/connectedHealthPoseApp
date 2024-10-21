import os
import math
import pandas as pd
from datetime import datetime
from typing import Union
from collections import defaultdict
from . import const

class LabDataFormatter:
  '''
  Format motion capture lab data from a csv file to a common format
  for comparison with mobile data. 
  '''

  def __init__(
    self,
    filepath: str,
    exercise_start: float | None = None,
    exercise_end: float | None = None
  ) -> None:
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file '{filepath}' does not exist")
    self.recording_start = LabDataFormatter.__recording_start(filepath)
    self.exercise_start = exercise_start
    self.exercise_end = exercise_end
    self.data = self.__preprocess(filepath)
    self.nan_keypoints = defaultdict(int)


  @staticmethod
  def __recording_start(filepath: str) -> float:
    '''
    Args:
      filepath: path to csv file containing motion capture lab data.

    Returns:
      Start time of the recording as a POSIX timestamp
    '''
    headers = pd.read_csv(filepath, nrows=1)
    start_time_str = headers.columns.tolist()[const.LAB_START_TIME_INDEX]
    start_time_dt = datetime.strptime(start_time_str, const.LAB_START_TIME_FORMAT)
    return start_time_dt.timestamp()


  def __preprocess(self, filepath: str) -> pd.DataFrame:
    '''
    Remove rotation columns and any all-null rows.
    Return only rows within exercise capture.

    Args:
      filepath: path to csv file containing motion capture lab data.

    Returns:
      pandas dataframe representing the motion capture data from the
      given csv file after preprocessing.
    '''
    data = pd.read_csv(filepath, skiprows=3, low_memory=False)

    # 'Name' column contains the timestamps, and must be added back in.
    position_cols = ['Name'] + data.columns[data.iloc[1] == 'Position'].tolist()
    rows_with_data = ~data.iloc[:, 2:].isna().all(axis=1)
    data = data[rows_with_data][position_cols].iloc[3:]

    # filter out rows not in exercise
    if self.exercise_start and self.exercise_end:
        timestamps = pd.to_numeric(data['Name'])
        exercise_mask = (timestamps > self.exercise_start) & (timestamps < self.exercise_end)
        data = data[exercise_mask]

    return data


  @staticmethod
  def __convert_elapsed_time(elapsed_time_str: str) -> Union[float, None]:
    '''
    Convert elapsed_time string to float.

    Args:
      elapsed_time: time since recording started.

    Returns:
      float representing time since recording started if conversion
      is successful and the result is a number, None otherwise.
    '''
    try:
      elapsed_time = float(elapsed_time_str)
      return elapsed_time if not math.isnan(elapsed_time) else None
    except:
      return None


  @staticmethod
  def __create_formatted_keypoint(row: pd.Series, lab_keypoint: str) -> dict:
    '''
    Format the lab data for a keypoint.

    Args:
      row: the current row in the lab data.
      lab_keypoint: the name of the keypoint in the lab data.

    Returns:
      A dictionary representing this keypoints data in the desired formatting
      for comparison with mobile data.

    Raises:
      Value error if x, y or z for given keypoint in given row are nan.
    '''
    x = float(row[lab_keypoint + const.X_SUFFIX])
    y = float(row[lab_keypoint + const.Y_SUFFIX])
    z = float(row[lab_keypoint + const.Z_SUFFIX])

    if math.isnan(x) or math.isnan(y) or math.isnan(z):
      raise ValueError(f'x: {x}, y: {y} or z: {z} value is not a number for keypoint {lab_keypoint}')

    return {
      'x': x,
      'y': y,
      'z': z,
      'name': const.KEYPOINT_MAPPINGS.get(lab_keypoint)
    }


  def add_nan_keypoint(self, lab_keypoint: str) -> None:
    '''
    Increment the count for the number of times that a given keypoint has
    been nan for a frame.

    Args:
      lab_keypoint: the name of the keypoint that was nan in a frame.
    '''
    self.nan_keypoints[lab_keypoint] += 1


  def print_nan_keypoints(self) -> None:
    '''Print the number of frames in which each keypoint was nan.'''
    if self.nan_keypoints == {}:
      print('no keypoints were nan in any frames :)')
      return

    sorted_nan_keypoints = dict(
        sorted(
          self.nan_keypoints.items(),
          key=lambda i: i[1],
          reverse=True
        )
    )
    for kp, times_nan in sorted_nan_keypoints.items():
      translated_name = const.KEYPOINT_MAPPINGS.get(kp)
      percent_nan = int((times_nan / len(self.data)) * 100)
      print(f'{kp} ({translated_name})\t-> nan {times_nan} times ({percent_nan}%)')


  def log(self) -> None:
    '''Print logging information collected during formatting process.'''
    print('\nLAB DATA FORMATTING LOG')
    print('=======================')
    self.print_nan_keypoints()
    print('=======================\n')


  def format(self) -> list:
    '''
    Format lab data so that it is in a common formatting for comparison
    with mobile data.

    Returns:
      list of formatted keypoints.
    '''
    poses = []
    for _, row in self.data.iterrows():
      time_since_start = LabDataFormatter.__convert_elapsed_time(row['Name'])
      if not time_since_start:
        continue
      if self.exercise_start:
        time_since_start -= self.exercise_start

      pose = {
        'time_since_start': time_since_start,
        'keypoints': []
      }

      # Build the formatted keypoints for this pose.
      for kp in const.LAB_KEYPOINTS:
        try:
          new_formatted_kp = LabDataFormatter.__create_formatted_keypoint(row, kp)
        except ValueError:
          # If any keypoints cannot be formatted, skip this pose.
          self.add_nan_keypoint(kp)
          break
        pose['keypoints'].append(new_formatted_kp)
      else:
        poses.append(pose)
    self.log()
    return poses

