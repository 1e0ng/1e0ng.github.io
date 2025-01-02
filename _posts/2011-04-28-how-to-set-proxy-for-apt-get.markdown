---
comments: true
date: 2011-04-28 11:15:46
layout: post
slug: how-to-set-proxy-for-apt-get
title: How To Set Proxy For apt-get
wordpress_id: 595
categories: articles
tags:
- Linux
---

Before running apt-get command, run the following command:

<!--more-->

``` bash    
$export http_proxy=http://<username>:<password>@<host>:<port>
```

The  and  are username and password corresponding to you proxy account. The  is the address of your proxy (either domain name or IP address). The  is the port your proxy service, for example, 80 or 8080.

You may use this command if you don't need a username and a password to access your proxy:

{% highlight bash linenos %}
$export http_proxy=http://<host>:<port>
{% endhighlight %}

You can use apt-get now.
