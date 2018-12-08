from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User

import time
from datetime import timedelta
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import pandas as pd
import seaborn
import numpy as np

from youtube.models import despacito as dsp
from . import youtube_lib as ytb


# Create your views here.
def get_token(request):
    crtuser = request.user
    social = crtuser.social_auth.get(provider='google-oauth2')
    auth_time = social.extra_data['auth_time']
    expire_time = social.extra_data['expires']
    if time.time() - auth_time > expire_time:
        raise Exception('Your AOuth2 has expired. Please log in again.')
    token = social.extra_data['access_token']
    return token


def youtubeRoot(request):
    return render(request, 'youtube.html')

def myLogout(request):
    logout(request)
    return render(request, 'youtube.html')

def channel_info_home(request):
    return render(request, 'ytb_searchchannel.html')

def channel_info_search(request):
    if request.method == 'POST':
        kw = request.POST['keyword']
        if not kw.replace(' ', ''):
            return render(request, 'ytb_searchchannel.html')

    chid = ytb.ch_title_to_id(kw)

    up_id_list = ytb.uploaded_viodeos(chid, 30)
    distrib = [0] * 50
    for vid in up_id_list:
        tmp = ytb.video_category(vid)
        # print(vid, tmp)
        distrib[tmp] += 1
    slices = []
    activities = []
    for i in range(len(distrib)):
        if distrib[i]:
            # print(i, ':', distrib[i], ytb.CATEGORY[i])
            slices.append(distrib[i])
            activities.append(ytb.CATEGORY[i])
    colors = ['c','m','r','b','g','c','gold','darkviolet']
    plt.pie(slices, labels=activities, colors=colors,
            startangle=90, autopct='%1.1f%%')
    plt.title('uploaded videos')
    path = '/home/test/zhduan/static/images/pie_{}.png'.format(chid)
    plt.savefig(path)
    plt.close()

    # all related video ids - all videos in 2018 in all playlist
    pl_id_list = ytb.all_playlists(chid)
    all_vid_list = ytb.lists_to_vids(pl_id_list)
    catgory_list = []
    distrib = [] # 2-d map
    for vid in all_vid_list:
        vinfo = ytb.video_list(vid, 'snippet')
        pubmon = vinfo['snippet']['publishedAt'][5:7] # published month
        pubmon = int(pubmon)
        vcgty = vinfo['snippet']['categoryId'] # video category
        vcgty = int(vcgty)
        if not vcgty in catgory_list:
            distrib.append([0]*12)
            catgory_list.append(vcgty)
        idx = catgory_list.index(vcgty) # index
        distrib[idx][pubmon-1] += 1
    distrib = np.array(distrib)
    ctgy_name = []
    for i in catgory_list:
        ctgy_name.append(ytb.CATEGORY[i])
    ctgy_name.reverse()
    df = pd.DataFrame(distrib, columns=[x for x in range(1,13)], 
                        index = ctgy_name)
    seaborn.heatmap(df, annot=True, cmap = 'Reds')
    plt.title('heat map')
    plt.xlabel('month')
    path = '/home/test/zhduan/static/images/heat_{}.png'.format(chid)
    plt.savefig(path)
    plt.close()

    print(chid)
    result = ytb.channel_list(chid)
    return render(request, 'ytb_searchchannel.html', result)


def ytb_my_like(request):
    try:
        token = get_token(request)
    except Exception as e:
        result = {'err_msg': str(e)}
        result['err_msg'] += ' Please try log in again.'
        return render(request, 'ytb_mylike.html', result)
    
    liked = ytb.liked_videos(token)

    distrib = [0] * 50
    for vid in liked:
        tmp = ytb.video_category(vid)
        # print(vid, tmp)
        distrib[tmp] += 1

    slices = []
    ctgy_labels = []
    for i in range(len(distrib)):
        if distrib[i]:
            # print(i, ':', distrib[i], ytb.CATEGORY[i])
            slices.append(distrib[i])
            ctgy_labels.append(ytb.CATEGORY[i])
    colors = ['c','m','r','b','g','c','gold','darkviolet']
    plt.pie(slices, labels=ctgy_labels, colors=colors,
            startangle=90, autopct='%1.1f%%')
    plt.title('liked videos')
    path = '/home/test/zhduan/static/images/pie_{}.png'.format(token[:10])
    plt.savefig(path)
    plt.close()

    result = {'token10': token[:10]}

    return render(request, 'ytb_mylike.html', result)


def my_youtube_stats(request):
    try:
        token = get_token(request)
    except Exception as e:
        result = {'err_msg':str(e)}
        result['err_msg'] += ' Please try log in again.'
        return render(request, 'ytb_myYoutube.html', result)
    result = ytb.mine_channel_list(token)
    tmp = ytb.list_items_num(result['mine_like_id'], token)
    result['mine_like_num'] = tmp
    return render(request, 'ytb_myYoutube.html', result)


def ytb_top_video(request):
    result = ytb.top_videos()
    if 'err_msg' in result:
        return render(request, 'ytb_topvideo.html', result)
    for i in range(len(result['videos'])):
        tmp = ytb.dateFmt(result['videos'][i]['snippet']['publishedAt'])
        result['videos'][i]['snippet']['publishedAt'] = tmp

        vid = result['videos'][i]['id']['videoId']
        result['videos'][i]['views'] = ytb.numFmt(ytb.video_viewCount(vid))
        result['videos'][i]['rank'] = i+1
    return render(request, 'ytb_topvideo.html', result)


def ytb_top_filter(request):
    if request.method == 'POST':
        time = request.POST['date']
        catgoryId = request.POST['category']
        duration = request.POST['duration']
        # deal with 'date'
        if time == 'all':
            time = None
        elif time == 'today':
            time = ytb.pre_time_RFC3339(d=1)
        elif time == 'week':
            time = ytb.pre_time_RFC3339(w=1)
        elif time == 'month':
            time = ytb.pre_time_RFC3339(m=1)
        elif time == 'year':
            time = ytb.pre_time_RFC3339(y=1)

        result = ytb.top_videos(after=time,
                                        cid=catgoryId, du=duration)
        for i in range(len(result['videos'])):
            tmp = result['videos'][i]['snippet']['publishedAt']
            tmp = tmp.replace('T', ' ')
            tmp = tmp.replace('Z', '')
            result['videos'][i]['snippet']['publishedAt'] = tmp[:-4]

            vid = result['videos'][i]['id']['videoId']
            count = ytb.video_viewCount(vid)
            count = int(count)
            count = format(count, ',')
            result['videos'][i]['views'] = count
            result['videos'][i]['rank'] = i+1
            result['videos'][i]['odd'] = (i+1)%2
        return render(request, 'ytb_topvideo.html', result)


def ytb_aboutus(request):
    return render(request, 'ytb_Aboutus.html')


def ytb_top_channel(request):
    if request.method == 'POST':
        result = ytb.top_channel(o=request.POST['order'])
    else:
        result = ytb.top_channel()

    for i in range(len(result['channels'])):
        tmp = ytb.dateFmt(result['channels'][i]['snippet']['publishedAt'])
        result['channels'][i]['snippet']['publishedAt'] = tmp

        cid = result['channels'][i]['id']['channelId']
        chinfo = ytb.channel_list(cid)

        if 'err_msg' in chinfo:
            result['err_msg'] = chinfo['err_msg']
            return render(request, 'ytb_topchannel.html', result)

        result['channels'][i]['views'] = ytb.numFmt(chinfo['ch_viewCount'])
        result['channels'][i]['videos'] = ytb.numFmt(chinfo['ch_videoCount'])
        result['channels'][i]['subs'] = ytb.numFmt(chinfo['chl_subCount'])
        result['channels'][i]['rank'] = i+1

    return render(request, 'ytb_topchannel.html', result)


def ytb_vstats_sample(request):
    all_set = dsp.objects.filter(date__contains='00:00')
    x = []
    yview = []
    dyview = []
    ylike = []
    dylike = []
    ydislike = []
    dydislike = []
    ycomment = []
    dycomment = []

    for i in all_set:
        tmp = i.date - timedelta(days=1)
        tmp = tmp.strftime('%a %b-%d')
        x.append(tmp)

        if len(yview) == 0:
            pass
        else:
            dyview.append(i.views - yview[-1])
            dylike.append(i.likes - ylike[-1])
            dydislike.append(i.dislikes - ydislike[-1])
            dycomment.append(i.comments - ycomment[-1])

        yview.append(i.views)
        ylike.append(i.likes)
        ydislike.append(i.dislikes)
        ycomment.append(i.comments)
    
    dx = x[1:]
    p = '/home/test/zhduan/static/images/line_{}_kJQP7kiw5Fk.png'
    # p = 'D:/Codes/zhduan.com/zhduan/youtube/line_{}_kJQP7kiw5Fk.png'
    tmp = p.format('view')
    plt_line(x, yview, tmp, 'Date', 'View count', 'Total views')
    tmp = p.format('dview')
    plt_line(dx, dyview, tmp, 'Date', 'Daily view', 'Daily views')
    tmp = p.format('like')
    plt_line(x, ylike, tmp, 'Date', 'Like count', 'Total likes')
    tmp = p.format('dlike')
    plt_line(dx, dylike, tmp, 'Date', 'Daily like', 'Daily views')
    tmp = p.format('dislike')
    plt_line(x, ydislike, tmp, 'Date', 'Dislike count', 'Total dislikes')
    tmp = p.format('ddislike')
    plt_line(dx, dydislike, tmp, 'Date', 'Daily dislike', 'Daily dislikes')
    tmp = p.format('comment')
    plt_line(x, ycomment, tmp, 'Date', 'Comment count', 'Total comments')
    tmp = p.format('dcomment')
    plt_line(dx, dycomment, tmp, 'Date', 'Daily comment', 'Daily comments')

    result = ytb.video_list('kJQP7kiw5Fk', 'snippet', 'statistics')
    result['snippet']['publishedAt'] = ytb.dateFmt(result['snippet']['publishedAt'])
    result['statistics']['viewCount'] = ytb.numFmt(result['statistics']['viewCount'])
    result['statistics']['likeCount'] = ytb.numFmt(result['statistics']['likeCount'])
    result['statistics']['dislikeCount'] = ytb.numFmt(result['statistics']['dislikeCount'])
    result['statistics']['commentCount'] = ytb.numFmt(result['statistics']['commentCount'])

    return render(request, 'ytb_statsdespacito.html', result)


def plt_line(x, y, path, xl, yl, title):
    '''
    :param x: list, x coordinate
    :param y: list, y coordinate
    :param path: str, the path to save
    :param xl: str, label of x
    :param yl: str, label of y
    :param title: str, the title of the graph
    :no return
    '''
    plt.figure(figsize=(15,8))
    plt.plot(x, y, marker='.')
    # set label of x and y
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.title(title)
    plt.xticks([t for t in x])
    plt.setp(plt.gca().get_xticklabels(), rotation=80, horizontalalignment='right')
    
    plt.savefig(path)
    plt.close()


# useless functions
def mylogin(request):
    return render(request, 'login.html')

def helloworld(request):
    return HttpResponse('Hello world')
