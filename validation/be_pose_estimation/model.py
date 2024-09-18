from abc import ABC, abstractmethod
from typing import Type
import numpy as np
from typing import Tuple

class Model(ABC):
    '''
    An abstract class for pose estimation models used in post-recording pose estimation.

    The purpose of this class is to make it easy to interchange pose estimation models,
    both for running pose estimation and for visualising the results as an animation.

    To run a new pose estimation model, simply implement a class for this model that
    inherits from this class, and import it into the scripts for running pose estimation
    and visualisation.
    '''
    @staticmethod
    @abstractmethod
    def format_pose(pose: list) -> list:
        '''
        Reformat pose data structure as it is received from the model into a more
        readable, generalised format.

        Args:
            pose: a list of keypoints as received from the pose estimation model.

        Returns:
            List containing formatted pose data.
        '''
        pass


    @staticmethod
    @abstractmethod
    def keypoint_connections() -> list:
        '''
        todo
        '''
        pass


    @staticmethod
    @abstractmethod
    def get_pixel_coordinate(keypoint: Tuple[float, float], frame_dimensions: Tuple[int, int]) -> Tuple[int, int]:
        '''
        Args:
            keypoints:          a tuple (x, y) of values for a particular keypoint.
            frame_dimensions:   the dimensions of the frame that the pose estimation model was run on,
                                in the form (width, height).

        Returns:
            An tuple of integers (x, y) representing the pixel coordinate for this keypoint.
        '''
        pass


    @staticmethod
    @abstractmethod
    def image_type() -> Type[np.generic]:
        '''
        Return the image type that this model requires.
        '''
        pass

    @staticmethod
    @abstractmethod
    def path() -> str:
        '''
        Return the path to where this model is stored.
        '''
        pass

