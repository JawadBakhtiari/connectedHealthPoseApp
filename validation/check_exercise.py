'''Output time when an exercise was completed based on json data from exercise.'''

import json
from exercises.timed_up_and_go import TimedUpAndGo as Exercise

lab_version = 'example_data/20240926/formatted_tuag.json'
mobile_version = 'be_pose_estimation/data/results/20240926/uncalibrated_tuag_thunder.json'

with open(lab_version) as f:
    lab_poses = json.load(f)
with open(mobile_version) as f:
    mobile_poses = json.load(f)

lab_exercise = Exercise()
mobile_exercise = Exercise()

print(f'lab data    -> completed in {lab_exercise.run_check(lab_poses):.2f} seconds')
print(f'mobile data -> completed in {mobile_exercise.run_check(mobile_poses):.2f} seconds')

