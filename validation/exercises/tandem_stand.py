from exercises.exercise import Exercise

class TandemStand(Exercise):
    '''
    Determine when a tandem stand exercise has ended (when one or
    both feet deviate too much from their original positions).

    Note that video must start with feet in tandem position.
    '''
    FRAME_WIDTH = 1080
    ANKLE_MOVEMENT_TOLERANCE = 30 / FRAME_WIDTH
    REQUIRED_CONSECUTIVE_FRAMES_OUT = 5

    def __init__(self):
        super().__init__()


    def run_check(self, poses: list) -> float:
        initial_pose = {kp['name']: kp for kp in poses[0]['keypoints']}
        left_ankle_start_x = initial_pose['left_ankle']['x']
        left_ankle_start_y = initial_pose['left_ankle']['y']
        right_ankle_start_x = initial_pose['right_ankle']['x']
        right_ankle_start_y = initial_pose['right_ankle']['y']
        consecutive_frames_out = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            left_ankle_x = pose['left_ankle']['x']
            left_ankle_y = pose['left_ankle']['y']
            right_ankle_x = pose['right_ankle']['x']
            right_ankle_y = pose['right_ankle']['y']
            if (abs(left_ankle_start_x - left_ankle_x) > TandemStand.ANKLE_MOVEMENT_TOLERANCE
                or abs(left_ankle_start_y - left_ankle_y) > TandemStand.ANKLE_MOVEMENT_TOLERANCE
                or abs(right_ankle_start_x - right_ankle_x) > TandemStand.ANKLE_MOVEMENT_TOLERANCE
                or abs(right_ankle_start_y - right_ankle_y) > TandemStand.ANKLE_MOVEMENT_TOLERANCE):
                consecutive_frames_out += 1
            else:
                consecutive_frames_out = 0
            if consecutive_frames_out >= TandemStand.REQUIRED_CONSECUTIVE_FRAMES_OUT:
                self.rep_times.append(time_since_start)
                return time_since_start
        return poses[-1]['time_since_start'] + 1

