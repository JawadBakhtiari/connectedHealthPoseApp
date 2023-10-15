'''Class that provides an abstraction for pose data and video storage.'''

from datastore.videostore import VideoStore
from datastore.posestore import PoseStore

class DataStore:
    def __init__(self, sid: str, clip_num: str):
        '''
        Args:
            sid (str)       - the id of the session
            clip_num (str)  - the clip number within this session
        '''
        self.video_store = VideoStore(sid, clip_num)
        self.pose_store = PoseStore(sid, clip_num)


    def set(self, poses: list, images: list):
        self.pose_store.set(poses)
        self.video_store.set(images)


    def populate(self):
        '''Populate the pose store and video store.
        Return:
            bool    ->  True if pose store and video store are both populated
                        successfully, False otherwise.
        '''
        return self.pose_store.populate() and self.video_store.populate_video()


    def get_video_path(self):
        return self.video_store.get_video_path()
    

    def get_poses(self):
        return self.pose_store.get()


    def write_locally(self):
        self.pose_store.write_locally()
        self.video_store.write_images_locally()


    def write_to_cloud(self):
        self.pose_store.write_to_cloud()
        self.video_store.write_video_to_cloud()


    def delete(self):
        self.pose_store.delete()
        self.video_store.delete()
