# Imports
import time
from . import Parser
from . import Calculator
from . import Plotter


# Calculate angles
def calculate_angles(joint, dimension, poseData):
    numFrames = len(poseData)
    joint = joint.lower().capitalize()
    dimension = dimension.lower()

    # Parse pose data
    parser = Parser.Parser(joint, poseData)
    leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints = parser.parse()

    # Calculate angles
    calculator = Calculator.Calculator(numFrames, leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints)
    leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d = calculator.Calculate()

    return [leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d]


# Generate all plots to keep in memory
def generate_plot_for_all_frames(joint, dimension, numFrames, angleData):
    all_frames = []

    # Generate plots
    print(f'Generating {numFrames} plots')
    startTime = time.time()

    # for frame in range(0, numFrames):
    for frame in range(0, 1):
        generated_frame = generate_plot(joint, dimension, numFrames, frame, angleData)
        all_frames.append(generated_frame)
        if frame % 5 == 0:
            print(f'Generated plot number {frame}')

    timeTaken = round(time.time() - startTime, 2)
    print("Time elapsed: " + str(timeTaken) + " seconds")

    return all_frames


# Generate a single plot
def generate_plot(joint, dimension, numFrames, frame, angleData):
    if dimension == '2d':
        data = Plotter.plot2d(numFrames, frame, joint, angleData[0], angleData[1], angleData[2], angleData[3], angleData[4], angleData[5])
    else:
        data = Plotter.plot3d(numFrames, frame, joint, angleData[6], angleData[7])
    
    return data
