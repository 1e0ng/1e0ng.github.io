---
comments: true
date: 2011-02-15 09:16:38
layout: post
slug: how-to-change-the-ip-address-of-the-svn-server
title: How to change the IP address of the SVN server in checked-out project?
wordpress_id: 17
categories: articles
tags:
- Skills
tags:
- Change
- Check Out
- IP
- SVN
---

{% highlight bash linenos %}
find . -name entries | xargs perl -pi -e 's/OLD_IP/NEW_IP/'
{% endhighlight %}
