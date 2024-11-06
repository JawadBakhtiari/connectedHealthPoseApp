from enum import Enum
import operator
from exercises.exercise import Exercise

class TandemWalk(Exercise):
    '''
    '''
    LAT_SPINAL_FLEX_THRESHOLD = 160
    REQUIRED_FRAMES_PAST_END = 3
    REQUIRED_CONSECUTIVE_FRAMES = 8
    FEET_TOGETHER_DISTANCE = 20
    def __init__(self, end: int, is_lab_data: bool = False):
        '''
        Args:
            end: value for where the walk ends on the relevant axis.
        '''
        super().__init__()
        self.end = end
        self.y = 'y' if not is_lab_data else 'x'
        self.is_lab_data = is_lab_data
        self.height_comparator = operator.gt if not is_lab_data else operator.le
        self.stage = TandemWalk.Stage.SWINGING_OUT


    class Stage(Enum):
        SWINGING_OUT = 1
        SWINGING_IN = 2


    def run_check(self, poses: list) -> float:
        if self.is_lab_data:
            pose = {kp['name']: kp for kp in poses[0]['keypoints']}
            self.end = pose['left_ankle'][self.y] - self.end

        frames_past_end = 0
        consecutive_frames_together = 0
        consecutive_frames_apart = 0

        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            left_ankle_x = pose['left_ankle']['x']
            right_ankle_x = pose['right_ankle']['x']
            left_ankle_y = pose['left_ankle'][self.y]
            right_ankle_y = pose['right_ankle'][self.y]

            is_off_balance = self.is_off_balance(pose, 'x', TandemWalk.LAT_SPINAL_FLEX_THRESHOLD)
            self.handle_failed_interval(is_off_balance, time_since_start)
            if is_off_balance:
                continue

            feet_together = abs(left_ankle_x - right_ankle_x) <= TandemWalk.FEET_TOGETHER_DISTANCE
            if self.stage == TandemWalk.Stage.SWINGING_IN and feet_together:
                consecutive_frames_together += 1
            elif self.stage == TandemWalk.Stage.SWINGING_OUT and not feet_together:
                consecutive_frames_apart += 1

            if self.height_comparator(left_ankle_y, self.end) and self.height_comparator(right_ankle_y, self.end):
                frames_past_end += 1
            else:
                frames_past_end = 0

            if (consecutive_frames_together >= TandemWalk.REQUIRED_CONSECUTIVE_FRAMES
                and self.stage == TandemWalk.Stage.SWINGING_IN):
                self.stage = TandemWalk.Stage.SWINGING_OUT
                consecutive_frames_together = 0
                self.rep_times.append(time_since_start)
            if (consecutive_frames_apart >= TandemWalk.REQUIRED_CONSECUTIVE_FRAMES
                and self.stage == TandemWalk.Stage.SWINGING_OUT):
                self.stage = TandemWalk.Stage.SWINGING_IN
                consecutive_frames_apart = 0
            if frames_past_end >= TandemWalk.REQUIRED_FRAMES_PAST_END:
                return time_since_start

        return poses[-1]['time_since_start'] + 1

