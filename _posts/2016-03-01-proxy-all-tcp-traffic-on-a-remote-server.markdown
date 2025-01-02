---
layout: post
title: "Proxy All TCP Traffic On a Remote Server"
date: 2016-03-01 10:39:09 +0800
comments: true
categories: articles
tags:
- Server
- Operation
- Linux
---

Even though SOCKS is a higher level protocol and more appropriate for doing proxy thing, there are no easy solution for building a global proxy for a Linux server except doing that on a router. For a remote server, normally a cloud server, it's not always convenient to access the router. So after several tries, I decide drop the SOCKS solution, and simply use Linux's `iptables`.

The easiest way I find from my recent research is with [shadowsocks-libev](https://github.com/shadowsocks/shadowsocks-libev). Shadowsocks-libev is a lightweight secured SOCKS5 proxy for embedded devices and low-end boxes. Shadowsocks-libev is written in pure C and only depends on libev and OpenSSL or PolarSSL. The use of mbedTLS is added but still for testing, and it is not officially supported yet.

<!-- more -->

Note the original shadowsocks doesn't support `ss-redir`, and `shadowsocks-libev` seems to be the only port that supports `ss-redir`. `ss-redir` is different from `ss-local` in that it's TCP protocol rather than SOCKS protocol.

### Install shadsocks-libev on Linux

```
git clone https://github.com/leonsim/shadowsocks-libev.git
cd shadowsocks-libev
./configure && make
sudo make install
```

### Create iptables rules

```
# Create new chain
iptables -t nat -N SHADOWSOCKS
iptables -t mangle -N SHADOWSOCKS

# Ignore your shadowsocks server's addresses
# It's very IMPORTANT, just be careful.
# Note 123.123.123.123 is the same as the remote server in /etc/config/shadowsocks.json
iptables -t nat -A SHADOWSOCKS -d 123.123.123.123 -j RETURN

# Ignore LANs and any other addresses you'd like to bypass the proxy
# See Wikipedia and RFC5735 for full list of reserved networks.
# See ashi009/bestroutetb for a highly optimized CHN route list.
iptables -t nat -A SHADOWSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 169.254.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 192.168.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 224.0.0.0/4 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 240.0.0.0/4 -j RETURN

# Anything else should be redirected to shadowsocks's local port
iptables -t nat -A SHADOWSOCKS -p tcp -j REDIRECT --to-ports 12345

# Add any UDP rules
ip rule add fwmark 0x01/0x01 table 100
ip route add local 0.0.0.0/0 dev lo table 100
iptables -t mangle -A SHADOWSOCKS -p udp --dport 53 -j TPROXY --on-port 12345 --tproxy-mark 0x01/0x01

# Apply the rules
iptables -t nat -A PREROUTING -p tcp -j SHADOWSOCKS
iptables -t mangle -A PREROUTING -j SHADOWSOCKS

# Start the shadowsocks-redir
ss-redir -u -c /etc/config/shadowsocks.json -f /var/run/shadowsocks.pid
```

If the UDP deosn't work, just not use the UDP part, aka only use the TCP part.

### Security Tips

Although shadowsocks-libev can handle thousands of concurrent connections nicely, we still recommend setting up your server's firewall rules to limit connections from each user:

```
# Up to 32 connections are enough for normal usage
iptables -A INPUT -p tcp --syn --dport ${SHADOWSOCKS_PORT} -m connlimit --connlimit-above 32 -j REJECT --reject-with tcp-reset
```
