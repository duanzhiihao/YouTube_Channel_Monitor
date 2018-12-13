# daily request to youtube
from django.utils import timezone

from youtube.models import despacito
from .ytbAPI import ytbAPI
from . import youtube_lib as ytb

def despacito_daily():
    result = ytb.video_list('kJQP7kiw5Fk','statistics')
    t = timezone.now()
    v = result['statistics']['viewCount']
    l = result['statistics']['likeCount']
    d = result['statistics']['dislikeCount']
    c = result['statistics']['commentCount']
    tmp = despacito(date=t, views=v, likes=l, dislikes=d, comments=c)
    tmp.save()
    print('despacito daily done: {} \n'.format(str(t)))
    
def test():
    print('testdaily')