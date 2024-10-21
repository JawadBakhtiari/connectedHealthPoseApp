import operator
from exercises.exercise import Exercise

class Walk(Exercise):
    '''
    Determine when a walk from a given starting position to
    a given ending position has been completed.
    '''
    REQUIRED_MATCHING_FRAMES = 3

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
        matching_frames = 0
        if self.is_lab_data:
            pose = {kp['name']: kp for kp in poses[0]['keypoints']}
            self.end = pose['left_ankle'][self.y] - self.end
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            left_ankle_y = pose['left_ankle'][self.y]
            right_ankle_y = pose['right_ankle'][self.y]
            if self.height_comparator(left_ankle_y, self.end) and self.height_comparator(right_ankle_y, self.end):
                matching_frames += 1
            else:
                matching_frames = 0
            if matching_frames >= Walk.REQUIRED_MATCHING_FRAMES:
                self.rep_times.append(time_since_start)
                return time_since_start
        return poses[-1]['time_since_start'] + 1

