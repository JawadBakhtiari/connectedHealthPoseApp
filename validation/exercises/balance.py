from exercises.exercise import Exercise

class Balance(Exercise):
    '''
    Add failing intervals for the times when the patient is
    off balance.

    Off balance is defined as the degree of lateral spinal flexion
    surpassing a set threshold (leaning too much to either side).
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
                rlat_spinal_flex = self.calc_joint_angle('x', rshoulder, rhip, rknee)
                llat_spinal_flex = self.calc_joint_angle('x', lshoulder, lhip, lknee)
                spine_too_flexed = (
                    rlat_spinal_flex < Balance.LAT_SPINAL_FLEX_THRESHOLD
                    or llat_spinal_flex < Balance.LAT_SPINAL_FLEX_THRESHOLD
                )
                self.handle_failed_interval(spine_too_flexed, time_since_start)
            except:
                continue
        return poses[-1]['time_since_start'] + 1

