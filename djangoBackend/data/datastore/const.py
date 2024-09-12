# Azure blob storage constants.
AZ_ACCOUNT_NAME = "connectedhealth"
AZ_ACCOUNT_KEY = "wq4q+wFN99NgDz0kkYdbTAArr5zrJH0x2yG9EFKgO13QYFlqrlX/9JvQRrKCEFAMQ77koN+oEP28+ASty7DtRA=="
AZ_CON_STR = f"DefaultEndpointsProtocol=https;AccountName={AZ_ACCOUNT_NAME};AccountKey={AZ_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
AZ_POSES_CONTAINER_NAME = "poses"
AZ_VIDEOS_CONTAINER_NAME = "videos"

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
