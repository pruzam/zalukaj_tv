#!/usr/bin/python
import cgi
import time
import os
import subprocess
import urllib2
import re
import glob

get = cgi.FieldStorage()
url1 = get.getvalue('url')
name = get.getvalue('name')

files = glob.glob('*.flv')
md = (None, None)
if len(files) > 5:
    for f in files:
        if md[1] is None:
            md = (os.path.getmtime(f), f)
        else:
            md_ = os.path.getmtime(f)
            if md[0] > md_:
                md = (md_, f) 
    os.unlink(md[1])    


if url1 is not None:
    movie = None

    response = urllib2.urlopen(url1)
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

                if movie is None:
                    with file('error.txt', 'w') as f:
                        f.write(html)

                subprocess.Popen("at now <<< 'wget %s --tries=100 -O /media/NASDRIVE/www/%s.flv'" % (movie, name), shell=True, executable='/bin/bash', stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)

print "Location: index.py\n\n"
