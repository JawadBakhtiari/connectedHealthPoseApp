# Parser class
class Parser:
    # Instantiate class
    def __init__(self, joint, poseData) -> None:
        # Get joint, keypoint and frame data
        self.joint = joint
        self.leftWristPoints = []
        self.leftElbowPoints = []
        self.leftShoulderPoints = []
        self.leftHipPoints = []
        self.leftKneePoints = []
        self.leftAnklePoints = []
        self.rightWristPoints = []
        self.rightElbowPoints = []
        self.rightShoulderPoints = []
        self.rightHipPoints = []
        self.rightKneePoints = []
        self.rightAnklePoints = []  
        self.data = poseData
        self.loadPoints()


    # Load points
    def loadPoints(self):
        # Get all joint points by looping through frames
        for current_frame in self.data:
            # Add joint points to respective arrays
            for points in current_frame["keypoints"]:
                if (points['name'] == 'left_wrist'):
                    self.leftWristPoints.append(points)

                if (points['name'] == 'left_elbow'):
                    self.leftElbowPoints.append(points)

                if (points['name'] == 'left_shoulder'):
                    self.leftShoulderPoints.append(points)

                if (points['name'] == 'left_hip'):
                    self.leftHipPoints.append(points)

                if (points['name'] == 'left_knee'):
                    self.leftKneePoints.append(points)

                if (points['name'] == 'left_ankle'):
                    self.leftAnklePoints.append(points)

                if (points['name'] == 'right_wrist'):
                    self.rightWristPoints.append(points)

                if (points['name'] == 'right_elbow'):
                    self.rightElbowPoints.append(points)

                if (points['name'] == 'right_shoulder'):
                    self.rightShoulderPoints.append(points)

                if (points['name'] == 'right_hip'):
                    self.rightHipPoints.append(points)

                if (points['name'] == 'right_knee'):
                    self.rightKneePoints.append(points)

                if (points['name'] == 'right_ankle'):
                    self.rightAnklePoints.append(points)


    # Parse points
    def parse(self):
        leftUpper = []
        leftMiddle = []
        leftLower = []
        rightUpper = []
        rightMiddle = []
        rightLower = []

        # Elbow joint
        if self.joint == 'Elbow':
            leftUpper = self.leftShoulderPoints
            leftMiddle = self.leftElbowPoints
            leftLower = self.leftWristPoints
            rightUpper = self.rightShoulderPoints
            rightMiddle = self.rightElbowPoints
            rightLower = self.rightWristPoints

        # Shoulder joint
        if self.joint == 'Shoulder':
            leftUpper = self.leftElbowPoints
            leftMiddle = self.leftShoulderPoints
            leftLower = self.leftHipPoints
            rightUpper = self.rightElbowPoints
            rightMiddle = self.rightShoulderPoints
            rightLower = self.rightHipPoints
                
        # Hip joint
        if self.joint == 'Hip':
            leftUpper = self.leftShoulderPoints
            leftMiddle = self.leftHipPoints
            leftLower = self.leftKneePoints
            rightUpper = self.rightShoulderPoints
            rightMiddle = self.rightHipPoints
            rightLower = self.rightKneePoints
        
        # Knee joint
        if self.joint == 'Knee':
            leftUpper = self.leftHipPoints
            leftMiddle = self.leftKneePoints
            leftLower = self.leftAnklePoints
            rightUpper = self.rightHipPoints
            rightMiddle = self.rightKneePoints
            rightLower = self.rightAnklePoints
        
        # Return a tuple with the left and right, upper, middle and lower points
        return leftUpper, leftMiddle, leftLower, rightUpper, rightMiddle, rightLower
