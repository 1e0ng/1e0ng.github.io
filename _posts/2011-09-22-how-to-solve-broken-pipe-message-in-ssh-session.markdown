---
comments: true
date: 2011-09-22 20:55:47
layout: post
slug: how-to-solve-broken-pipe-message-in-ssh-session
title: How to Solve Broken Pipe Message in SSH Session
wordpress_id: 757
categories:
- Network
tags:
- Broken Pipe
- SSH
---

Sometimes my SSH session disconnects with a Write failed: Broken pipe message. What does it mean? And how can I keep my session open?

It's possible that your server closes connections that are idle for too long. You can update either your client (ServerAliveInterval) or your server (ClientAliveInterval).
<!-- more -->

{% quote %}
ServerAliveInterval Sets a timeout interval in seconds after which if no data has been received from the server, ssh(1) will send a message through the encrypted channel to request a response from the server. The default is 0, indicating that these messages will not be sent to the server.
This option applies to protocol version 2 only.

ClientAliveInterval Sets a timeout interval in seconds after which if no data has been received from the client, sshd(8) will send a message through the encrypted channel to request a response from the client. The default is 0, indicating that these messages will not be sent to the client.
This option applies to protocol version 2 only.
{% endquote %}


To update your server (and restart your sshd)

``` bash    
$ echo "ClientAliveInterval 60" | sudo tee -a /etc/ssh/sshd_config
```

Or client-side:

``` bash    
$ echo "ServerAliveInterval 60" >> ~/.ssh/config
```


Although you have configured all the above parameters, sometimes the connection just breaks. To solve this problem, I wrote this shell script to automatically restart ssh as soon as it breaks down.

{% highlight bash linenos %}
#!/bin/sh

#This is an SSH-D proxy with auto-reconnect on disconnect

#Created by Leon on 28, Sep, 2011
#Email: i@leons.im

i=0
while test 1==1
do
    remote_ip=YOUR_REMOTE_IP
    remote_user=YOUR_REMOTE_USER
    local_port=YOUR_LOCAL_PORT

    exist=`ps aux | grep $remote_user@$remote_ip | grep $local_port`
    #echo $exist
    if test -n "$exist"
    then
        if test $i -eq 0
        then
            echo "I'm alive since $(date)"
        fi  
        i=1 
    else
        i=0 
        echo "I died... God is bringing me back..."
        ssh $remote_user@$remote_ip -f -N -D 0.0.0.0:$local_port
    fi  
    sleep 1
done
{% endhighlight %}

(Replace YOUR_REMOTE_USER and YOUR_REMOTE_IP with the username and ip address of your remote server correspondingly. Replace YOUR_LOCAL_PORT with the local port you want to listen on for proxy.)

If you want to connect to your remote machine via SSH without a password, go to [/2011/11/ssh-login-without-password/](/2011/11/ssh-login-without-password/)

### Update:
As John replies in the comments, you can also place this line in your ~/.ssh/config file `ServerAliveCountMax = 120` to make your SSH connection stays alive longer.
