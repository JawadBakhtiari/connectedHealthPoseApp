import os
import pandas as pd

class LabDataFormatter:
  def __init__(self, filepath: str) -> None:
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file {filepath} does not exist")
    self.data = LabDataFormatter.__preprocess(filepath)
 
  @staticmethod
  def __preprocess(filepath: str) -> pd.DataFrame:
    '''Remove rotation columns and any all null rows.'''
    data = pd.read_csv(filepath, skiprows=3)
    rows_with_data = ~data.iloc[:, 2:].isna().all(axis=1)
    data = data[rows_with_data]
    position_cols = data.columns[data.iloc[1] == 'Position']
    return data[position_cols]

  def format() -> list:
    pass
  
  def get_data(self) -> pd.DataFrame:
    return self.data
