#encoding:utf-8
import re
import os
import sys

def trans(f):
    s = open(f).read().decode('utf-8')
    tbodys = re.findall(ur'<TABLE cellSpacing=8 width="100%">\s*<tbody>([\s\S]*?)</tbody>', s, re.I|re.M)

    assert len(tbodys) == 1
    body = tbodys[0]
    tds = re.findall(ur'<td[^>]*>([\s\S]*?)</td>', body, re.I|re.M)
    assert len(tds) == 1
    td = tds[0]
    td = re.sub(ur'<br>', '</p><p>', td, flags=re.I|re.M)
    td = re.sub(u'\r', '\n', td, flags=re.I|re.M)
    td = re.sub(ur'[【】]', '', td, flags=re.I|re.M)
    td = re.sub(ur'&nbsp;', ' ', td, flags=re.I|re.M)

    lines = re.findall(ur'<p>([\s\S]*?)</p>', td, re.I|re.M)
    lines = [l.strip() for l in lines]
    lines = filter(lambda x:x, lines)

    headline = lines[0]
    lines = lines[1:]
    path = f[:-4]
    #if not os.path.exists(path):
    #    os.makedirs(path)
    o = open(path + '.markdown', 'w')
    o.write('''---
layout: page
title: "%s"
date: 2015-01-10 14:47
comments: true
sharing: true
footer: true
---
''' % headline.encode('utf-8'))
    for l in lines:
        l = re.sub(ur'∷(.*)', ur'\n### \1', l)
        l += '\n\n'
        o.write(l.encode('utf-8'))

    o.write('\n[Back](./)\n')
    o.close()

file_pattern = ur'.*\.htm'
path = os.path.abspath(os.path.dirname(sys.argv[0]))
print "Current Path: " + path
errors = []
for dirpath, dirs, files in os.walk(path):
    for filename in files:
        if re.search(file_pattern, filename) and filename != __file__:
            print filename + ' ... '
            trans(filename)
