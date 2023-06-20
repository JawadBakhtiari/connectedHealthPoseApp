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
from datastore.datastore import DataStore
from .models import User, InvolvedIn, Session
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.http import HttpResponse as response

# Decorator is just to mitigate some cookies problem that was preventing testing
@csrf_exempt
def frames_upload(request):
    '''Receive frame data from the frontend and store this data persistently in the backend.'''
    data = json.loads(request.body)

    uid = data.get('uid')
    sid = data.get('sid')
    clip_num = data.get('clipNum')  # Get clip number from request
    session_finished = data.get('sessionFinished')  # Get session_finished flag from request
    clip_data = data.get('frames')

    user = User.objects.filter(id=uid)
    if not len(user):
        return response("user with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    
    session = Session.objects.filter(id=sid)
    if not len(session):
        return response("session with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        return response("user was not involved in this session", status=status.HTTP_403_FORBIDDEN)

    store = DataStore()
    store.set(clip_data)
    store.write_clip_locally(sid, clip_num)

    # Write to Azure blob only when the session has been completed
    if session_finished:
        store.write_session_to_cloud(sid)

    return render(request, 'frames_upload.html', {'sid': sid}, status=status.HTTP_200_OK)

def visualise_coordinates(request):
    '''Present an animation of the frame data for a session.'''
    # hardcode session id, user id and clip num for now (should actually be obtained from request)
    uid = 1
    sid = 10
    clip_num = 1

    # Get the user with this user id
    user = User.objects.filter(id=uid)
    if not len(user):
        # user with this id does not exist ...
        print("user doesn't exist ... this case is not yet handled!")

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        # this session doesn't exist, or it does but this user wasn't part of it
        print("user was not involved in this session ... this case is not yet handled!")
    
    store = DataStore()
    if not store.populate(sid, clip_num):
        print("No session data exists for this session ... this case is not yet handled!")

    session_frames = store.get()
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