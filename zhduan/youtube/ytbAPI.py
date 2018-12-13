from urllib import request
import json

CATEGORY = ['no such category'] * 50
CATEGORY[1] = 'Film & Animation'
CATEGORY[2] = 'Autos & Vehicles'
CATEGORY[10] = 'Music'
CATEGORY[15] = 'Pets & Animals'
CATEGORY[17] = 'Sports'
CATEGORY[18] = 'Short Movies'
CATEGORY[19] = 'Travel & Events'
CATEGORY[20] = 'Gaming'
CATEGORY[21] = 'Videoblogging'
CATEGORY[22] = 'People & Blogs'
CATEGORY[23] = 'Comedy'
CATEGORY[24] = 'Entertainment'
CATEGORY[25] = 'News & Politics'
CATEGORY[26] = 'How to & Style'
CATEGORY[27] = 'Education'
CATEGORY[28] = 'Science & Technology'
CATEGORY[29] = 'Nonprofits & Activism'
CATEGORY[30] = 'Movies'
CATEGORY[31] = 'Anime/Animation'
CATEGORY[32] = 'Action/Adventure'
CATEGORY[33] = 'Classics'
CATEGORY[34] = 'Comedy'
CATEGORY[35] = 'Documentary'
CATEGORY[36] = 'Drama'
CATEGORY[37] = 'Family'
CATEGORY[38] = 'Foreign'
CATEGORY[39] = 'Horror'
CATEGORY[40] = 'Sci-Fi/Fantasy'
CATEGORY[41] = 'Thriller'
CATEGORY[42] = 'Shorts'
CATEGORY[43] = 'Shows'
CATEGORY[44] = 'Trailers'

class ytbAPI(object):

    DATA_V3_BASE = 'https://www.googleapis.com/youtube/v3/'
    __API_KEY = "your google api key" # 

    def __init__(self):
        self.keyStr = '&key=' + self.__API_KEY
        self.url = self.DATA_V3_BASE

    def scope(self, scp):
        '''
        set the scope

        :param scp: str, name of scope
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

    def channelId(self, chid):
        '''
        :param chid: str, input channel id
        '''
        self.chidStr = '&channelId=' + chid
        self.url += self.chidStr

    def id(self, i):
        '''
        i: str, input id
        '''
        self.idStr = '&id=' + i
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
        :param m: str or int or float, the max number of results per page
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
    
    def set_q(self, kw):
        '''
        set the searching keyword q
        :param kw: str, search keyword
        '''
        self.q = '&q=' + kw.replace(' ', '+')
        self.url += self.q

    def safeSearch(self, s='none'):
        '''
        s: str, 'moderate', 'none', 'strict'
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
    
    def pageToken(self, pt):
        '''
        :param pt: str, next page token
        '''
        if 'pageToken' in self.url:
            self.url = self.url.replace(self.pageStr, '')
        self.pageStr = '&pageToken=' + pt
        self.url += self.pageStr

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
        try:
            req = request.Request(self.url)
            page = request.urlopen(req).read()
            page = page.decode('utf-8')
            return json.loads(page)
        except Exception as e:
            return {'error': {'message': e} }
