from django.db import models

#
#   May also need an ActiveUser model, for user's who are currently using the app?
#

class User(models.Model):
    """Represent a User in the database."""
    first_name = models.TextField(max_length=100, help_text='Enter user first name: ')
    last_name = models.TextField(max_length=100, help_text='Enter user last name: ')
    #   etc ...
    #
    #   Might want to add something like 'type',
    #   to distinguish between things like client vs physio ???
    #

    def __str__(self) -> str:
        """String for representing the Model object."""
        return f"{self.first_name} {self.last_name}"


class Frame(models.Model):
    """Represent a Frame in the database."""
    name = models.TextField(max_length=100, help_text='Enter name of frame: ')
    description = models.TextField(max_length=1000, help_text='Enter description of frame: ')
    date_created = models.DateTimeField(help_text='Enter date and time that this frame was created: ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Enter the id of the user who owns this frame: ')

    def __str__(self) -> str:
        """String for representing the Model object."""
        return self.name


class Coordinate(models.Model):
    """Represent a Coordinate in the database."""
    x = models.FloatField(help_text='Enter the width (x value) for the coordinate: ')
    y = models.FloatField(help_text='Enter the height (y value) for the coordinate: ')
    z = models.FloatField(help_text='Enter the depth (z value) for the coordinate: ')
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, help_text='Enter the id of the frame corresponding to this coordinate: ')

    def __str__(self) -> str:
        """String for representing the Model object."""
        return f"Frame #{self.frame}, coord: ({self.x}, {self.y}, {self.z})"