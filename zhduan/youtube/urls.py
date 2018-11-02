from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.youtubeRoot, name = 'youtubehome'),
    # path('login', views.login, name='ytblogin'),
    path('logout', views.myLogout, name='ytblogout'),
    # path('showtoken', views.show_token, name='showTokenPage'),
    path('chinfo', views.channel_info_home, name='ChannelInfoPage'),
    path('chinfo/search', views.channel_info_search, name='chInfoSearch'),
    path('myytb', views.my_youtube_stats, name='myYoutubePage'),
    path('topvideo', views.ytb_top_video, name='ytbTopVideos'),
    path('topfilter', views.ytb_top_filter, name='ytbTopFilter'),

    path('oath', include('social_django.urls', namespace='social')),
]