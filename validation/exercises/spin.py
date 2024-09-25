import heapq
from enum import Enum
from exercises.exercise import Exercise

class Spin(Exercise):
    '''
    Determine when a 360 degree spin has been completed.
    '''
    # Pose estimation is inherently a bit noisy, so to calculate
    # shoulder width from a video values from multiple frames are
    # collected to improve accuracy.
    NUM_SHOULDER_WIDTHS = 10
    SHOULDER_WIDTH_DIFF_TOLERANCE = 0.01


    class Stage(Enum):
        GET_SHOULDER_WIDTH = 1
        DETECT_SPIN_COMPLETED = 2


    def __init__(self) -> None:
        super().__init__()
        self.last_shoulder_dist = None
        self.shoulder_dists = []
        self.shoulder_width = None
        self.stage = Spin.Stage.GET_SHOULDER_WIDTH


    @staticmethod
    def same_sign(a, b):
        return a * b > 0


    def get_shoulder_width(self, pose) -> None:
        pose = {kp['name']: kp for kp in pose['keypoints']}
        shoulder_dist = pose['left_shoulder']['x'] - pose['right_shoulder']['x']
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


    def detect_spin_completed(self, pose) -> float | None:
        time_since_start = pose['time_since_start']
        pose = {kp['name']: kp for kp in pose['keypoints']}
        shoulder_dist = pose['left_shoulder']['x'] - pose['right_shoulder']['x']
        if abs(shoulder_dist - self.shoulder_width) <= Spin.SHOULDER_WIDTH_DIFF_TOLERANCE:
            self.rep_times.append(time_since_start)
            return time_since_start
        return None


    def run_check(self, poses: list) -> float:
        for pose in poses:
            if self.stage == Spin.Stage.GET_SHOULDER_WIDTH:
                self.get_shoulder_width(pose)
            else:
                time_completed = self.detect_spin_completed(pose)
                if time_completed:
                    return time_completed
        return poses[-1]['time_since_start'] + 1

