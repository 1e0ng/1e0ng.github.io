---
comments: true
date: 2011-06-28 20:35:14
layout: post
slug: set-up-a-server-environment-on-arch
title: Set Up a Server Environment on Arch
wordpress_id: 664
categories:
- Linux
tags:
- Arch
- Mongodb
- Nginx
- PHP
- Server
---

This article is about how to set up a PHP production environment on Arch system.

<!--more-->

### First, install php:

{% highlight bash linenos %}
$sudo pacman –Syu php php-fpm php-memcache php-memcached php-pear php-curl
{% endhighlight %}

Configure php:

```
$sudo emacs /etc/php/php.ini
--------------------------------------------------
open_basedir = /srv/http:/:/home/:/tmp/:/Something else/
...
extension=curl.so
extension=json.so
extension=mysql.so
extension=zip.so
extension=memcache.so
extension=memcached.so
extension=mongo.so
...
date.timezone = Asia/Shanghai
```

### Second, install mongodb and mysql:


<!--more-->

{% highlight bash linenos %}
$sudo pacman –Syu mongodb mysql
$sudo pecl install mongo
{% endhighlight %}

Reset mysql password:

{% highlight bash linenos %}
$mysqladmin -u root -p password 'NEW_PASSWORD'
{% endhighlight %}

Start mongodb:

{% highlight bash linenos %}
$sudo rc.d start mongodb
{% endhighlight %}

Start mysqld:

{% highlight bash linenos %}
$sudo rc.d start mysqld
{% endhighlight %}

Add mongodb to auto-start list on boot:

{% highlight bash linenos %}
$sudo emacs /etc/rc.conf
{% endhighlight %}

and add mongodb and mysqld to the DAEMONS variable:

DAEMONS=(syslog-ng network ... mongodb mysqld)

### Third, install nginx:

{% highlight bash linenos %}
$sudo pacman –Syu nginx
{% endhighlight %}

Configure nginx:

{% highlight bash linenos %}
$sudo emacs /etc/nginx/conf/nginx.conf
{% endhighlight %}

Start nginx:

{% highlight bash linenos %}
$sudo rc.d start nginx
{% endhighlight %}

and add nginxto auto-start list:

```
$sudo emacs /etc/rc.conf
---------------------------------------------------
DAEMONS=(syslog-ng network ... nginx)
```

Configure php-fpm:

```
$sudo emacs /etc/php/php-fpm.conf
----------------------------------------------------
listen = 127.0.0.1:9000
;listen = /var/run/php-fpm/php-fpm.sock
```

Start php-fpm:

{% highlight bash linenos %}
$sudo rc.d start php-fpm
{% endhighlight %}

To add php-fpm to auto-start list:

```
$sudo emacs /etc/rc.conf
---------------------------------------------------
DAEMONS=(syslog-ng network ... php-fpm)
```

### Then, install some others:

{% highlight bash linenos %}
$sudo pacman –Syu memcached mercurial autoconf
{% endhighlight %}

Start memcached:

{% highlight bash linenos %}
$sudo rc.d start memcached
{% endhighlight %}

and add memcached to auto-start list:

```
$sudo emacs /etc/rc.conf
------------------------------------------
DAEMONS=(syslog-ng network ... memcached)
```

You can add some memcache:

```
$sudo emacs /etc/rc.local
------------------------------
/usr/bin/memcached -d -m 256 -p 11211 -u nobody -l 127.0.0.1
/usr/bin/memcached -d -m 64 -p 11220 -u nobody -l 127.0.0.1
/usr/bin/memcached -d -m 1024 -p 11300 -u nobody -l 127.0.0.1
```
