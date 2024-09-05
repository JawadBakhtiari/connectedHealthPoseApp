'''Api for formatting pose estimation data on backend side ('format' function)'''

# The number of keypoints captured by the pose estimation model.
NUM_KEYPOINTS = 39

# The number of values associated with each keypoint (x, y, z, presence, visibility).
VALS_PER_KEYPOINT = 5

# Mappings from indexes in data returned from pose estimation model to joint names.
KEYPOINT_MAPPINGS = {
  0: "nose",
  1: "left_eye_inner",
  2: "left_eye_center",
  3: "left_eye_outer",
  4: "right_eye_inner",
  5: "right_eye_center",
  6: "right_eye_outer",
  7: "left_ear",
  8: "right_ear",
  9: "left_mouth",
  10: "right_mouth",
  11: "left_shoulder",
  12: "right_shoulder",
  13: "left_elbow",
  14: "right_elbow",
  15: "left_wrist",
  16: "right_wrist",
  17: "left_palm",
  18: "right_palm",
  19: "left_index",
  20: "right_index",
  21: "left_pinky",
  22: "right_pinky",
  23: "left_hip",
  24: "right_hip",
  25: "left_knee",
  26: "right_knee",
  27: "left_ankle",
  28: "right_ankle",
  29: "left_heel",
  30: "right_heel",
  31: "left_foot",
  32: "right_foot",
  33: "body_center",
  34: "forehead",
  35: "left_thumb",
  36: "left_hand",
  37: "right_thumb",
  38: "right_hand"
}

def get_keypoint_value_keys(keypoint_index: int):
  '''
    Args:
      keypoint_index: index of keypoint in pose data list.

    Returns:
      list of keys for the values of this keypoint, in this order:
      [x, y, z, visibility, presence]
  '''
  return [
    keypoint_index,
    keypoint_index + 1,
    keypoint_index + 2,
    keypoint_index + 3,
    keypoint_index + 4
  ]

def format_pose(pose: list) -> list:
    '''
    Reformat pose data structure and return it.

    Args:
        pose: a list of keypoints as received from the pose estimation model.

    Returns:
        List containing formatted pose data.
    '''
    formatted_keypoints = []
    for i in range(NUM_KEYPOINTS):
        keypoint_index = i * VALS_PER_KEYPOINT
        formatted_keypoint = format_keypoint(pose, keypoint_index)
        formatted_keypoints.append(formatted_keypoint)
    return formatted_keypoints


def format_keypoint(pose: list, keypoint_index: int) -> dict:
    '''
    Format keypoint data in a more readable way.

    Args:
        pose: list representing a single pose, from pose estimation model
        keypoint_index: index of this keypoint in the pose list

    Returns:
        Dictionary with newly formatted keypoint data.
    '''
    xi, yi, zi, visi, presi = get_keypoint_value_keys(keypoint_index)
    x = pose[xi]
    y = pose[yi]
    z = pose[zi]
    visibility = pose[visi]
    presence = pose[presi]

    return {
        'name': KEYPOINT_MAPPINGS.get(keypoint_index // VALS_PER_KEYPOINT),
        'x': x,
        'y': y,
        'z': z,
        'visibility': visibility,
        'presence': presence
    }
