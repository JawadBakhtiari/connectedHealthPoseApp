import os
from contextlib import contextmanager

@contextmanager
def redirect_output(log_file):
    '''
    Context manager to redirect stdout and stderr to a log file.
    '''
    # Save the original file descriptors
    original_stdout_fd = os.dup(1)
    original_stderr_fd = os.dup(2)

    try:
        os.dup2(log_file.fileno(), 1)
        os.dup2(log_file.fileno(), 2)
        yield

    finally:
        # Restore the original stdout and stderr
        os.dup2(original_stdout_fd, 1)
        os.dup2(original_stderr_fd, 2)

        # Close the duplicated file descriptors
        os.close(original_stdout_fd)
        os.close(original_stderr_fd)

