import bisect
from abc import ABC, abstractmethod

class Exercise(ABC):
    '''
    Abstract base class for exercises, outlining methods that must be
    implemented for use in exercise detection and visualisation of this.
    '''
    def __init__(self):
        self.rep_times = []


    @abstractmethod
    def run_check(self, poses: list) -> float:
        '''
        Using pose data, determine if an exercise was completed,
        and return the time it took to complete.

        Returns:
            float: the time (in seconds) that it took to complete
            the exercise. If exercise was not completed, a time longer
            than the video data will be returned.
        '''
        pass


    def num_reps_completed(self, query_time: float) -> int:
        '''
        Return the number of reps of this exercise that have been completed
        at query_time.
        '''
        return bisect.bisect_right(self.rep_times, query_time)

