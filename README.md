# YouTube channel analyzer
BU EC601 Project

# Web application
www.zhduan.com/youtube

# Our codes
Our whole project codes are in folder ```zhduan```. There are two ways you can reuse our codes.

1. Run our website on your own computer.
2. Use our YouTube API library.

# Run our website
We use [Django](https://www.djangoproject.com) as our server framework. You can try our website on your localhost simply by the following steps.

0. Make sure you have a python 3.x

1. Install [Django](https://www.djangoproject.com) and [Python Social Auth of Django](https://github.com/python-social-auth/social-app-django)
```bash
pip install Django
pip install social-auth-app-django
```
2. Download our codes, open terminal in ```/zhduan```, then
```bash
python manage.py runserver 0:80
or
python manage.py runserver
```
3. You are all set! Open your browser and enter ```localhost```(python manage.py runserver 0:80) or ```localhost:8000```(python manage.py runserver), then you should see a UI of the website.

4. Open ```/zhduan/youtube/ytbAPI.py```, enter your Google API Key at ```line 7```. For how to get a Google API Key, you can read the [official doc](https://cloud.google.com/docs/authentication/api-keys?hl=en&authuser=0&visit_id=1541530248023-3715642940710334230&rd=1), or create API key [here](https://console.cloud.google.com/apis/credentials).

5. Now you can access most functions of the website on your localhost, except ones need OAuth 2 (for how to use Google OAuth 2, please see our ```docs/Google OAuth 2.md```).

# Use our YouTube API library
If you just want to try our YouTube API instead of the whole project, take the following steps. (Make sure you have Python 3.x)

0. ```/zhduan/youtube/ytbAPI.py``` is a simple API to connect YouTube/Google. ```/zhduan/youtube/youtube_lib.py``` contains many functions which use ```ytbAPI.py``` to connect YouTube/Google. There are build-in comments in these files, and they are pretty ez to read.

1. Install urllib3
```bash
pip install urllib3
```

2. Download ```/zhduan/youtube/ytbAPI.py```. Put it in the same folder with your own codes. Enter your Google API Key at ```line 7```. For how to get a Google API Key, you can read the [official doc](https://cloud.google.com/docs/authentication/api-keys?hl=en&authuser=0&visit_id=1541530248023-3715642940710334230&rd=1), or create API key [here](https://console.cloud.google.com/apis/credentials).

3. Import our library
```Python
from .ytbAPI import ytbAPI
```

4. You are all set!

5. Here is an example of getting top 10 viewed video in YouTube in the history. There are more in ```youtube_lib.py```.
```python
from .ytbAPI import ytbAPI

ytb0 = ytbAPI()
ytb0.scope('search')
ytb0.part('snippet')
ytb0.maxResults(10)
ytb0.order('viewCount')
ytb0.type('video')
ytb0.key()
response = ytb0.GET()

for i in response['items']:
    print(i['snippet']['title'])
```
