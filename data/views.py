import base64
from datetime import datetime
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
from django.http import HttpResponse as response, JsonResponse
import uuid
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.http import FileResponse
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from django.contrib.auth.decorators import login_required
import base64
import io
import data.const as const
import os

def dashboard(request):
    user = request.user
    involvements = InvolvedIn.objects.filter(user=user)
    sessions = [inv.session for inv in involvements]
    context = {'sessions': sessions}
    return render(request, 'dashboard.html', context)



@csrf_exempt
def user_init(request):
    '''Initialise a new user.'''
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user details from request data
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Generate a unique user id
        uid = str(uuid.uuid4())

        # Create and save new user
        new_user = User(uid, first_name, last_name)
        new_user.save()

        # Return a success response with the new user id
        return JsonResponse({'uid': uid}, status=201)

    # Handle non-POST requests
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def session_init(request):
    '''Initialise session metadata for a newly started session.'''
    data = json.loads(request.body)

    uids = data.get('uids')
    session = data.get('session')

    # First, ensure every user that is involved in this session exists
    users = User.objects.filter(id__in=uids)
    if len(users) != len(uids):
        return response("one or more invalid users provided", status=status.HTTP_401_UNAUTHORIZED)

    # Create and save new session
    new_sid = str(uuid.uuid4())
    new_session = Session(
        new_sid,
        session.get('name'),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        session.get('description')
    )
    new_session.save()

    # Record each user as being involved in this session
    for user in users:
        InvolvedIn(id=str(uuid.uuid4()), user=user, session=new_session).save()

    return response(
        json.dumps({'sid': new_sid, 'debug': len(users)}),
        content_type="application/json",
        status=status.HTTP_200_OK
    )

# Decorator is just to mitigate some cookies problem that was preventing testing
@csrf_exempt
def frames_upload(request):
    '''Receive frame data from the frontend and store this data persistently in the backend.'''
    data = json.loads(request.body)

    uid = data.get('uid')
    sid = data.get('sid')
    clip_num = data.get('clipNum')
    session_finished = data.get('sessionFinished')
    pose_data = data.get('poses')
    image_data = data.get('images')

    user = User.objects.filter(id=uid)
    if not len(user):
        return response("user with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    
    session = Session.objects.filter(id=sid)
    if not len(session):
        return response("session with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        return response("user was not involved in this session", status=status.HTTP_403_FORBIDDEN)
    
    store = DataStore()
    store.set_poses(pose_data)
    store.set_images(image_data)
    store.write_poses_locally(sid, clip_num)
    store.write_images_locally(sid, clip_num)

    # Write to Azure blob only when the session has been completed
    if session_finished:
        store.write_session_to_cloud(sid)

    return response(status=status.HTTP_200_OK)

def visualise_2D_temporary_helper(sid: str, clip_num: str, fps=15):
    '''Convert a directory of images stored on the file system into a video.

    NOTE:   ->  This function will become obselete and should be removed once cloud 
                storage is implemented for clip images (video)'''
    images_path = os.path.join(os.path.dirname(__file__), "tests/sample_poses_and_images", DataStore.get_images_name(sid, clip_num))
    images = sorted(os.listdir(images_path), key=lambda x: int(x[3:len(x)-4]))

    # Get the first image to get dimensions
    image_path = os.path.join(images_path, images[0])
    frame = cv2.imread(image_path)
    height, width, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter("vid.mp4", fourcc, fps, (width, height))

    for image in images:
        image_path = os.path.join(images_path, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()

def visualise_2D(request):
    '''Present a 2D visualisation of pose data overlayed over the video from 
    which this data was extracted.'''
    #data = json.loads(request.body)
    #sid = data.get('sid')
    #clip_num = data.get('clip_num')
    #store = DataStore()
    #store.populate_poses(sid, clip_num)
    #poses = store.get_poses()

    # NOTE
    # skip all error checking: assume user was involved in this session, session exists, etc.
    # use sample pose and image data currently - for testing
    sid = "6d6895ee-6e5b-4097-923c-b98aa7968d0d"
    clip_num = "1"

    with open(os.path.join(os.path.dirname(__file__), "tests/sample_poses_and_images/poses_6d6895ee-6e5b-4097-923c-b98aa7968d0d_1.json")) as f:
        poses = json.load(f)

    visualise_2D_temporary_helper(sid, clip_num)
    cap = cv2.VideoCapture("vid.mp4")

    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return response(status=status.HTTP_404_NOT_FOUND)

    frames = []
    for p in poses:
        ret, frame_image = cap.read()
        if not ret:
            # video has reached the end
            break

        frame_height, frame_width, _ = frame_image.shape

        # Create a copy of the frame for overlaying keypoints
        overlay_image = frame_image.copy()

        # Overlay each keypoint onto the image for this frame
        keypoints = []
        for kp in p.get("keypoints3D"):
            x, y = int(kp['x'] * frame_width + frame_width/2), int(kp['y'] * frame_height + frame_height/2)
            keypoints.append((x, y))
            cv2.circle(overlay_image, (x, y), radius=2, color=(0, 255, 0), thickness=-1)

        # Connect the dots - draw lines between joints to form a human stick-figure shape
        for joint1, joint2 in const.KP_CONNS:
            pt1 = keypoints[joint1]
            pt2 = keypoints[joint2]
            cv2.line(overlay_image, pt1, pt2, (0, 255, 0), 1)

        _, buffer = cv2.imencode('.png', overlay_image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        frames.append(img_base64)

    cv2.destroyAllWindows()
    os.remove("vid.mp4")
    frames = json.dumps(frames)
    return render(request, 'animation.html', {'frames': frames})


# WORK IN PROGRESS 3D VISUALISATION
def visualise_3D(request):
    '''Present an animation of the frame data for a session.'''
    uid = "a4db80a8-bac7-4831-8954-d3e402f469bc"
    sid = "e2b7957a-a1e3-490f-a5a3-b4d00905dd6e"
    clip_num = 2

    user = User.objects.filter(id=uid)
    if not len(user):
        print("user doesn't exist ... this case is not yet handled!")

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        print("user was not involved in this session ... this case is not yet handled!")

    store = DataStore()
    if not store.populate_poses(sid, clip_num):
        print("No session data exists for this session ... this case is not yet handled!")

    session_frames = store.get_poses()

    # create a list of numpy arrays for each keypoint
    frames = []
    for frame_num, session_frame in enumerate(session_frames):
        keypoints3D_arrays = []
        for kp in session_frame.get("keypoints3D"):
            keypoints3D_arrays.append(np.array([kp.get('x', 0), kp.get('y', 0), kp.get('z', 0)]))

        xdata = np.array([kp[0] for kp in keypoints3D_arrays])
        ydata = np.array([kp[1] for kp in keypoints3D_arrays])
        zdata = np.array([kp[2] for kp in keypoints3D_arrays])

        trace = go.Scatter3d(
            x=xdata,
            y=ydata,
            z=zdata,
            mode='markers',
            marker=dict(size=2, color='red')
        )

        lines = [
            go.Scatter3d(
                x=[xdata[joint1], xdata[joint2]],
                y=[ydata[joint1], ydata[joint2]],
                z=[zdata[joint1], zdata[joint2]],
                mode='lines',
                line=dict(width=2, color='blue')
            )
            for joint1, joint2 in const.KP_CONNS
        ]

        frames.append(go.Frame(data=[trace] + lines, name=str(frame_num)))

    layout = go.Layout(
        scene=dict(
            aspectmode="data",
            aspectratio=dict(x=2, y=2, z=1),
            xaxis=dict(range=[-2, 2], visible=False),
            yaxis=dict(range=[-2, 2], visible=False),
            zaxis=dict(range=[-2, 2]),
        ),
        showlegend=False,
        height=800,
        margin=dict(l=0, r=0, b=0, t=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[dict(label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 100, "redraw": True}}])])  # Adjust duration for speed
        ]
    )

    fig = go.Figure(
        data=[trace] + lines,
        layout=layout,
        frames=frames
    )

    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return render(request, 'visualise_coordinates.html', context={'plot_div': plot_div})

#2D VISUALISATION - OLD, NO VIDEO BACKGROUND
# def visualise_coordinates(request):
#     '''Present an animation of the frame data for a session.'''
#     # hardcode session id, user id and clip num for now (should actually be obtained from request)
#     uid = "a4db80a8-bac7-4831-8954-d3e402f469bc"
#     sid = "e2b7957a-a1e3-490f-a5a3-b4d00905dd6e"
#     clip_num = 1

#     # Get the user with this user id
#     user = User.objects.filter(id=uid)
#     if not len(user):
#         # user with this id does not exist ...
#         print("user doesn't exist ... this case is not yet handled!")

#     if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
#         # this session doesn't exist, or it does but this user wasn't part of it
#         print("user was not involved in this session ... this case is not yet handled!")
    
#     store = DataStore()
#     if not store.populate(sid, clip_num):
#         print("No session data exists for this session ... this case is not yet handled!")

#     session_frames = store.get()
#     frames = []

#     for session_frame in session_frames.values():
#         keypoints3D_arrays = []
#         for kp in session_frame:
#             keypoints3D_arrays.append(np.array([kp.get('x', 0), kp.get('y', 0), kp.get('z', 0)]))

#         keypoints2D_arrays = [(int(kp[0] * 100 + 300), int(kp[1] * 100 + 300)) for kp in keypoints3D_arrays]

#         img = np.zeros((600, 600, 3), dtype=np.uint8)

#         for kp in keypoints2D_arrays:
#             cv2.circle(img, kp, 2, (0, 0, 255), -1)

#         for joint1, joint2 in const.KP_CONNS:
#             pt1 = keypoints2D_arrays[joint1]
#             pt2 = keypoints2D_arrays[joint2]
#             cv2.line(img, pt1, pt2, (255, 0, 0), 1)

#         _, buffer = cv2.imencode('.png', img)
#         img_base64 = base64.b64encode(buffer).decode('utf-8')
#         frames.append(img_base64)

#     frames = json.dumps(frames)
#     return render(request, 'animation.html', {'frames': frames})
