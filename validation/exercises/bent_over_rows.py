from enum import Enum
from exercises.exercise import Exercise

class BentOverRows(Exercise):
    '''
    Detect repetitions of the bent over rows exercise.

    Poor form (not hinging enough at the hips) is also tracked.
    Over arching/rounding of the spine is not tracked.
    '''
    MAX_ELBOW_EXTENSION = 170
    MAX_ELBOW_FLEXION = 90
    MAX_HIP_EXTENSION = 110
    REQUIRED_CONSECUTIVE = 3
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.target_reps = target_reps
        self.stage = BentOverRows.Stage.FLEXING


    class Stage(Enum):
        FLEXING = 1
        EXTENDING = 2


    def run_check(self, poses: list) -> float:
        num_consecutive = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            try:
                elbow_flexion = self.calc_joint_angle('x', pose['left_wrist'], pose['left_elbow'], pose['left_shoulder'])
                hip_flexion = self.calc_joint_angle('x', pose['left_shoulder'], pose['left_hip'], pose['left_knee'])
            except:
                continue

            hips_not_flexed_enough = hip_flexion >= BentOverRows.MAX_HIP_EXTENSION
            self.handle_failed_interval(hips_not_flexed_enough, time_since_start)
            if hips_not_flexed_enough:
                self.stage = BentOverRows.Stage.FLEXING
                continue

            if self.stage == BentOverRows.Stage.FLEXING and elbow_flexion <= BentOverRows.MAX_ELBOW_FLEXION:
                num_consecutive += 1
                if num_consecutive == BentOverRows.REQUIRED_CONSECUTIVE:
                    self.stage = BentOverRows.Stage.EXTENDING
                    num_consecutive = 0
            elif self.stage == BentOverRows.Stage.EXTENDING and elbow_flexion >= BentOverRows.MAX_ELBOW_EXTENSION:
                num_consecutive += 1
                if num_consecutive == BentOverRows.REQUIRED_CONSECUTIVE:
                    self.stage = BentOverRows.Stage.FLEXING
                    self.rep_times.append(time_since_start)
                    if len(self.rep_times) == self.target_reps:
                        return time_since_start
                    num_consecutive = 0

        return poses[-1]['time_since_start'] + 1

