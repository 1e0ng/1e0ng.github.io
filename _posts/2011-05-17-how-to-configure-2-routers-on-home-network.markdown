---
comments: true
date: 2011-05-17 08:51:49
layout: post
slug: how-to-configure-2-routers-on-home-network
title: How to Configure 2 Routers on Home Network
wordpress_id: 644
categories:
- Network
tags:
- 2 Routers
- Home Network
- Hub
---

You need to connect 4 computers to the internet. Now you have 2 routers, but each with 3 LAN ports. How would you solve this issue?

<!--more-->

[![](/uploads/2011-05-1router.jpg)](/uploads/2011-05-1router.jpg)

There are 2 methods to solve this problem.

* Use the second routers as a hub. This is easier, and you don't need to configure anything, just wiring them up.

  [![](/uploads/2011-05-2routers_1.jpg)](/uploads/2011-05-2routers_1.jpg)

* The second method is more sophistics. Look at the following picture. You need to configure a level-2 router. This means you need to set up a new local network on a local network, and these networks should be different. Then how to make them different? Consider the level-1 network (the first network) is 192.168.1.0, which means every computers connected with this router has an IP as 192.168.1.*. After you wiring up your 4th computer to the Router 2, you configure Router 2 through a web browser, and set the WAN IP as 192.168.1.10, (or 192.168.1.11, or 192.168.1.12... just make it different from the IPs of the first 3 computers, or you may choose DHCP to dynamically get an IP address.) Then set the LAN IP of Router 2 as 192.168.2.1. Then set the IP of your 4th computer as 192.168.2.2. It should work now.

  Note the level-1 local network is 192.168.1.0, while the level-2 local network is 192.168.2.0. So they are on different local networks.

  [![](/uploads/2011-05-2routers_2.jpg)](/uploads/2011-05-2routers_2.jpg)

