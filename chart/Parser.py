# Imports
import json

# Parser class
class Parser:
    # Instantiate class
    # @params joint, filename, shouldIgnore, shouldWarn
    def __init__(self, joint, filename, shouldIgnore, shouldWarn) -> None:
        # Instance variables for joint, input filename and error checking
        self.joint = joint.lower()
        self.filename = filename
        self.shouldIgnore = shouldIgnore
        self.shouldWarn = shouldWarn
        self.hasErrors = False

        # Number of frames
        self.numFrames = 0

        # Arrays for keypoints
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

        # Open json file
        try:
            with open(filename) as inputFile:
                # Parse json file into dictionary
                self.data = json.load(inputFile)
        
        except:
            print('File Error: ' + filename + ' cannot be read')
            exit(1)

        # Error checking for keypoints and joints
        if not self.isJointValid():
            print('Parse Error: joint (' + self.joint + ') is invalid')
            exit(1)

        if not self.arePointsValid() and not self.shouldIgnore:
            print('Parse Error: keypoints in a frame are invalid')
            print('Note: There may be duplicate or non-existant keypoints')
            exit(1)

        # Get points for all joints
        self.loadPoints()


    # Check if joint is valid
    def isJointValid(self):
        if self.joint in ['elbow', 'shoulder', 'hip', 'knee']:
            return True
        return False


    # Check if input file has keypoint errors
    def arePointsValid(self):
        frames = self.data['frames']
        numPoints = len(frames['1'])

        for frame in frames:
            # Check if number of keypoints in frame is valid
            if not len(frames[frame]) == numPoints:
                self.hasErrors = True
                return False
            
            # Check if number of elements in keypoint is valid
            for keypoint in frames[frame]:
                if not len(keypoint) == 5:
                    self.hasErrors = True
                    return False

        return True


    # Load points from file
    def loadPoints(self):
        # Get dictionary frames
        frames = self.data['frames']

        # Get number of frames
        self.numFrames = len(frames)

        # Get all joint points by looping through frames
        for frame in frames:
            # Get the current frame
            current_frame = frames[frame]

            # Add joint points to respective arrays
            for points in current_frame:
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

            if self.shouldIgnore:
                self.fix(frame)


#####################################################################################################
# Update this function so that it uses line of best fit
#####################################################################################################
    # Pad arrays if there are value errors
    def fix(self, frame):
        if len(self.leftWristPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in left_wrist")

            if (len(self.leftWristPoints) < self.numFrames):
                while len(self.leftWristPoints) != self.numFrames:
                    self.leftWristPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.leftWristPoints) != self.numFrames:
                self.leftWristPoints.pop()
        
        if len(self.leftElbowPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in left_elbow")

            if (len(self.leftElbowPoints) < self.numFrames):
                while len(self.leftElbowPoints) != self.numFrames:
                    self.leftElbowPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.leftElbowPoints) != self.numFrames:
                self.leftElbowPoints.pop()
        
        if len(self.leftShoulderPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in left_shoulder")
            
            if (len(self.leftShoulderPoints) < self.numFrames):
                while len(self.leftShoulderPoints) != self.numFrames:
                    self.leftShoulderPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.leftShoulderPoints) != self.numFrames:
                self.leftShoulderPoints.pop()
        
        if len(self.leftHipPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in left_hip")
            
            if (len(self.leftHipPoints) < self.numFrames):
                while len(self.leftHipPoints) != self.numFrames:
                    self.leftHipPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.leftHipPoints) != self.numFrames:
                self.leftHipPoints.pop()
        
        if len(self.leftKneePoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in left_knee")
            
            if (len(self.leftKneePoints) < self.numFrames):
                while len(self.leftKneePoints) != self.numFrames:
                    self.leftKneePoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.leftKneePoints) != self.numFrames:
                self.leftKneePoints.pop()

        if len(self.leftAnklePoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in left_ankle")
            
            if (len(self.leftAnklePoints) < self.numFrames):
                while len(self.leftAnklePoints) != self.numFrames:
                    self.leftAnklePoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.leftAnklePoints) != self.numFrames:
                self.leftAnklePoints.pop()

        if len(self.rightWristPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in right_wrist")
            
            if (len(self.rightWristPoints) < self.numFrames):
                while len(self.rightWristPoints) != self.numFrames:
                    self.rightWristPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.rightWristPoints) != self.numFrames:
                self.rightWristPoints.pop()
        
        if len(self.rightElbowPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in right_elbow")
            
            if (len(self.rightElbowPoints) < self.numFrames):
                while len(self.rightElbowPoints) != self.numFrames:
                    self.rightElbowPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.rightElbowPoints) != self.numFrames:
                self.rightElbowPoints.pop()
        
        if len(self.rightShoulderPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in right_shoulder")

            if (len(self.rightShoulderPoints) < self.numFrames):
                while len(self.rightShoulderPoints) != self.numFrames:
                    self.rightShoulderPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.rightShoulderPoints) != self.numFrames:
                self.rightShoulderPoints.pop()
        
        if len(self.rightHipPoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in right_hip")
            
            if (len(self.rightHipPoints) < self.numFrames):
                while len(self.rightHipPoints) != self.numFrames:
                    self.rightHipPoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.rightHipPoints) != self.numFrames:
                self.rightHipPoints.pop()
        
        if len(self.rightKneePoints) != self.numFrames:
            if self.shouldWarn:
                print("Warning: point error in frame " + frame + " in right_knee")
            
            if (len(self.rightKneePoints) < self.numFrames):
                while len(self.rightKneePoints) != self.numFrames:
                    self.rightKneePoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.rightKneePoints) != self.numFrames:
                self.rightKneePoints.pop()

        if len(self.rightAnklePoints) != self.numFrames:
            if self.shouldWarn:    
                print("Warning: point error in frame " + frame + " in right_ankle")

            if (len(self.rightAnklePoints) < self.numFrames):
                while len(self.rightAnklePoints) != self.numFrames:
                    self.rightAnklePoints.append({'x':0, 'y': 0, 'z': 0})
            
            while len(self.rightAnklePoints) != self.numFrames:
                self.rightAnklePoints.pop()
#####################################################################################################


    # Parse points
    def parse(self):
        # Arrays for joint points
        leftUpper = []
        leftMiddle = []
        leftLower = []
        rightUpper = []
        rightMiddle = []
        rightLower = []

        # Elbow joint
        if self.joint == 'elbow':
            leftUpper = self.leftShoulderPoints
            leftMiddle = self.leftElbowPoints
            leftLower = self.leftWristPoints
            rightUpper = self.rightShoulderPoints
            rightMiddle = self.rightElbowPoints
            rightLower = self.rightWristPoints

        # Shoulder joint
        if self.joint == 'shoulder':
            leftUpper = self.leftElbowPoints
            leftMiddle = self.leftShoulderPoints
            leftLower = self.leftHipPoints
            rightUpper = self.rightElbowPoints
            rightMiddle = self.rightShoulderPoints
            rightLower = self.rightHipPoints
                
        # Hip joint
        if self.joint == 'hip':
            leftUpper = self.leftShoulderPoints
            leftMiddle = self.leftHipPoints
            leftLower = self.leftKneePoints
            rightUpper = self.rightShoulderPoints
            rightMiddle = self.rightHipPoints
            rightLower = self.rightKneePoints
        
        # Knee joint
        if self.joint == 'knee':
            leftUpper = self.leftHipPoints
            leftMiddle = self.leftKneePoints
            leftLower = self.leftAnklePoints
            rightUpper = self.rightHipPoints
            rightMiddle = self.rightKneePoints
            rightLower = self.rightAnklePoints
        
        # Return a tuple with the left and right, upper, middle and lower points
        return self.numFrames, leftUpper, leftMiddle, leftLower, rightUpper, rightMiddle, rightLower


    # Save file with default filename
    def save(self):
        # Create default filename
        uid = self.data['uid']
        sid = self.data['sid']
        clipNum = self.data['clipNum']
        filename = 'uid-' + str(uid) + '-sid-' + str(sid) + '-clipNum-' + str(clipNum)

        # Get keypoints in parsed file
        keypoints = self.parse()

        # Create a dictionary for the keypoints
        keypointsDictionary = {
            'numFrames': keypoints[0], 
            'leftUpper': keypoints[1],
            'leftMiddle': keypoints[2],
            'leftLower': keypoints[3],
            'rightUpper': keypoints[4],
            'rightMiddle': keypoints[5],
            'rightLower': keypoints[6]
        }

        # Save in a json file
        if 'json' not in filename:
            filename = filename + '.json'

        with open(filename, 'w') as saveFile:
            saveFile.write(json.dumps(keypointsDictionary, indent=2))
