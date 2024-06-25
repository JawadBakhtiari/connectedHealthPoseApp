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
    # TODO -> rotation cols currently not being filtered out successfully
    position_cols_only = data.loc[:, data.iloc[1] == 'Position']
    rows_with_data = ~position_cols_only.iloc[:, 2:].isna().all(axis=1)
    return data[rows_with_data]
  
  def get_data(self) -> pd.DataFrame:
    return self.data
