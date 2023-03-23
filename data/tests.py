from django.test import TestCase
from datetime import datetime
from .models import Coordinate, Frame, User, Session, InvolvedInSession

# Frame 1 Coordinates
c1 = (1.2, 8.4, 5.2)
c2 = (7.0, 7.4, 76.3)
f1_coords = [c1, c2]

# Frame 2 Coordinates
c3 = (16.6, 2.0, 1.3)
c4 = (3.0, 23.4, 4.7)
f2_coords = [c3, c4]

def get_coord_tuples(coords: list) -> list:
    """Map a query set of coordinates into a list of coordinate tuples."""
    return list(map(lambda c: (c.x, c.y, c.z), coords))

class BasicTests(TestCase):
    def setUp(self) -> None:
        self.steve = User.objects.create(first_name="Steve", last_name="Smith")
        self.emma = User.objects.create(first_name="Emma", last_name="Jones")

        self.s1 = Session.objects.create(date=datetime.now())
        self.s2 = Session.objects.create(date=datetime.now())

        # Emma and Steve are both involved in Session s1
        self.i1 = InvolvedInSession.objects.create(
            user=self.steve,
            session=self.s1
        )
        self.i2 = InvolvedInSession.objects.create(
            user=self.emma,
            session=self.s1
        )

        # Only Emma is involved in Session s2
        self.i3 = InvolvedInSession.objects.create(
            user=self.emma,
            session=self.s2
        )

        # Frames f1 and f2 both associated with Session s1
        self.f1 = Frame.objects.create(
            name="frame 1",
            description="first frame",
            session=self.s1
        )
        self.f2 = Frame.objects.create(
            name="frame 2",
            description="second frame",
            session=self.s1
        )

        # Coordinates belonging to Frame f1, which belongs Session s1
        Coordinate.objects.create(x=c1[0], y=c1[1], z=c1[2], frame=self.f1)
        Coordinate.objects.create(x=c2[0], y=c2[1], z=c2[2], frame=self.f1)

        # Coordinates belonging to Frame f2, which belongs to Session s1
        Coordinate.objects.create(x=c3[0], y=c3[1], z=c3[2], frame=self.f2)
        Coordinate.objects.create(x=c4[0], y=c4[1], z=c4[2], frame=self.f2)


    def test_group_coordinates_by_frame(self) -> None:
        """Check that when we have a specific frame, that we can get all
            associated coordinates."""
        self.assertEqual(f1_coords, get_coord_tuples(self.f1.coordinate_set.all()))

    def test_group_users_by_session(self) -> None:
        """Check that given a Session id, that Users involved in that Session can be 
            grouped together."""
        users_in_session_1 = [
            i.user for i in InvolvedInSession.objects.filter(session=self.s1.id)
        ]
        self.assertEqual(list(User.objects.all()), users_in_session_1)

    def test_group_frames_by_session(self) -> None:
        """Check that given a Session id, that Frames involved in that Session can be 
            grouped together."""
        frames_in_session_1 = self.s1.frame_set.all()
        self.assertEqual(list(frames_in_session_1), list(Frame.objects.all()))