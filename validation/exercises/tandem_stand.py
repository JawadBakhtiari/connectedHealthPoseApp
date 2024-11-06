from exercises.exercise import Exercise

class TandemStand(Exercise):
    '''
    Determine when a tandem stand exercise has ended (when one or
    both feet deviate too much from their original positions).

    Note that video must start with feet in tandem position.
    '''
    ANKLE_MOVEMENT_TOLERANCE_LAB = 509.903
    ANKLE_MOVEMENT_TOLERANCE_MOBILE = 50
    REQUIRED_CONSECUTIVE_FRAMES_OUT = 5

    def __init__(self, is_lab_data: bool = False):
        super().__init__()
        self.x = 'x' if not is_lab_data else 'z'
        self.ankle_movement_tolerance = TandemStand.ANKLE_MOVEMENT_TOLERANCE_MOBILE if not is_lab_data else TandemStand.ANKLE_MOVEMENT_TOLERANCE_LAB


    def run_check(self, poses: list) -> float:
        initial_pose = {kp['name']: kp for kp in poses[0]['keypoints']}
        left_ankle_start_x = initial_pose['left_ankle'][self.x]
        right_ankle_start_x = initial_pose['right_ankle'][self.x]
        consecutive_frames_out = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}

            self.handle_failed_interval(self.is_off_balance(pose, self.x), time_since_start)

            left_ankle_x = pose['left_ankle'][self.x]
            right_ankle_x = pose['right_ankle'][self.x]
            if (abs(left_ankle_start_x - left_ankle_x) > self.ankle_movement_tolerance
                or abs(right_ankle_start_x - right_ankle_x) > self.ankle_movement_tolerance):
                consecutive_frames_out += 1
            else:
                consecutive_frames_out = 0
            if consecutive_frames_out >= TandemStand.REQUIRED_CONSECUTIVE_FRAMES_OUT:
                self.rep_times.append(time_since_start)
                return time_since_start
        return poses[-1]['time_since_start'] + 1

