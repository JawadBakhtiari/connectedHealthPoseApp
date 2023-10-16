"""
Application
Filename: application.py

Author: Jacqueline, Ahmad
Created: 11/03/2023

Description: Contains the server information for
the API routes and swagger API methods
"""

import signal
import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
import io, base64
from PIL import Image
import numpy as np


def quit_gracefully(*args):
    sys.exit()


def default_handler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


application = Flask(__name__, static_folder="static", static_url_path='')

CORS(application)

application.config['TRAP_HTTP_EXCEPTIONS'] = True
application.register_error_handler(Exception, default_handler)


# # API Routes

@application.route('/')
def serve():
    return send_from_directory(application.static_folder, 'index.html')


def generate_tensor(tensorAsArray, poses):
    # for i in range(len(tensorAsArray)):
    #     img = Image.open(io.BytesIO(base64.decodebytes(bytes(tensorAsArray[i], "utf-8"))))
    #     img.save('my-image.jpeg')
        # img.show()

    # # Display JPG image
    # img = Image.open(io.BytesIO(base64.decodebytes(bytes(tensorAsArray[0], "utf-8"))))
    # img.save('my-image.jpeg')
    # # img.show()

    # # Display RGB image
    # data = np.array(tensorAsArray[0], dtype=np.uint8)
    # img = Image.fromarray(data, 'RGB')
    # # img.show()
    # img.save('my-image.jpeg')

    print(len(tensorAsArray))
    print(len(poses))

    # # Save keypoints
    # file = open("poses.txt","a") 
    # file.write(str(poses))
    # file.write("\n")

    # # Save base64 jpeg encoded image
    # file2 = open("imageData.txt","a") 
    # file2.write(str(tensorAsArray))
    # file2.write("\n")

    # file.close()

    return "T"


@application.route("/send/get_tensor", methods=['POST'])
def handle_get_tensor():
    request_data = request.get_json()
    tensorAsArray = request_data['tensorAsArray']
    poses = request_data['poses']

    return generate_tensor(tensorAsArray, poses)


# To run the API server
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)
    application.run(port=9090, host='0.0.0.0')
