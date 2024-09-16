#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import json

with open('example_data/random/poses1.json') as f:
  POSES = json.load(f)

for pose in POSES:
    keypoints = [(kp['x'], kp['y']) for kp in pose['keypoints']]
    keypoints = np.array(keypoints)
    plt.scatter(keypoints[:, 0], keypoints[:, 1])
    plt.gca().invert_yaxis()
    plt.show()

