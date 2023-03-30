import math
import os
import random
from datetime import datetime, timezone
import django
from django.conf import settings
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HumanPose3D.settings')
django.setup()

from data.models import User, Session, InvolvedInSession, Frame, Coordinate


def add_dummy_data():
   # create a session and users involved
    session = Session(date=timezone.now())
    session.save()
    user1 = User(first_name='John', last_name='Doe')
    user1.save()
    user2 = User(first_name='Jane', last_name='Doe')
    user2.save()
    involved_in_session1 = InvolvedInSession(user=user1, session=session)
    involved_in_session1.save()
    involved_in_session2 = InvolvedInSession(user=user2, session=session)
    involved_in_session2.save()

    # create a frame for the pose
    frame = Frame(name='Human Pose', description='Sample pose for testing', session=session)
    frame.save()

    # create coordinates for the pose
    coords = [
        {'x': 0.1, 'y': 0.2, 'z': 0.3},
        {'x': 0.2, 'y': 0.3, 'z': 0.4},
        {'x': 0.3, 'y': 0.4, 'z': 0.5},
        {'x': 0.4, 'y': 0.5, 'z': 0.6},
        {'x': 0.5, 'y': 0.6, 'z': 0.7},
        {'x': 0.6, 'y': 0.7, 'z': 0.8},
        {'x': 0.7, 'y': 0.8, 'z': 0.9},
        {'x': 0.8, 'y': 0.9, 'z': 1.0},
    ]

    for coord in coords:
        coordinate = Coordinate(x=coord['x'], y=coord['y'], z=coord['z'], frame=frame)
        coordinate.save()

if __name__ == '__main__':
    add_dummy_data()
