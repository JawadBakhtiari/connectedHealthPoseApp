'''Output time when an exercise was completed based on json data from exercise.'''

import json
from exercises.timed_up_and_go import TimedUpAndGo as Exercise

lab_version = 'example_data/20240926/formatted_tuag.json'
mobile_version = 'be_pose_estimation/data/results/20240926/uncalibrated_tuag_thunder.json'

with open(lab_version) as f:
    poses = json.load(f)

exercise = Exercise()
print(f'exercise completed after {exercise.run_check(poses)} seconds')

