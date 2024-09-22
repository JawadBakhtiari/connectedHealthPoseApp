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
    1: 'left_eye',
    2: 'right_eye',
    3: 'left_ear',
    4: 'right_ear',
    5: 'left_shoulder',
    6: 'right_shoulder',
    7: 'left_elbow',
    8: 'right_elbow',
    9: 'left_wrist',
    10: 'right_wrist',
    11: 'left_hip',
    12: 'right_hip',
    13: 'left_knee',
    14: 'right_knee',
    15: 'left_ankle',
    16: 'right_ankle'
}

class Movenet(Model):
    '''
    A parent class for the movenet models 'lightning' and 'thunder'.
    '''
    @staticmethod
    def image_type() -> Type[np.generic]:
        return np.uint8


    @staticmethod
    def format_pose(pose: list) -> list:
        format_keypoint = lambda i, kp: {
            'name': KEYPOINT_MAPPINGS.get(i),
            'x': kp[1],
            'y': kp[0],
            'confidence': kp[2]
        }
        return [format_keypoint(i, kp) for i, kp in enumerate(pose[0])]


    @staticmethod
    def get_pixel_coordinate(keypoint: Tuple[float, float], frame_dimensions: Tuple[int, int]) -> Tuple[int, int]:
        return (int(keypoint[0] * frame_dimensions[0]), int(keypoint[1] * frame_dimensions[1]))

    @staticmethod
    def joint_connections() -> list:
        return [
            (0, 1),
            (0, 2),
            (1, 3),
            (2, 4),
            (5, 6),
            (5, 7),
            (7, 9),
            (6, 8),
            (8, 10),
            (11, 12),
            (5, 11),
            (6, 12),
            (11, 13),
            (13, 15),
            (12, 14),
            (14, 16),
        ]

