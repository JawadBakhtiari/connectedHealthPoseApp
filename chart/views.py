from django.shortcuts import render
from . import Plotter
from . import Visualise
from .Visualise import generate_plot
import matplotlib
matplotlib.use('Agg') 
import os

def input_frame(request):
    return render(request, 'chart/input.html')

def result(request):
    if request.method == 'POST':
        frame = int(request.POST.get('frame'))
        joint = request.POST.get('joint')
        interval = request.POST.get('interval')
        dimension = request.POST.get('dimension')
        return generate_plot(joint, interval, dimension, frame)
