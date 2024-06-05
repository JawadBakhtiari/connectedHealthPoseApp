#!/usr/bin/env python3
# Play around with the formatting of data captured by the livability lab motion capture system

import pandas as pd

filepath = 'exampleData/firstSampleSitToStand/livabilityLabPoses.csv'
NUM_SYNCHRONISATION_MARKERS = 5

def preprocess(filepath: str) -> pd.DataFrame:
  '''Remove null rows from livibility lab data capture.'''
  data = pd.read_csv(filepath, skiprows=3)
  rows_with_data = ~data.iloc[:, 2:].isna().all(axis=1)
  return data[rows_with_data]

def clean_data(filepath: str) -> None:
  '''Currently messy - will clean up once properly implemented.'''
  data = preprocess(filepath)
  headers = data.columns.tolist()
  unlabelled_and_timestamp_cols = [col for col in headers if 'Unlabeled' in col or col == 'Name']
  filtered_data = data[unlabelled_and_timestamp_cols]
  next_row = filtered_data.iloc[0]
  position_cols_only = [col for col in unlabelled_and_timestamp_cols if 'Rotation' not in next_row[col]]
  result = filtered_data[position_cols_only].iloc[3:]

  for _, row in result.iterrows():
    print(row)
    print(len(list(filter(lambda x: x, list(row.drop('Name').isnull())))))
    num_undetected_markers = list(filter(lambda x: x, list(row.drop('Name').isnull()))).sum()
    if num_undetected_markers > NUM_SYNCHRONISATION_MARKERS * 3:
      timestamp = row['Name']
      print("Time when all unlabeled markers are null (and not all markers are null):", timestamp)
      break

def get_joint_at_time(filepath: str) -> None:
  data = pd.read_csv(filepath, skiprows=3)
  headers = [
              'Name',
              'Skeleton 001:LShoulder.4',
              'Skeleton 001:LShoulder.5',
              'Skeleton 001:LShoulder.6'
            ]
  data = data[headers]
  print(data.loc[data['Name'] == 21.550000])

get_joint_at_time(filepath)
