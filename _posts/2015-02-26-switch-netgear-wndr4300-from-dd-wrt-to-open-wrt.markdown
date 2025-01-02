---
layout: post
title: "Switch Netgear WNDR4300 from DD-WRT to Open-WRT"
date: 2015-02-26 00:57:58 +0800
comments: true
categories: articles
tags:
- Network
---

DD-WRT is a really nice way to free your router. It has a polished web interface, gives you far greater control than most proprietary firmware, and is supported on a large number of devices. However, Open-WRT is better! In my installed version of DD-WRT, ssh doesn't work, and I can not install an external driver like rtl8187 for my Alfa AWUS036H. After seaching Google for some time, I realise that I need to change the operating system, even though installing DD-WRT cost me several hours.

<!--more-->

## Why Open-WRT

Compared to DD-WRT, it provides more options to users or developers, so that we can customize it in a way we prefer. We can install packages, or even build customized version of firmware. I find a hope to combine Netgear WNDR4300 router with Alfa AWUS036H. In addition, I can install some cool packages to break the so-called Great Firewa11.

## How to Install Open-WRT

Thanks to the Open-WRT forum and wiki, which is much better than those of DD-WRT, the installation may take less than 5 minutes. (According to [Switch from DD-WRT to OpenWrt in under 30 minutes](https://samhobbs.co.uk/2013/11/switch-from-dd-wrt-to-openwrt-in-under-30-minutes), it costs less than 30 minutes, but actually it wastes time by restoring to the original stock firmware.)


For this article, I will use my router Netgear WNDR4300 as an example.

### Download Open-WRT Image

According to <http://wiki.openwrt.org/toh/netgear/wndr4300>, this router supports Barrier Breaker 14.07 RC1. By reading the release note of 14.07 RC2 to RC4, I think the most recent version of Open-WRT should work.

There seems less information for WNDR4300v1, but it's similar to WNDR3700v4 but 3T3R, so why not read <http://wiki.openwrt.org/toh/netgear/wndr3700>?

Then we find the right version of image to download: <http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/nand/openwrt-ar71xx-nand-wndr4300-ubi-factory.img>

### Install by TFTP

Set computer network to static IP: 192.168.1.5 with gateway and router 192.168.1.1

Power off the router, wait 30s, and keep pressing reset button, power on, release reset button until power led turns green.


{% highlight bash linenos %}
cd ~/Downloads/

tftp -e 192.168.1.1
mode binary
put openwrt-ar71xx-nand-wndr4300-ubi-factory.img
quit
{% endhighlight %}

Wait until the power led changes to green.

Done. Open <http://192.168.1.1> to configure.

## 5G radio

Wait the 5G radio not working?

Here is the solution.

{%quote%}

Sometimes the 5G wifi interface (a separate AR9580 chip attached on PCIe) will completely disappear, because the PCIE_RC strap bit gets stuck at '0'. This can be checked by running "devmem 0x180600b0" and looking at bit 6:

- GOOD: 0x002F055A
- BAD: 0x002F051A

On OpenWRT this causes the kernel to completely ignore the PCIe interface and everything attached to it, so only the onchip 2.4GHz radio will work. On the original firmware it may cause the unit to get stuck in a reboot loop.

If this happens, just power the unit off for about 30 seconds. In fact it might be a good idea to power cycle the unit before OpenWRT's initial boot. See this thread for more information.

{%endquote%}

## Security is Important

To automatical encryption for a foregin IP while accessing domestic IP directly, just install some packages and do some configuration. Search Shadowsocks for Open-WRT and ChianDNS. There is a perfect solution there.

## SSH

Of course it works. To prove it wroks:

```
leon@ls-mbp$  ssh root@10.0.1.1


BusyBox v1.22.1 (2014-09-20 22:31:09 CEST) built-in shell (ash)
Enter 'help' for a list of built-in commands.

  _______                     ________        __
 |       |.-----.-----.-----.|  |  |  |.----.|  |_
 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
 |_______||   __|_____|__|__||________||__|  |____|
          |__| W I R E L E S S   F R E E D O M
 -----------------------------------------------------
 BARRIER BREAKER (14.07, r42625)
 -----------------------------------------------------
  * 1/2 oz Galliano         Pour all ingredients into
  * 4 oz cold Coffee        an irish coffee mug filled
  * 1 1/2 oz Dark Rum       with crushed ice. Stir.
  * 2 tsp. Creme de Cacao
 -----------------------------------------------------
```



## What about rtl8187

Well, it's too late tonight, I will get it work some day, surely.

