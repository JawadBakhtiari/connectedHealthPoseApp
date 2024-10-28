from enum import Enum
from exercises.exercise import Exercise

class SideBend(Exercise):
    '''
    '''
    ANKLE_MOVEMENT_TOLERANCE_LAB = 509.903
    ANKLE_MOVEMENT_TOLERANCE_MOBILE = 70
    LAT_SPINAL_FLEX_TARGET_MOBILE = 150
    LAT_SPINAL_FLEX_TARGET_LAB = 130.5
    REQUIRED_FRAMES_FLEXED = 8
    OFF_BALANCE_FRAMES_THRESHOLD = 5
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.target_reps = target_reps
        self.direction = SideBend.Direction.EITHER
        self.x = 'x' if not is_lab_data else 'z'
        self.ankle_movement_tolerance = SideBend.ANKLE_MOVEMENT_TOLERANCE_MOBILE if not is_lab_data else SideBend.ANKLE_MOVEMENT_TOLERANCE_LAB
        self.lat_spinal_flex_target = SideBend.LAT_SPINAL_FLEX_TARGET_MOBILE if not is_lab_data else SideBend.LAT_SPINAL_FLEX_TARGET_LAB


    class Direction(Enum):
        LEFT = 1
        RIGHT = 2
        EITHER = 3


    def change_direction(self, pose: dict) -> None:
        if self.direction == SideBend.Direction.LEFT:
            self.direction = SideBend.Direction.RIGHT
        elif self.direction == SideBend.Direction.RIGHT:
            self.direction = SideBend.Direction.LEFT
        else:
            # either
            left = self.check_rep(pose, SideBend.Direction.LEFT)
            right = self.check_rep(pose, SideBend.Direction.RIGHT)
            if left < right:
                self.direction = SideBend.Direction.RIGHT
            else:
                self.direction = SideBend.Direction.LEFT


    def check_rep(self, pose: dict, direction: Direction):
        if direction == SideBend.Direction.LEFT:
            lshoulder = pose['left_shoulder']
            lhip = pose['left_hip']
            lknee = pose['left_knee']
            return self.calc_joint_angle(self.x, lshoulder, lhip, lknee)
        elif direction == SideBend.Direction.RIGHT:
            rshoulder = pose['right_shoulder']
            rhip = pose['right_hip']
            rknee = pose['right_knee']
            return self.calc_joint_angle(self.x, rshoulder, rhip, rknee)
        else:
            # either
            left = self.check_rep(pose, SideBend.Direction.LEFT)
            right = self.check_rep(pose, SideBend.Direction.RIGHT)
            return min(left, right)


    def run_check(self, poses: list) -> float:
        failing = False
        consecutive_frames_flexed = 0
        failed_interval_start = None
        failed_interval_end = None
        initial_pose = {kp['name']: kp for kp in poses[0]['keypoints']}
        left_ankle_start_x = initial_pose['left_ankle'][self.x]
        right_ankle_start_x = initial_pose['right_ankle'][self.x]
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}

            spinal_flexion = self.check_rep(pose, self.direction)
            if spinal_flexion <= self.lat_spinal_flex_target:
                consecutive_frames_flexed += 1
            else:
                consecutive_frames_flexed = 0

            left_ankle_x = pose['left_ankle'][self.x]
            right_ankle_x = pose['right_ankle'][self.x]
            if (abs(left_ankle_start_x - left_ankle_x) > self.ankle_movement_tolerance
                or abs(right_ankle_start_x - right_ankle_x) > self.ankle_movement_tolerance):
                failing = True
                consecutive_frames_flexed = 0
                if not failed_interval_start:
                    failed_interval_start = time_since_start
                else:
                    failed_interval_end = time_since_start
                continue
            else:
                failing = False

            if not failing and failed_interval_end:
                self.failing_intervals.append((failed_interval_start, failed_interval_end))
                failed_interval_start = None
                failed_interval_end = None

            if consecutive_frames_flexed == SideBend.REQUIRED_FRAMES_FLEXED:
                self.change_direction(pose)
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
        return poses[-1]['time_since_start'] + 1

