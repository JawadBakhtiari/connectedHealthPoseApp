from enum import Enum
from exercises.exercise import Exercise

class BicepCurls(Exercise):
    '''
    Identify repetitions of bicep curls.

    Also identifies excessive shoulder flexion as poor form.
    '''
    MAX_ELBOW_EXTENSION = 140
    MAX_ELBOW_FLEXION = 65
    MAX_SHOULDER_FLEXION = 40
    SHOULDER_FLEXION_CEILING = 120
    REQUIRED_CONSECUTIVE = 3
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.target_reps = target_reps
        self.stage = BicepCurls.Stage.EXTENDING
        self.x = 'x' if not is_lab_data else 'z'


    class Stage(Enum):
        FLEXING = 1
        EXTENDING = 2


    def run_check(self, poses: list) -> float:
        num_consecutive = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            elbow_flexion = self.calc_joint_angle(self.x, pose['right_wrist'], pose['right_elbow'], pose['right_shoulder'])
            shoulder_flexion = self.calc_joint_angle(self.x, pose['right_elbow'], pose['right_shoulder'], pose['right_hip'])

            shoulder_too_flexed = (
                shoulder_flexion >= BicepCurls.MAX_SHOULDER_FLEXION
                and shoulder_flexion <= BicepCurls.SHOULDER_FLEXION_CEILING
            )
            self.handle_failed_interval(shoulder_too_flexed, time_since_start)
            if shoulder_too_flexed:
                self.stage = BicepCurls.Stage.EXTENDING

            if self.stage == BicepCurls.Stage.FLEXING and elbow_flexion <= BicepCurls.MAX_ELBOW_FLEXION:
                num_consecutive += 1
                if num_consecutive == BicepCurls.REQUIRED_CONSECUTIVE:
                    self.stage = BicepCurls.Stage.EXTENDING
                    self.rep_times.append(time_since_start)
                    if len(self.rep_times) == self.target_reps:
                        return time_since_start
                    num_consecutive = 0
            elif self.stage == BicepCurls.Stage.EXTENDING and elbow_flexion >= BicepCurls.MAX_ELBOW_EXTENSION:
                num_consecutive += 1
                if num_consecutive == BicepCurls.REQUIRED_CONSECUTIVE:
                    self.stage = BicepCurls.Stage.FLEXING
                    num_consecutive = 0
        return poses[-1]['time_since_start'] + 1

