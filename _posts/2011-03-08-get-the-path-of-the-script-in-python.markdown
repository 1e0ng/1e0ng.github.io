---
comments: true
date: 2011-03-08 17:33:39
layout: post
slug: get-the-path-of-the-script-in-python
title: Get The Absolute Path Of The Current Script
wordpress_id: 453
categories:
- Python
tags:
- Path
- Python
- Script
---

There are a lot of methods to get the path of a script in Python, but the following method always work, even you use py2exe or PyInstaller to compile the script to binary executable file.

<!--more-->

{% highlight python linenos %}
import sys, os

print 'sys.argv[0] =', sys.argv[0]            
pathname = os.path.dirname(sys.argv[0])        
print 'path =', pathname
print 'full path =', os.path.abspath(pathname)
{% endhighlight %}

Note there is a big difference between the path of the script and the current path, ie the "." path in Windows and POSIX systems.
When you run the script from other folder, such like this:

{% highlight bash linenos %}
$python bin/myscript.py
{% endhighlight %}

Then the current folder is /home/leon/, while the path of the script is /home/leon/bin.
