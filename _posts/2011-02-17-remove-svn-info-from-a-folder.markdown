---
comments: true
date: 2011-02-17 10:09:02
layout: post
slug: remove-svn-info-from-a-folder
title: Remove SVN info from a folder
wordpress_id: 143
categories: articles
tags:
- Script
tags:
- Info
- Python
- Remove
- SVN
---

{% highlight bash linenos %}
find . -name .svn -exec rm -rf {} ;
{% endhighlight %}
