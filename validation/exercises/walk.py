from exercises.exercise import Exercise

class Walk(Exercise):
    '''
    Determine when a walk from a given starting position to
    a given ending position has been completed.
    '''
    REQUIRED_MATCHING_FRAMES = 3
    FRAME_WIDTH = 1080

    def __init__(self, start_x: int, end_x: int):
        '''
        Args:
            start_x: pixel value for where the walk starts on the x axis.
            end_x: pixel value for where the walk ends on the x axis.
        '''
        super().__init__()

        # Normalise pixel values for use with movenet thunder model
        self.start_x = start_x / Walk.FRAME_WIDTH
        self.end_x = end_x / Walk.FRAME_WIDTH


    def cmp(self, x1: float, x2: float):
        if self.end_x < self.start_x:
            return x1 < self.end_x and x2 < self.end_x
        else:
            return x1 > self.end_x and x2 > self.end_x


    def run_check(self, poses: list) -> float:
        matching_frames = 0
        for pose in poses:
            time_since_start = pose['time_since_start']
            pose = {kp['name']: kp for kp in pose['keypoints']}
            left_hip_x = pose['left_hip']['x']
            right_hip_x = pose['right_hip']['x']
            if self.cmp(left_hip_x, right_hip_x):
                matching_frames += 1
            else:
                matching_frames = 0
            if matching_frames >= Walk.REQUIRED_MATCHING_FRAMES:
                self.rep_times.append(time_since_start)
                return time_since_start
        return poses[-1]['time_since_start'] + 1

