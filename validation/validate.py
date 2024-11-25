#!/usr/bin/env python3

import os
import sys
import json
import curses
import matplotlib.pyplot as plt
from exercises.exercise import Exercise
from screen.options_screen import OptionsScreen
from screen.util import output_progress
from screen import const

WELCOME = 'welcome to the validator :)'
POSE_DATA_OPTIONS = ['mobile', 'calibrated backend', 'uncalibrated backend', 'all']
POSE_DATA_HEADER = 'select the type of pose data to be compared with lab data'
END_MESSAGE = 'validation complete, press any key to exit'

if len(sys.argv) != 2:
    print(f'usage: {sys.argv[0]} <path/to/data/directory>')
    exit(1)
target_dir = sys.argv[1]
uncal_backend_pose_dir = target_dir + '/mobile/poses/backend/uncalibrated/'
cal_backend_pose_dir = target_dir + '/mobile/poses/backend/calibrated/'
mobile_pose_dir = target_dir + '/mobile/poses/frontend/'

error_graphs_dir = target_dir + '/results/error_graphs/'
os.makedirs(os.path.dirname(target_dir + '/results/error_graphs/'), exist_ok=True)
results_file = open(target_dir + '/results/results.txt', 'w')

# initialise curses (screen handling library)
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)
opscr = OptionsScreen(stdscr)

selected_pose_data = None
selected_exercise = None

########################################################################
########################### preambles ##################################
########################################################################
def add_header_text(header: str, options: list) -> None:
    stdscr.addstr(
        (opscr.get_height() // 2) - (len(options) // 2) - 2,
        (opscr.get_width() // 2) - (len(header) // 2),
        header
    )

def exercise_preamble() -> None:
    add_header_text(const.EXERCISE_HEADER, const.EXERCISES)

def pose_data_preamble() -> None:
    add_header_text(POSE_DATA_HEADER, POSE_DATA_OPTIONS)

def confirmation_preamble() -> None:
    exercise = 'all exercises' if selected_exercise == 'all' else selected_exercise
    confirmation_text = f'run validation for \'{selected_pose_data}\' data on {exercise}?'
    add_header_text(confirmation_text, const.CONFIRMATION)
########################################################################
########################################################################

########################################################################
############################# jumps ####################################
########################################################################
def goto_exercises():
    opscr.display_options(const.EXERCISES, exercise_preamble, on_enter_exercise)

def goto_confirmation():
    opscr.display_options(const.CONFIRMATION, confirmation_preamble, on_enter_confirmation)

def goto_start():
    opscr.display_instructions(WELCOME)
    opscr.display_options(POSE_DATA_OPTIONS, pose_data_preamble, on_enter_pose_data)
########################################################################
########################################################################

########################################################################
############################# hooks ####################################
########################################################################
def on_enter_exercise() -> None:
    global selected_exercise
    selected_exercise = const.EXERCISES[opscr.get_current_row()]
    goto_confirmation()

def on_enter_pose_data() -> None:
    global selected_pose_data
    selected_pose_data = POSE_DATA_OPTIONS[opscr.get_current_row()]
    goto_exercises()

def on_enter_confirmation() -> None:
    if const.CONFIRMATION[opscr.get_current_row()] == "continue":
        run_validation()
        stdscr.clear()
        stdscr.addstr(opscr.get_height() // 2, opscr.get_width() // 2 - (len(END_MESSAGE) // 2 + 2), END_MESSAGE)
        stdscr.refresh()
        stdscr.getch()
        curses.endwin()
        exit(0)
    else:
        goto_start()
########################################################################
########################################################################

########################################################################
########################### validation #################################
########################################################################
def create_error_graph(
    exercise_name: str,
    mobile_exercise: Exercise,
    lab_exercise: Exercise,
    pid: str,
    data_type: str
    ) -> None:
    _, ax = plt.subplots()

    for (start, end) in mobile_exercise.get_failing_intervals():
        ax.hlines(y=0.8, xmin=start, xmax=end, color='red', linewidth=4, label='mobile')
    for (start, end) in lab_exercise.get_failing_intervals():
        ax.hlines(y=0.9, xmin=start, xmax=end, color='red', linewidth=4, label='lab')

    ax.set_yticks([0.8, 0.9])
    ax.set_yticklabels(['mobile', 'lab'])
    ax.set_xlabel('time')
    ax.set_title(f'{' '.join(exercise_name.split('_'))} failed intervals')
    ax.set_ylim(0.25, 1.5)
    plt.grid(True)

    graph_dir = error_graphs_dir + f'{pid}/{data_type}/'
    os.makedirs(os.path.dirname(graph_dir), exist_ok=True)
    plt.savefig(graph_dir + f'/{exercise_name}.png', dpi=300, bbox_inches='tight')

def compare_results(lab_file_path: str, exercise_name: str, pid: str, data_type: str) -> None:
    pose_dir = cal_backend_pose_dir + pid + '/'
    for pose_file in os.listdir(pose_dir):
        if pose_file.startswith(exercise_name):
            Exercise, arg = const.EXERCISES_TO_CLASSES[' '.join(exercise_name.split('_'))]
            lab_exercise = Exercise(arg, True)
            mobile_exercise = Exercise(arg)
            with open(lab_file_path) as f:
                lab_poses = json.load(f)
            with open(pose_dir + pose_file) as f:
                mobile_poses = json.load(f)

            lab_finish_time = lab_exercise.run_check(lab_poses)
            mobile_finish_time = mobile_exercise.run_check(mobile_poses)

            create_error_graph(exercise_name, mobile_exercise, lab_exercise, pid, data_type)

            print(f'lab data    -> completed in {lab_finish_time:.2f} seconds', file=results_file)
            print(f'lab data    -> rep times: {lab_exercise.rep_times}', file=results_file)
            print(f'lab data    -> failed intervals: {lab_exercise.get_failing_intervals()}', file=results_file)
            print(file=results_file)
            print(f'mobile data -> completed in {mobile_finish_time:.2f} seconds', file=results_file)
            print(f'mobile data -> rep times: {mobile_exercise.rep_times}', file=results_file)
            print(f'mobile data -> failed intervals: {mobile_exercise.get_failing_intervals()}', file=results_file)

def validate_exercise(lab_file: str, current_lab_dir: str, pid: str) -> None:
    exercise_name = lab_file[:-len('.json')]
    print(f'================================================================', file=results_file)
    print(f'======================= VALIDATING {exercise_name} ========================', file=results_file)
    print(f'================================================================\n', file=results_file)
    lab_file_path = current_lab_dir + lab_file
    if selected_pose_data in ['uncalibrated backend', 'all']:
        print('---------------- uncalibrated backend results ------------------', file=results_file)
        compare_results(lab_file_path, exercise_name, pid, 'uncalibrated')
        print('----------------------------------------------------------------\n', file=results_file)
    if selected_pose_data in ['calibrated backend', 'all']:
        print('----------------- calibrated backend results -------------------', file=results_file)
        compare_results(lab_file_path, exercise_name, pid, 'calibrated')
        print('----------------------------------------------------------------\n', file=results_file)
    if selected_pose_data in ['mobile', 'all']:
        print('---------------------- frontend results ------------------------', file=results_file)
        compare_results(mobile_pose_dir + pid + '/', lab_file_path, exercise_name, 'mobile')
        print('----------------------------------------------------------------\n', file=results_file)
    print(f'================================================================', file=results_file)
    print(f'================================================================\n', file=results_file)

def run_validation() -> None:
    formatted_lab_data_dir = target_dir + '/lab/formatted/'
    participant_count = 1
    num_participants = len(os.listdir(formatted_lab_data_dir))
    for pid in os.listdir(formatted_lab_data_dir):
        current_lab_dir = formatted_lab_data_dir + pid + '/'
        if selected_exercise == 'all':
            num_files = len(os.listdir(current_lab_dir))
            file_count = 1
            for lab_file in os.listdir(current_lab_dir):
                output_progress(stdscr, opscr.get_height(), opscr.get_width(), 'validating exercise', file_count, num_files, participant_count, num_participants, lab_file)
                validate_exercise(lab_file, current_lab_dir, pid)
                file_count += 1
        else:
            lab_file = '_'.join(selected_exercise.split()) + '.json'
            output_progress(stdscr, opscr.get_height(), opscr.get_width(), 'validating exercise', 1, 1, participant_count, num_participants, lab_file)
            validate_exercise(lab_file, current_lab_dir, pid)
        participant_count += 1

########################################################################
############################ run script ################################
########################################################################
if __name__ == "__main__":
    goto_start()
########################################################################
########################################################################

