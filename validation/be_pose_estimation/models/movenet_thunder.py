from .movenet import Movenet

class MovenetThunder(Movenet):
    '''
    One of the two movenet models (slower but more accurate).
    '''
    @staticmethod
    def path() -> str:
        return 'be_pose_estimation/data/models/movenet_thunder.tflite'

