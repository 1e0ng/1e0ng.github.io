---
comments: true
date: 2011-03-11 21:29:50
layout: post
slug: python-script-to-transform-all-files-to-utf-8-encoding
title: Transform All Files to UTF-8 encoding
wordpress_id: 443
categories:
- Python
tags:
- Encoding
- Python
- Transform
- UTF-8
---

### Update

This blog is obselete, please head forward to this [blog](/posts/transform-all-files-to-utf-8/).

<hr>

I'm tired of transform shift-jis encoding to UTF-8 encoding for each file in my project these days, so I want to write a script to automatically do this job for me. After searching the Internet, I find it's an easy job with the tool of Python.

Python, at least 2.6 version, has a library called codecs, and all we have to do is just using this library to read and write files in different encodings.

This code transforms all files, including files in sub-folders, from shift-jis encoding(or detected encodings) to UTF-8 encoding.
<!--more-->

Install chardet first.

{% highlight sh linenos %}
pip install chardet
{% endhighlight %}

Copy this script and put it in the folder you want to do transform and run it.

{% highlight python linenos %}
#!/usr/bin/python
import os
import re
import sys

import chardet

#Created by Leon on March, 5, 2011
#Translate all files in current folder to utf-8 encoding

file_pattern = r'^.*\.(h|m|mm|cpp|inl|def|txt|js|html?|c|py|css)$'
to_encoding = 'utf-8'

def transcode(file_name):
    # Backup
    bk_file = file_name + '.bk'
    fi = open(file_name)
    fo = open(bk_file, 'w')
    fo.write(fi.read())
    fo.close()
    fi.close()

    # Trans
    fin = open(bk_file)

    succeed = True
    try:
        data = fin.read()
        c = chardet.detect(data)
        if c is None or c['confidence'] < 0.618:
            raise Exception
        if c['encoding'] != to_encoding:
            if c['encoding'] in ('GB2312', 'GBK'):
                c['encoding'] = 'GB18030'
            print file_name + ': ' + c['encoding'] + ' ==> ' + to_encoding
            data = unicode(data, encoding=c['encoding']).encode(to_encoding)
            fout = open(file_name, 'w')
            fout.write(data)
            fout.close()
    except:
        succeed = False
        print file_name + '\'s encoding not known.'

    fin.close()

    os.remove(bk_file)
    return succeed

path = os.path.abspath(os.path.dirname(sys.argv[0]))
print "Current Path: " + path
errors = []
for dirpath, dirs, files in os.walk(path):
    for filename in files:
        if re.search(file_pattern, filename) and filename != __file__:
            print filename + ' ... '
            if not transcode(os.path.join(dirpath, filename)):
                errors.append(filename)
if errors:
    print "--------------------------------------------------------"
    print "These files got error:"
    for err in errors:
        print err
    print "--------------------------------------------------------"
else:
    print
    print "All files have been translated successfully."
print
print "Created for you by Leon on March, 5, 2011."
raw_input()
{% endhighlight %}

Actually this script can detect the encoding of files, and transform all files not in utf-8, like shift-jis, gbk, gb2312, asscii(trival) or cp936 etc to utf-8 encoding.

