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
from datastore.datastore import Sessionstore
from .models import User, InvolvedIn
import json
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Decorator is just to mitigate some cookies problem that was preventing testing
@csrf_exempt
def frames_upload(request):
    # Testing phase, assume that the session is being written to for the first time (
    # we are not appending frames, just adding whatever frames received to the session
    # file and closing it).

    # Output request to server terminal for testing
    data = json.loads(request.body)
    print(data)

    uid = data.get('uid')       # Should be 1 for testing
    sid = data.get('sid')    # Should be 2 for testing
    
    assert(uid == 1)
    assert(sid == 4)

    session_data = data.get('frames')   # Assuming this is a dictionary of frames, where
                                        # keys are frame number and values are a list of
                                        # 3D coordinates. Could also be a list of frames
                                        # if prefered
    # session_store = Sessionstore()
    # session_store.set(session_data)
    # session_store.write(sid)

    # replaced above with azure storage
    # Create a blob client 
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=connectedhealthunsw;AccountKey=ByogeEDjYWdSoG+kCY1uR+KXHQwullTwi3F6kZ7QSZQoWshzq/wHXkgdBHlwmGYOg3MyI9NKh+iF+AStjaqaYw==;EndpointSuffix=core.windows.net")
    blob_client = blob_service_client.get_blob_client("framedata", f"session{sid}")

    # Upload the session data.
    # if blob under that sessionId exists, append frames
    if blob_client.exists():
        # Download the existing session data 
        downloaded_bytes = blob_client.download_blob().readall()
        existing_data = json.loads(downloaded_bytes)

        # Append the new frame to the existing session data
        existing_data.update(session_data)
        updated_session_data_bytes = json.dumps(existing_data).encode('utf-8')

        # Upload the updated session data (overwrite with updated information)
        blob_client.upload_blob(updated_session_data_bytes, overwrite=True)
    else:
        # If the sessionId does not exist, upload the session data as a new blob
        session_data_bytes = json.dumps(session_data).encode('utf-8')
        blob_client.upload_blob(session_data_bytes)


    return render(request, 'frames_upload.html', {'sid': sid})

def visualise_coordinates(request):
    # Assume that we want session and user both with id 1
    # These would actually be contained within the request
    sid = 4
    uid = 1

    # Get the user with this user id
    user = User.objects.filter(id=uid)
    if not len(user):
        # user with this id does not exist ...
        pass

    if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
        # this session doesn't exist, or it does but this user wasn't part of it
        pass

    
    # session_store = Sessionstore()
    # if not session_store.populate(sid):
    #     # session file could not be located, ignore this case currently.
    #     # above check should prevent this ever being true
    #     pass

    # session_frames = session_store.get()

    # replaced above with getting data from azure
    # Create a blob client using the local file name as the name for the blob
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=connectedhealthunsw;AccountKey=ByogeEDjYWdSoG+kCY1uR+KXHQwullTwi3F6kZ7QSZQoWshzq/wHXkgdBHlwmGYOg3MyI9NKh+iF+AStjaqaYw==;EndpointSuffix=core.windows.net")
    blob_client = blob_service_client.get_blob_client("framedata", f"session{sid}")

    # Download the blob from that session as a string as convert to json
    session_data_string = blob_client.download_blob().content_as_text()
    session_frames = json.loads(session_data_string)


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