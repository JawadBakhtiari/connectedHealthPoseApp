from django.contrib import admin
from .models import Coordinate, User, Session, InvolvedIn

admin.site.register(User)
admin.site.register(Coordinate)
admin.site.register(Session)
admin.site.register(InvolvedIn)
