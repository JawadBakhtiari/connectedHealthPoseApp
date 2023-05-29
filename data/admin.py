from django.contrib import admin
from .models import User, Session, InvolvedIn

admin.site.register(User)
admin.site.register(Session)
admin.site.register(InvolvedIn)
