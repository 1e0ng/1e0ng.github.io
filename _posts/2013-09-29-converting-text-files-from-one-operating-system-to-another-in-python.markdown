---
layout: post
title: "Converting Text Files From One Operating System to Another in Python"
date: 2013-09-29 20:56
comments: true
categories: 
- Python

---

Linux and modern OS X Macs end their lines with the same character, the LF. To cut down on confusion, think of OS X Macs and Linux as being interchangeable. They are interchangeable in terms of the end-of-line character.
Whilse Microsoft Windows does things yet another way. Under Microsoft Windows, lines end with a combination of 2 characters -- a CR followed by a LF. Symbolically, this is represented as CRLF or carriage return, line feed.

There are issues when you cooperate with others using different operating systems. So I write two Python script to resolve this issue. They also deals with BOM in text files which is automatically added by Windows platforms.

<!--more-->
From Linux to Windows:

{% highlight python linenos %}
#encoding:utf-8
import os, re
for f in os.listdir('.'):
    if re.match(r'.*\.txt$', f):
        print f
        c = open(f).read()
        open(f+'1', 'w').write(re.sub(r'(?<!\r)\n', r'\r\n', c))
{% endhighlight %}

From Windows to Linux:

{% highlight python linenos %}
#encoding:utf-8
import os, re
for f in os.listdir('.'):
    if re.match(r'.*\.txt$', f):
        print f
        c = open(f).read()
        c = c[1:] if len(c) > 0 and ord(c[0]) == 0xfeff else c
        open(f, 'w').write(re.sub(r'\r', r'', c))
{% endhighlight %}

