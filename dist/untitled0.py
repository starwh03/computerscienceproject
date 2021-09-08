from pytube import YouTube, Playlist
import json
import sys
import os
import urllib.request
p = os.path.abspath('appdata')

def collect(yt, dir):

    code = yt.thumbnail_url

    urllib.request.urlretrieve(code, os.path.join(dir, yt.title + '.jpg'))

    out = yt.streams.filter(only_audio = True, 
    	file_extension = 'mp4').order_by('abr').desc().first().download(dir)

def list_update(code):

    link = 'https://www.youtube.com/playlist?list=' + code

    dir = os.path.join(p, code)
    list = Playlist(link)
    files = [os.path.splitext(filename)[0] for filename in os.listdir(dir)]

    for l in list:
        yt = YouTube(l)
        if yt.title not in files:
            collect(yt, dir)

def add_music(code):

    dir = os.path.join(p, 'all')
    link = 'https://www.youtube.com/watch?v=' + code

    yt = YouTube(link)
    collect(yt, os.path.join(p, 'all'))

query = sys.argv[1]

if query == 'addlist':
    code = sys.argv[2]

    list = os.listdir(p)

    if code not in list:
        os.mkdir(os.path.join(p, code))
    list_update(code)

elif query == 'addmusic':
    code = sys.argv[2]
    add_music(code)

elif query == 'update':

    with open(os.path.abspath('playlists.json'), 'r', encoding = 'utf-8') as f:
        dic = json.load(f)

    l = dic['dcodes']

    for code in l:
        list_update(code)

