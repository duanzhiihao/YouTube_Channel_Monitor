import ytbAPI
import time
import models
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
def pre_time_RFC3339(d=0, w=0, m=0, y=0):
	'''
	minus current local time with the parameter,
	then return the time in format of RFC 3339
	d: int, day
	w: int, week
	m: int, month
	y: int, year
	return: str, like '2018-10-30T14:03:06Z'
	'''
	assert d >= 0
	assert w >= 0
	assert m >= 0
	assert y >= 0

	lt = time.time()
	if d:
		lt -= 86400*d
	if w:
		lt -= 604800*w
	if m:
		lt -= 2592000*m
	if y:
		lt -= 31536000*y
	lt = time.localtime(lt)
	timeStr = time.strftime("%Y-%m-%dT%H:%M:%SZ", lt)

	return timeStr

#API class


from urllib import request
import json

class ytbAPI(object):

	DATA_V3_BASE = 'https://www.googleapis.com/youtube/v3/'
	__API_KEY = "AIzaSyCSvURiKWPils3rKRP-Uh18s8lwwRFbKgc"

	def __init__(self):
		self.keyStr = '&key=' + self.__API_KEY
		self.url = self.DATA_V3_BASE

	def scope(self, scp):
		'''
		scp: str, name of scope
		'''
		self.scopeStr = scp + '?'
		self.url += self.scopeStr



	
	def part(self, *args):
		'''
		*args: tuple of str, input 'part'
		'''
		if len(args)==0:
			raise Exception('No input part parameter')
		self.partStr = 'part='
		for arg in args:
			self.partStr += arg + '%2C'
		self.partStr = self.partStr[:-3]
		self.url += self.partStr

	def id(self, i):
		'''
		i: str, input id
		'''
		self.idStr = '&id=' + i
		self.url += self.idStr
	
	def cid(self, i):
		'''
		i: str, input id
		'''
		self.idStr = '&channelId=' + i
		self.url += self.idStr


	def myRating(self, myRating):
		'''
		myRating: str, like or dislike
		'''
		self.idStr = '&myRating='+myRating
		self.url += self.idStr



	def mine(self, m=True):
		'''
        m: bool, the value of 'mine'
        '''
		if m:
			self.mineStr = '&mine=true'
			self.url += self.mineStr

	def maxResults(self, m):
		'''
		m: str or int or float, the max number of results per page
		'''
		m = int(m)
		m = str(m)
		self.maxStr = '&maxResults=' + m
		self.url += self.maxStr

	def playlistId(self, i):
		'''
		i: str, input playlist id
		'''
		self.listIdStr = '&playlistId=' + i
		self.url += self.listIdStr

	def order(self, o):
		'''
		o: str, the type of order
		'''
		self.orderStr = '&order=' + o
		self.url += self.orderStr
	
	def safeSearch(self, s='none'):
		'''
		s: str, '	erate', 'none', 'strict'
		'''
		self.safeSrchStr = '&safeSearch=' + s
		self.url += self.safeSrchStr

	def type(self, t):
		'''
		t: str, 'channel', 'playlist', 'video'
		'''
		self.typeStr = '&type=' + t
		self.url += self.typeStr

	def videoCategoryId(self, i):
		'''
		i: str, video category id
		'''
		self.vctgyIdStr = '&videoCategoryId=' + i
		self.url += self.vctgyIdStr

	def publishedAfter(self, t):
		'''
		t: str, the time, like '2018-01-01T00:00:00Z'
		'''
		t = t.replace(':','%3A')
		self.pbAfterStr = '&publishedAfter=' + t
		self.url += self.pbAfterStr

	def videoDuration(self, d='any'):
		'''
		d: str, the duration of video, can be:
								'any',
								'long' > 20 mins,
								'medium' 4 - 20 mins,
								'short' < 4 mins
		'''
		valid = ('any','long','medium','short')
		assert d in valid, '{} is not a valid duration'.format(d)
		self.vDrtnStr = '&videoDuration=' + d
		self.url += self.vDrtnStr

	#---------------------------------------------------

	def key(self, k=False):
		'''
		k: str, the api_key of Google Cloud
		'''
		if k:
			self.keyStr = '&key=' + k
		self.url += self.keyStr
	
	def access_token(self, t):
		'''
		t: str, input OAuth 2 access token
		'''
		self.tokenStr = '&access_token=' + t
		self.url += self.tokenStr

	def GET(self):
		'''
		return: dictionary, response of youtube/google
		'''
		#print(self.url)						#only for test
		try:
			req = request.Request(self.url)
			page = request.urlopen(req).read()
			page = page.decode('utf-8')
			return json.loads(page)
		except Exception as e:
			return {'error': e}





#API class
def channel_list(cid):
	'''
	cid: channel id
	return: key-value dict
	'''
	ytb0 = ytbAPI()
	ytb0.scope('channels')
	ytb0.part('topicDetails','snippet', 'contentDetails','statistics')
	ytb0.id(cid)
	ytb0.key()
	response = ytb0.GET()

	re_map = {}
	if 'error' in response:
		re_map['err_msg'] = 'Error from google: Invalid channel id'
		return re_map
	if not 'items' in response:
		re_map['err_msg'] = 'No item in response: Invalid channel id'
		return re_map
	elif len(response['items'])==0:
		re_map['err_msg'] = 'No result: Invalid channel id'
		return re_map
	
	items0 = response['items'][0]
	re_map['ch_title'] = items0['snippet']['title']
	re_map['ch_id'] = items0['id']
	re_map['ch_viewCount'] = items0['statistics']['viewCount']
	re_map['ch_videoCount'] = items0['statistics']['videoCount']
	if items0['statistics']['hiddenSubscriberCount'] == True:
		re_map['chl_subCount'] = 'invisible'
	else:
		re_map['chl_subCount'] = items0['statistics']['subscriberCount']

	return re_map


def mine_channel_list(token):
	'''
	token: access token of OAuth 2 user
	return: key-value dict
	'''
	ytb0 = ytbAPI()
	ytb0.scope('channels')
	ytb0.part('snippet', 'contentDetails', 'statistics')
	ytb0.mine()
	ytb0.access_token(token)
	response = ytb0.GET()

	re_map = {}
	if 'error' in response:
		re_map['err_msg'] = response['error']['message']
		return re_map
	elif not 'items' in response:
		re_map['err_msg'] = 'No item in response.'
		return re_map
	
	items0 = response['items'][0]
	try:
		re_map['mine_title'] = items0['snippet']['title']
		re_map['mine_ch_id'] = items0['id']
		tmp = items0['snippet']['publishedAt']
		tmp = tmp.replace('T', ' ')
		tmp = tmp.replace('Z','')
		re_map['publishDate'] = tmp[:-4]
		re_map['thumb_88_url'] = items0['snippet']['thumbnails']['default']['url']
		re_map['mine_like_id'] = items0['contentDetails']['relatedPlaylists']['likes']
		re_map['mine_upload'] = items0['contentDetails']['relatedPlaylists']['uploads']
		re_map['mine_sub_num'] = my_sub_num(token)
	except Exception as e:
		re_map['err_msg'] = e
		return re_map
	
	return re_map


def my_sub_num(token):
	'''
	calculate and return the number of my subscriptions
	token: str, OAuth 2 user's access token
	return: str, user's subscription number
			or str, the exception message
	'''
	ytb0 = ytbAPI()
	ytb0.scope('subscriptions')
	ytb0.part('contentDetails')
	ytb0.mine()
	ytb0.access_token(token)
	response = ytb0.GET()

	try:
		num = response['pageInfo']['totalResults']
	except Exception as e:
		return e
	return num


def list_items_num(lid, token):
	'''
	lid: playlist id
	token: access token of OAuth 2 user
	return: int, number of items of the list
	'''
	ytb0 = ytbAPI()
	ytb0.scope('playlistItems')
	ytb0.part('snippet', 'contentDetails')
	ytb0.maxResults(1)
	ytb0.playlistId(lid)
	ytb0.access_token(token)
	response = ytb0.GET()

	if 'error' in response:
		return response['error']['message']
	elif not 'pageInfo' in response:
		return 'no page info in response'
	else:
		return response['pageInfo']['totalResults']
	

def top_videos(num=10, after=None, cid='all', du='any'):
	'''
	num: int, how many videos to return
	after: str,  the time, like '2018-01-01T00:00:00Z'
	cid: str, video category id
	du: str, the duration of video: 'any',
									'long' > 20 mins,
									'medium' 4 - 20 mins,
									'short' < 4 mins

	return: dict, ['videos']: a list of (num) dicts, ['err_msg']
	'''
	ytb0 = ytbAPI()
	ytb0.scope('search')
	ytb0.part('snippet')
	ytb0.maxResults(num)
	ytb0.order('viewCount')
	ytb0.safeSearch('none')
	ytb0.type('video')
	ytb0.key()
	if after:
		ytb0.publishedAfter(after)
	if cid != 'all':
		ytb0.videoCategoryId(cid)
	if du != 'any':
		ytb0.videoDuration(du)

	print(ytb0.url)
	response = ytb0.GET()

	re_map = {}
	if 'error' in response:
		re_map['err_msg'] = response['error']['message']
		return re_map
	elif not 'items' in response:
		re_map['err_msg'] = 'No item in response.'
		return re_map
	
	re_map['videos'] = response['items'] # a list
	return re_map


def video_list(vid, *args):
	'''
	vid: str, video id
	*args: parts of request
	return: dict, json file
	'''
	ytb0 = ytbAPI()
	ytb0.scope('videos')
	ytb0.part(*args)
	ytb0.id(vid)
	ytb0.key()
	response = ytb0.GET()

	if 'error' in response:
		raise Exception(response['error']['message'])
	elif not 'items' in response:
		raise Exception('No items in response')
		return ['no item']

	if (len(response['items'])):
		return response['items'][0]
	else:
		return 'items = []'

def video_viewCount(vid):
	'''
	Get the view count of a video
	vid: str, video id
	return: str, the number of views, like '320000'
	'''
	stat = video_list(vid, 'statistics')
	return stat['statistics']['viewCount']








# def most_video_ch():





def video_associated(cid):			#return a list of video id associated with user
									#through activities, like/dislike/playlist

	videosids=[]					#get video ids of videos in playlist
	ytb0=ytbAPI()					
	ytb0.scope('playlists')
	ytb0.part('snippet')
	ytb0.cid(cid)
	ytb0.maxResults(10)
	ytb0.key()
	response = ytb0.GET()
	re_map = []
	'''
	if 'error' in response:
		re_map['err_msg'] = response['error']['message']
		return re_map
	elif not 'items' in response:
		re_map['err_msg'] = 'No item in response.'
		return re_map
	'''


	playlists=[]	
		
	for item in response['items']:
		playlists.append(item['id'])
	

	for a in playlists:			
		ytb0=ytbAPI()	
		ytb0.scope('playlistItems')
		ytb0.part('snippet')
		ytb0.playlistId(a)
		ytb0.maxResults(50)
		ytb0.key()
		response = ytb0.GET()
		for b in response['items']:
			if ((b['snippet']['resourceId']['videoId']) not in videosids):
				videosids.append(b['snippet']['resourceId']['videoId'])

		
	

	'''				
	ytb0=ytbAPI()					#get video id of like videos
	ytb0.scope('videos')
	ytb0.part('snippet')
	ytb0.myRating('like')
	ytb0.key()
	response = ytb0.GET()
	for a in response['items']:
		if a['id'] not in videosids:
			videosids.append(a['id'])


	ytb0=ytbAPI()					#get video id of dislike videos
	ytb0.scope('videos')
	ytb0.part('snippet')
	ytb0.myRating('dislike')
	ytb0.key()
	response = ytb0.GET()
	for a in response['items']:
		if a['id'] not in videosids:
			videosids.append(a['id'])
	return (videosids)

	'''
	ytb0=ytbAPI()					#get video id of uploaded videos
	ytb0.scope('activities')
	ytb0.part('snippet')
	ytb0.cid(cid)
	ytb0.maxResults(10)
	ytb0.key()
	response = ytb0.GET()
	for a in response['items']:
		b = (a['snippet']['thumbnails']['default']['url'])	
		i = -1
		while(b[i]!='/'):
			i=i-1
		i=i-1
		idstr=''
		while(b[i]!='/'):
			idstr=idstr+b[i]
			i=i-1

		videosids.append(idstr[::-1])


	return (videosids)




# input a video id, and return a dictionary of type and num
def video_type(vid):

	ytb0=ytbAPI()					
	ytb0.scope('videos')
	ytb0.part('snippet')
	ytb0.id(vid)
	ytb0.key()
	response = ytb0.GET()
	for a in response['items']:
		if (int(a['snippet']['categoryId'])!=None):
			return(int(a['snippet']['categoryId']))
		else:
			return 0








def cataname(cataid):
	

	
	catatrans = ['no such catagory']
	for i in range (0,50):
		catatrans.append('no such catagory')	

	catatrans[1] = 'Film & Animation'
	catatrans[2] = 'Autos & Vehicles'
	catatrans[10] = 'Music'
	catatrans[15] = 'Pets & Animals'
	catatrans[17] = 'Sports'
	catatrans[18] = 'Short Movies'
	catatrans[19] = 'Travel & Events'
	catatrans[20] = 'Gaming'
	catatrans[21] = 'Videoblogging'
	catatrans[22] = 'People & Blogs'
	catatrans[23] = 'Comedy'
	catatrans[24] = 'Entertainment'
	catatrans[25] = 'News & Politics'
	catatrans[26] = 'How to & Style'
	catatrans[27] = 'Education'
	catatrans[28] = 'Science & Technology'
	catatrans[29] = 'Nonprofits & Activism'
	catatrans[30] = 'Movies'
	catatrans[31] = 'Anime/Animation'
	catatrans[32] = 'Action/Adventure'
	catatrans[33] = 'Classics'
	catatrans[34] = 'Comedy'
	catatrans[35] = 'Documentary'
	catatrans[36] = 'Drama'
	catatrans[37] = 'Family'
	catatrans[38] = 'Foreign'
	catatrans[39] = 'Horror'
	catatrans[40] = 'Sci-Fi/Fantasy'
	catatrans[41] = 'Thriller'
	catatrans[42] = 'Shorts'
	catatrans[43] = 'Shows'
	catatrans[44] = 'Trailers'
	return catatrans[cataid]



#get associated video ids
video_ids = video_associated('UCBR8-60-B28hp2BmDPdntcQ')			#input channel ID e.g. UCLVkacKvPLT_p6rVDSyl6GQ    UC9k-yiEpRHMNVOnOi_aQK8w		UCBR8-60-B28hp2BmDPdntcQ
print('here is the list of vidoes associated with the user')
print(video_ids)



##### heat map
videomonth = []
videotype = []
typelabel = []
typenum = 0
for videoid in video_ids:										#get publish month
	if(video_list(videoid,'snippet')!='items = []'):
		a = video_list(videoid,'snippet')

	if(type(a)==dict):
		a = a['snippet']['publishedAt']
	#else:
		#continue
	b = int(a[0:4])
	if b!=2018:
		continue
	b = a[5:7]
	
	videomonth.append(int(b))
	if(video_type(videoid) not in videotype):
		if(video_type(videoid)!=None):
			typenum = typenum + 1
			typelabel.append(video_type(videoid))
	videotype.append(video_type(videoid))
b = len(videomonth)
a = len(videotype)
y = [0]
for i in range(1,typenum*12+1):
	y.append(0)

y = np.zeros(typenum*12)
for i in range(typenum,0,-1):	
	for j in range(1,13):
		value = 0
		for k in range(0,a):
				if (typelabel[i-1] == videotype[k]):
					if (j == videomonth[k]):
						value = value+1
						
						
		y[(typenum-i)*12+j-1] = value
		
typelabelname=[]
print('typelabel=',typelabel)
for x in typelabel:
	if(x!=None):
		typelabelname.append(cataname(x))
	else:typenum = typenum

typelabelname.reverse()
print('typelabelname=',typelabelname)

month = [1,2,3,4,5,6,7,8,9,10,11,12]
y = y.reshape((typenum,12))							#x,y size
df = pd.DataFrame(y,columns=[x for x in range(1,13)],index = typelabelname)

sns.heatmap(df,annot=True,cmap = 'Reds')
plt.title('heat map')
plt.xlabel('month')
plt.show()


#####	
print('published at:',videomonth)
print('type:',videotype)
#####


person = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for a in video_ids:
	b = video_type(a)
	if(b!=None):
		person[b]=person[b]+1


#plot type graph

slices = []
activities = []
for i in range (0,30):
	if (person[i]):
		slices.append(person[i])
		activities.append(cataname(i))
		print('category:',end='')
		print(i,end='	')
		print('num:',end='')
		print(person[i])









cols = ['c','m','r','b','g','c','gold','darkviolet']            #颜色

plt.pie(slices,
        labels=activities,
        colors=cols,
        startangle=90,
        shadow= True,
        autopct='%1.1f%%')

plt.title('interested videos')
plt.show()






