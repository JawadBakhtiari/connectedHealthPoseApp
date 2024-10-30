import math
import bisect
from abc import ABC, abstractmethod

class Exercise(ABC):
    '''
    Abstract base class for exercises, outlining methods that must be
    implemented for use in exercise detection and visualisation.
    '''
    def __init__(self):
        self.rep_times = []
        self.failing_intervals = []
        self.failed_interval_start = None
        self.failed_interval_end = None


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


    def calc_joint_angle(
            self,
            x:str,
            initial_side: dict,
            vertex: dict,
            terminal_side: dict
        ) -> float:
        '''
        Calculate the angle between initial_side, vertex and terminal_side.

        Returns:
            A float representing this angle in degrees.
        '''
        v1 = (vertex[x] - initial_side[x], vertex['y'] - initial_side['y'])
        v2 = (vertex[x] - terminal_side[x], vertex['y'] - terminal_side['y'])

        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
        magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

        cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
        angle_radians = math.acos(cos_angle)
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees


    def is_failing_interval(self, query_time: float) -> bool:
        '''
        Return true if query_time is withing a failing interval,
        False otherwise.

        A failing interval is defined as any point in time where
        the given exercise was not being performed correctly.
        '''
        for start,end in self.failing_intervals:
            if query_time >= start and query_time <= end:
                return True
        return False


    def get_failing_intervals(self) -> list:
        return self.failing_intervals


    def handle_failed_interval(self, failing: bool, time_since_start: int) -> None:
        '''
        Store the start and end times of a failing interval for an exercise
        and append this to the list of failing intervals when this interval
        has ended.

        Args:
            failing:            whether or not the exercise is being failed at
                                the current point in time.
            time_since_start:   time since the exercise began, as a posix timestamp.
        '''
        if failing:
            if self.failed_interval_start:
                self.failed_interval_end = time_since_start
            else:
                self.failed_interval_start = time_since_start
        elif self.failed_interval_start:
            if self.failed_interval_end:
                self.failing_intervals.append((self.failed_interval_start, self.failed_interval_end))
                self.failed_interval_end = None
            self.failed_interval_start = None


    def num_reps_completed(self, query_time: float) -> int:
        '''
        Return the number of reps of this exercise that have been completed
        at query_time.
        '''
        return bisect.bisect_right(self.rep_times, query_time)

