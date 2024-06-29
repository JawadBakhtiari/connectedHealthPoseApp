import os
import math
import pandas as pd
from datetime import datetime
from typing import Union
from collections import defaultdict
from . import const
from .util import get_x_y_z_suffixes

class LabDataFormatter:
  '''
    Format motion capture lab data from a csv file to a common format
    for comparison with mobile data. 
  '''

  def __init__(self, filepath: str) -> None:
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file '{filepath}' does not exist")
    self.data = LabDataFormatter.__preprocess(filepath)
    self.start_time = LabDataFormatter.__get_start_time(filepath)
    self.nan_keypoints = defaultdict(int)

  @staticmethod
  def __get_start_time(filepath: str) -> float:
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
 
  @staticmethod
  def __preprocess(filepath: str) -> pd.DataFrame:
    '''
      Remove rotation columns and any all-null rows.
      
      Args:
        filepath: path to csv file containing motion capture lab data.

      Returns:
        pandas dataframe representing the motion capture data from the
        given csv file after preprocessing.
    '''
    data = pd.read_csv(filepath, skiprows=3, low_memory=False)
    rows_with_data = ~data.iloc[:, 2:].isna().all(axis=1)
    data = data[rows_with_data]
    position_cols = data.columns[data.iloc[1] == 'Position']

    # 'Name' column contains the timestamps, and must be added back in
    final_cols = list(position_cols) + ['Name']
    return data[final_cols] 

  @staticmethod
  def __convert_elapsed_time(elapsed_time: str) -> Union[float, None]:
    '''
      Convert elapsed_time string to float.

      Args:
        elapsed_time: time since recording started.

      Returns:
        float representing time since recording started if conversion
        is successful and the result is a number, None otherwise.
    '''
    try:
      elapsed_time = float(elapsed_time)
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
    x_suffix, y_suffix, z_suffix = get_x_y_z_suffixes(lab_keypoint)
    x = float(row[lab_keypoint + x_suffix])
    y = float(row[lab_keypoint + y_suffix])
    z = float(row[lab_keypoint + z_suffix])

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

    for kp, time_nan in self.nan_keypoints.items():
      print(f'{kp} ({const.KEYPOINT_MAPPINGS.get(kp)}) was nan {time_nan} times.')

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
      timestamp = LabDataFormatter.__convert_elapsed_time(row['Name'])
      if not timestamp:
        continue

      pose = {
        'timestamp': self.start_time + timestamp, 
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
 