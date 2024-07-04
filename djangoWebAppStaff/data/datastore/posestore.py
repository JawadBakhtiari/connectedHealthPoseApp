import os
import json
import data.datastore.const as const
from data.datastore.cloud import get_blob_client
from data.datastore.util import get_keypoint_value_keys

class PoseStore:
    '''
    Handle the storage and retrieval of pose data for a clip.  
    '''
    def __init__(self, sid: str, clip_num: str) -> None:
        '''
        Args:
            sid (str)       - the id of the session
            clip_num (str)  - the clip number within this session
        '''
        self.sid = sid
        self.clip_num = clip_num


    def get(self) -> list:
        '''
        Return the pose data for this clip.

        Raises:
            ValueError: if pose data for this clip is not found.
        '''
        blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())
        if blob_client.exists():
            pose_data_string = blob_client.download_blob().content_as_text()
            return json.loads(pose_data_string)
        raise ValueError(
            f"poses from clip with sid '{self.sid}' and clip number '{self.clip_num}' not found"
        )


    def write_to_cloud(self) -> None:
        '''
        Write pose data for a this clip to cloud storage and delete local copy.
        '''
        file_path = self.get_path()
        if not os.path.exists(file_path):
            print(f"can't write poses to cloud for clip with sid '{self.sid}' and clip number '{self.clip_num}', no local poses")
            return

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
            else:
                # Upload the clip data as a new blob
                pose_data_bytes = json.dumps(pose_data).encode('utf-8')
                blob_client.upload_blob(pose_data_bytes)

        # NOTE -> commented out for validation
        # os.remove(file_path)


    def write_locally(self, poses: list) -> None:
        '''
        Write poses to locally (to file in file system).

        Args:
            poses: a list of poses as received from the pose estimation model.

        Raises:
            TypeError: if poses are not of type list.
        '''
        if not isinstance(poses, list):
            raise TypeError('poses must be of type list')

        poses = PoseStore.format_poses(poses)
        file_path = self.get_path()

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        existing_data += poses

        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)


    @staticmethod
    def format_poses(poses: list) -> list:
        '''
        Reformat pose data structure and return it.

        Args:
            poses: a list of poses as received from the pose estimation model.

        Returns:
            List containing formatted pose data.
        '''
        formatted_poses = []
        for pose in poses:
            timestamp = pose.get('timestamp')
            keypoints = []
            for i in range(const.NUM_KEYPOINTS):
                keypoint_index = i * const.VALS_PER_KEYPOINT
                new_keypoint = PoseStore.__create_formatted_keypoint(pose, keypoint_index)
                keypoints.append(new_keypoint)
            formatted_poses.append({'timestamp': timestamp, 'keypoints': keypoints})
        return formatted_poses


    @staticmethod
    def __create_formatted_keypoint(pose: dict, keypoint_index: int) -> dict:
        '''
        Format keypoint data in a more readable way.

        Args:
            pose: dictionary representing a single pose, from pose estimation model
            keypoint_index: index of this keypoint in the pose dictionary

        Returns:
            Dictionary with newly formatted keypoint data.
        '''
        xi, yi, zi, visi, presi = get_keypoint_value_keys(keypoint_index)
        x = pose.get(xi)
        y = pose.get(yi)
        z = pose.get(zi)
        visibility = pose.get(visi)
        presence = pose.get(presi)

        return {
            'name': const.KEYPOINT_MAPPINGS.get(keypoint_index / const.VALS_PER_KEYPOINT),
            'x': x,
            'y': y,
            'z': z,
            'visibility': visibility,
            'presence': presence
        }


    def get_name(self) -> str:
        '''
        Return the name that should be used to identify the file containing poses for this clip.
        '''
        return f"{self.sid}_{self.clip_num}"
    

    def get_path(self) -> str:
        '''
        Return the path to the file containing pose data for this clip in local storage.
        '''
        path = os.path.dirname(__file__)
        filename = self.get_name() + ".json"
        return os.path.join(path, "sessions", "poses", filename)


    def delete(self) -> None:
        '''
        Delete the pose data for a given clip from cloud storage.
        '''
        blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())
        if blob_client.exists():
            blob_client.delete_blob()
