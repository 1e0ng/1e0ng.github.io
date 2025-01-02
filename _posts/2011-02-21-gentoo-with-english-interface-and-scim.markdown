---
comments: true
date: 2011-02-21 10:55:30
layout: post
slug: gentoo-with-english-interface-and-scim
title: Configuring Gentoo with English interface and SCIM
wordpress_id: 259
categories: articles
tags:
- Linux
post_format:
- Gallery
tags:
- Chinese
- English
- Gentoo
- Input Method
- SCIM
---

To install SCIM, follow the following steps:

<!--more-->

```
1. #emerge arphicfonts
2. #emerge scim scim-pinyin
3. $nano ~/.xinitc
```



Add these lines to the .xinitc file:  

{% highlight bash linenos %}
export XMODIFIERS=@im=SCIM  
export GTK_IM_MODULE=scim  
export QT_IM_MODULE=scim  
/usr/bin/scim -d
{% endhighlight %}

As a result, the .xinitc file may look like this:  

{% highlight bash linenos %}
export XDG_MENU_PREFIX=gnome-  
export XMODIFIERS=@im=SCIM  
export GTK_IM_MODULE=scim  
export QT_IM_MODULE=scim  
/usr/bin/scim -d  
exec gnome-session
{% endhighlight %}

If your SCIM can startup, but it can't switch to pinyin engine, you can add a line to the .xinitc file:  

{% highlight bash linenos %}
export XDG_MENU_PREFIX=gnome-  
export LC_CTYPE=zh_CN.UTF-8  
export XMODIFIERS=@im=SCIM  
export GTK_IM_MODULE=scim  
export QT_IM_MODULE=scim  
/usr/bin/scim -d  
exec gnome-session
{% endhighlight %}

After these have been done, you need to restart gnome to make it work.
