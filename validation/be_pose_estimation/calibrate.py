#!/usr/bin/env python3

'''
    Use cv2 library and chessboard images to calculate camera matrix and distortion coefficients
    required to undistort images taken by the camera. Save these to values to a file for access later.
'''

import numpy as np
import cv2
import glob

CORNER_ROWS = 7
CORNER_COLS = 5
IMAGES_PATH = 'data/calibration_images/20240904/side_cam/'
IMAGES = IMAGES_PATH + '*.jpg'
TEST_IMAGE_NAME = 'img1.jpg'
IMAGE_DISPLAY_TIME = 5000
OUT_FILE_PATH = 'data/camera_parameters/20240904/side_cam.npz'

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((CORNER_COLS*CORNER_ROWS,3), np.float32)
objp[:,:2] = np.mgrid[0:CORNER_ROWS,0:CORNER_COLS].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob(IMAGES)
for img in images:
    print(f'processing {img}')
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (CORNER_ROWS, CORNER_COLS), None)
    if ret == True:
        # If found, add object points, image points (after refining them)
        print('found chessboard')
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

cv2.destroyAllWindows()

ret, mtx, dst, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
test_img = cv2.imread(IMAGES_PATH + TEST_IMAGE_NAME)
h, w = test_img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dst, (w,h), 1, (w,h))
undst = cv2.undistort(test_img, mtx, dst, None, newcameramtx)

# Save camera parameters
np.savez_compressed(OUT_FILE_PATH, mtx=mtx, dst=dst)

# Output an example image distorted and undistorted (and save these images)
cv2.namedWindow('distorted', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('distorted', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('distorted', test_img)
cv2.waitKey(IMAGE_DISPLAY_TIME)
cv2.destroyAllWindows()
cv2.namedWindow('undistorted', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('undistorted', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('undistorted', undst)
cv2.waitKey(IMAGE_DISPLAY_TIME)
cv2.destroyAllWindows()

