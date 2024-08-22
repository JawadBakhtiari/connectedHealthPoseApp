#!/usr/bin/env python3

from validator import Validator

lab_data_filepath = 'example_data/second_sample_sit_to_stand/sit_to_stand_1.csv'
mobile_data_filepath = 'example_data/second_sample_sit_to_stand/sit_to_stand_1.json'

def run():
  validator = Validator(mobile_data_filepath, lab_data_filepath)
  validator.validate()

if __name__ == "__main__":
  run()
