#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
import cgi
import os
import unicodedata
import glob
import time

from bs4 import BeautifulSoup

get = cgi.FieldStorage()
type = get.getvalue('type')
page = get.getvalue('page')

c = ''

if page is None:
    url = 'http://zalukaj.tv/'
else:
    page = int(page)
    url = 'http://zalukaj.tv/gatunek,%s/ostatnio-dodane,wszystkie,strona-%s' % (type, page)
    
    c += '<br /><br />'
    if page > 1:
        c += '<a href="index.py?type=%s&page=%s"><--</a> | <a href="index.py?type=%s&page=%s">--></a>' % (type, page-1, type, page+1)
    else:
        c += '<a href="index.py?type=%s&page=%s">--></a>' % (type, page+1)

response = urllib2.urlopen(url)
html = response.read()

movie_id = re.compile('http://zalukaj.tv/zalukaj-film/(\d+)/.+')
tmp = []

movies = re.compile('<div class="rmk23m4">.+?<a href="(.+?/(\d+)/.+?)" title="(.+?)">.+?<div style="min-height:110px;font-size:10px;">(.+?)&nbsp;', re.M | re.S)

for m in movies.findall(html):
    tmp_ = m[0]
    i = m[1]
    if os.path.exists('%s.flv' % i):
        tmp_ = '%s.flv' % i
    t = m[2]
    d = m[3]
    tmp.append('<div style="clear:both;"><div style="float:left;width:150px;margin-right:-150px;"><a href="action.py?img=%s&url=%s"><img style="width:150px;height:200px;" src="http://static.zalukaj.tv/image/%s.jpg" /></a><br /></div><div style="float:left;margin-left:160px">%s<br />%s</div></div><div style="clear:both;margin-top:10px">&nbsp;</div>' % (i, tmp_, i, t, d))

tmp2 = []
for e in set(re.findall('<td class="wef32f"><a href=".*gatunek/(\d+)">(.+)</a></td>', html)):
    tmp2.append('<a href="index.py?type=%s&page=1">%s</a>' % (e[0], e[1]))

tmp3 = []
files = glob.glob('*.flv')
t = time.time()
for f in files:
    tmp3.append([os.path.getmtime(f), f])

tmp4 = []
for f in [e[1] for e in sorted(tmp3)]:
    if t - os.path.getmtime(f) > 30:
        tmp4.append('<a href="action.py?img=%s&url=%s"><img style="width:150px;height:200px;" src="http://static.zalukaj.tv/image/%s.jpg" /></a>' % (f[:-4], f, f[:-4]))
    else:
        tmp4.append('<img style="width:150px;height:200px;" src="http://static.zalukaj.tv/image/%s.jpg" />' % (f[:-4]))

print 'Content-Type: text/html\n\n'

print """
<html>
<head>
  <Title>Hello in HTML</Title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, target-densityDpi=device-dpi">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<div style="text-align: center;font-size:200%%;">
%s
<hr>
%s
%s
<br />
<br />
%s
</div>
</body>
</html> """ % (''.join(tmp4), ' | '.join(tmp2), c, ''.join(tmp))
