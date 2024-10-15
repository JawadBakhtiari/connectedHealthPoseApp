from exercises.exercise import Exercise

class Balance(Exercise):
    '''
    '''
    LAT_SPINAL_FLEX_THRESHOLD = 160
    def __init__(self):
        super().__init__()


    def run_check(self, poses: list) -> float:
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            rshoulder = pose['right_shoulder']
            lshoulder = pose['left_shoulder']
            rhip = pose['right_hip']
            lhip = pose['left_hip']
            rknee = pose['right_knee']
            lknee = pose['left_knee']
            try:
                print(self.calc_joint_angle('x', rshoulder, rhip, rknee))
            except:
                continue
        return 2.0

