from .movenet_model import MovenetModel

class MovenetLightning(MovenetModel):
    '''
    One of the two movenet models (faster but less accurate).
    '''
    @staticmethod
    def path() -> str:
        return 'data/models/movenet_lighting.tflite'

