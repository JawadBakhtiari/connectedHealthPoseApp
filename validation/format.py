#!/usr/bin/env python3
# Play around with the formatting of data captured by the livability lab motion capture system

import pandas as pd
from PIL import Image

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
  print(data.loc[data['Name'] == 33.683333])

def get_image_dimensions(filepath: str) -> tuple:
  with Image.open(filepath) as img:
    width, height = img.size
  return { 'width': width, 'height': height }

def get_pixel_values(keypoints: dict, image_dimensions: dict) -> dict:
  return {
    'x': keypoints.get('x') * image_dimensions.get('width'),
    'y': keypoints.get('y') * image_dimensions.get('height')
  }

def get_real_values(pixel_values: dict, scale_factor: float) -> dict:
  return {
    'x': pixel_values.get('x') * scale_factor,
    'y': pixel_values.get('y') * scale_factor
  }


#######################################################################
############################# CALIBRATION #############################
#######################################################################
'''Convert normalised keypoint values into real world units (cm).'''

image_dimensions = get_image_dimensions('./exampleData/sampleImage.jpg')

# The known distance and pixel distance between two points
# Could measure the distance between width endpoints of the camera view?
known_distance = 361.24  # in cm
pixel_distance = image_dimensions.get('width')
scale_factor = known_distance / pixel_distance


keypoints_list = [
  { 'x': 0.16928645068762274, 'y': -0.44030459023353513 },
  { 'x': 0.17897597532043577, 'y': -0.4176582666896209 },
  { 'x': 0.16916240187325227, 'y': -0.4643509656251208 }
]

for keypoints in keypoints_list:
  pixel_values = get_pixel_values(keypoints, image_dimensions)
  real_values = get_real_values(pixel_values, scale_factor)
  print(real_values)

#######################################################################
#######################################################################
