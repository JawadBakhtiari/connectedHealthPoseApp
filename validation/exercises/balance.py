from exercises.exercise import Exercise

class Balance(Exercise):
    '''
    '''
    # LAT_SPINAL_FLEX_THRESHOLD = 160
    LAT_SPINAL_FLEX_THRESHOLD = 170
    def __init__(self):
        super().__init__()


    def run_check(self, poses: list) -> float:
        failed_interval_start = None
        failed_interval_end = None
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
                print(rlat_spinal_flex, llat_spinal_flex)
                if (rlat_spinal_flex < Balance.LAT_SPINAL_FLEX_THRESHOLD
                    or llat_spinal_flex < Balance.LAT_SPINAL_FLEX_THRESHOLD):
                    if failed_interval_start:
                        failed_interval_end = time_since_start
                    else:
                        failed_interval_start = time_since_start
                elif failed_interval_start:
                    if failed_interval_end:
                        self.failing_intervals.append((failed_interval_start, failed_interval_end))
                        failed_interval_end = None
                    failed_interval_start = None
            except:
                continue
        return poses[-1]['time_since_start'] + 1

