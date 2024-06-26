import os
import math
import pandas as pd
from datetime import datetime
from typing import Union
from . import const

class LabDataFormatter:
  '''
    Format motion capture lab data from a csv file to match the
    formatting of motion capture data from our mobile app. 
  '''

  def __init__(self, filepath: str) -> None:
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file {filepath} does not exist")
    self.data = LabDataFormatter.__preprocess(filepath)
    self.start_time = LabDataFormatter.__get_start_time(filepath)

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
    x = row[lab_keypoint + const.X_SUFFIX]
    y = row[lab_keypoint + const.Y_SUFFIX]
    z = row[lab_keypoint + const.Z_SUFFIX]

    if not x or not y or not z:
      raise ValueError('x, y or z value is not a number')

    return {
      'x': x,
      'y': y,
      'z': z,
      'name': const.KEYPOINT_MAPPINGS.get(lab_keypoint)
    }

  def format(self) -> list:
    '''
      Format lab data to match the formatting of our mobile app data.

      Returns:
        list of keypoints for this recording using the same data structure
        as our mobile data. 
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
        except:
          # If any keypoints cannot be formatted, skip this pose.
          break
        pose['keypoints'].append(new_formatted_kp)
      else:
        poses.append(pose)

    return poses
 