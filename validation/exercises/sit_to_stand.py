from enum import Enum
import operator
from exercises.exercise import Exercise

class SitToStand(Exercise):
    '''
    Determine when a target number of sit to stand repetitions have been completed.
    '''
    MAX_KNEE_EXTENSION = 145
    MAX_KNEE_FLEXION = 103
    def __init__(self, target_reps: int, is_lab_data: bool = False):
        super().__init__()
        self.target_reps = target_reps
        self.height_comparator = operator.gt if not is_lab_data else operator.lt
        self.x = 'x' if not is_lab_data else 'z'
        self.stage = SitToStand.Stage.STANDING


    class Stage(Enum):
        SEATED = 1
        STANDING = 2


    def run_check(self, poses: list) -> float:
        failed_interval_start = None
        failed_interval_end = None
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            wrist_height = pose['left_wrist']['y']
            hip_height = pose['left_hip']['y']
            if (self.height_comparator(wrist_height, hip_height)):
                # Hands must be on shoulders throughout exercise, so check
                # that hands are above hips or the rep doesn't count.
                self.stage = SitToStand.Stage.STANDING
                if failed_interval_start:
                    failed_interval_end = time_since_start
                else:
                    failed_interval_start = time_since_start
            elif failed_interval_start:
                if failed_interval_end:
                    self.failing_intervals.append((failed_interval_start, failed_interval_end))
                    failed_interval_end = None
                failed_interval_start = None
            knee_flexion = self.calc_joint_angle(self.x, pose['right_ankle'], pose['right_knee'], pose['right_hip'])
            if self.stage == SitToStand.Stage.STANDING and knee_flexion <= SitToStand.MAX_KNEE_FLEXION:
               self.stage = SitToStand.Stage.SEATED
            elif self.stage == SitToStand.Stage.SEATED and knee_flexion >= SitToStand.MAX_KNEE_EXTENSION:
                self.stage = SitToStand.Stage.STANDING
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
        return poses[-1]['time_since_start'] + 1

