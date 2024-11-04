import operator
from exercises.exercise import Exercise

class TandemWalk(Exercise):
    '''
    '''
    REQUIRED_FRAMES_PAST_END = 3
    REQUIRED_STATIONARY_FRAMES = 5
    FEET_TOGETHER_DISTANCE = 10
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


    def run_check(self, poses: list) -> float:
        frames_past_end = 0
        frames_stationary = 0
        if self.is_lab_data:
            pose = {kp['name']: kp for kp in poses[0]['keypoints']}
            self.end = pose['left_ankle'][self.y] - self.end
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            left_ankle_x = pose['left_ankle']['x']
            right_ankle_x = pose['right_ankle']['x']
            left_ankle_y = pose['left_ankle'][self.y]
            right_ankle_y = pose['right_ankle'][self.y]
            print(abs(left_ankle_x - right_ankle_x), left_ankle_y - right_ankle_y)
            if abs(left_ankle_x - right_ankle_x) <= TandemWalk.FEET_TOGETHER_DISTANCE:
                frames_stationary += 1
            else:
                frames_stationary = 0
            if self.height_comparator(left_ankle_y, self.end) and self.height_comparator(right_ankle_y, self.end):
                frames_past_end += 1
            else:
                frames_past_end = 0
            if frames_stationary >= TandemWalk.REQUIRED_STATIONARY_FRAMES:
                self.rep_times.append(time_since_start)
            if frames_past_end >= TandemWalk.REQUIRED_FRAMES_PAST_END:
                self.rep_times.append(time_since_start)
                return time_since_start
        return poses[-1]['time_since_start'] + 1

