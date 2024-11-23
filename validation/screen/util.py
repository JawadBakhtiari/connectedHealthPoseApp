'''Utility functions for interacting with screen.'''

import curses

def output_progress(
    stdscr: curses.window,
    height: int,
    width: int,
    action_title: str,
    file_count: int,
    num_files: int,
    participant_count: int,
    num_participants: int,
    filename: str
    ) -> None:
    stdscr.clear()
    progress_text = f'{action_title} {file_count}/{num_files} for participant {participant_count}/{num_participants} ...'
    stdscr.addstr(height // 2, width // 2 - (len(progress_text) // 2 + 2), progress_text)
    stdscr.refresh()
    print(f'processing {filename} ...')

