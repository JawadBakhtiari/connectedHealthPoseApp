#!/usr/bin/env python3

import json
from format.labdataformatter import LabDataFormatter
from validator import Validator

lab_filepath = 'example_data/second_sample_sit_to_stand/sit_to_stand_1.csv'
mobile_filepath = 'example_data/second_sample_sit_to_stand/sit_to_stand_1.json'

def run():
  ldf = LabDataFormatter(lab_filepath)
  lab_data = ldf.format()

  with open('test.json', 'w') as f:
    json.dump(lab_data, f, indent=4)

  start, end = ldf.get_exercise_start_end()
  validator = Validator(mobile_filepath, lab_data, start, end)
  zipped_data = validator.zip()
  validator.validate()

  with open('test_zip.json', 'w') as f:
    json.dump(zipped_data, f, indent=4)

if __name__ == "__main__":
  run()
