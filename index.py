#!/usr/bin/python
import urllib2
import re
import cgi
import os

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

tmp = []
for e in set(re.findall('<div class="rmk23m4">.+?<div style=".*?">(.+?)&nbsp;<a href="(/zalukaj-film/(\d+)/.+?html)">.+?</a></div>', html, re.M | re.S )):
    tmp_ = 'http://zalukaj.tv%s' % e[1]
    if os.path.exists('%s.flv' % e[2]):
        tmp_ = '%s.flv' % e[2]
    tmp.append('<div style="clear:both;"><div style="float:left;width:150px;margin-right:-150px;"><a href="action.py?img=%s&url=%s"><img style="width:150px;height:200px;" src="http://static.zalukaj.tv/image/%s.jpg" /></a><br /></div><div style="float:left;margin-left:160px">%s</div></div><div style="clear:both;margin-top:10px">&nbsp;</div>' % (e[2], tmp_, e[2], e[0]))

tmp2 = []
for e in set(re.findall('<td class="wef32f"><a href=".*gatunek/(\d+)">(.+)</a></td>', html)):
    tmp2.append('<a href="index.py?type=%s&page=1">%s</a>' % (e[0], e[1]))

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
%s
<br />
<br />
%s
</div>
</body>
</html> """ % (' | '.join(tmp2), c, ''.join(tmp))
