import heapq
from enum import Enum
from exercises.exercise import Exercise

class Spin(Exercise):
    '''
    Determine when a 360 degree spin has been completed. Current
    implementation makes no effort to distinguish between
    directions, so two reps consecutively in the same direction
    is equally as valid as two reps in consecutively in
    opposite directions.
    '''
    # Pose estimation is inherently noisy, so to calculate
    # shoulder width from a video, values from multiple frames are
    # collected to improve accuracy.
    NUM_SHOULDER_WIDTHS = 10
    MOBILE_SHOULDER_WIDTH_DIFF_TOLERANCE = 3
    LAB_SHOULDER_WIDTH_DIFF_TOLERANCE = 10
    LAB_X = 'z'
    MOBILE_X = 'x'


    class Stage(Enum):
        GET_SHOULDER_WIDTH = 1
        DETECT_SPIN_COMPLETED = 2
        SPINNING_BACK = 3


    def __init__(self, target: int, is_lab_data: bool = False) -> None:
        super().__init__()
        self.last_shoulder_dist = None
        self.shoulder_dists = []
        self.shoulder_width = None
        self.stage = Spin.Stage.GET_SHOULDER_WIDTH
        self.target = target
        if is_lab_data:
            self.shoulder_width_diff_tolerance = Spin.LAB_SHOULDER_WIDTH_DIFF_TOLERANCE
            self.x = Spin.LAB_X
        else:
            self.shoulder_width_diff_tolerance = Spin.MOBILE_SHOULDER_WIDTH_DIFF_TOLERANCE
            self.x = Spin.MOBILE_X


    @staticmethod
    def same_sign(a, b):
        return a * b > 0


    def get_shoulder_width(self, shoulder_dist: float) -> None:
        if self.last_shoulder_dist != None and not Spin.same_sign(shoulder_dist, self.last_shoulder_dist):
            # turning point
            self.stage = Spin.Stage.DETECT_SPIN_COMPLETED
            self.shoulder_width = self.shoulder_dists[Spin.NUM_SHOULDER_WIDTHS // 2]
            return
        if len(self.shoulder_dists) < Spin.NUM_SHOULDER_WIDTHS:
            heapq.heappush(self.shoulder_dists, shoulder_dist)
        elif shoulder_dist > self.shoulder_dists[0]:
            heapq.heapreplace(self.shoulder_dists, shoulder_dist)
        self.last_shoulder_dist = shoulder_dist


    def spin_completed(self, shoulder_dist, time_since_start) -> bool:
        if abs(shoulder_dist - self.shoulder_width) <= self.shoulder_width_diff_tolerance:
            self.stage = Spin.Stage.SPINNING_BACK
            self.rep_times.append(time_since_start)
            return True
        return False


    def detect_spin_back(self, shoulder_dist: float) -> None:
        if self.last_shoulder_dist != None and not Spin.same_sign(shoulder_dist, self.last_shoulder_dist):
            # turning point
            self.stage = Spin.Stage.DETECT_SPIN_COMPLETED


    def run_check(self, poses: list) -> float:
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            shoulder_dist = pose['left_shoulder'][self.x] - pose['right_shoulder'][self.x]
            if self.stage == Spin.Stage.GET_SHOULDER_WIDTH:
                self.get_shoulder_width(shoulder_dist)
            elif self.stage == Spin.Stage.SPINNING_BACK:
                self.detect_spin_back(shoulder_dist)
            # stage is DETECT_SPIN_COMPLETED
            elif self.spin_completed(shoulder_dist, time_since_start) and len(self.rep_times) == self.target:
                return time_since_start
        return poses[-1]['time_since_start'] + 1

