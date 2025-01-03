---
comments: true
date: 2011-03-31 15:40:01
layout: post
slug: netcat-file-transfers
title: 'Netcat File Transfers '
wordpress_id: 575
categories:
- Linux
---

In a very simple way it can be used to transfer files between two computers. You can create a server that serves the file with the following:

<!--more-->
{% highlight bash linenos %}
$ cat backup.iso | nc -l 3333
{% endhighlight %}

Receive backup.iso on the client machine with the following:

{% highlight bash linenos %}
$ nc 192.168.0.1 3333 > backup.iso
{% endhighlight %}

As you may have noticed, netcat does not show any info about the progress of the data transfer. This is inconvenient when dealing with large files. In such cases, a pipe-monitoring utility like [pv](http://www.ivarch.com/programs/pv.shtml) can be used to show a progress indicator. For example, the following shows the total amount of data that has been transfered in real-time on the server side:

```
$ cat backup.iso | pv -b | nc -l 3333
```

Of course, the same can be implemented on the client side by piping netcat’s output through pv:

```
$ nc 192.168.0.1 3333 | pv -b > backup.iso
```

------------------------------------------------------------------------------------------------------------------------------

Another way:

from: http://www.onlamp.com/pub/a/onlamp/2003/05/29/netcat.html

One of the most practical usages of this network connection is the file transfer. As a basic Netcat function, this feature may be used to great effect in the hands of an experienced user. For a freshly installed computer, setting up a ftp server or, worse, meddling with rcp or scp protocols may be nauseating. Those commands may not be available for one, and multiple layers of control mechanisms may interfere with their functionality. You can still transfer files with just one nc command.

At the server console:

```
$ nc -v -w 30 -p 5600 l- > filename.back
```

and on the client side:

```
$ nc -v -w 2 10.0.1.1 5600 < filename
```

Magically, the file named filename is transfered from the client to the server. You can check that they are identical.

The command line uses the new argument -w to cause Netcat to wait for a few seconds. We made that longer in the server side because it is most affected by a pause. Another important point is the > and < redirection commands, with which Unix users are very familiar.

In the server we said > filename.back. Any output will be directed to this file. As it happens, the output is the file filename which is send by the client. Think of this as a pipeline. We take a bucket (file), pour the contents to the pipeline (Netcat's port), and, at the other end we fill another bucket from the pipeline.


------

Update: Why bother to use `netcat` if ssh deamon is running? Just use `scp` to transfer files!
