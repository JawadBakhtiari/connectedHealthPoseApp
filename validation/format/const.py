'''Constants used for formatting lab data.'''

LAB_START_TIME_FORMAT = "%Y-%m-%d %I.%M.%S.%f %p"
LAB_START_TIME_INDEX = 11
X_SUFFIX = '.4'
Y_SUFFIX = '.5'
Z_SUFFIX = '.6'

LSHOULDER = 'Skeleton 001:LShoulder'
RSHOULDER = 'Skeleton 001:RShoulder'

LAB_KEYPOINTS = [
  LSHOULDER,
  RSHOULDER,
]

KEYPOINT_MAPPINGS = {
  LSHOULDER : 'left_shoulder',
  RSHOULDER: 'right_shoulder'
}
