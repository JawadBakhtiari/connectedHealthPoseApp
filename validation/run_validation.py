#!/usr/bin/env python3

from format.labdataformatter import LabDataFormatter
from validator import Validator

lab_filepath = 'example_data/second_sample_sit_to_stand/sit_to_stand_1.csv'
mobile_filepath = 'example_data/second_sample_sit_to_stand/sit_to_stand_1.json'

def run():
  ldf = LabDataFormatter(lab_filepath)
  lab_data = ldf.format()

  start, end = ldf.get_exercise_start_end()
  validator = Validator(mobile_filepath, lab_data, start, end)
  validator.zip()
  validator.validate()

if __name__ == "__main__":
  run()
