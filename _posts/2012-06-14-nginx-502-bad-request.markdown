---
comments: true
date: 2012-06-14 14:12:21
layout: post
slug: nginx-502-bad-request
title: Nginx 502 Bad Request
wordpress_id: 968
categories:
- Web
---

I have got this error many times. Today, I dived into it and resolved it.

I use php-fpm and nginx on my server. Occasionally, I got 502 bad request error. When I check the nginx log, it says `upstream sent too big header`. In my memory, the default buffer size if big enough. To make sure it's not caused by this, I add the following lines to the nginx configuration file:
<!-- more --> 

```
proxy_buffers 16 16k;
proxy_buffer_size 32k;
```

But that makes no difference. Finally, I found the answer at the nginx forum: [http://forum.nginx.org/read.php?2,188352](http://forum.nginx.org/read.php?2,188352)

It's not caused by nginx, it's due to the fastcgi buffer. Simply add the following lines to nginx configuration file and the 502 error never happens again:

```
fastcgi_buffers 16 16k;
fastcgi_buffer_size 32k;
```

Some internet service providers add parameters to users' requests, and that make a very large header. I realized one of my friend told me he could access his website normally via 2G network but not via 3G network (also got a 502 error). Since I didn't have time to help him to resolve his issue that time, I just suggested him check the nginx configuration. I think it was probably caused by same reason.
