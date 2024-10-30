from enum import Enum
from exercises.exercise import Exercise

class Dartboard(Exercise):
    '''
    Detect dartboard stepping exercise repetitions.

    Also tracks being too off balance as poor form.
    Currently does nothing to identify mis-steps.
    '''
    LAT_SPINAL_FLEX_THRESHOLD = 160
    Y_TARGET_CHANGE_BACKWARD = 25
    Y_TARGET_CHANGE_FORWARD = 55
    X_TARGET_CHANGE = 200
    FEET_TOGETHER_THRESHOLD = 30
    REQUIRED_CONSECUTIVE_FRAMES = 3
    def __init__(self, target_reps: int):
        super().__init__()
        self.goal = Dartboard.Goal.RIGHT_FORWARD
        self.stage = Dartboard.Stage.AWAY
        self.target_reps = target_reps * len(Dartboard.Goal)


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
        self.left_ankle_start_y = initial_pose['left_ankle']['y']
        self.left_ankle_start_x = initial_pose['left_ankle']['x']
        self.right_ankle_start_y = initial_pose['right_ankle']['y']
        self.right_ankle_start_x = initial_pose['right_ankle']['x']


    def stepped_correctly(self, pose: dict) -> bool:
        if self.goal == Dartboard.Goal.RIGHT_FORWARD:
            right_ankle_y = pose['right_ankle']['y']
            if right_ankle_y - self.right_ankle_start_y > Dartboard.Y_TARGET_CHANGE_FORWARD:
                return True
        elif self.goal == Dartboard.Goal.RIGHT_SIDE:
            right_ankle_x = pose['right_ankle']['x']
            if self.right_ankle_start_x - right_ankle_x > Dartboard.X_TARGET_CHANGE:
                return True
        elif self.goal == Dartboard.Goal.RIGHT_BACK:
            right_ankle_y = pose['right_ankle']['y']
            if self.right_ankle_start_y - right_ankle_y > Dartboard.Y_TARGET_CHANGE_BACKWARD:
                return True
        elif self.goal == Dartboard.Goal.LEFT_FORWARD:
            left_ankle_y = pose['left_ankle']['y']
            if left_ankle_y - self.left_ankle_start_y > Dartboard.Y_TARGET_CHANGE_FORWARD:
                return True
        elif self.goal == Dartboard.Goal.LEFT_SIDE:
            left_ankle_x = pose['left_ankle']['x']
            if left_ankle_x - self.left_ankle_start_x > Dartboard.X_TARGET_CHANGE:
                return True
        elif self.goal == Dartboard.Goal.LEFT_BACK:
            left_ankle_y = pose['left_ankle']['y']
            if self.left_ankle_start_y - left_ankle_y > Dartboard.Y_TARGET_CHANGE_BACKWARD:
                return True
        return False


    def is_off_balance(self, pose: dict) -> bool:
        rshoulder = pose['right_shoulder']
        lshoulder = pose['left_shoulder']
        rhip = pose['right_hip']
        lhip = pose['left_hip']
        rknee = pose['right_knee']
        lknee = pose['left_knee']
        rlat_spinal_flex = self.calc_joint_angle('x', rshoulder, rhip, rknee)
        llat_spinal_flex = self.calc_joint_angle('x', lshoulder, lhip, lknee)
        if (self.goal == Dartboard.Goal.LEFT_SIDE
            or self.goal == Dartboard.Goal.RIGHT_SIDE):
            return False
        else:
            return (rlat_spinal_flex < Dartboard.LAT_SPINAL_FLEX_THRESHOLD
                    or llat_spinal_flex < Dartboard.LAT_SPINAL_FLEX_THRESHOLD)


    def feet_together(self, pose: dict) -> bool:
        left_ankle_x = pose['left_ankle']['x']
        left_ankle_y = pose['left_ankle']['y']
        right_ankle_x = pose['right_ankle']['x']
        right_ankle_y = pose['right_ankle']['y']
        if (abs(left_ankle_x - self.left_ankle_start_x) <= Dartboard.FEET_TOGETHER_THRESHOLD
            and abs(left_ankle_y - self.left_ankle_start_y) <= Dartboard.FEET_TOGETHER_THRESHOLD
            and abs(right_ankle_x - self.right_ankle_start_x) <= Dartboard.FEET_TOGETHER_THRESHOLD
            and abs(right_ankle_y - self.right_ankle_start_y) <= Dartboard.FEET_TOGETHER_THRESHOLD):
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

