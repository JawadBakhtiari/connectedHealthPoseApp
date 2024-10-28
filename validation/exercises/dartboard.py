from enum import Enum
from exercises.exercise import Exercise

class Dartboard(Exercise):
    '''
    '''
    Y_TARGET_CHANGE = 65
    REQUIRED_CONSECUTIVE_FRAMES = 3
    def __init__(self, target_reps: int):
        super().__init__()
        self.stage = Dartboard.Stage.RIGHT_FORWARD
        self.target_reps = target_reps


    class Stage(Enum):
        RIGHT_FORWARD = 1
        RIGHT_SIDE = 2
        RIGHT_BACK = 3
        LEFT_FORWARD = 4
        LEFT_SIDE = 5
        LEFT_BACK = 6


    def next_stage(self) -> None:
        if self.stage == Dartboard.Stage.RIGHT_FORWARD:
            self.stage = Dartboard.Stage.RIGHT_SIDE
        elif self.stage == Dartboard.Stage.RIGHT_SIDE:
            self.stage = Dartboard.Stage.RIGHT_BACK
        elif self.stage == Dartboard.Stage.RIGHT_BACK:
            self.stage = Dartboard.Stage.LEFT_FORWARD
        elif self.stage == Dartboard.Stage.LEFT_FORWARD:
            self.stage = Dartboard.Stage.LEFT_SIDE
        elif self.stage == Dartboard.Stage.LEFT_SIDE:
            self.stage = Dartboard.Stage.LEFT_BACK
        elif self.stage == Dartboard.Stage.LEFT_BACK:
            self.stage = Dartboard.Stage.RIGHT_FORWARD


    def run_check(self, poses: list) -> float:
        num_consecutive = 0
        initial_pose = {kp['name']: kp for kp in poses[0]['keypoints']}
        right_ankle_start_y = initial_pose['right_ankle']['y']
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            if self.stage == Dartboard.Stage.RIGHT_FORWARD:
                right_ankle_y = pose['right_ankle']['y']
                if right_ankle_y - right_ankle_start_y > Dartboard.Y_TARGET_CHANGE:
                    num_consecutive += 1

            if num_consecutive == Dartboard.REQUIRED_CONSECUTIVE_FRAMES:
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
                self.next_stage()
                num_consecutive = 0
        return 40.0

