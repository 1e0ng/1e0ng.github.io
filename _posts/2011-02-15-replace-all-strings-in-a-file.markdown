---
comments: false
date: 2011-02-15 11:52:27
layout: post
slug: replace-all-strings-in-a-file
title: Replace all strings in a file
wordpress_id: 20
categories: articles
tags:
- Python
post_format:
- Gallery
tags:
- File
- Python
- Replace
- String
---

Here is the script to replace all strings in a file.

<!--more-->
``` python Replace Strings In A File
#!/usr/bin/python
#Created by Leon
import os, glob, re
old = "oldfile"
new = "newfile"
fin1 = open(old)
fout = open(newfile, "w")
data = fin1.readlines()
for line in data:
    fout.write(line)
    m = re.search(r"some string", line)
    if m:
        print m.group(1)
        fout.write("some new strings")
fin1.close()
fout.close()
```


You can also use the sed command:


{% highlight bash linenos %}
sed -i .bk 's/OLD_STRING/NEW_STRING/g' FILE_NAME
{% endhighlight %}

As on some system, sed is at a very old version, and some useful characters cannot be recognized. In this case, you can use Perl as an alternative:

{% highlight bash linenos %}
perl -e '($_ = join "",<>) =~ s/OLD_STR/NEW_STR/g; print;' OLD_FILE > NEW_FILE
{% endhighlight %}
