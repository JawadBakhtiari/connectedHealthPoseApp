# Imports
from . import Parser
from . import Calculator
from . import Plotter

import time


# Generate all plots to keep in memory
def generate_plot_for_all_frames(joint, dimension, poseData):
    all_frames = []
    numFrames = len(poseData)
    joint = joint.lower().capitalize()
    dimension = dimension.lower()

    # Parse pose data
    parser = Parser.Parser(joint, poseData)
    leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints = parser.parse()

    # Calculate angles
    calculator = Calculator.Calculator(numFrames, leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints)
    leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d = calculator.Calculate()

    # Generate plots
    print(f'Generating {numFrames} plots')
    startTime = time.time()

    # for frame in range(0, len(poseData)):
    for frame in range(0, 1):
        generated_frame = generate_plot(joint, dimension, numFrames, frame, leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d)
        all_frames.append(generated_frame)

    timeTaken = round(time.time() - startTime, 2)
    print("Time elapsed: " + str(timeTaken) + " seconds")

    return all_frames


# Generate a single plot
def generate_plot(joint, dimension, numFrames, frame, leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d):
    if dimension == '2d':
        data = Plotter.plot2d(numFrames, frame, joint, leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw)
    else:
        data = Plotter.plot3d(numFrames, frame, joint, left3d, right3d)
    
    return data