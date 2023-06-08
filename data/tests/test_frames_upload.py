from django.test import TestCase, Client
from data.models import User, InvolvedIn, Session
from django.db import models
import json
import os
from rest_framework import status
from datetime import datetime
from django.urls import reverse

class FramesUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create an example user, session, and store the user as having been involved in this session
        self.user = User(1, "Steve", "Smith")
        self.user.save()
        self.session = Session(1, "Steve's Session", datetime.now().strftime("%Y-%m-%d"), "an example session")
        self.session.save()
        InvolvedIn(id=1, user=self.user, session=self.session).save()

        # ids for a user and a session that do not exist
        self.bad_uid = 99
        self.bad_sid = 99

        # Load in some example session data
        with open(os.path.dirname(__file__) + "/example_session.json", "r") as f:
            self.session_data = json.loads(f.read())


    def test_frames_upload_successful(self):
        request = {
            'uid': self.user.id,
            'sid': self.session.id,
            'frames': self.session_data,
        }
        response = self.client.post(path='/data/frames/upload', data=request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_frames_upload_user_does_not_exist(self):
        request = {
            'uid': self.bad_uid,
            'sid': self.session.id,
            'frames': self.session_data,
        }
        response = self.client.post(path='/data/frames/upload', data=request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_frames_upload_session_does_not_exist(self):
        request = {
            'uid': self.user.id,
            'sid': self.bad_sid,
            'frames': self.session_data,
        }
        response = self.client.post(path='/data/frames/upload', data=request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_frames_upload_user_not_involved_in_session(self):
        new_session = Session(
            2,
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
        response = self.client.post(path='/data/frames/upload', data=request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)