from django.test import TestCase, Client
from data.models import User, InvolvedIn, Session
import json
import os
from rest_framework import status
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import datastore.const as const
import uuid

class FramesUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Add the path to the endpoint
        self.path = "/data/frames/upload/"

        # Create an example user, session, and store the user as having been involved in this session
        self.user = User(str(uuid.uuid4()), "Stevey", "Smithy")
        self.user.save()
        self.session = Session(str(uuid.uuid4()), "Steve's Session", datetime.now().strftime("%Y-%m-%d"), "an example session")
        self.session.save()
        InvolvedIn(id=str(uuid.uuid4()), user=self.user, session=self.session).save()

        # ids for a user and a session that do not exist
        self.bad_uid = "nogood"
        self.bad_sid = "badid"

        # Load in some example session data
        with open(os.path.dirname(__file__) + "/data.json", "r") as f:
            self.session_data = json.loads(f.read())


    def test_frames_upload_append_to_session(self):
        # First request to create a session and upload session1_data
        request1 = {
            'uid': self.user.id,
            'sid': self.session.id,
            'clipNum': 1,
            'sessionFinished': False,
            'frames': self.session_data["poses"],
            'images': self.session_data["tensorAsArray"]
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

