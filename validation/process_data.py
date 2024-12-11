#!/usr/bin/env python3

import os
import sys
import json
import curses
import contextlib
import subprocess
import numpy as np
import pandas as pd
import opensim as osim
from io import StringIO
from typing import Callable
from redirect_output import redirect_output
from format.labdataformatter import LabDataFormatter
from screen.options_screen import OptionsScreen
from screen.util import output_progress
from screen import const

DATA_OPTIONS = ['run pose estimation', 'format lab data', 'all']
MODELS = ['blazepose', 'thunder', 'all']
WELCOME = 'welcome to the data processor :)'
END_MESSAGE = 'data processing complete, press any key to exit'
DATA_SELECTION_HEADER = 'select data type to be formatted (or all)'
MODELS_HEADER = 'select model for pose estimation'
CALIBRATION_HEADER = 'select image calibration for pose estimation'
FORMATTING_ACTION_TITLE = 'formatting file'
INTERPOLATION_ACTION_TITLE = 'interpolating file'
IK_ACTION_TITLE = '(this will be slow) running inverse kinematics on file'
POSE_ESTIMATION_ACTION_TITLE = 'running pose estimation on file'

if len(sys.argv) != 2:
    print(f'usage: {sys.argv[0]} <path/to/data/directory>')
    exit(1)
target_dir = sys.argv[1]

# redirect output to a log file
os.makedirs(target_dir + '/results/', exist_ok=True)
log_file = open(target_dir + '/results/format_log.txt', 'w')
sys.stdout = log_file
sys.stderr = log_file

# initialise curses (screen handling library)
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)
opscr = OptionsScreen(stdscr)

# please forgive this sin (global variables)
selected_exercise = None
selected_data = None
selected_model = None

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

def data_selection_preamble() -> None:
    add_header_text(DATA_SELECTION_HEADER, DATA_OPTIONS)

def confirmation_preamble() -> None:
    exercise = 'all exercises' if selected_exercise == 'all' else selected_exercise
    confirmation_text = f'run formatting for \'{selected_data}\' on {exercise}?'
    add_header_text(confirmation_text, const.CONFIRMATION)

def model_preamble() -> None:
    add_header_text(MODELS_HEADER, MODELS)
########################################################################
########################################################################

########################################################################
############################# hooks ####################################
########################################################################
def on_enter_exercise() -> None:
    global selected_exercise
    selected_exercise = const.EXERCISES[opscr.get_current_row()]
    goto_confirmation()

def on_enter_data_selection() -> None:
    global selected_data
    selected_data = DATA_OPTIONS[opscr.get_current_row()]
    goto_exercises()

def on_enter_confirmation() -> None:
    if const.CONFIRMATION[opscr.get_current_row()] == "continue":
        run_formatting()
        stdscr.clear()
        stdscr.addstr(opscr.get_height() // 2, opscr.get_width() // 2 - (len(END_MESSAGE) // 2 + 2), END_MESSAGE)
        stdscr.refresh()
        stdscr.getch()
        curses.endwin()
        exit(0)
    else:
        goto_start()

def on_enter_model() -> None:
    global selected_model
    selected_model = MODELS[opscr.get_current_row()]
########################################################################
########################################################################

########################################################################
############################# jumps ####################################
########################################################################
def goto_models():
    opscr.display_options(MODELS, model_preamble, on_enter_model)

def goto_exercises():
    opscr.display_options(const.EXERCISES, exercise_preamble, on_enter_exercise)

def goto_confirmation():
    opscr.display_options(const.CONFIRMATION, confirmation_preamble, on_enter_confirmation)

def goto_start():
    opscr.display_instructions(WELCOME)
    opscr.display_options(DATA_OPTIONS, data_selection_preamble, on_enter_data_selection)
########################################################################
########################################################################

########################################################################
######################### data processing ###############################
########################################################################
def format_lab_data_file(filepath: str, out_file: str) -> None:
    ldf = LabDataFormatter(filepath)
    formatted_data = ldf.format()
    with open(out_file, 'w') as f:
        json.dump(formatted_data, f, indent=4)


def run_sts_ik() -> None:
    ''' Run opensim inverse kinematics on sit to stand data.'''
    formatted_sts_dir = target_dir + '/lab/sts/formatted/'
    model = osim.Model('conventional.osim')
    ik_tool = osim.InverseKinematicsTool()
    ik_tool.setModel(model)
    num_participants = len(os.listdir(formatted_sts_dir))
    participant_count = 1
    for pid in os.listdir(formatted_sts_dir):
        output_progress(stdscr, opscr.get_height(), opscr.get_width(), IK_ACTION_TITLE , 1, 1, participant_count, num_participants, 'sts.trc')
        marker_file = formatted_sts_dir + f'{pid}/sts.trc'
        ik_tool.setMarkerDataFileName(marker_file)
        os.makedirs(formatted_sts_dir + f'{pid}/', exist_ok=True)
        ik_tool.setOutputMotionFileName(formatted_sts_dir + f'{pid}/sts.mot')
        ik_tool.set_report_errors(True)
        # ik_tool.setStartTime(0.0)
        # ik_tool.setEndTime(1.0)
        with redirect_output(log_file):
            ik_tool.run()
        participant_count += 1


def run_sts_interpolation() -> None:
    '''Interpolate missing values in sts exercise data.'''
    raw_sts_dir = target_dir + '/lab/sts/raw/'
    formatted_sts_dir = target_dir + '/lab/sts/formatted/'
    num_participants = len(os.listdir(raw_sts_dir))
    participant_count = 1
    for pid in os.listdir(raw_sts_dir):
        output_progress(stdscr, opscr.get_height(), opscr.get_width(), INTERPOLATION_ACTION_TITLE, 1, 1, participant_count, num_participants, 'sts.trc')
        with redirect_output(log_file):
            with open(raw_sts_dir + f'{pid}/sts.trc', 'r') as file:
                lines = file.readlines()
            header_lines = lines[:3]
            data_lines = lines[3:]
            data = pd.read_csv(StringIO(''.join(data_lines)), delimiter='\t', header=None)
            joint_names_row = data.iloc[0].copy()

            # Drop the row with joint names from the data for interpolation
            data_no_names = data.drop(index=0).reset_index(drop=True)

            # Interpolate missing values
            data_no_names.replace('', np.nan, inplace=True)
            data_no_names.interpolate(method='linear', inplace=True, limit_direction='forward', axis=0)
            data_no_names.fillna(method='bfill', inplace=True)

            # Add the joint names row back to the DataFrame
            data_fixed = pd.concat([pd.DataFrame([joint_names_row]), data_no_names], ignore_index=True)
            data_fixed.iloc[1, 0] = ''
            data_fixed.iloc[1, 1] = ''

            os.makedirs(formatted_sts_dir + pid, exist_ok=True)
            with open(formatted_sts_dir + f'{pid}/sts.trc', 'w') as f:
                f.writelines(header_lines)
                data_fixed.to_csv(f, sep='\t', index=False, header=False)
        participant_count += 1


def format_sts_data() -> None:
    run_sts_interpolation()
    run_sts_ik()


def format_lab_data() -> None:
    print('formatting lab data...')
    raw_lab_data_dir = target_dir + '/lab/raw/'
    formatted_lab_data_dir = target_dir + '/lab/formatted/'
    participant_count = 1
    num_participants = len(os.listdir(raw_lab_data_dir))
    for pid in os.listdir(raw_lab_data_dir):
        in_dir = raw_lab_data_dir + pid + '/'
        out_dir = formatted_lab_data_dir + pid + '/'
        os.makedirs(os.path.dirname(out_dir), exist_ok=True)
        if selected_exercise == 'all':
            format_sts_data()
            file_count = 1
            num_files = len(os.listdir(in_dir))
            for filename in os.listdir(in_dir):
                output_progress(stdscr, opscr.get_height(), opscr.get_width(), FORMATTING_ACTION_TITLE, file_count, num_files, participant_count, num_participants, filename)
                format_lab_data_file(in_dir + filename, out_dir + filename[:len('.csv')] + '.json')
                file_count += 1
        elif selected_exercise == 'sit to stand':
            format_sts_data()
        else:
            filename = '_'.join(selected_exercise.split()) + '.csv'
            output_progress(stdscr, opscr.get_height(), opscr.get_width(), FORMATTING_ACTION_TITLE, 1, 1, participant_count, num_participants, filename)
            format_lab_data_file(in_dir + filename, out_dir + selected_exercise + '.json')
        participant_count += 1


def run_calibration(calibration_dir: str, primary_params: str) -> None:
    stdscr.clear()
    update_text = 'running calibration ...'
    stdscr.addstr(opscr.get_height() // 2, opscr.get_width() // 2 - (len(update_text) // 2 + 2), update_text)
    stdscr.refresh()
    print(update_text)
    subprocess.run(['python3', 'be_pose_estimation/calibrate.py', calibration_dir + 'images/primary/', primary_params], stdout=log_file, stderr=log_file)


def run_pose_estimation() -> None:
    print('running pose estimation ...')
    goto_models()
    calibration_dir = target_dir + '/mobile/calibration/'
    primary_params = calibration_dir + 'parameters/primary/parameters.npz'
    if not os.path.exists(primary_params):
        run_calibration(calibration_dir, primary_params)

    video_dir = target_dir + '/mobile/videos/primary/'
    participant_count = 1
    num_participants = len(os.listdir(video_dir))
    for pid in os.listdir(video_dir):
        in_dir = video_dir + pid + '/'
        uncal_out_dir = target_dir + '/mobile/poses/backend/uncalibrated/' + pid + '/'
        cal_out_dir = target_dir + '/mobile/poses/backend/calibrated/' + pid + '/'
        os.makedirs(os.path.dirname(uncal_out_dir), exist_ok=True)
        os.makedirs(os.path.dirname(cal_out_dir), exist_ok=True)
        if selected_exercise == 'all':
            file_count = 1
            num_files = len(os.listdir(in_dir))
            for filename in os.listdir(in_dir):
                output_progress(
                    stdscr,
                    opscr.get_height(),
                    opscr.get_width(),
                    POSE_ESTIMATION_ACTION_TITLE,
                    file_count,
                    num_files,
                    participant_count,
                    num_participants,
                    filename
                )
                subprocess.run(['python3', 'be_pose_estimation/run_pose_estimation.py', filename[:-len('.mp4')], selected_model, in_dir, primary_params, uncal_out_dir, cal_out_dir], stdout=log_file, stderr=log_file)
                file_count += 1
        else:
            filename = '_'.join(selected_exercise.split()) + '.mp4'
            output_progress(
                stdscr,
                opscr.get_height(),
                opscr.get_width(),
                POSE_ESTIMATION_ACTION_TITLE,
                1,
                1,
                participant_count,
                num_participants,
                filename
            )
            subprocess.run(['python3', 'be_pose_estimation/run_pose_estimation.py', filename[:-len('.mp4')], selected_model, in_dir, primary_params, uncal_out_dir, cal_out_dir], stdout=log_file, stderr=log_file)
        participant_count += 1


def run_formatting() -> None:
    if selected_data == 'format lab data':
        format_lab_data()
    elif selected_data == 'run pose estimation':
        run_pose_estimation()
    else:
        run_pose_estimation()
        format_lab_data()
########################################################################
########################################################################

########################################################################
############################ run script ################################
########################################################################
if __name__ == "__main__":
    goto_start()
########################################################################
########################################################################

