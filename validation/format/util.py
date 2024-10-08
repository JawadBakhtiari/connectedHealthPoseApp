'''Utility functions used for formatting lab data.'''

from .const import (
    X_SUFFIX,
    Y_SUFFIX,
    Z_SUFFIX,
    SHOULDER_X_SUFFIX,
    SHOULDER_Y_SUFFIX,
    SHOULDER_Z_SUFFIX,
  )

def get_x_y_z_suffixes(lab_keypoint: str) -> list:
  '''
    Get x, y, z suffixes for a given lab keypoint.

    Args:
      lab_keypoint: the name of the lab keypoint.

    Returns:
      A list of suffixes [x, y, z].
  '''
  if 'Shoulder' not in lab_keypoint:
    return [X_SUFFIX, Y_SUFFIX, Z_SUFFIX]
  return [SHOULDER_X_SUFFIX, SHOULDER_Y_SUFFIX, SHOULDER_Z_SUFFIX]

