---
comments: true
date: 2011-11-26 23:41:37
layout: post
slug: ssh-login-without-password
title: SSH login without password
wordpress_id: 875
categories:
- Linux
tags:
- Password
- SSH
---

Why must login without password? Because it saves time and automizes tasks.
<!--more-->

## How to do it

First log in on A as user a and generate a pair of authentication keys. Do not enter a passphrase: 
    
{% highlight bash linenos %}
a@A:~> ssh-keygen -t rsa
---------------------------------------------------------
Generating public/private rsa key pair.
Enter file in which to save the key (/home/a/.ssh/id_rsa): 
Created directory '/home/a/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/a/.ssh/id_rsa.
Your public key has been saved in /home/a/.ssh/id_rsa.pub.
The key fingerprint is:
3e:4f:05:79:3a:9f:96:7c:3b:ad:e9:58:37:bc:37:e4 a@A
{% endhighlight %}

Now use ssh to create a directory ~/.ssh as user b on B. (The directory may already exist, which is fine):

``` bash    
a@A:~> ssh b@B mkdir -p .ssh
b@B's password: 
```

Finally append a's new public key to b@B:.ssh/authorized_keys and enter b's password one last time:
    
{% highlight bash linenos %}
a@A:~> cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
b@B's password: 
{% endhighlight %}

From now on you can log into B as b from A as a without password:

{% highlight bash linenos %}
a@A:~> ssh b@B hostname
B
{% endhighlight %}

## If error happens

{% highlight bash linenos %}
Change the permissions of .ssh to 700
Change the permissions of .ssh/authorized_keys to 600
{% endhighlight %}
