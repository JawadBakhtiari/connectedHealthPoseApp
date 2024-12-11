'''Output time when an exercise was completed based on json data from exercise.'''

import matplotlib.pyplot as plt
import sys
import json
from exercises.walk import Walk as Exercise

show_error_graph = '-e' in sys.argv
exercise = 'walk'
model = 'thunder'
lab_version = f'example_data/20241204/lab/formatted/test_id/{exercise}.json'
mobile_version = f'example_data/20241204/mobile/poses/backend/uncalibrated/test_id/{exercise}_{model}.json'

with open(lab_version) as f:
    lab_poses = json.load(f)
with open(mobile_version) as f:
    mobile_poses = json.load(f)

lab_exercise = Exercise(1000, True)
mobile_exercise = Exercise(1000)

lab_finish_time = lab_exercise.run_check(lab_poses)
mobile_finish_time = mobile_exercise.run_check(mobile_poses)

print(f'lab data    -> completed in {lab_finish_time:.2f} seconds')
print(f'lab data    -> rep times: {lab_exercise.rep_times}')
print(f'lab data    -> failed intervals: {lab_exercise.get_failing_intervals()}')
print()
print(f'mobile data -> completed in {mobile_finish_time:.2f} seconds')
print(f'mobile data -> rep times: {mobile_exercise.rep_times}')
print(f'mobile data -> failed intervals: {mobile_exercise.get_failing_intervals()}')

if show_error_graph:
    fig, ax = plt.subplots()

    for (start, end) in mobile_exercise.get_failing_intervals():
        ax.hlines(y=0.8, xmin=start, xmax=end, color='red', linewidth=4, label='mobile')

    for (start, end) in lab_exercise.get_failing_intervals():
        ax.hlines(y=0.9, xmin=start, xmax=end, color='red', linewidth=4, label='lab')

    ax.set_yticks([0.8, 0.9])
    ax.set_yticklabels(['mobile', 'lab'])
    ax.set_xlabel('time')
    ax.set_title(f'{" ".join(exercise.split("_"))} failed intervals')
    ax.set_ylim(0.25, 1.5)

    plt.grid(True)
    plt.show()

