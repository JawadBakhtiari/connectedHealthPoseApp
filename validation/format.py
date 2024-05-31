#!/usr/bin/env python3

# Play around with the formatting of data captured by the livability lab motion capture system

import pandas as pd

filepath = 'exampleData/firstSampleSitToStand/livabilityLabPoses.csv'

def clean_data(filepath: str):
  '''Currently messy - will clean up once properly implemented.'''
  baseline_data = pd.read_csv(filepath, skiprows=6).iloc[:, 1:]

  data = pd.read_csv(filepath, skiprows=3)
  headers = data.columns.tolist()
  unlabeled_cols = [col for col in headers if 'Unlabeled' in col]
  unlabeled_cols.append('Name')
  filtered_data = data[unlabeled_cols]
  next_row = filtered_data.iloc[0]
  position_cols_only = [col for col in unlabeled_cols if 'Rotation' not in next_row[col]]
  result = filtered_data[position_cols_only].iloc[3:]

  for _, row in result.iterrows():
    if row.drop('Name').isnull().all():
      timestamp = row['Name']
      all_other_vals_at_this_time = baseline_data[baseline_data.iloc[:, 0] == float(timestamp)]
      all_null = all_other_vals_at_this_time.iloc[:, 1:].isnull().all(axis=1).all()
      if not all_null:
        # make sure that data capture has not faulted at this time
        print("Time when all unlabeled markers are null (and not all markers are null):", timestamp)
        break

clean_data(filepath)
