#!/usr/bin/env python3

import json
from format.labdataformatter import LabDataFormatter
from validator import Validator

lab_filepath = 'exampleData/secondSampleSitToStand/sit_to_stand_1.csv'
mobile_filepath = 'exampleData/secondSampleSitToStand/sit_to_stand_1.json'

def run():
  ldf = LabDataFormatter(lab_filepath)
  lab_data = ldf.format()

  with open('test.json', 'w') as f:
    json.dump(lab_data, f, indent=4)

  # NOTE -> bug in method on next line
  start, end = ldf.get_exercise_start_end()
  print(start, end)

  validator = Validator(mobile_filepath, lab_data, start, end)

if __name__ == "__main__":
  run()
