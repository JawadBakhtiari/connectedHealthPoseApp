'''Output time when an exercise was completed based on json data from exercise.'''

import networkx as nx
import matplotlib.pyplot as plt
import sys
import json
from exercises.tandem_stand import TandemStand as Exercise

show_error_graph = '-e' in sys.argv
lab_version = 'example_data/20240926/formatted_sbta.json'
mobile_version = 'example_data/random/tandem_stand_balance_thunder.json'

with open(lab_version) as f:
    lab_poses = json.load(f)
with open(mobile_version) as f:
    mobile_poses = json.load(f)

lab_exercise = Exercise(True)
mobile_exercise = Exercise()

lab_finish_time = lab_exercise.run_check(lab_poses)
mobile_finish_time = mobile_exercise.run_check(mobile_poses)

print(f'lab data    -> completed in {lab_finish_time:.2f} seconds')
# print(f'mobile data -> completed in {mobile_finish_time:.2f} seconds')

if show_error_graph:
    fig, ax = plt.subplots()

    for (start, end) in mobile_exercise.get_failing_intervals():
        ax.hlines(y=1, xmin=start, xmax=end, color='blue', linewidth=2, label='mobile')

    for (start, end) in lab_exercise.get_failing_intervals():
        ax.hlines(y=2, xmin=start, xmax=end, color='green', linewidth=2, label='lab')

    ax.set_yticks([1, 2])
    ax.set_yticklabels(['mobile', 'lab'])
    ax.set_xlabel('time')
    ax.set_title('exercise failed intervals (mobile vs lab)')

    # Remove duplicate labels in the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.grid(True)
    plt.show()
