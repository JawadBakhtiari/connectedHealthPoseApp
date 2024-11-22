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
    LAT_SPINAL_FLEX_THRESHOLD_MOBILE = 160
    LAT_SPINAL_FLEX_THRESHOLD_LAB = 145
    X_TARGET_CHANGE_MOBILE = 250
    X_TARGET_CHANGE_LAB = 300
    Y_TARGET_CHANGE_MOBILE = 30
    Y_TARGET_CHANGE_LAB = 400
    X_FEET_TOGETHER_MOBILE = 60
    X_FEET_TOGETHER_LAB = 250
    Y_FEET_TOGETHER_MOBILE = 20
    Y_FEET_TOGETHER_LAB = 50
    X_FEET_CLOSE_MOBILE = 80
    X_FEET_CLOSE_LAB = 200
    Y_FEET_CLOSE_MOBILE = 30
    Y_FEET_CLOSE_LAB = 80
    REQUIRED_CONSECUTIVE_FRAMES = 3
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.target_reps = target_reps
        self.x = 'z' if is_lab_data else 'x'
        self.y = 'x' if is_lab_data else 'y'
        self.x_feet_together = GridSteps.X_FEET_TOGETHER_LAB if is_lab_data else GridSteps.X_FEET_TOGETHER_MOBILE
        self.y_feet_together = GridSteps.Y_FEET_TOGETHER_LAB if is_lab_data else GridSteps.Y_FEET_TOGETHER_MOBILE
        self.x_feet_close = GridSteps.X_FEET_CLOSE_LAB if is_lab_data else GridSteps.X_FEET_CLOSE_MOBILE
        self.y_feet_close = GridSteps.Y_FEET_CLOSE_LAB if is_lab_data else GridSteps.Y_FEET_CLOSE_MOBILE
        self.x_target_change = GridSteps.X_TARGET_CHANGE_LAB if is_lab_data else GridSteps.X_TARGET_CHANGE_MOBILE
        self.y_target_change = GridSteps.Y_TARGET_CHANGE_LAB if is_lab_data else GridSteps.Y_TARGET_CHANGE_MOBILE
        self.stage = GridSteps.Stage.TOGETHER
        self.lat_spinal_flex_threshold = GridSteps.LAT_SPINAL_FLEX_THRESHOLD_LAB if is_lab_data else GridSteps.LAT_SPINAL_FLEX_THRESHOLD_MOBILE


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


    def feet_within_distance(self, pose: dict, x_dist: int, y_dist: int) -> bool:
        left_ankle_x = pose['left_ankle'][self.x]
        left_ankle_y = pose['left_ankle'][self.y]
        right_ankle_x = pose['right_ankle'][self.x]
        right_ankle_y = pose['right_ankle'][self.y]
        if (abs(left_ankle_x - right_ankle_x) <= x_dist
            and abs(left_ankle_y - right_ankle_y) <= y_dist):
            self.left_ankle_x = left_ankle_x
            self.right_ankle_x = right_ankle_x
            self.left_ankle_y = left_ankle_y
            self.right_ankle_y = right_ankle_y
            return True
        return False


    def feet_together(self, pose: dict) -> bool:
        return self.feet_within_distance(pose, self.x_feet_together, self.y_feet_together)


    def feet_close_balance(self, pose:dict) -> bool:
        return self.feet_within_distance(pose, self.x_feet_close, self.y_feet_close)


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
            if self.feet_close_balance(pose):
                # Only check balance if feet are close - an outward step is too
                # difficult to disctinguish from being off balance.
                is_off_balance = self.is_off_balance(pose, self.x, self.lat_spinal_flex_threshold)
                self.handle_failed_interval(is_off_balance, time_since_start)

            if consecutive_frames == GridSteps.REQUIRED_CONSECUTIVE_FRAMES:
                if self.stage == GridSteps.Stage.APART:
                    self.rep_times.append(time_since_start)
                    if len(self.rep_times) == self.target_reps:
                        return time_since_start
                consecutive_frames = 0
                self.cycle_stage()

        return poses[-1]['time_since_start'] + 1

