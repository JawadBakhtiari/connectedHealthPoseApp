# Imports
import math
import numpy as np


# Calculator class
class Calculator:
    # Instantiate class
    def __init__(self, numFrames, leftUpperPoints, leftMiddlePoints, leftLowerPoints, rightUpperPoints, rightMiddlePoints, rightLowerPoints) -> None:
        # Instance variables for numFrames and points
        self.numFrames = numFrames
        self.leftUpperPoints = leftUpperPoints
        self.leftMiddlePoints = leftMiddlePoints
        self.leftLowerPoints = leftLowerPoints
        self.rightUpperPoints = rightUpperPoints
        self.rightMiddlePoints = rightMiddlePoints
        self.rightLowerPoints = rightLowerPoints


    # Find the magnitude of a vector
    def calculateMagnitude(self, vector):
        return math.sqrt(sum(pow(element, 2) for element in vector))


    # Calcaulte the angle between two vectors
    def calculateAngle(self, lowerVector, upperVector):
        dotProduct = np.dot(lowerVector, upperVector)
        magnitudes = self.calculateMagnitude(lowerVector) * self.calculateMagnitude(upperVector)

        return 180 - np.rad2deg(np.arccos(dotProduct / magnitudes))


    # Calculate angles
    def Calculate(self):
        # Angles of joints
        leftJointRoll = []
        leftJointPitch = []
        leftJointYaw = []
        rightJointRoll = []
        rightJointPitch = []
        rightJointYaw = []
        left3d = []
        right3d = []

        for p in range(self.numFrames):
            # Calculate roll, pitch and yaw for left and right joints using the upper vector as a directional reference
            # Forumla = create two vectors then use the dot product and arccos to find the angle between them
            lup = self.leftUpperPoints[p]
            lmp = self.leftMiddlePoints[p]
            llp = self.leftLowerPoints[p]
            rup = self.rightUpperPoints[p]
            rmp = self.rightMiddlePoints[p]
            rlp = self.rightLowerPoints[p]

            # Roll: From a reference vector (vectorUpperMiddle), we need the x and y coordinates to calculate roll
            # Note: the magnitude of the vectors must be from Upper to Middle and from Middle to Lower, convert results from radians to degrees
            # vectorUpperMiddle = (middle[x] - upper[x], middle[y] - upper[y])
            # vectorMiddleLower = (lower[x] - middle[x], lower[y] - middle[y])
            vectorUpperMiddle = [lmp['x'] - lup['x'], lmp['y'] - lup['y']]
            vectorMiddleLower = [llp['x'] - lmp['x'], llp['y'] - lmp['y']]
            angleMiddleRoll = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            leftJointRoll.append(angleMiddleRoll)

            vectorUpperMiddle = [rup['x'] - rmp['x'], rup['y'] - rmp['y']]
            vectorMiddleLower = [rlp['x'] - rmp['x'], rlp['y'] - rmp['y']]
            angleMiddleRoll = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            rightJointRoll.append(angleMiddleRoll)

            # Pitch: From a reference vector (vectorUpperMiddle), we need the y and z coordinates to calculate pitch
            # Note: the magnitude of the vectors must be from Upper to Middle and from Middle to Lower, convert results from radians to degrees
            # vectorUpperMiddle = (middle[z] - upper[z], middle[y] - upper[y])
            # vectorMiddleLower = (lower[z] - middle[z], lower[y] - middle[y])
            vectorUpperMiddle = [lmp['z'] - lup['z'], lmp['y'] - lup['y']]
            vectorMiddleLower = [llp['z'] - lmp['z'], llp['y'] - lmp['y']]
            angleMiddlePitch = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            leftJointPitch.append(angleMiddlePitch)

            vectorUpperMiddle = [rmp['z'] - rup['z'], rmp['y'] - rup['y']]
            vectorMiddleLower = [rlp['z'] - rmp['z'], rlp['y'] - rmp['y']]
            angleMiddlePitch = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            rightJointPitch.append(angleMiddlePitch)

            # Yaw: From a reference vector (vectorUpperMiddle), we need the x and z coordinates to calculate yaw
            # Note: the magnitude of the vectors must be from Upper to Middle and from Middle to Lower, convert results from radians to degrees
            # vectorUpperMiddle = (middle[x] - upper[x], middle[z] - upper[z])
            # vectorMiddleLower = (lower[x] - middle[x], lower[z] - middle[z])
            vectorUpperMiddle = [lmp['x'] - lup['x'], lmp['z'] - lup['z']]
            vectorMiddleLower = [llp['x'] - lmp['x'], llp['z'] - lmp['z']]
            angleMiddleYaw = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            leftJointYaw.append(angleMiddleYaw)

            vectorUpperMiddle = [rmp['x'] - rup['x'], rmp['z'] - rup['z']]
            vectorMiddleLower = [rlp['x'] - rmp['x'], rlp['z'] - rmp['z']]
            angleMiddleYaw = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            rightJointYaw.append(angleMiddleYaw)

            # 3D Angle: From a reference vector (vectorUpperMiddle), we need the 3D vector to calculate angles
            # Note: the magnitude of the vectors must be from Upper to Middle and from Middle to Lower, convert results from radians to degrees
            # vectorUpperMiddle = (middle[x] - upper[x], middle[y] - upper[y], middle[z] - upper[z])
            # vectorMiddleLower = (lower[x] - middle[x], lower[y] - middle[y], lower[z] - middle[z])
            vectorUpperMiddle = [lmp['x'] - lup['x'], lmp['y'] - lup['y'], lmp['z'] - lup['z']]
            vectorMiddleLower = [llp['x'] - lmp['x'], llp['y'] - lmp['y'], llp['z'] - lmp['z']]
            angleMiddle3d = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            left3d.append(angleMiddle3d)

            vectorUpperMiddle = [rmp['x'] - rup['x'], rmp['y'] - rup['y'], rmp['z'] - rup['z']]
            vectorMiddleLower = [rlp['x'] - rmp['x'], rlp['y'] - rmp['y'], rlp['z'] - rmp['z']]
            angleMiddle3d = self.calculateAngle(vectorUpperMiddle, vectorMiddleLower)
            right3d.append(angleMiddle3d)

        return leftJointRoll, leftJointPitch, leftJointYaw, rightJointRoll, rightJointPitch, rightJointYaw, left3d, right3d
