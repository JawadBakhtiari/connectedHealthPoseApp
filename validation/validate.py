#!/usr/bin/env python3

import os
import sys
import json
import math
import curses
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from exercises.exercise import Exercise
from redirect_output import redirect_output
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
        compare_results(mobile_pose_dir + pid + '/', exercise_name, pid, 'mobile')
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
            validate_sts()
            num_files = len(os.listdir(current_lab_dir))
            file_count = 1
            for lab_file in os.listdir(current_lab_dir):
                output_progress(stdscr, opscr.get_height(), opscr.get_width(), 'validating exercise', file_count, num_files, participant_count, num_participants, lab_file)
                validate_exercise(lab_file, current_lab_dir, pid)
                file_count += 1
        elif selected_exercise == 'sit to stand':
            validate_sts()
        else:
            lab_file = '_'.join(selected_exercise.split()) + '.json'
            output_progress(stdscr, opscr.get_height(), opscr.get_width(), 'validating exercise', 1, 1, participant_count, num_participants, lab_file)
            validate_exercise(lab_file, current_lab_dir, pid)
        participant_count += 1

def validate_sts_dir(mobile_data_type: str) -> None:
    mobile_dir = mobile_data_type if mobile_data_type == 'frontend' else f'backend/{mobile_data_type}'
    mobile_dir = target_dir + f'/mobile/poses/{mobile_dir}/'
    for pid in os.listdir(mobile_dir):
        for pose_file in os.listdir(mobile_dir + f'{pid}/'):
            if pose_file.startswith('sts'):
                lab_filepath = target_dir + f'/lab/sts/formatted/{pid}/sts.mot'
                mobile_filepath = mobile_dir + f'{pid}/{pose_file}'
                generate_sts_comparison_graph(
                    lab_filepath,
                    mobile_filepath,
                    pid,
                    mobile_data_type + pose_file[len('sts'):-len('.json')]
                )

def validate_sts() -> None:
    if selected_pose_data in ['uncalibrated backend', 'all']:
        validate_sts_dir('uncalibrated')
    if selected_pose_data in ['calibrated backend', 'all']:
        validate_sts_dir('calibrated')
    if selected_pose_data in ['mobile', 'all']:
        validate_sts_dir('frontend')

def calc_joint_angle(initial_side: dict, vertex: dict, terminal_side: dict):
    v1 = (vertex['x'] - initial_side['x'], vertex['y'] - initial_side['y'])
    v2 = (vertex['x'] - terminal_side['x'], vertex['y'] - terminal_side['y'])

    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle_radians = math.acos(cos_angle)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def generate_sts_comparison_graph(
    lab_filepath: str,
    mobile_filepath: str,
    pid: str,
    mobile_data_type: str
    ) -> None:
    save_dir = target_dir + f'/results/sts_graphs/{pid}/'
    os.makedirs(save_dir, exist_ok=True)
    with open(os.devnull, 'w') as null:
        with redirect_output(null):
            ik = pd.read_csv(lab_filepath, delim_whitespace=True, skiprows=10)
    lab_knee_angles = ik['knee_angle_r']
    with open(mobile_filepath) as f:
        poses = json.load(f)

    mobile_knee_angles = []
    for pose in poses:
        pose = {kp['name']: kp for kp in pose['keypoints']}
        try:
            hip = pose['right_hip']
            knee = pose['right_knee']
            ankle = pose['right_ankle']
            mobile_knee_angles.append(180 - calc_joint_angle(hip, knee, ankle))
        except:
            continue

    time_lab = np.linspace(0, 1, len(lab_knee_angles))
    time_mobile = np.linspace(0, 1, len(mobile_knee_angles))
    interpolator = PchipInterpolator(time_mobile, mobile_knee_angles)
    interpolated_mobile_knee_angles = interpolator(time_lab)
    plt.plot(time_lab, lab_knee_angles, label='opensim')
    plt.plot(time_lab, interpolated_mobile_knee_angles, label='pose_estimation')
    plt.xlabel('Relative Time')
    plt.ylabel('Knee Flexion Angle')
    plt.title(f'opensim vs pose estimation ({mobile_data_type})')
    plt.legend()
    plt.savefig(f'{save_dir}{mobile_data_type}.png')

########################################################################
############################ run script ################################
########################################################################
if __name__ == "__main__":
    goto_start()
########################################################################
########################################################################

