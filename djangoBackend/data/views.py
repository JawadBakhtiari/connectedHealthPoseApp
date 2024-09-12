import os
import cv2
import json
import uuid
from datetime import datetime
from rest_framework import status
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse as response, JsonResponse
from .models import User, Session
import data.datastore.sessionmeta as sm
from data.datastore.posestore import PoseStore
from data.datastore.videostore import VideoStore
from data.visualise import create_2D_visualisation 
from django.conf import settings

@csrf_exempt
def user_init(request):
    '''
    Initialise a new user.
    '''
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    uid = str(uuid.uuid4())
    new_user = User(uid, first_name, last_name)
    new_user.save()

    return JsonResponse({'uid': uid}, status=201)


@csrf_exempt
def session_init(request):
    '''
    Initialise session metadata for a newly started session.
    '''
    data = json.loads(request.body)
    # uids = data.get('uids')
    session = data.get('session')

    # NOTE -> skip error checking for now
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

    # NOTE -> skip for now
    # Record each user as being involved in this session
    # for user in users:
    #    InvolvedIn(id=str(uuid.uuid4()), user=user, session=new_session).save()

    return response(
        json.dumps({'sid': new_sid}),
        content_type="application/json",
        status=status.HTTP_200_OK
    )


@csrf_exempt
def poses_upload(request):
    '''
    Receive pose data, process it and store it locally. 
    '''
    data = json.loads(request.body)

    # uid = data.get('uid')
    sid = data.get('sid')
    poses = data.get('poses')

    # NOTE -> skip error checking for now
    # user = User.objects.filter(id=uid)
    # if not len(user):
    #    return response("user with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    # session = Session.objects.filter(id=sid)
    # if not len(session):
    #    return response("session with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    # if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
    #    return response("user was not involved in this session", status=status.HTTP_403_FORBIDDEN)

    clip_num = sm.get_clip_num(sid)
    pose_store = PoseStore(sid, clip_num)
    pose_store.write_locally(json.loads(poses))
    return response(status=status.HTTP_200_OK)


@csrf_exempt
def video_upload(request):
    '''
    Receive video data and store it in cloud storage.

    Currently, receiving video data means the end of a clip, so also:
        - increment clip number for this session
        - write pose data for this clip to cloud storage
    '''
    video = request.FILES['video']
    sid = request.POST.get('sid', '')
    clip_num = sm.get_clip_num(sid)

    video_store = VideoStore(sid, clip_num)
    video_store.write(video)

    pose_store = PoseStore(sid, clip_num)
    pose_store.write_to_cloud()

    sm.increment_clip_num(sid)

    message = f"\nUpload Finished\nsid: {sid}\nclip num: {clip_num}\n"

    print(message)

    # Write message to a file
    log_file_path = os.path.join(settings.BASE_DIR, 'upload_log.txt')
    with open(log_file_path, 'a') as f:
        f.write(message + '\n')

    return response(status=status.HTTP_200_OK)

@csrf_exempt
def show_log(request):
    # Define the path to the log file
    log_file_path = os.path.join(settings.BASE_DIR, 'upload_log.txt')

    # Read the contents of the log file
    try:
        with open(log_file_path, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = "No logs available."

    # Pass the log content to the template
    return render(request, 'show_log.html', {'log_content': log_content})

@csrf_exempt
def visualise_2D(request):
    '''
    Present a 2D visualisation of pose data overlayed over the video from 
    which this data was extracted.
    '''
    # NOTE ->   skip error checking involving users
    #           don't expect user id in request currently
    sid = request.GET.get('sid')
    clip_num = request.GET.get('clipNum')

    pose_store = PoseStore(sid, clip_num)
    video_store = VideoStore(sid, clip_num)
    try:
        poses = pose_store.get()
        cap = cv2.VideoCapture(video_store.get())
    except ValueError as e:
        print(e)
        return render(request, 'visualise2D.html', {'frames': None})

    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return render(request, 'visualise2D.html', {'frames': None})

    frames = json.dumps(create_2D_visualisation(poses, cap))
    return render(request, 'visualise2D.html', {'frames': frames}, content_type='text/html')
