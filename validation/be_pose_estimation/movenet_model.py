from .model import Model
from typing import Type
import numpy as np
from typing import Tuple

# The number of keypoints captured by the pose estimation model.
NUM_KEYPOINTS = 17

# The number of values associated with each keypoint (x, y, confidence).
VALS_PER_KEYPOINT = 3

# Mappings from indexes in data returned from pose estimation model to joint names.
KEYPOINT_MAPPINGS = {
    0: 'nose',
    1: 'left eye',
    2: 'right eye',
    3: 'left ear',
    4: 'right ear',
    5: 'left shoulder',
    6: 'right shoulder',
    7: 'left elbow',
    8: 'right elbow',
    9: 'left wrist',
    10: 'right wrist',
    11: 'left hip',
    12: 'right hip',
    13: 'left knee',
    14: 'right knee',
    15: 'left ankle',
    16: 'right ankle'
}

class MovenetModel(Model):
    @staticmethod
    def image_type() -> Type[np.generic]:
        return np.uint8


    @staticmethod
    def format_pose(pose: list) -> list:
        format_keypoint = lambda i, kp: {
            'name': KEYPOINT_MAPPINGS.get(i),
            'x': kp[0],
            'y': kp[1],
            'confidence': kp[2]
        }
        return [format_keypoint(i, kp) for i, kp in enumerate(pose[0])]


    @staticmethod
    def get_pixel_coordinate(keypoint: Tuple[float, float], frame_dimensions: Tuple[int, int]) -> Tuple[int, int]:
        return (int(keypoint[0] * frame_dimensions[0]), int(keypoint[1] * frame_dimensions[1]))


    @staticmethod
    def path() -> str:
        return 'data/models/movenet_lightning.tflite'

