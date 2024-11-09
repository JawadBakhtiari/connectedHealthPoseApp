#!/usr/bin/env python3

import curses
from typing import Callable

EXERCISES = ['bent over rows', 'bicep curls', 'dartboard', 'shoulder taps', 'side bend', 'spin', 'tandem stand', 'tandem walk', 'timed up and go', 'walk', 'all']
CONFIRMATION = ['continue', 'back']
DATA_OPTIONS = ['run backend pose estimation', 'format lab data', 'all']
MAX_EXERCISE_LEN = max(len(e) for e in EXERCISES)
KEY_UP = 'k'
KEY_DOWN = 'j'
KEY_QUIT = 'q'
WELCOME = 'welcome to the data formatter :)'
INSTRUCTIONS = f'use {KEY_UP} and {KEY_DOWN} to move up and down, {KEY_QUIT} to quit'
INSTRUCTIONS2 = f'press any key to continue'
EXERCISE_HEADER = 'select an exercise (or all)'
DATA_SELECTION_HEADER = 'select data type to be formatted (or all)'

# please forgive this sin (global variables)
selected_exercise = None
selected_data = None

def exercise_preamble(
    stdscr: curses.window,
    options: list,
    height: int,
    width: int,
    ) -> None:
    stdscr.addstr((height // 2) - (len(options) // 2) - 2, width // 2 - len(EXERCISE_HEADER) // 2, EXERCISE_HEADER)


def on_enter_exercise(current_row: int) -> None:
    global selected_exercise
    selected_exercise = EXERCISES[current_row]
    goto_confirmation()


def data_selection_preamble(
    stdscr: curses.window,
    options: list,
    height: int,
    width: int,
    ) -> None:
    stdscr.addstr((height // 2) - (len(options) // 2) - 2, width // 2 - len(DATA_SELECTION_HEADER) // 2, DATA_SELECTION_HEADER)


def on_enter_data_selection(current_row: int) -> None:
    global selected_data
    selected_data = DATA_OPTIONS[current_row]
    goto_exercises()


def confirmation_preamble(
    stdscr: curses.window,
    options: list,
    height: int,
    width: int,
    ) -> None:
    exercise = 'all exercises' if selected_exercise == 'all' else selected_exercise
    confirmation_text = f'run formatting for \'{selected_data}\' on {exercise}?'
    stdscr.addstr((height // 2) - (len(options) // 2) - 2, width // 2 - len(confirmation_text) // 2, confirmation_text)


def on_enter_confirmation(current_row: int) -> None:
    if CONFIRMATION[current_row] == "continue":
        pass
    else:
        goto_start()


def main(stdscr: curses.window, options: list, preamble: Callable, on_enter: Callable) -> None:
    # try:
    curses.curs_set(0)  # Hide cursor
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        preamble(stdscr, options, height, width)
        max_option_len = max(len(e) for e in options)

        for i, option in enumerate(options):
            x = (width - max_option_len) // 2
            y = height // 2 - len(options) // 2 + i
            if i == current_row:
                stdscr.addstr(y, x - 2, "> ")
                stdscr.addstr(y, x, option)
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()
        key = stdscr.getch()

        if key == ord(KEY_UP):
            current_row = current_row - 1 if current_row > 0 else len(options) - 1
        elif key == ord(KEY_DOWN):
            current_row = current_row + 1 if current_row < len(options) - 1 else 0
        elif key == ord(KEY_QUIT):
            return
        elif key == curses.KEY_ENTER or key in [10, 13]:
            on_enter(current_row)
    # except:
    #     curses.endwin()
    #     print('uh oh, an error occurred displaying the interface (your terminal window is probably too small!)')
    #     input('press enter to end program ...')
    #     exit(1)


def display_instructions(stdscr: curses.window) -> None:
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.addstr(height // 2 - 3, width // 2 - len(WELCOME) // 2, WELCOME)
    stdscr.addstr(height // 2, width // 2 - len(INSTRUCTIONS) // 2, INSTRUCTIONS)
    stdscr.addstr(height // 2 + 1, width // 2 - len(INSTRUCTIONS2) // 2, INSTRUCTIONS2)
    stdscr.refresh()
    stdscr.getch()


def goto_start():
    curses.wrapper(display_instructions)
    curses.wrapper(main, DATA_OPTIONS, data_selection_preamble, on_enter_data_selection)


def goto_exercises():
    curses.wrapper(main, EXERCISES, exercise_preamble, on_enter_exercise)


def goto_confirmation():
    curses.wrapper(main, CONFIRMATION, confirmation_preamble, on_enter_confirmation)


goto_start()

