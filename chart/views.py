import cv2
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from data.datastore.datastore import DataStore
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

    store = DataStore(sid, clip_num)
    if not store.populate():
        print("Error: data (poses or video or both) not found")
        return render(request, 'result.html', {'frames': None})

    cap = cv2.VideoCapture(store.get_video_path())
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

    poseData = store.get_poses()
    angleData = calculate_angles(joint, dimension, poseData)

    joints = json.dumps(joint)
    dimensions = json.dumps(dimension)
    angles = json.dumps(angleData)
    frames = json.dumps(create_2D_visualisation(poseData, cap))

    return render(request, 'result.html', {'frames': frames, 'angles': angles, 'joint': joints, 'dimension': dimensions}, content_type='text/html')
