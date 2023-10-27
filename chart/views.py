from django.shortcuts import render
from .Visualise import generate_plot
import matplotlib
matplotlib.use('Agg') 
from django.views.decorators.csrf import csrf_exempt

import cv2
import json
from data.datastore.datastore import DataStore
from data.visualise import create_2D_visualisation

def input_frame(request):
    return render(request, 'chart/input.html')

# def result(request):
#     if request.method == 'POST':
#         frame = int(request.POST.get('frame'))
#         joint = request.POST.get('joint')
#         dimension = request.POST.get('dimension')
#         return generate_plot(joint, dimension, frame)
    
@csrf_exempt
def result(request):
    '''Present a 2D visualisation of pose data overlayed over the video with the joint angle graph'''

    # Use sample data on empty request
    sid = "ccbe340e-f1db-4037-8f91-257bcac2c2f9"
    clip_num = "1"

    if request.method == 'POST':
        sid = request.GET.get('sid')
        clip_num = request.GET.get('clipNum')
        joint = request.POST.get('joint')
        dimension = request.POST.get('dimension')

    store = DataStore(sid, clip_num)
    if not store.populate():
        print("Error: data (poses or video or both) not found")
        return render(request, 'visualise2D.html', {'frames': None})

    cap = cv2.VideoCapture(store.get_video_path())
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return render(request, 'visualise2D.html', {'frames': None})

    frames = json.dumps(create_2D_visualisation(store.get_poses(), cap))
    return render(request, 'result.html', {'frames': frames, 'charts': charts}, content_type='text/html')