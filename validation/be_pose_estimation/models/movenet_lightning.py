from .movenet import Movenet

class MovenetLightning(Movenet):
    '''
    One of the two movenet models (faster but less accurate).
    '''
    @staticmethod
    def path() -> str:
        return 'data/models/movenet_lighting.tflite'

