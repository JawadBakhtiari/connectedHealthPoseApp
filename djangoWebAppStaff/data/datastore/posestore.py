'''Class for storing and retreiving pose data (keypoints) '''

import os
import json
import data.datastore.const as const
from data.datastore.cloud import get_blob_client

class PoseStore:
    def __init__(self, sid: str, clip_num: str):
        '''
        Args:
            sid (str)       - the id of the session
            clip_num (str)  - the clip number within this session
        '''
        self.sid = sid
        self.clip_num = clip_num
        self.poses = []


    def get(self):
        return self.poses


    def set(self, poses: list):
        pose_data = json.loads(poses)

        timestamp = pose_data[0]["timestamp"]

        keypoint_mapping = {
            "0": "Nose",
            "1": "Left Eye Inner",
            "2": "Left Eye Center",
            "3": "Left Eye Outer",
            "4": "Right Eye Inner",
            "5": "Right Eye Center",
            "6": "Right Eye Outer",
            "7": "Left Ear",
            "8": "Right Ear",
            "9": "Left Mouth",
            "10": "Right Mouth",
            "11": "Left Shoulder",
            "12": "Right Shoulder",
            "13": "Left Elbow",
            "14": "Right Elbow",
            "15": "Left Wrist",
            "16": "Right Wrist",
            "17": "Left Palm",
            "18": "Right Palm",
            "19": "Left Index",
            "20": "Right Index",
            "21": "Left Pinky",
            "22": "Right Pinky",
            "23": "Left Hip",
            "24": "Right Hip",
            "25": "Left Knee",
            "26": "Right Knee",
            "27": "Left Ankle",
            "28": "Right Ankle",
            "29": "Left Heel",
            "30": "Right Heel",
            "31": "Left Foot",
            "32": "Right Foot",
            "33": "Body Center",
            "34": "Forehead",
            "35": "Left Thumb",
            "36": "Left Hand",
            "37": "Right Thumb",
            "38": "Right Hand"
        }

        all_poses = []
        for item in pose_data:
            body_parts_list = []
            for i in range(39):
                index = i * 5  # Each keypoint has 5 values (x, y, z, visibility, presence)
                # print(index)
                x = item[str(index)]
                y = item[str(index + 1)]
                z = item[str(index + 2)]
                visibility = item[str(index + 3)]
                presence = item[str(index + 4)]

                body_parts_dict = {
                    "key_points": keypoint_mapping.get(str(i)),
                    "x": x,
                    "y": y,
                    "z": z,
                    "visibility": visibility,
                    "presence": presence
                }
                body_parts_list.append(body_parts_dict)
            all_poses.append({"timestamp": timestamp, "keypoints": body_parts_list})



        # # Define a mapping from numeric indices to body part names (adjust as needed)
        # body_part_mapping = {
        #     "0": "nose",
        #     "1": "left_eye",
        #     "2": "right_eye",
        #     "3": "left_ear",
        #     "4": "right_ear",
        #     "5": "left_shoulder",
        #     "6": "right_shoulder",
        #     "7": "left_elbow",
        #     "8": "right_elbow",
        #     "9": "left_wrist",
        #     "10": "right_wrist",
        #     "11": "left_hip",
        #     "12": "right_hip",
        #     "13": "left_knee",
        #     "14": "right_knee",
        #     "15": "left_ankle",
        #     "16": "right_ankle"
        # }

        
        # all_poses = []

        # # Iterate over the body parts and their coordinates
        # for item in pose_data:
        #     body_parts_list = []
        #     for index in range(17):  # Adjust the range based on the number of keypoints
        #         body_part = body_part_mapping.get(str(index))
        #         if body_part:
        #             x_coordinate = item[str(index)]
        #             y_coordinate = item[str(index + 17)]  # Adjust index for y-coordinate
        #             confidence = item[str(index + 34)]   # Adjust index for confidence score
        #             # Create a dictionary for the body part
        #             body_part_dict = {
        #                 "name": body_part,
        #                 "x": x_coordinate,
        #                 "y": y_coordinate,
        #                 "score": confidence
        #             }
            
        #             # Append the dictionary to the list
        #             body_parts_list.append(body_part_dict)
        #     all_poses.append({"timestamp": timestamp, "keypoints": body_parts_list})
            

        if not isinstance(pose_data, list):
            raise TypeError('poses must be of type list')
        self.poses = all_poses


    def get_name(self):
        '''Return the name that should be used to identify the file containing poses for this clip.
        '''
        return f"poses_{self.sid}_{self.clip_num}"
    

    def get_path(self):
        '''Return the path to the file containing pose data for this clip in local storage.'''
        path = os.path.dirname(__file__)
        filename = PoseStore.get_name(self) + ".json"
        return os.path.join(path, "sessions", "poses", filename)


    def populate(self):
        '''Populate clip dict with the contents of a specific clip from a session from cloud storage.
        Return true if clip file already exists, false otherwise.'''
        blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())

        if blob_client.exists():
            # Download the blob from that clip as a string and convert to json
            pose_data_string = blob_client.download_blob().content_as_text()
            self.poses = json.loads(pose_data_string)
            return True
        else:
            return False


    def write_locally(self):
        '''Write poses to file stored on file system.'''
        file_path = self.get_path()

        # Check if the file already exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_data = json.load(f)  # Load existing data from the file
        else:
            existing_data = []  # Create a new dictionary if the file doesn't exist

        # Update the existing data with the new pose data
        existing_data += self.poses

        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)


    def write_to_cloud(self):
        '''Write pose data for a given clip to cloud storage, delete local copy of pose data.'''
        file_path = self.get_path()

        try: 
            with open(file_path, "r") as f:
                pose_data = json.load(f)
                blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())
                if blob_client.exists():
                    # Shouldn't be reached, but handle this case just to be safe
                    downloaded_bytes = blob_client.download_blob().readall()
                    existing_data = json.loads(downloaded_bytes)
                    existing_data.update(pose_data)
                    updated_clip_data_bytes = json.dumps(existing_data).encode('utf-8')

                    # Upload the updated clip data (overwrite with updated information)
                    blob_client.upload_blob(updated_clip_data_bytes, overwrite=True)
                    print(self.sid)
                    print(self.clip_num)
                else:
                    # Upload the clip data as a new blob
                    pose_data_bytes = json.dumps(pose_data).encode('utf-8')
                    blob_client.upload_blob(pose_data_bytes)
                    print(self.sid)
                    print(self.clip_num)
        except:
            print(f"Failed to upload clip sid: {self.sid} clip_num: {self.clip_num} to cloud storage.")
        

    def delete(self):
        '''Delete the pose data for a given clip from cloud storage.'''
        blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())

        if blob_client.exists():
            blob_client.delete_blob()
