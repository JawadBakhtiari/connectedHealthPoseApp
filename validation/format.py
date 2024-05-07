#!/usr/bin/env python3

# Play around with the formatting of data captured by the livability lab motion capture system

import csv

csv_file_path = 'exampleData/example.csv'

def csv_to_dict(filepath: str):
  '''
    Convert csv motion capture data into a list of dictionaries.
    Each dictionary contains frame number, time captured, and x,y,z,w values.
  '''
  with open(filepath) as f:

    # Skip headers
    for _ in range(6):
      next(f)

    # Return frame data
    return list(csv.DictReader(f))


print(csv_to_dict(csv_file_path))
