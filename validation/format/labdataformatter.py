import os
import re
import math
import pandas as pd
from datetime import datetime, timedelta
from typing import Union, Tuple
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
    self.recording_start = LabDataFormatter.__recording_start(filepath)
    self.data = self.__preprocess(filepath)
    self.nan_keypoints = defaultdict(int)

  def get_exercise_start_end(self) -> Tuple[float, float]:
    '''
    Return the start and end time of exercise capture as 13 digit posix
    timestamps (to match formatting of mobile data timestamps).

    Returns:
      (start: float, end: float)
    '''
    return (
      int((self.recording_start + self.exercise_start) * 1000),
      int((self.recording_start + self.exercise_end) * 1000)
    )

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

  @staticmethod
  def __exercise_start_end(data: pd.DataFrame) -> Tuple[float, float]:
    '''
    Return the start and end time of exercise capture, in terms of the number
    of seconds elapsed since the recording started.

    Returns:
      (start: float, end: float)
    '''
    sync_cols = ['Name'] + [c for c in data.columns.tolist() if re.match(const.SYNC_MARKER_NAME, c)]
    sync_data = data[sync_cols]
    exercise_capture_rows = sync_data.iloc[:, 1:].isna().all(axis=1)
    start = sync_data[exercise_capture_rows].iloc[0]['Name']
    end = sync_data[exercise_capture_rows].iloc[-1]['Name']
    return (float(start), float(end))

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

    # Set start and end of exercise capture + filter out rows not in this range
    self.exercise_start, self.exercise_end = LabDataFormatter.__exercise_start_end(data)
    timestamps = pd.to_numeric(data['Name'])
    exercise_mask = (timestamps > self.exercise_start) & (timestamps < self.exercise_end)

    return data[exercise_mask] 

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
        'timestamp': int((self.recording_start + timestamp) * 1000), 
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
 
