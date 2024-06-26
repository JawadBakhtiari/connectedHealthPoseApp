#!/usr/bin/env python3

from labdataformatter import LabDataFormatter

filepath = 'exampleData/firstSampleSitToStand/livabilityLabPoses.csv'

def run():
  ldf = LabDataFormatter(filepath)
  ldf.format()

if __name__ == "__main__":
  run()
