# Imports
import time
from . import Parser
from . import Calculator


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
