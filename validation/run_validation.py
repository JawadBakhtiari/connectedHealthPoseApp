#!/usr/bin/env python3

import json
from format.labdataformatter import LabDataFormatter

filepath = 'exampleData/secondSampleSitToStand/livabilityLabPoses.csv'

def run():
  ldf = LabDataFormatter(filepath)
  lab_data = ldf.format()
  start, end = ldf.get_exercise_start_end()
  print(f'start and end time for exercise recording: ({start}, {end})')
  with open('test.json', 'w') as f:
    json.dump(lab_data, f, indent=4)

if __name__ == "__main__":
  run()
