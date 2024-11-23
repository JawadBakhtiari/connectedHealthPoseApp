import curses
from typing import Callable

class OptionsScreen():
    '''
    Display a provided list of options to the user and allow them to toggle
    through these options.

    Allow the selection of an option, and run provided functionality when
    this occurs.
    '''
    KEY_UP = 'k'
    KEY_DOWN = 'j'
    KEY_QUIT = 'q'
    MAIN_INSTRUCTIONS = f'use {KEY_UP} and {KEY_DOWN} to move up and down, {KEY_QUIT} to quit'
    SUB_INSTRUCTIONS = f'press any key to continue'
    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.current_row = 0
        self.height, self.width = stdscr.getmaxyx()


    def get_height(self) -> int:
        return self.height


    def get_width(self) -> int:
        return self.width


    def get_current_row(self) -> int:
        return self.current_row


    def display_instructions(self, welcome: str = '') -> None:
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.stdscr.addstr(height // 2 - 3, width // 2 - len(welcome) // 2, welcome)
        self.stdscr.addstr(height // 2, width // 2 - len(OptionsScreen.MAIN_INSTRUCTIONS) // 2, OptionsScreen.MAIN_INSTRUCTIONS)
        self.stdscr.addstr(height // 2 + 1, width // 2 - len(OptionsScreen.SUB_INSTRUCTIONS) // 2, OptionsScreen.SUB_INSTRUCTIONS)
        self.stdscr.refresh()
        self.stdscr.getch()


    def display_options(self, options: list, preamble: Callable, on_enter: Callable) -> None:
        '''
        Display options to the user and handle the selection of one of these options.

        Args:
            options:    list of options to be displayed.
            preamble:   function to be run to display any desired text before the options.
            on_enter:   function to be called when one of the options is selected.
        '''
        curses.curs_set(0)
        self.current_row = 0

        while True:
            self.stdscr.clear()
            self.height, self.width = self.stdscr.getmaxyx()
            preamble()
            max_option_len = max(len(e) for e in options)

            for i, option in enumerate(options):
                x = (self.width - max_option_len) // 2
                y = self.height // 2 - len(options) // 2 + i
                if i == self.current_row:
                    self.stdscr.addstr(y, x - 2, "> ")
                    self.stdscr.addstr(y, x, option)
                else:
                    self.stdscr.addstr(y, x, option)

            self.stdscr.refresh()
            key = self.stdscr.getch()

            if key == ord(OptionsScreen.KEY_UP):
                self.current_row = self.current_row - 1 if self.current_row > 0 else len(options) - 1
            elif key == ord(OptionsScreen.KEY_DOWN):
                self.current_row = self.current_row + 1 if self.current_row < len(options) - 1 else 0
            elif key == ord(OptionsScreen.KEY_QUIT):
                return
            elif key == curses.KEY_ENTER or key in [10, 13]:
                on_enter()
                break

