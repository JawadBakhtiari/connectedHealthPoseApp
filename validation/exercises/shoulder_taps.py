from enum import Enum
from exercises.exercise import Exercise
from exercises.balance import Balance

class ShoulderTaps(Exercise):
    '''
    '''
    MOBILE_X_THRESHOLD = 120
    MOBILE_Y_THRESHOLD = 100
    LAB_X_THRESHOLD = 600
    LAB_Y_THRESHOLD = 450


    class Stage(Enum):
        PENDING = 1
        LSHOULDER_TAPPED = 2
        RSHOULDER_TAPPED = 3


    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.balance = Balance()
        self.target_reps = target_reps
        self.stage = ShoulderTaps.Stage.PENDING
        if is_lab_data:
            self.x_threshold = ShoulderTaps.LAB_X_THRESHOLD
            self.y_threshold = ShoulderTaps.LAB_Y_THRESHOLD
        else:
            self.x_threshold = ShoulderTaps.MOBILE_X_THRESHOLD
            self.y_threshold = ShoulderTaps.MOBILE_Y_THRESHOLD


    def run_check(self, poses: list) -> float:
        self.balance.run_check(poses)
        self.failing_intervals = self.balance.failing_intervals
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            rshoulder_x = pose['right_shoulder']['x']
            rshoulder_y = pose['right_shoulder']['y']
            lshoulder_x = pose['left_shoulder']['x']
            lshoulder_y = pose['left_shoulder']['y']
            rwrist_x = pose['right_wrist']['x']
            rwrist_y = pose['right_wrist']['y']
            lwrist_x = pose['left_wrist']['x']
            lwrist_y = pose['left_wrist']['y']

            if self.stage == ShoulderTaps.Stage.PENDING:
                if (abs(lshoulder_x - rwrist_x) < self.x_threshold
                    and abs(lshoulder_y - rwrist_y) < self.y_threshold):
                    self.stage = ShoulderTaps.Stage.LSHOULDER_TAPPED
                    self.rep_times.append(time_since_start)
                elif (abs(rshoulder_x - lwrist_x) < self.x_threshold
                    and abs(rshoulder_y - lwrist_y) < self.y_threshold):
                    self.stage = ShoulderTaps.Stage.RSHOULDER_TAPPED
                    self.rep_times.append(time_since_start)
            elif self.stage == ShoulderTaps.Stage.LSHOULDER_TAPPED:
                if (abs(lshoulder_x - rwrist_x) > self.x_threshold
                    or abs(lshoulder_y - rwrist_y) > self.y_threshold):
                    self.stage = ShoulderTaps.Stage.PENDING
            elif self.stage == ShoulderTaps.Stage.RSHOULDER_TAPPED:
                if (abs(rshoulder_x - lwrist_x) > self.x_threshold
                    or abs(rshoulder_y - lwrist_y) > self.y_threshold):
                    self.stage = ShoulderTaps.Stage.PENDING

            if self.target_reps == len(self.rep_times):
                return time_since_start

        return poses[-1]['time_since_start'] + 1

