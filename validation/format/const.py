'''Constants used for formatting lab data.'''

LAB_START_TIME_FORMAT = "%Y-%m-%d %I.%M.%S.%f %p"
LAB_START_TIME_INDEX = 11

SYNC_MARKER_NAME = r'Sync 001:Marker.*[.][345]\b'

X_SUFFIX = '.3'
Y_SUFFIX = '.4'
Z_SUFFIX = '.5'

LSHOULDER = 'Skeleton:LSHO'
RSHOULDER = 'Skeleton:RSHO'
LELBOW = 'Skeleton:LELB'
RELBOW = 'Skeleton:RELB'
LWRIST = 'Skeleton:LWRA'
RWRIST = 'Skeleton:RWRA'
LHIP = 'Skeleton:LPSI'
RHIP = 'Skeleton:RPSI'
LKNEE = 'Skeleton:LKNE'
RKNEE = 'Skeleton:RKNE'
LANKLE = 'Skeleton:LANK'
RANKLE = 'Skeleton:RANK'

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

