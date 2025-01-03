---
comments: true
date: 2012-02-20 22:33:21
layout: post
slug: python-code-for-counting-loclines-of-code
title: Python Code For Counting LOC(Lines Of Code)
wordpress_id: 922
categories:
- Python
- Tools
tags:
- LOC
- Python
---

Before I know CLOC, SourceCounter or Ohcount, I write this script. 

<!--more-->

{% highlight python linenos %}

# Created by Leon <i@leons.im> in 2012
# This code is for Python 2.x

import os, sys 

exts = ['.py', '.ini', '.c', '.h']
count_empty_line = True
here = os.path.abspath(os.path.dirname(sys.argv[0]))

def read_line_count(fname):
    count = 0 
    for line in open(fname).readlines():
        if count_empty_line or len(line.strip()) > 0:
            count += 1
    return count
if __name__ == '__main__':
    line_count = 0 
    file_count = 0 
    for base, dirs, files in os.walk(here):
        for file in files:
            # Check the sub directorys            
            if file.find('.') < 0:
                continue
            ext = (file[file.rindex('.'):]).lower()
            try:
                if exts.index(ext) >= 0:
                    file_count += 1
                    path = (base + '/'+ file)
                    c = read_line_count(path)
                    print ".%s : %d" % (path[len(here):], c)
                    line_count += c
            except:
                pass
    print 'File count : %d' % file_count
    print 'Line count : %d' % line_count
{% endhighlight %}





Copy and save the script as analytics.py and modify the `exts` list to include all the file extensions in your project, and put this script in your source code folder, then run:



    
    python analytics.py
