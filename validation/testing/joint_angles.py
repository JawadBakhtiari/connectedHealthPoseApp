#!/usr/bin/env python3

'''Play around with using opensim to calculate joint angles from optitrack data'''

import opensim as osim

model = osim.Model('data/Gait2392_Simbody/gait2392_simbody.osim')
model.initSystem()

# configure the inverse kinematics tool (for calculating joint angles)
itk = osim.InverseKinematicsTool()
itk.setModel(model)
itk.setMarkerDataFileName('data/sample_lab_data.trc')
itk.setStartTime(1)
itk.setEndTime(3)
itk.setOutputMotionFileName('data/joint_angles_out.mot')
itk.run()

# Load the output motion file
motion = osim.Storage('data/joint_angles_out.mot')
print(motion)

