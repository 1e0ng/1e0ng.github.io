---
comments: true
date: 2011-02-17 10:20:03
layout: post
slug: foce-the-mail-app-to-use-utf-8-encoding-on-macintosh
title: Force the Mail.app to use UTF-8 encoding on Macintosh
wordpress_id: 145
categories:
- Mac OS
post_format:
- Gallery
tags:
- Encoding
- Macintosh
- Mail
- UTF-8
---

Open a terminal, and run the following command:

{% highlight bash linenos %}
defaults write com.apple.mail NSPreferredMailCharset "UTF-8"
{% endhighlight %}
