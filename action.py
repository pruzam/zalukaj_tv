#!/usr/bin/python
import cgi
import time
import os
import subprocess
import urllib2
import re
import os
import glob

def remove_movie(max=10):
    files = glob.glob('*.flv')
    md = (None, None)
    if len(files) > max:
        for f in files:
            if md[1] is None:
                md = (os.path.getmtime(f), f)
            else:
                md_ = os.path.getmtime(f)
                if md[0] > md_:
                    md = (md_, f)
        os.unlink(md[1])


get = cgi.FieldStorage()
img = get.getvalue('img')
url = get.getvalue('url')
action = get.getvalue('action')

pipe_path = '/tmp/omx.pipe'

if url is not None and not os.path.exists(url):
    response = urllib2.urlopen(url)
    html = response.read()

    m1 = re.search('player.php\?w=([A-Z0-9]+)&id=\d+', html)
    if m1:
        url2 = 'http://st.dwn.so/player/embed.php?v=%s&width=470&height=305' % m1.group(1)

        response = urllib2.urlopen(url2)
        html = response.read()

        m2 = re.search('http://st.dwn.so/player/play4.swf\?v=%s&yk=([a-z0-9]+)' % m1.group(1), html)
        if m2:
            url3 = 'http://st.dwn.so/xml/videolink.php?v=%s&yk=%s&width=1920&id=1390769276988&u=undefined' % (m1.group(1), m2.group(1))
        
            response = urllib2.urlopen(url3)
            html = response.read()

            m3 = re.search('s\d+.dwn.so/movie-stream,[a-z0-9]+,[a-z0-9]+,%s.flv,0' % m1.group(1), html)
 
            if m3:
                movie = 'http://%s' % m3.group(0)
                url = '%s.flv' % img

                remove_movie()
                subprocess.Popen("at now <<< 'wget %s --tries=100 -O %s'" % (movie, url), shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
                time.sleep(1)


if url is not None and os.path.exists(url):
    #kill all omxplayer prrocesses
    subprocess.Popen("ps -C omxplayer.bin -o pid=|xargs kill", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)

    if os.path.exists(pipe_path):
        os.unlink(pipe_path)

    os.mkfifo(pipe_path)

    subprocess.Popen("at now <<< 'omxplayer --video_queue 20 --audio_queue 5 -o hdmi %s < /tmp/omx.pipe'" % url, shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
    subprocess.Popen("echo -n . > /tmp/omx.pipe", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)

if action == 'pause':
    subprocess.Popen("if pids=$(pidof omxplayer.bin); then echo -n p > /tmp/omx.pipe; fi", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
if action == 'i_seek_600':
    subprocess.Popen("if pids=$(pidof omxplayer.bin); then echo -n $'\x1b\x5b\x41' > /tmp/omx.pipe; fi", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
if action == 'd_seek_600':
    subprocess.Popen("if pids=$(pidof omxplayer.bin); then echo -n $'\x1b\x5b\x42' > /tmp/omx.pipe; fi", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
if action == 'i_seek_30':
    subprocess.Popen("if pids=$(pidof omxplayer.bin); then echo -n $'\x1b\x5b\x43' > /tmp/omx.pipe; fi", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
if action == 'd_seek_30':
    subprocess.Popen("if pids=$(pidof omxplayer.bin); then echo -n $'\x1b\x5b\x44' > /tmp/omx.pipe; fi", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)

if action == 'stop' or (url is not None and not os.path.exists(url)):
    subprocess.Popen("if pids=$(pidof omxplayer.bin); then echo -n q > /tmp/omx.pipe; fi", shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)    
    print "Location: index.py\n\n";
else:
    print 'Content-Type: text/html\n\n'

    print '''<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, target-densityDpi=device-dpi">
</head>
<body>
<div style="text-align: center;font-size: 200%%">
<img style="width:150px;height:200px;" src="http://static.zalukaj.tv/image/%s.jpg" />
<br />
<a href="action.py?img=%s&action=d_seek_600"><<</a> |
<a href="action.py?img=%s&action=d_seek_30"><</a> |
<a href="action.py?img=%s&action=pause">PLAY/PAUSE</a> | 
<a href="action.py?img=%s&action=stop">STOP/EXIT</a> |
<a href="action.py?img=%s&action=i_seek_30">></a> |
<a href="action.py?img=%s&action=i_seek_600">>></a> 
</div>
</body>
</html>
''' % (img, img, img, img, img, img, img)
