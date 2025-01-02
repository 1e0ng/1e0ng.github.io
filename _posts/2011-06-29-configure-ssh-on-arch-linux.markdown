---
comments: true
date: 2011-06-29 10:36:06
layout: post
slug: configure-ssh-on-arch-linux
title: Configure SSH on Arch Linux
wordpress_id: 668
categories: articles
tags:
- Linux
tags:
- Arch
- Connection
- SSH
---

Just record this for possbile uses.

<!--more-->
Install sshd:

{% highlight bash linenos %}
$sudo pacman -Syu openssh
{% endhighlight %}

Start sshd:

{% highlight bash linenos %}
$sudo rc.d start sshd
{% endhighlight %}

and add "sshd" to your DAEMONS array in /etc/rc.conf

```
$sudo emacs /etc/rc.conf
----------------------------------
DAEMONS = (... sshd)
```

Everything should be OK, but if you met the following errors:

```
"connection refused"
```

or

```
"Server unexpectedly closed network connection"
```

Check if you start sshd successfully:

{% highlight bash linenos %}
$sudo rc.d list | grep sshd
{% endhighlight %}

You should see:

```
[STARTED][AUTO] sshd
```

otherwise, you didn't start sshd successfully, and you may need to

```
$sudo rc.d start sshd
```

and check if some errors appear and try to solve them.
If you started sshd successfully, but still can't use sshd service, try to restart sshd:

{% highlight bash linenos %}
$sudo rc.d restart sshd
{% endhighlight %}

If you have configured deny-host list, you should add sshd to the exception list:

```
$sudo emacs /etc/hosts.allow
-------------------
sshd: all
```
