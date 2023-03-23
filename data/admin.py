from django.contrib import admin
from .models import Coordinate, Frame, User, Session, InvolvedInSession

admin.site.register(User)
admin.site.register(Frame)
admin.site.register(Coordinate)
admin.site.register(Session)
admin.site.register(InvolvedInSession)
