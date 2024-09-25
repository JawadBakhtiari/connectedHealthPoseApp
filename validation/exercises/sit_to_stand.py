import math
from exercises.exercise import Exercise

class SitToStand(Exercise):
    '''
    Determine when a target number of sit to stand repetitions have been completed.
    '''
    MAX_KNEE_EXTENSION = 145
    MAX_KNEE_FLEXION = 90
    def __init__(self, target_reps):
        super().__init__()
        self.target_reps = target_reps


    @staticmethod
    def calc_joint_angle(initial_side: dict, vertex: dict, terminal_side: dict):
        v1 = (vertex['x'] - initial_side['x'], vertex['y'] - initial_side['y'])
        v2 = (vertex['x'] - terminal_side['x'], vertex['y'] - terminal_side['y'])

        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
        magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

        cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
        angle_radians = math.acos(cos_angle)
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees


    def run_check(self, poses: list) -> float:
        check_seated = True
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            wrist_height = pose['left_wrist']['y']
            hip_height = pose['left_hip']['y']
            if (wrist_height > hip_height):
                # Hands must be on shoulders throughout exercise.
                # This seems backwards, but it's checking that hands
                # are above hips or else the rep doesn't count
                check_seated = True
            knee_flexion = SitToStand.calc_joint_angle(pose['left_ankle'], pose['left_knee'], pose['left_hip'])
            if check_seated:
                if knee_flexion <= SitToStand.MAX_KNEE_FLEXION:
                    check_seated = False
            elif knee_flexion >= SitToStand.MAX_KNEE_EXTENSION:
                check_seated = True
                self.rep_times.append(time_since_start)
                if len(self.rep_times) == self.target_reps:
                    return time_since_start
        return poses[-1]['time_since_start'] + 1

