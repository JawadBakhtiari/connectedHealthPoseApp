from enum import Enum
from exercises.exercise import Exercise

class Dartboard(Exercise):
    '''
    Detect dartboard stepping exercise repetitions.

    Also tracks being too off balance as poor form.
    Currently does nothing to identify mis-steps.
    '''
    LAT_SPINAL_FLEX_THRESHOLD_MOBILE = 160
    LAT_SPINAL_FLEX_THRESHOLD_LAB = 142
    Y_TARGET_CHANGE_BACKWARD_MOBILE = 25
    Y_TARGET_CHANGE_FORWARD_MOBILE = 55
    Y_TARGET_CHANGE_LAB = 400
    X_TARGET_CHANGE_MOBILE = 200
    X_TARGET_CHANGE_LAB = 400
    FEET_TOGETHER_THRESHOLD_MOBILE = 30
    FEET_TOGETHER_THRESHOLD_LAB = 60
    REQUIRED_CONSECUTIVE_FRAMES = 3
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.goal = Dartboard.Goal.RIGHT_FORWARD
        self.stage = Dartboard.Stage.AWAY
        self.is_lab_data = is_lab_data
        self.target_reps = target_reps * len(Dartboard.Goal)
        self.x = 'z' if is_lab_data else 'x'
        self.y = 'x' if is_lab_data else 'y'
        self.y_target_change_forward =  Dartboard.Y_TARGET_CHANGE_LAB if is_lab_data else Dartboard.Y_TARGET_CHANGE_FORWARD_MOBILE
        self.y_target_change_backward =  Dartboard.Y_TARGET_CHANGE_LAB if is_lab_data else Dartboard.Y_TARGET_CHANGE_BACKWARD_MOBILE
        self.x_target_change = Dartboard.X_TARGET_CHANGE_LAB if is_lab_data else Dartboard.X_TARGET_CHANGE_MOBILE
        self.lat_spinal_flex_threshold = Dartboard.LAT_SPINAL_FLEX_THRESHOLD_LAB if is_lab_data else Dartboard.LAT_SPINAL_FLEX_THRESHOLD_MOBILE
        self.feet_together_threshold = Dartboard.FEET_TOGETHER_THRESHOLD_LAB if is_lab_data else Dartboard.FEET_TOGETHER_THRESHOLD_MOBILE


    class Goal(Enum):
        RIGHT_FORWARD = 1
        RIGHT_SIDE = 2
        RIGHT_BACK = 3
        LEFT_FORWARD = 4
        LEFT_SIDE = 5
        LEFT_BACK = 6


    class Stage(Enum):
        AWAY = 1
        BACK = 2


    def next_goal(self) -> None:
        if self.goal == Dartboard.Goal.RIGHT_FORWARD:
            self.goal = Dartboard.Goal.RIGHT_SIDE
        elif self.goal == Dartboard.Goal.RIGHT_SIDE:
            self.goal = Dartboard.Goal.RIGHT_BACK
        elif self.goal == Dartboard.Goal.RIGHT_BACK:
            self.goal = Dartboard.Goal.LEFT_FORWARD
        elif self.goal == Dartboard.Goal.LEFT_FORWARD:
            self.goal = Dartboard.Goal.LEFT_SIDE
        elif self.goal == Dartboard.Goal.LEFT_SIDE:
            self.goal = Dartboard.Goal.LEFT_BACK
        elif self.goal == Dartboard.Goal.LEFT_BACK:
            self.goal = Dartboard.Goal.RIGHT_FORWARD


    def set_initial_values(self, pose: dict) -> None:
        initial_pose = {kp['name']: kp for kp in pose['keypoints']}
        self.left_ankle_start_y = initial_pose['left_ankle'][self.y]
        self.left_ankle_start_x = initial_pose['left_ankle'][self.x]
        self.right_ankle_start_y = initial_pose['right_ankle'][self.y]
        self.right_ankle_start_x = initial_pose['right_ankle'][self.x]


    def get_diff(self, a: float, b: float) -> float:
        return b - a if self.is_lab_data else a - b


    def stepped_correctly(self, pose: dict) -> bool:
        if self.goal == Dartboard.Goal.RIGHT_FORWARD:
            right_ankle_y = pose['right_ankle'][self.y]
            if self.get_diff(right_ankle_y, self.right_ankle_start_y) > self.y_target_change_forward:
                return True
        elif self.goal == Dartboard.Goal.RIGHT_SIDE:
            right_ankle_x = pose['right_ankle'][self.x]
            if self.right_ankle_start_x - right_ankle_x > self.x_target_change:
                return True
        elif self.goal == Dartboard.Goal.RIGHT_BACK:
            right_ankle_y = pose['right_ankle'][self.y]
            if self.get_diff(self.right_ankle_start_y, right_ankle_y) > self.y_target_change_backward:
                return True
        elif self.goal == Dartboard.Goal.LEFT_FORWARD:
            left_ankle_y = pose['left_ankle'][self.y]
            if self.get_diff(left_ankle_y, self.left_ankle_start_y) > self.y_target_change_forward:
                return True
        elif self.goal == Dartboard.Goal.LEFT_SIDE:
            left_ankle_x = pose['left_ankle'][self.x]
            if left_ankle_x - self.left_ankle_start_x > self.x_target_change:
                return True
        elif self.goal == Dartboard.Goal.LEFT_BACK:
            left_ankle_y = pose['left_ankle'][self.y]
            if self.get_diff(self.left_ankle_start_y, left_ankle_y) > self.y_target_change_backward:
                return True
        return False


    def is_off_balance(self, pose: dict) -> bool:
        rshoulder = pose['right_shoulder']
        lshoulder = pose['left_shoulder']
        rhip = pose['right_hip']
        lhip = pose['left_hip']
        rknee = pose['right_knee']
        lknee = pose['left_knee']
        rlat_spinal_flex = self.calc_joint_angle(self.x, rshoulder, rhip, rknee)
        llat_spinal_flex = self.calc_joint_angle(self.x, lshoulder, lhip, lknee)
        if (self.goal == Dartboard.Goal.LEFT_SIDE
            or self.goal == Dartboard.Goal.RIGHT_SIDE):
            return False
        else:
            return (rlat_spinal_flex < self.lat_spinal_flex_threshold
                    or llat_spinal_flex < self.lat_spinal_flex_threshold)


    def feet_together(self, pose: dict) -> bool:
        left_ankle_x = pose['left_ankle'][self.x]
        left_ankle_y = pose['left_ankle'][self.y]
        right_ankle_x = pose['right_ankle'][self.x]
        right_ankle_y = pose['right_ankle'][self.y]
        if (abs(left_ankle_x - self.left_ankle_start_x) <= self.feet_together_threshold
            and abs(left_ankle_y - self.left_ankle_start_y) <= self.feet_together_threshold
            and abs(right_ankle_x - self.right_ankle_start_x) <= self.feet_together_threshold
            and abs(right_ankle_y - self.right_ankle_start_y) <= self.feet_together_threshold
            ):
            return True
        return False


    def run_check(self, poses: list) -> float:
        self.set_initial_values(poses[0])
        num_consecutive = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}

            if self.stage == Dartboard.Stage.BACK:
                if self.feet_together(pose):
                    self.stage = Dartboard.Stage.AWAY
                continue

            is_off_balance = self.is_off_balance(pose)
            self.handle_failed_interval(is_off_balance, time_since_start)
            if is_off_balance:
                continue

            if self.stepped_correctly(pose):
                num_consecutive += 1

            if num_consecutive == Dartboard.REQUIRED_CONSECUTIVE_FRAMES:
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
                self.next_goal()
                self.stage = Dartboard.Stage.BACK
                num_consecutive = 0

        return poses[-1]['time_since_start'] + 1

