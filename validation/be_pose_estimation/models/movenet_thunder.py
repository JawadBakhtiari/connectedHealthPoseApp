from .movenet import Movenet

class MovenetThunder(Movenet):
    '''
    One of the two movenet models (slower but more accurate).
    '''
    @staticmethod
    def path() -> str:
        return 'data/models/movenet_thunder.tflite'

