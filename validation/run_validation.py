#!/usr/bin/env python3

import json
from format.labdataformatter import LabDataFormatter

filepath = 'exampleData/firstSampleSitToStand/livabilityLabPoses.csv'

def run():
  ldf = LabDataFormatter(filepath)
  lab_data = ldf.format()
  with open('test.json', 'w') as f:
    json.dump(lab_data, f, indent=4)

if __name__ == "__main__":
  run()
