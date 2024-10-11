from exercises.exercise import Exercise

class TimedUpAndGo(Exercise):
    '''
    '''
    MAX_KNEE_EXTENSION = 170
    MAX_KNEE_FLEXION = 90
    TARGET_STS_REPS = 1
    def __init__(self):
        super().__init__()


    def run_check(self, poses: list) -> float:
        check_seated = False
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            try:
                knee_flexion = self.calc_joint_angle('x', pose['left_ankle'], pose['left_knee'], pose['left_hip'])
            except:
                continue
            if not check_seated:
                if knee_flexion >= TimedUpAndGo.MAX_KNEE_EXTENSION:
                    check_seated = True
            elif knee_flexion <= TimedUpAndGo.MAX_KNEE_FLEXION:
                    check_seated = False
                    self.rep_times.append(time_since_start)
                    if len(self.rep_times) == TimedUpAndGo.TARGET_STS_REPS:
                        return time_since_start
        return poses[-1]['time_since_start'] + 1

