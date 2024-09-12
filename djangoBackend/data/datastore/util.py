def get_keypoint_value_keys(keypoint_index: int):
  '''
    Args:
      keypoint_index: index of keypoint in pose data list.

    Returns:
      list of keys for the values of this keypoint, in this order:
      [x, y, z, visibility, presence]
  '''
  return [
    str(keypoint_index),
    str(keypoint_index + 1),
    str(keypoint_index + 2),
    str(keypoint_index + 3),
    str(keypoint_index + 4)
  ]