from exercises.exercise import Exercise

class GridSteps(Exercise):
    '''
    '''
    def __init__(self, target_reps: int):
        super().__init__()
        self.target_reps = target_reps


    def run_check(self, poses: list) -> float:
        return poses[-1]['time_since_start'] + 1

