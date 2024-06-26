import os
import pandas as pd
from datetime import datetime
import const

class LabDataFormatter:
  def __init__(self, filepath: str) -> None:
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file {filepath} does not exist")
    self.data = LabDataFormatter.__preprocess(filepath)
    self.start_time = LabDataFormatter.__get_start_time(filepath)

  @staticmethod
  def __get_start_time(filepath: str) -> float:
    '''
      Extract the start time of the recording and return it
      as a POSIX timestamp.
    '''
    headers = pd.read_csv(filepath, nrows=1)
    start_time_str = headers.columns.tolist()[const.LAB_START_TIME_INDEX]
    start_time_dt = datetime.strptime(start_time_str, const.LAB_START_TIME_FORMAT)
    return start_time_dt.timestamp()
 
  @staticmethod
  def __preprocess(filepath: str) -> pd.DataFrame:
    '''Remove rotation columns and any all null rows.'''
    data = pd.read_csv(filepath, skiprows=3, low_memory=False)
    rows_with_data = ~data.iloc[:, 2:].isna().all(axis=1)
    data = data[rows_with_data]
    position_cols = data.columns[data.iloc[1] == 'Position']

    # 'Name' column contains the timestamps, and must be added back in
    final_cols = list(position_cols) + ['Name']
    return data[final_cols] 

  def format(self) -> list:
    headers = self.data.columns.tolist()
    keypoints = [h for h in headers if any(h.startswith(kp) for kp in const.LAB_KEYPOINTS)]
    print(keypoints)
    for _, row in self.data.iterrows():
      for kp in const.LAB_KEYPOINTS:
        pass

  def get_data(self) -> pd.DataFrame:
    return self.data
