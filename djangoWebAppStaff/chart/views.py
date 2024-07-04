import cv2
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from data.datastore.posestore import PoseStore
from data.datastore.videostore import VideoStore
from data.visualise import create_2D_visualisation
from chart.Visualise import calculate_angles

def input_frame(request):
    return render(request, 'chart/input.html')

@csrf_exempt
def result(request):
    '''Present a 2D visualisation of pose data overlayed over the video with the joint angle graph'''

    if request.method == 'POST':
        sid = request.POST.get('sid')
        clip_num = request.POST.get('clipNum')
        joint = request.POST.get('joint')
        dimension = request.POST.get('dimension')

    # Use sample data on empty request
    if sid == None or clip_num == None or len(sid) == 0 or len(clip_num) == 0:
        sid = "ccbe340e-f1db-4037-8f91-257bcac2c2f9"
        clip_num = "1"

    if joint == None or dimension == None or len(joint) == 0 or len(dimension) == 0:
        joint = 'shoulder'
        dimension = '2d'

    pose_store = PoseStore(sid, clip_num)
    video_store = VideoStore(sid, clip_num)
    try:
        poses = pose_store.get()
        cap = cv2.VideoCapture(video_store.get())
    except ValueError as e:
        print(e)
        return render(request, 'result.html', {'frames': None})

    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return render(request, 'result.html', {'frames': None})

    if joint.lower() not in ['elbow', 'shoulder', 'hip', 'knee']:
        print("Error: invalid joint.")
        return render(request, 'result.html', {'frames': None})
    
    if dimension.lower() not in ['2d', '3d']:
        print("Error: invalid dimension.")
        return render(request, 'result.html', {'frames': None})

    # Format parameters
    joint = joint.lower().capitalize()
    dimension = dimension.lower()
    angleData = calculate_angles(joint, dimension, poses)

    joints = json.dumps(joint)
    dimensions = json.dumps(dimension)
    angles = json.dumps(angleData)
    frames = json.dumps(create_2D_visualisation(poses, cap))

    return render(request, 'result.html', {'frames': frames, 'angles': angles, 'joint': joints, 'dimension': dimensions}, content_type='text/html')
