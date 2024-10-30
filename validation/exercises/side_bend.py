from enum import Enum
from exercises.exercise import Exercise

class SideBend(Exercise):
    '''
    Count side bend exercise repetitions.

    Also detect being off balance as a failure of the current rep,
    where being off balance is defined as moving either foot out
    of tandem position.
    '''
    ANKLE_MOVEMENT_TOLERANCE_LAB = 509.903
    ANKLE_MOVEMENT_TOLERANCE_MOBILE = 70
    LAT_SPINAL_FLEX_TARGET_MOBILE = 148
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


    def set_initial_values(self, pose: dict) -> None:
        initial_pose = {kp['name']: kp for kp in pose['keypoints']}
        self.left_ankle_start_x = initial_pose['left_ankle'][self.x]
        self.right_ankle_start_x = initial_pose['right_ankle'][self.x]


    def change_direction(self, pose: dict) -> None:
        if self.direction == SideBend.Direction.LEFT:
            self.direction = SideBend.Direction.RIGHT
        elif self.direction == SideBend.Direction.RIGHT:
            self.direction = SideBend.Direction.LEFT
        else:
            # either
            left = self.get_spinal_flexion(pose, SideBend.Direction.LEFT)
            right = self.get_spinal_flexion(pose, SideBend.Direction.RIGHT)
            if left < right:
                self.direction = SideBend.Direction.RIGHT
            else:
                self.direction = SideBend.Direction.LEFT


    def get_spinal_flexion(self, pose: dict, direction: Direction):
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
            left = self.get_spinal_flexion(pose, SideBend.Direction.LEFT)
            right = self.get_spinal_flexion(pose, SideBend.Direction.RIGHT)
            return min(left, right)


    def run_check(self, poses: list) -> float:
        consecutive_frames_flexed = 0
        self.set_initial_values(poses[0])
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}

            spinal_flexion = self.get_spinal_flexion(pose, self.direction)
            spine_flexed = spinal_flexion <= self.lat_spinal_flex_target
            consecutive_frames_flexed += 1 if spine_flexed else 0
            left_ankle_x = pose['left_ankle'][self.x]
            right_ankle_x = pose['right_ankle'][self.x]
            feet_moved = (
                abs(self.left_ankle_start_x - left_ankle_x) > self.ankle_movement_tolerance
                or abs(self.right_ankle_start_x - right_ankle_x) > self.ankle_movement_tolerance
            )

            self.handle_failed_interval(feet_moved, time_since_start)
            if feet_moved:
                consecutive_frames_flexed = 0

            if consecutive_frames_flexed == SideBend.REQUIRED_FRAMES_FLEXED:
                self.change_direction(pose)
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
                consecutive_frames_flexed = 0
        return poses[-1]['time_since_start'] + 1

