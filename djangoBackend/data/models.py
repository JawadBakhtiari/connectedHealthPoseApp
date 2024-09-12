from django.db import models

class User(models.Model):
    id = models.TextField(max_length=200, primary_key=True)
    first_name = models.TextField(max_length=100, help_text='Enter user first name: ')
    last_name = models.TextField(max_length=100, help_text='Enter user last name: ')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Session(models.Model):
    id = models.TextField(max_length=200, primary_key=True)
    name = models.TextField(max_length=100, help_text='Enter the name of this session: ')
    date = models.DateTimeField(help_text='Enter date and time that this session started: ')
    description = models.TextField(max_length=1000, help_text='Enter description of the session: ')
    clip_num = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"Session #{self.id} ({self.name}) on {self.date}"


class InvolvedIn(models.Model):
    '''
    Map Sessions to Users, since multiple Users may participate in a given Session and
    a given User may participate in multiple Sessions.
    '''
    id = models.TextField(max_length=200, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Enter the id of the user who participated in this session: ')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, help_text='Enter the id of the session that this user participated in: ')

    def __str__(self) -> str:
        user_info = User.objects.get(id=self.user.id)
        session_info = Session.objects.get(id=self.session.id)
        return f"{user_info.first_name} {user_info.last_name} (user id #{user_info.id}) "\
                f"was involved in session #{session_info.id} on {session_info.date}"
    