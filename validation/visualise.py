#!/usr/bin/env python3

'''Helper script to visualise a set of poses over a video capture'''

import cv2
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

with open('example_data/random/poses1.json') as f:
  POSES = json.load(f)

VIDEO_PATH = 'example_data/random/vid1.MOV'

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames

def create_animation(frames, keypoint_data):
    fig, ax = plt.subplots(figsize=(10, 6))

    def animate(i):
        ax.clear()
        ax.imshow(frames[i])

        # Plot keypoints
        for keypoint in keypoint_data[i]:
            x, y = keypoint['x'], keypoint['y']
            ax.plot(x, y, 'ro', markersize=5)
            ax.text(x, y, keypoint['name'], fontsize=8, color='white', backgroundcolor='black')

        ax.set_title(f'Frame {i}')
        ax.axis('off')

    anim = animation.FuncAnimation(fig, animate, frames=len(frames), interval=33, blit=False)
    return anim

frames = read_video(VIDEO_PATH)
anim = create_animation(frames, POSES)
anim.save('animation.mp4', writer='ffmpeg', fps=30)
plt.close()

