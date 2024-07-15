'''Constants used for formatting lab data.'''

LAB_START_TIME_FORMAT = "%Y-%m-%d %I.%M.%S.%f %p"
LAB_START_TIME_INDEX = 11

SYNC_MARKER_NAME = r'Sync 001:Marker.*[.][345]\b'

# Painfully, shoulder joints have different suffixes
# to all other joints.
X_SUFFIX = '.3'
Y_SUFFIX = '.4'
Z_SUFFIX = '.5'
SHOULDER_X_SUFFIX = '.4'
SHOULDER_Y_SUFFIX = '.5'
SHOULDER_Z_SUFFIX = '.6'

LSHOULDER = 'Skeleton 001:LShoulder'
RSHOULDER = 'Skeleton 001:RShoulder'
LELBOW = 'Skeleton 001:LElbowOut'
RELBOW = 'Skeleton 001:RElbowOut'
LWRIST = 'Skeleton 001:LWristOut'
RWRIST = 'Skeleton 001:RWristOut'
LHIP = 'Skeleton 001:WaistLFront'
RHIP = 'Skeleton 001:WaistRFront'

LAB_KEYPOINTS = [
  LSHOULDER,
  RSHOULDER,
  LELBOW,
  RELBOW,
  LWRIST,
  RWRIST,
  LHIP,
  RHIP,
]

# Mappings from names of keypoints in lab data to their equivalents
# in the mobile data.
KEYPOINT_MAPPINGS = {
  LSHOULDER : 'left_shoulder',
  RSHOULDER: 'right_shoulder',
  LELBOW: 'left_elbow',
  RELBOW: 'right_elbow', 
  LWRIST: 'left_wrist',
  RWRIST: 'right_wrist', 
  LHIP: 'left_hip',
  RHIP: 'right_hip',
}
