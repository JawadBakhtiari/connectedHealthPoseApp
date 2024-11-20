from enum import Enum
from exercises.exercise import Exercise

class GridSteps(Exercise):
    '''
    Exercise detection for grid steps exercise.

    Currently grid steps can occur in any direction at any point in time.

    A repetition of this exercise is considered to be complete when both
    feet are back together.

    A check is in place for patient being off balance, which constitutes
    'failure' of the exercise for the duration of the time spent off
    balance.
    '''
    REQUIRED_CONSECUTIVE_FRAMES = 3
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.target_reps = target_reps
        self.x = 'z' if is_lab_data else 'x'
        self.y = 'x' if is_lab_data else 'y'
        self.feet_together_threshold_x = 60
        self.feet_together_threshold_y = 20
        self.x_target_change = 250
        self.y_target_change = 30
        self.stage = GridSteps.Stage.TOGETHER


    class Stage(Enum):
        APART = 1
        TOGETHER = 2


    def set_initial_values(self, pose: dict) -> None:
        initial_pose = {kp['name']: kp for kp in pose['keypoints']}
        self.left_ankle_y = initial_pose['left_ankle'][self.y]
        self.left_ankle_x = initial_pose['left_ankle'][self.x]
        self.right_ankle_y = initial_pose['right_ankle'][self.y]
        self.right_ankle_x = initial_pose['right_ankle'][self.x]


    def cycle_stage(self) -> None:
        if self.stage == GridSteps.Stage.TOGETHER:
            self.stage = GridSteps.Stage.APART
        else:
            self.stage = GridSteps.Stage.TOGETHER


    def feet_together(self, pose: dict) -> bool:
        left_ankle_x = pose['left_ankle'][self.x]
        left_ankle_y = pose['left_ankle'][self.y]
        right_ankle_x = pose['right_ankle'][self.x]
        right_ankle_y = pose['right_ankle'][self.y]
        if (abs(left_ankle_x - right_ankle_x) <= self.feet_together_threshold_x
            and abs(left_ankle_y - right_ankle_y) <= self.feet_together_threshold_y):
            self.left_ankle_x = left_ankle_x
            self.right_ankle_x = right_ankle_x
            self.left_ankle_y = left_ankle_y
            self.right_ankle_y = right_ankle_y
            return True
        return False


    def is_successful_step(self, pose: dict) -> bool:
        left_ankle_x = pose['left_ankle'][self.x]
        right_ankle_x = pose['right_ankle'][self.x]
        left_ankle_y = pose['left_ankle'][self.y]
        right_ankle_y = pose['right_ankle'][self.y]
        if (self.stage == GridSteps.Stage.TOGETHER
            and
            (abs(self.left_ankle_x - left_ankle_x) >= self.x_target_change
            or abs(self.right_ankle_x - right_ankle_x) >= self.x_target_change)
            ):
            return True
        elif (self.stage == GridSteps.Stage.TOGETHER
              and
              (abs(self.left_ankle_y - left_ankle_y) >= self.y_target_change
              or abs(self.right_ankle_y - right_ankle_y) >= self.y_target_change)
              ):
            return True
        elif self.stage == GridSteps.Stage.APART and self.feet_together(pose):
            return True
        return False


    def run_check(self, poses: list) -> float:
        self.set_initial_values(poses[0])
        consecutive_frames = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}

            if self.is_successful_step(pose):
                consecutive_frames += 1
            if self.stage != GridSteps.Stage.TOGETHER:
                self.handle_failed_interval(self.is_off_balance(pose, self.x), time_since_start)

            if consecutive_frames == GridSteps.REQUIRED_CONSECUTIVE_FRAMES:
                if self.stage == GridSteps.Stage.APART:
                    self.rep_times.append(time_since_start)
                    if len(self.rep_times) == self.target_reps:
                        return time_since_start
                consecutive_frames = 0
                self.cycle_stage()

        return poses[-1]['time_since_start'] + 1

