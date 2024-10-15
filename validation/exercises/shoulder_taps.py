from enum import Enum
from exercises.exercise import Exercise

class ShoulderTaps(Exercise):
    '''
    '''
    X_THRESHOLD = 120
    Y_THRESHOLD = 100


    class Stage(Enum):
        PENDING = 1
        LSHOULDER_TAPPED = 2
        RSHOULDER_TAPPED = 3


    def __init__(self, target_reps: int):
        super().__init__()
        self.target_reps = target_reps
        self.stage = ShoulderTaps.Stage.PENDING


    def run_check(self, poses: list) -> float:
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
                if (abs(lshoulder_x - rwrist_x) < ShoulderTaps.X_THRESHOLD
                    and abs(lshoulder_y - rwrist_y) < ShoulderTaps.Y_THRESHOLD):
                    self.stage = ShoulderTaps.Stage.LSHOULDER_TAPPED
                    self.rep_times.append(time_since_start)
                elif (abs(rshoulder_x - lwrist_x) < ShoulderTaps.X_THRESHOLD
                    and abs(rshoulder_y - lwrist_y) < ShoulderTaps.Y_THRESHOLD):
                    self.stage = ShoulderTaps.Stage.RSHOULDER_TAPPED
                    self.rep_times.append(time_since_start)
            elif self.stage == ShoulderTaps.Stage.LSHOULDER_TAPPED:
                if (abs(lshoulder_x - rwrist_x) > ShoulderTaps.X_THRESHOLD
                    or abs(lshoulder_y - rwrist_y) > ShoulderTaps.Y_THRESHOLD):
                    self.stage = ShoulderTaps.Stage.PENDING
            elif self.stage == ShoulderTaps.Stage.RSHOULDER_TAPPED:
                if (abs(rshoulder_x - lwrist_x) > ShoulderTaps.X_THRESHOLD
                    or abs(rshoulder_y - lwrist_y) > ShoulderTaps.Y_THRESHOLD):
                    self.stage = ShoulderTaps.Stage.PENDING

            if self.target_reps == len(self.rep_times):
                return time_since_start

        return poses[-1]['time_since_start'] + 1

