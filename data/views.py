import cv2
import json
import uuid
import matplotlib
import data.datastore.sessionmeta as sm
from datetime import datetime
from rest_framework import status
from django.shortcuts import render
from data.datastore.datastore import DataStore
from data.datastore.posestore import PoseStore
from .models import User, InvolvedIn, Session
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse as response, JsonResponse
from data.visualise import create_2D_visualisation, create_3D_visualisation

matplotlib.use('Agg')


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

    # uids = data.get('uids')
    session = data.get('session')

    # NOTE -> skip error checking for demo
    # First, ensure every user that is involved in this session exists
    # users = User.objects.filter(id__in=uids)
    # if len(users) != len(uids):
    #    return response("one or more invalid users provided", status=status.HTTP_401_UNAUTHORIZED)

    # Create and save new session
    new_sid = str(uuid.uuid4())
    new_session = Session(
        new_sid,
        session.get('name'),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        session.get('description')
    )
    new_session.save()

    # NOTE -> skip for demo
    # Record each user as being involved in this session
    # for user in users:
    #    InvolvedIn(id=str(uuid.uuid4()), user=user, session=new_session).save()

    return response(
        json.dumps({'sid': new_sid}),
        content_type="application/json",
        status=status.HTTP_200_OK
    )

# Decorator is just to mitigate some cookies problem that was preventing testing


@csrf_exempt
def frames_upload(request):
    '''Receive frame data from the frontend and store this data persistently in the backend.'''
    data = json.loads(request.body)

    # uid = data.get('uid')
    sid = data.get('sid')
    clipFinished = data.get('clipFinished')
    poses = data.get('poses')
    images = data.get('tensorAsArray')

    # NOTE -> skip error checking for demonstration
    # user = User.objects.filter(id=uid)
    # if not len(user):
    #    return response("user with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    # session = Session.objects.filter(id=sid)
    # if not len(session):
    #    return response("session with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    # if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
    #    return response("user was not involved in this session", status=status.HTTP_403_FORBIDDEN)

    clip_num = sm.get_clip_num(sid)
    store = DataStore(sid, clip_num)
    store.set(poses, images)
    store.write_locally()

    if clipFinished:
        store.write_to_cloud()
        sm.increment_clip_num(sid)

    return response(status=status.HTTP_200_OK)


@csrf_exempt
def visualise_2D(request):
    '''Present a 2D visualisation of pose data overlayed over the video from 
    which this data was extracted.'''
    # NOTE ->   skip error checking involving users
    #           don't expect user id in request currently

    # use sample data if request is empty (happens when page is first loaded by url)
    sid = "215eaafc-41ba-40a2-9a8a-57b73e61b2c0"
    clip_num = "2"
    if request.GET:
        # if request non-empty, use this data
        sid = request.GET.get('sid')
        clip_num = request.GET.get('clipNum')

    store = DataStore(sid, clip_num)
    if not store.populate():
        print("Error: data (poses or video or both) not found")
        return render(request, 'visualise2D.html', {'frames': None})

    cap = cv2.VideoCapture(store.get_video_path())
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return render(request, 'visualise2D.html', {'frames': None})

    frames = json.dumps(create_2D_visualisation(store.get_poses(), cap))
    return render(request, 'visualise2D.html', {'frames': frames}, content_type='text/html')


@csrf_exempt
def visualise_3D(request):
    '''Present a 3D visualisation of pose data.'''
    sid = "215eaafc-41ba-40a2-9a8a-57b73e61b2c0"
    clip_num = "2"
    if request.GET:
        # if request non-empty, use this data
        sid = request.GET.get('sid')
        clip_num = request.GET.get('clipNum')

    pose_store = PoseStore(sid, clip_num)
    if not pose_store.populate():
        print("Error: Pose data not found in Azure Blob Storage.")
        return render(request, '3D_visualise2D.html', {'image': None})

    frames = json.dumps(create_3D_visualisation(pose_store.get()))
    return render(request, '3D_visualise2D.html', {'frames': frames})
