'''Output time when an exercise was completed based on json data from exercise.'''

import json
from exercises.tandem_stand import TandemStand as Exercise

lab_version = 'example_data/20240926/formatted_spin.json'
mobile_version = 'be_pose_estimation/data/results/20240926/uncalibrated_spin_thunder.json'

with open(lab_version) as f:
    poses = json.load(f)

exercise = Exercise()
print(f'exercise completed after {exercise.run_check(poses)} seconds')

