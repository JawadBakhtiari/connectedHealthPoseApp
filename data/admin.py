from django.contrib import admin
from .models import Coordinate, Frame, User

admin.site.register(User)
admin.site.register(Frame)
admin.site.register(Coordinate)
