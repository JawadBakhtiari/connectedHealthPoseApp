import os
from django.shortcuts import render
import numpy as np
import plotly.graph_objs as go
import plotly.offline as opy
import plotly.graph_objs as go
from django.shortcuts import render
import plotly.graph_objs as go
import numpy as np
import tensorflow as tf
from datastore.datastore import data_store


def visualise_coordinates(request):
    eg_user_id = "1"
    eg_session_id = "1"
    eg_frame_id = "1"

    data = data_store.get()
    eg_keypoints3D = data.get(eg_user_id) \
                        .get("sessions") \
                        .get(eg_session_id) \
                        .get("frames") \
                        .get(eg_frame_id) \

    # create a list of numpy arrays for each keypoint
    keypoints3D_arrays = []
    for kp in eg_keypoints3D:
        keypoints3D_arrays.append(np.array([kp['x'], kp['y'], kp['z']]))

    # extract x, y, and z coordinates from keypoints3D_arrays
    xdata = np.array([kp[0] for kp in keypoints3D_arrays])
    ydata = np.array([kp[1] for kp in keypoints3D_arrays])
    zdata = np.array([kp[2] for kp in keypoints3D_arrays])

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
        for joint1, joint2 in connections
    ]

    layout = go.Layout(
        scene=dict(
            aspectmode="data",
            aspectratio=dict(x=2, y=2, z=1),
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[-2, 2]),
            zaxis=dict(range=[-2, 2])
        ),
        showlegend=False,

        height=800,
        margin=dict(l=0, r=0, b=0, t=0)
    )

    fig = go.Figure(data=[trace] + lines, layout=layout)
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return render(request, 'visualise_coordinates.html', context={'plot_div': plot_div})



 