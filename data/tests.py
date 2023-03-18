from django.test import TestCase
from datetime import datetime
from .models import Coordinate, Frame, User

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
        
        # frames owned by steve
        self.f1 = Frame.objects.create(
            name="frame 1",
            description="first frame",
            date_created=datetime.now(),
            user=self.steve
        )
        self.f2 = Frame.objects.create(
            name="frame 2",
            description="second frame",
            date_created=datetime.now(),
            user=self.steve
        )

        # Coordinates belonging to frame 1, which belongs to steve
        Coordinate.objects.create(x=c1[0], y=c1[1], z=c1[2], frame=self.f1)
        Coordinate.objects.create(x=c2[0], y=c2[1], z=c2[2], frame=self.f1)

        # Coordinates belonging to frame 2, which belongs to steve
        Coordinate.objects.create(x=c3[0], y=c3[1], z=c3[2], frame=self.f2)
        Coordinate.objects.create(x=c4[0], y=c4[1], z=c4[2], frame=self.f2)


    def test_group_coordinates_by_frame(self) -> None:
        """Check that when we have a specific frame, that we can get all
            associated coordinates."""
        self.assertEqual(f1_coords, get_coord_tuples(self.f1.coordinate_set.all()))

    def test_group_coordinates_by_frame_by_user(self) -> None:
        """Check that when we have a specific user, that we can get all of the coordinates
            associated with a specific frame associated with that user."""

        frame2 = self.steve.frame_set.filter(id=self.f2.id)
        self.assertEqual(1, len(frame2))
        frame2 = frame2[0]
        self.assertEqual(f2_coords, get_coord_tuples(frame2.coordinate_set.all()))
