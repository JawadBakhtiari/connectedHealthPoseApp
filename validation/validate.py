#!/usr/bin/env python3

import curses
from options_screen import OptionsScreen

WELCOME = 'welcome to the validator :)'
POSE_DATA_OPTIONS = ['mobile', 'calibrated backend', 'uncalibrated backend', 'all']
EXERCISES = ['bent over rows', 'bicep curls', 'dartboard', 'shoulder taps', 'side bend', 'spin', 'tandem stand', 'tandem walk', 'timed up and go', 'walk', 'all']
EXERCISE_HEADER = 'select an exercise (or all)'
POSE_DATA_HEADER = 'select the type of pose data to be compared with lab data'

# initialise curses (screen handling library)
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)
opscr = OptionsScreen(stdscr)

selected_pose_data = None

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
########################################################################
########################################################################

########################################################################
############################# jumps ####################################
########################################################################
def goto_exercises():
    opscr.display_options(EXERCISES, exercise_preamble, on_enter_exercise)

def goto_start():
    opscr.display_instructions(WELCOME)
    opscr.display_options(POSE_DATA_OPTIONS, pose_data_preamble, on_enter_pose_data)
########################################################################
########################################################################

########################################################################
############################# hooks ####################################
########################################################################
def on_enter_exercise() -> None:
    pass

def on_enter_pose_data() -> None:
    global selected_pose_data
    selected_pose_data = POSE_DATA_OPTIONS[opscr.get_current_row()]
    goto_exercises()
########################################################################
########################################################################

########################################################################
############################ run script ################################
########################################################################
if __name__ == "__main__":
    goto_start()
########################################################################
########################################################################

