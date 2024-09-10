#!/usr/bin/env python3

'''A script for playing around with different ideas'''

from format.labdataformatter import LabDataFormatter

ldf = LabDataFormatter('~/uni/teleRehab/validation/be_pose_estimation/data/videos/stsstruggle.csv')
print(ldf.get_exercise_start_end())

