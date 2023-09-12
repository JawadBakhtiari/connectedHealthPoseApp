from django.test import TestCase, Client
from data.models import User, InvolvedIn, Session
import json
import os
from rest_framework import status
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import datastore.const as const
from datastore.datastore import DataStore
import uuid


class FramesUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Add the path to the endpoint
        self.path = "/data/frames/upload/"

        # Create an example user, session, and store the user as having been involved in this session
        self.user = User(str(uuid.uuid4()), "Steve", "Smith")
        self.user.save()
        self.session = Session(str(uuid.uuid4()), "Steve's Session", datetime.now().strftime("%Y-%m-%d"), "an example session")
        self.session.save()
        InvolvedIn(id=str(uuid.uuid4()), user=self.user, session=self.session).save()

        # ids for a user and a session that do not exist
        self.bad_uid = "nogood"
        self.bad_sid = "badid"

        # Load in some example frames data
        with open(os.path.dirname(__file__) + "/example_frames.json", "r") as f:
            self.frames = json.loads(f.read())

    def test_frames_upload_append_to_clip(self):
        # Send frame data
        request1 = {
            'uid': self.user.id,
            'sid': self.session.id,
            'clipNum': 1,
            'sessionFinished': False,
            'poses': self.frames["poses"],
            'images': self.frames["tensorAsArray"]
        }
        response1 = self.client.post(
            path=self.path,
            data=json.dumps(request1),
            content_type="application/json",
            follow=True
        )

        # Check if the response is successful
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Check that both directory for images and poses file have been created
        poses_file_path = os.path.join("datastore", "sessions", "poses", DataStore.get_poses_name(self.session.id, request1.get('clipNum'))) + ".json"
        images_dir_path = os.path.join("datastore", "sessions", "images", DataStore.get_images_name(self.session.id, request1.get('clipNum')))

        self.assertTrue(os.path.exists(poses_file_path))
        self.assertTrue(os.path.exists(images_dir_path))

        # Send same frame data again, but this time session is finished
        request2 = {
            'uid': self.user.id,
            'sid': self.session.id,
            'clipNum': 1,
            'sessionFinished': True,
            'poses': self.frames["poses"],
            'images': self.frames["tensorAsArray"]
        }
        response2 = self.client.post(
            path=self.path,
            data=json.dumps(request2),
            content_type="application/json",
            follow=True
        )

        # Check if the response is successful
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Check that local copy of poses file has been removed
        self.assertFalse(os.path.exists(poses_file_path))

        # all session files are uploaded on azure and are 
        # deleted from the sessions directory. 

        # TODO ->   once cloud storage implemented for images, check image
        #           blob as well as poses blob (poses blob already checked)

        # Check that right number of poses have been recorded
        expected_pose_data_length = len(self.frames.get("poses")) * 2
        store = DataStore()
        store.populate_poses(self.session.id, request2.get('clipNum'))

        self.assertEquals(len(store.get_poses()), expected_pose_data_length)

        # Delete the blob
        store.delete_clip(self.session.id, request2.get('clipNum'))
    

    def test_frames_upload_user_does_not_exist(self):
        request = {
            'uid': self.bad_uid,
            'sid': self.session.id,
            'clipNum': 1,
            'poses': self.frames["poses"],
            'images': self.frames["tensorAsArray"]
        }
        response = self.client.post(
            path=self.path,
            data=json.dumps(request),
            content_type="application/json",
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_frames_upload_session_does_not_exist(self):
        request = {
            'uid': self.user.id,
            'sid': self.bad_sid,
            'poses': self.frames["poses"],
            'images': self.frames["tensorAsArray"]
        }
        response = self.client.post(
            path=self.path,
            data=json.dumps(request),
            content_type="application/json",
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_frames_upload_user_not_involved_in_session(self):
        new_session = Session(
            str(uuid.uuid4()),
            "a new session",
            datetime.now().strftime("%Y-%m-%d"),
            "no one is involved in this session!"
        )
        new_session.save()
        request = {
            'uid': self.user.id,
            'sid': new_session.id,
            'poses': self.frames["poses"],
            'images': self.frames["tensorAsArray"]
        }
        response = self.client.post(
            path=self.path,
            data=json.dumps(request),
            content_type="application/json",
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
