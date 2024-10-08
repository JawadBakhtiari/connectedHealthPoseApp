import math
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


    def run_check(self, poses: list) -> float:
        check_seated = True
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            wrist_height = pose['left_wrist']['y']
            hip_height = pose['left_hip']['y']
            if (self.height_comparator(wrist_height, hip_height)):
                # Hands must be on shoulders throughout exercise, so check
                # that hands are above hips or the rep doesn't count.
                check_seated = True
            knee_flexion = self.calc_joint_angle(self.x, pose['right_ankle'], pose['right_knee'], pose['right_hip'])
            if check_seated:
                if knee_flexion <= SitToStand.MAX_KNEE_FLEXION:
                    check_seated = False
            elif knee_flexion >= SitToStand.MAX_KNEE_EXTENSION:
                check_seated = True
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
        return poses[-1]['time_since_start'] + 1

