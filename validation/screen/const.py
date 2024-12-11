'''
Constants for interacting with user through data processing and
validation scripts.
'''

from exercises.bent_over_rows import BentOverRows
from exercises.bicep_curls import BicepCurls
from exercises.dartboard import Dartboard
from exercises.shoulder_taps import ShoulderTaps
from exercises.side_bend import SideBend
from exercises.spin import Spin
from exercises.tandem_stand import TandemStand
from exercises.tandem_walk import TandemWalk
from exercises.timed_up_and_go import TimedUpAndGo
from exercises.walk import Walk


EXERCISES_TO_CLASSES = {
    'bent over rows': (BentOverRows, 12),
    'bicep curls': (BicepCurls, 12),
    'dartboard': (Dartboard, 1),
    'shoulder taps': (ShoulderTaps, 12),
    'side bend': (SideBend, 12),
    'spin': (Spin, 2),
    'tandem stand': (TandemStand, None),
    'tandem walk': (TandemWalk, 1600),
    'timed up and go': (TimedUpAndGo, 1600),
    'walk': (Walk, 1000),
}

EXERCISES = [
    'bent over rows',
    'bicep curls',
    'dartboard',
    'shoulder taps',
    'side bend',
    'sit to stand',
    'spin',
    'tandem stand',
    'tandem walk',
    'timed up and go',
    'walk',
    'all'
]

CONFIRMATION = ['continue', 'back']
EXERCISE_HEADER = 'select an exercise (or all)'

