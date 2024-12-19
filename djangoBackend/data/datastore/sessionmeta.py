'''Functionality related to retrieving and updating session metadata.'''

from ..models import Session


def get_clip_num(sid: str):
    '''
    Get the current clip number for this session.
    '''
    return Session.objects.get(id=sid).clip_num

def increment_clip_num(sid: str):
    '''
    Increment the current clip number for this session by 1.
    '''
    s = Session.objects.get(id=sid)
    s.clip_num += 1
    s.save()
