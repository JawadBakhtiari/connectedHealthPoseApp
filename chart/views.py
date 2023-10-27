import cv2
import json
import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .Visualise import generate_plot
from data.datastore.datastore import DataStore
from data.visualise import create_2D_visualisation
from chart.Visualise import generate_plot_for_all_frames

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
    if sid == None or clip_num == None:  
        sid = "ccbe340e-f1db-4037-8f91-257bcac2c2f9"
        clip_num = "1"

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

    frames = json.dumps(create_2D_visualisation(store.get_poses(), cap))
    charts = json.dumps(generate_plot_for_all_frames(joint, dimension, store.get_poses()))
    return render(request, 'result.html', {'frames': frames, 'charts': charts}, content_type='text/html')