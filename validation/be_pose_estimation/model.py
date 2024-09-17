from abc import ABC, abstractmethod
from typing import Type
import numpy as np

class Model(ABC):
    @staticmethod
    @abstractmethod
    def format_pose(pose: list) -> list:
        '''
        Reformat pose data structure and return it.

        Args:
            pose: a list of keypoints as received from the pose estimation model.

        Returns:
            List containing formatted pose data.
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
