from __future__ import unicode_literals
import youtube_dl
import os

#from urllib.parse import urlparse
#import re
from urlparse import urlparse
import re


from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')




class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


# https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278 

ydl_opts = {
    'noplaylist' : True,
    'progress_hooks': [my_hook],
    'format': 'bestaudio/best',
    # On windows should be commented 
    # On Linux works 
    # 'postprocessors': [{
    #    'key': 'FFmpegExtractAudio',
    #    'preferredcodec': 'mp3',
    #    'preferredquality': '192',
    #}],
    'logger': MyLogger(),
    'outtmpl': os.path.join(app.config['DOWNLOAD_FILES'] , '%(title)s-%(id)s.%(ext)s')
}



# https://pymotw.com/2/urlparse/

def validate_url(url):
    """

    print( 'scheme  :', parsed.scheme)
    print( 'netloc  :', parsed.netloc)
    print( 'path    :', parsed.path)
    print( 'params  :', parsed.params)
    print( 'query   :', parsed.query)
    print( 'fragment:', parsed.fragment)
    print( 'username:', parsed.username)
    print( 'password:', parsed.password)
    print( 'hostname:', parsed.hostname, '(netloc in lower case)')
    print( 'port    :', parsed.port)

    parsed = urlparse('https://www.youtube.com/watch?v=f_1ptfcb4zo')
    parseresult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=f_1ptfcb4zo', fragment='')
    print(parsed)
    """
    parsed = urlparse(url)

    if "freesound.org" in parsed.netloc:
        return True
    return False



def ytdl(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])
        if result is None:
            return False
        else:
            return True

