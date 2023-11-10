# Imports
import time
from . import Parser
from . import Calculator
from . import Plotter
import concurrent.futures


# Calculate angles
def calculate_angles(joint, dimension, poseData):
    numFrames = len(poseData)

    # Parse pose data
    parser = Parser.Parser(joint, poseData)
    leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints = parser.parse()

    # Calculate angles
    calculator = Calculator.Calculator(numFrames, leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints)
    leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d = calculator.Calculate()

    return [leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d]


# Generate all plots to keep in memory
def generate_plot_for_all_frames(joint, dimension, numFrames, angleData):
    # List of frames
    all_frames = [None] * numFrames

    # Start timer
    print(f'Generating {numFrames} plots')
    startTime = time.time()

    # Use a ProcessPoolExecutor to generate plots in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Map over the frames to maintain order, the executor will handle the task distribution
        results = executor.map(generate_plot, [joint]*numFrames, [dimension]*numFrames, [numFrames]*numFrames, range(numFrames), [angleData]*numFrames)
        
        # Sort generated plots
        for i, generated_frame in enumerate(results):
            all_frames[i] = generated_frame
            if i % 5 == 0:
                print(f'Generated plot number {i}')

    # Print statistics
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
