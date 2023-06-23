from django.test import TestCase, Client
from data.models import User, InvolvedIn, Session
import json
import os
from rest_framework import status
from datetime import datetime
import uuid

class SessionInitTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Add the path to the endpoint
        self.path = "/data/session/init/"

        # Create example users
        self.user1 = User(str(uuid.uuid4()), "Steve", "Smith")
        self.user1.save()
        self.user2 = User(str(uuid.uuid4()), "Sarah", "Jones")
        self.user2.save()

        # id for a user that does not exist
        self.bad_uid = "badid"

    def test_init_session_good(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request = {
            'uids': [self.user1.id, self.user2.id],
            'session': {
                'name': "first session",
                'date': date,
                'description': "a test session"
            }
        }
        response = self.client.post(
            path=self.path,
            data=json.dumps(request),
            content_type="application/json",
            follow=True
        )

        # Check success
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)
        sid = response_data.get('sid')
        new_session = Session.objects.filter(id=sid)[0]

        # Check that session is stored with the correct metadata
        self.assertEquals(new_session.name, "first session")
        self.assertEquals(new_session.date.strftime("%Y-%m-%d %H:%M:%S"), date)
        self.assertEquals(new_session.description, "a test session")

        # Check that both users have been recorded as being involved in this session
        users = [self.user1, self.user2]
        users_involved = InvolvedIn.objects.filter(session=new_session, user__in=users)
        self.assertEquals(len(users_involved), len(users))

    def test_init_session_invalid_user(self):
        request = {
            'uids': [self.user1.id, self.bad_uid],
            'session': {
                'name': "first session",
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'description': "a test session"
            }
        }
        response = self.client.post(
            path=self.path,
            data=json.dumps(request),
            content_type="application/json",
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)