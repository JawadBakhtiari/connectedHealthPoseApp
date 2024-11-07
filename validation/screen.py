#!/usr/bin/env python3

import curses
from typing import Callable

EXERCISES = ["bent over rows", "bicep curls", "dartboard", "shoulder taps", "side bend", "sit to stand", "spin", "tandem stand", "tandem walk", "timed up and go", "walk"]
CONFIRMATION = ["continue", "back"]
MAX_EXERCISE_LEN = max(len(e) for e in EXERCISES)
KEY_UP = 'k'
KEY_DOWN = 'j'
KEY_QUIT = 'q'
INSTRUCTIONS = f"use {KEY_UP} and {KEY_DOWN} to move up and down, {KEY_QUIT} to quit"


def exercise_preamble(
    stdscr: curses.window,
    _: int,
    width: int,
    ) -> None:
    stdscr.addstr(1, width // 2 - len(INSTRUCTIONS) // 2, INSTRUCTIONS)


def on_enter_exercise(current_row: int) -> None:
    curses.wrapper(main, CONFIRMATION, confirmation_preamble, on_enter_confirmation, EXERCISES[current_row])


def confirmation_preamble(
    stdscr: curses.window,
    height: int,
    width: int,
    selected_exercise: str
    ) -> None:
    selected_str = f"selected: {selected_exercise}"
    stdscr.addstr(height // 2 - len(CONFIRMATION), width // 2 - len(selected_str) // 2, selected_str)


def on_enter_confirmation(current_row: int) -> None:
    if CONFIRMATION[current_row] == "continue":
        pass
    else:
        curses.wrapper(main, EXERCISES, exercise_preamble, on_enter_exercise)


def main(stdscr: curses.window, options: list, preamble: Callable, on_enter: Callable, *args) -> None:
    curses.curs_set(0)  # Hide cursor
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        preamble(stdscr, height, width, *args)
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

def display_instructions(stdscr: curses.window) -> None:
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.addstr(height // 4, width // 2 - len(INSTRUCTIONS) // 2, INSTRUCTIONS)
    stdscr.refresh()
    stdscr.getch()


# Initialize curses and show the welcome message before starting the main program
curses.wrapper(display_instructions)
curses.wrapper(main, EXERCISES, exercise_preamble, on_enter_exercise)

