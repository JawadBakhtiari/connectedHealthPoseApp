import base64
import cv2
from django.shortcuts import render
import numpy as np
import plotly.graph_objs as go
import plotly.offline as opy
import plotly.graph_objs as go
from django.shortcuts import render
import plotly.graph_objs as go
import numpy as np
from datastore.datastore import Sessionstore
from .models import User, InvolvedIn
import json
from django.views.decorators.csrf import csrf_exempt



# Decorator is just to mitigate some cookies problem that was preventing testing
@csrf_exempt
def frames_upload(request):
    '''Receive frame data from the frontend and store this data persistently in the backend.'''

    # Output request to server terminal for testing
    data = json.loads(request.body)

    uid = data.get('uid')
    sid = data.get('sid')
    clipNum = data.get('clipNum')  # Get clip number from request
    sessionFinished = data.get('sessionFinished')  # Get sessionFinished flag from request
    session_data = data.get('frames')

    # Get the user with this user id
    user = User.objects.filter(id=uid)
    if not len(user):
        # user with this id does not exist ...
        print("user doesn't exist ... this case is not yet handled!")

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        # this session doesn't exist, or it does but this user wasn't part of it
        print("user was not involved in this session ... this case is not yet handled!")

    # Don't create a new Sessionstore object, instead use the global one
    session_store = Sessionstore()

    # Buffer frames locally
    #session_store.buffer_frames(sid, clipNum, session_data)

    session_store.set(session_data)
    session_store.write_local(sid, clipNum)

    # session_store.print_buffer()
    # Write to Azure blob only when the session has been completed
    if sessionFinished:
        session_store.write(sid, sessionFinished)

    return render(request, 'frames_upload.html', {'sid': sid})

def visualise_coordinates(request):
    '''Present an animation of the frame data for a session.'''
    # Assume that we want session and user both with id 1
    # These would actually be contained within the request
    sid = "10_1"
    uid = 1

    # Get the user with this user id
    user = User.objects.filter(id=uid)
    if not len(user):
        # user with this id does not exist ...
        print("user doesn't exist ... this case is not yet handled!")

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        # this session doesn't exist, or it does but this user wasn't part of it
        print("user was not involved in this session ... this case is not yet handled!")

    
    session_store = Sessionstore()
    if not session_store.populate(sid):
        print("No session data exists for this session ... this case is not yet handled!")

    session_frames = session_store.get()
    frames = []

    for session_frame in session_frames.values():
        keypoints3D_arrays = []
        for kp in session_frame:
            keypoints3D_arrays.append(np.array([kp.get('x', 0), kp.get('y', 0), kp.get('z', 0)]))

        keypoints2D_arrays = [(int(kp[0] * 100 + 300), int(kp[1] * 100 + 300)) for kp in keypoints3D_arrays]

        img = np.zeros((600, 600, 3), dtype=np.uint8)

        for kp in keypoints2D_arrays:
            cv2.circle(img, kp, 2, (0, 0, 255), -1)

        # define connections based on BlazePose Keypoints: Used in MediaPipe BlazePose
        connections = [
            (0, 4),
            (0, 1),
            (4, 5),
            (5, 6),
            (6, 8),
            (1, 2),
            (2, 3),
            (3, 7),
            (10, 9),
            (12, 11),
            (12, 14),
            (14, 16),
            (16, 22),
            (16, 20),
            (16, 18),
            (18, 20),
            (11, 13),
            (13, 15),
            (15, 21),
            (15, 19),
            (15, 17),
            (17, 19),
            (12, 24),
            (11, 23),
            (24, 23),
            (24, 26),
            (23, 25),
            (26, 28),
            (25, 27),
            (28, 32),
            (28, 30),
            (30, 32),
            (27, 29),
            (27, 31),
            (29, 31)
        ]

        for joint1, joint2 in connections:
            pt1 = keypoints2D_arrays[joint1]
            pt2 = keypoints2D_arrays[joint2]
            cv2.line(img, pt1, pt2, (255, 0, 0), 1)

        _, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        frames.append(img_base64)

    frames = json.dumps(frames)
    return render(request, 'animation.html', {'frames': frames})