from django.test import TestCase, Client
from data.models import User, InvolvedIn, Session
import json
import os
from rest_framework import status
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import datastore.const as const
import uuid

'''
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

        # Load in some example session data
        with open(os.path.dirname(__file__) + "/example_session.json", "r") as f:
            self.session_data = json.loads(f.read())

    def test_frames_upload_append_to_session(self):
        # Load the example session data
        with open(os.path.dirname(__file__) + "/example_session.json", "r") as f:
            session1_data = json.loads(f.read())

        # Load the second example session data
        with open(os.path.dirname(__file__) + "/example_session2.json", "r") as f:
            session2_data = json.loads(f.read())

        # First request to create a session and upload session1_data
        request1 = {
            'uid': self.user.id,
            'sid': self.session.id,
            'clipNum': 1,
            'sessionFinished': False,
            'frames': session1_data,
        }
        response1 = self.client.post(
            path=self.path,
            data=json.dumps(request1),
            content_type="application/json",
            follow=True
        )

        # Check if the response is successful
        self.assertEqual(response1.status_code, status.HTTP_200_OK)


        # Check if the file is uploaded locally in datastore/sessions/session_1_1
        session_file_path = os.path.join("datastore", "sessions", f"session_{self.session.id}_{request1['clipNum']}")
        self.assertTrue(os.path.exists(session_file_path))

        # Second request to append session2_data to the existing session
        request2 = {
            'uid': self.user.id,
            'sid': self.session.id,
            'clipNum': 1,
            'sessionFinished': True,
            'frames': session2_data,
        }
        response2 = self.client.post(
            path=self.path,
            data=json.dumps(request2),
            content_type="application/json",
            follow=True
        )

        # Check if the response is successful
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Check if the file session_1_1 is deleted
        self.assertFalse(os.path.exists(session_file_path))

        # all session files are uploaded on azure and are 
        # deleted from the sessions directory. 

        blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)
        blob_name = f"session_{self.session.id}_{request2['clipNum']}"
        blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, blob=blob_name)

        blob_exists = blob_client.exists()

        # Check if the blob exists
        self.assertTrue(blob_exists)

        # Delete the blob
        blob_client.delete_blob()

        # Check if the blob is deleted
        blob_exists = blob_client.exists()
        self.assertFalse(blob_exists)
    

    def test_frames_upload_user_does_not_exist(self):
        request = {
            'uid': self.bad_uid,
            'sid': self.session.id,
            'clipNum': 1,
            'frames': self.session_data,
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
            'frames': self.session_data,
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
            'frames': self.session_data,
        }
        response = self.client.post(
            path=self.path,
            data=json.dumps(request),
            content_type="application/json",
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

'''