---
comments: true
date: 2011-08-08 09:47:53
layout: post
slug: configure-network-using-ifconfig-and-route
title: Configure Network Using ifconfig and route
wordpress_id: 698
categories: articles
tags:
- Linux
tags:
- gateway
- ifconfig
- IP
- nameserver
- network
- route
---

Setting up your network consists of three steps.  First we assign ourselves an IP address using ifconfig. Then we set up routing to the gateway using route. Then we finish up by placing the nameserver IPs in /etc/resolv.conf.

<!--more-->
### 1

To assign an IP address, you will need your IP address, broadcast address and netmask. Then execute the following command, substituting ${IP_ADDR} with your IP address, ${BROADCAST} with your broadcast address and ${NETMASK} with your netmask:

{% highlight bash linenos %}
# ifconfig eth0 ${IP_ADDR} broadcast ${BROADCAST} netmask ${NETMASK} up
{% endhighlight %}

### 2

Now set up routing using route. Substitute ${GATEWAY} with your gateway IP address:

{% highlight bash linenos %}
# route add default gw ${GATEWAY}
{% endhighlight %}

### 3

Now open /etc/resolv.conf with your favorite editor (in our example, we use nano):

{% highlight bash linenos %}
# nano -w /etc/resolv.conf
{% endhighlight %}

Now fill in your nameserver(s) using the following as a template. Make sure you substitute ${NAMESERVER1} and ${NAMESERVER2} with the appropriate nameserver addresses:

```
nameserver ${NAMESERVER1}
nameserver ${NAMESERVER2}
```
