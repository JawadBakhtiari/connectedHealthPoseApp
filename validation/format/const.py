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

LSHOULDER = 'Skeleton 001:LSHO'
RSHOULDER = 'Skeleton 001:RSHO'
LELBOW = 'Skeleton 001:LELB'
RELBOW = 'Skeleton 001:RELB'
LWRIST = 'Skeleton 001:LWRA'
RWRIST = 'Skeleton 001:RWRA'
LHIP = 'Skeleton 001:LPSI'
RHIP = 'Skeleton 001:RPSI'
LKNEE = 'Skeleton 001:LKNE'
RKNEE = 'Skeleton 001:RKNE'
LANKLE = 'Skeleton 001:LANK'
RANKLE = 'Skeleton 001:RANK'

LAB_KEYPOINTS = [
  LSHOULDER,
  RSHOULDER,
  LELBOW,
  RELBOW,
  LWRIST,
  RWRIST,
  LHIP,
  RHIP,
  LKNEE,
  RKNEE,
  LANKLE,
  RANKLE,
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
  LKNEE: 'left_knee',
  RKNEE: 'right_knee',
  LANKLE: 'left_ankle',
  RANKLE: 'right_ankle',
}

