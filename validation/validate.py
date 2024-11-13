#!/usr/bin/env python3

import os
import sys
import json
import curses
from exercises.exercise import Exercise
from options_screen import OptionsScreen

WELCOME = 'welcome to the validator :)'
POSE_DATA_OPTIONS = ['mobile', 'calibrated backend', 'uncalibrated backend', 'all']
EXERCISES = ['bent over rows', 'bicep curls', 'dartboard', 'shoulder taps', 'side bend', 'spin', 'tandem stand', 'tandem walk', 'timed up and go', 'walk', 'all']
EXERCISE_HEADER = 'select an exercise (or all)'
POSE_DATA_HEADER = 'select the type of pose data to be compared with lab data'
CONFIRMATION = ['continue', 'back']
END_MESSAGE = 'validation complete, press any key to exit'

if len(sys.argv) != 2:
    print(f'usage: {sys.argv[0]} <path/to/data/directory>')
    exit(1)
target_dir = sys.argv[1]
uncal_backend_pose_dir = target_dir + '/mobile/poses/backend/uncalibrated/'
cal_backend_pose_dir = target_dir + '/mobile/poses/backend/calibrated/'
mobile_pose_dir = target_dir + '/mobile/poses/frontend/'
os.makedirs(os.path.dirname(target_dir + '/results/'), exist_ok=True)
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
    add_header_text(EXERCISE_HEADER, EXERCISES)

def pose_data_preamble() -> None:
    add_header_text(POSE_DATA_HEADER, POSE_DATA_OPTIONS)

def confirmation_preamble() -> None:
    exercise = 'all exercises' if selected_exercise == 'all' else selected_exercise
    confirmation_text = f'run validation for \'{selected_pose_data}\' data on {exercise}?'
    add_header_text(confirmation_text, CONFIRMATION)
########################################################################
########################################################################

########################################################################
############################# jumps ####################################
########################################################################
def goto_exercises():
    opscr.display_options(EXERCISES, exercise_preamble, on_enter_exercise)

def goto_confirmation():
    opscr.display_options(CONFIRMATION, confirmation_preamble, on_enter_confirmation)

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
    selected_exercise = EXERCISES[opscr.get_current_row()]
    goto_confirmation()

def on_enter_pose_data() -> None:
    global selected_pose_data
    selected_pose_data = POSE_DATA_OPTIONS[opscr.get_current_row()]
    goto_exercises()

def on_enter_confirmation() -> None:
    if CONFIRMATION[opscr.get_current_row()] == "continue":
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

def output_progress(
    action_title: str,
    file_count: int,
    num_files: int,
    participant_count: int,
    num_participants: int,
    filename: str) -> None:
    stdscr.clear()
    progress_text = f'{action_title} {file_count}/{num_files} for participant {participant_count}/{num_participants} ...'
    stdscr.addstr(opscr.get_height() // 2, opscr.get_width() // 2 - (len(progress_text) // 2 + 2), progress_text)
    stdscr.refresh()
    print(f'processing {filename} ...')

from exercises.bent_over_rows import BentOverRows
from exercises.bicep_curls import BicepCurls
from exercises.dartboard import Dartboard
from exercises.shoulder_taps import ShoulderTaps
from exercises.side_bend import SideBend
from exercises.spin import Spin
from exercises.tandem_stand import TandemStand
from exercises.tandem_walk import TandemWalk
from exercises.timed_up_and_go import TimedUpAndGo
from exercises.walk import Walk
EXERCISES_TO_CLASSES = {
    'bent over rows': (BentOverRows, 12),
    'bicep curls': (BicepCurls, 12),
    'dartboard': (Dartboard, 1),
    'shoulder taps': (ShoulderTaps, 12),
    'side bend': (SideBend, 12),
    'spin': (Spin, 1),
    'tandem stand': (TandemStand, None),
    'tandem walk': (TandemWalk, 1600),
    'timed up and go': (TimedUpAndGo, 1600),
    'walk': (Walk, 1600),
}

def compare_results(pose_dir: str, lab_file_path: str, exercise_name: str) -> None:
    for pose_file in os.listdir(pose_dir):
        if pose_file.startswith(exercise_name):
            Exercise, arg = EXERCISES_TO_CLASSES[' '.join(exercise_name.split('_'))]
            lab_exercise = Exercise(arg, True)
            mobile_exercise = Exercise(arg)
            with open(lab_file_path) as f:
                lab_poses = json.load(f)
            with open(pose_dir + pose_file) as f:
                mobile_poses = json.load(f)

            lab_finish_time = lab_exercise.run_check(lab_poses)
            mobile_finish_time = mobile_exercise.run_check(mobile_poses)

            print(f'lab data    -> completed in {lab_finish_time:.2f} seconds', file=results_file)
            print(f'lab data    -> rep times: {lab_exercise.rep_times}', file=results_file)
            print(f'lab data    -> failed intervals: {lab_exercise.get_failing_intervals()}', file=results_file)
            print(file=results_file)
            print(f'mobile data -> completed in {mobile_finish_time:.2f} seconds', file=results_file)
            print(f'mobile data -> rep times: {mobile_exercise.rep_times}', file=results_file)
            print(f'mobile data -> failed intervals: {mobile_exercise.get_failing_intervals()}', file=results_file)

def run_validation() -> None:
    formatted_lab_data_dir = target_dir + '/lab/formatted/'
    participant_count = 1
    num_participants = len(os.listdir(formatted_lab_data_dir))
    for pid in os.listdir(formatted_lab_data_dir):
        file_count = 1
        current_lab_dir = formatted_lab_data_dir + pid + '/'
        num_files = len(os.listdir(current_lab_dir))
        mobile_pose_dir = target_dir + '/mobile/poses/frontend/' + pid + '/'
        for lab_file in os.listdir(current_lab_dir):
            output_progress('validating exercise', file_count, num_files, participant_count, num_participants, lab_file)
            exercise_name = lab_file[:-len('.json')]
            lab_file_path = current_lab_dir + lab_file
            if selected_pose_data in ['uncalibrated backend', 'all']:
                print('-------------------- uncalibrated backend results ---------------------', file=results_file)
                compare_results(uncal_backend_pose_dir + pid + '/', lab_file_path, exercise_name)
            elif selected_pose_data in ['calibrated backend', 'all']:
                compare_results(cal_backend_pose_dir + pid + '/', lab_file_path, exercise_name)
            elif selected_pose_data in ['mobile', 'all']:
                compare_results(mobile_pose_dir + pid + '/', lab_file_path, exercise_name)
            file_count += 1
        participant_count += 1






########################################################################
############################ run script ################################
########################################################################
if __name__ == "__main__":
    goto_start()
########################################################################
########################################################################

