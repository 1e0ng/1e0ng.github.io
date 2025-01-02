---
layout: post
title: "Mod Supermicro Motherboard BIOS to Support NVME"
date: 2020-08-06 21:03:25 +0800
comments: true
categories:
- BIOS
---

Sometimes when we think something is too hard to begin, the only reason is that we don't understand it. With a little determination, we can archive something that we could never believe we were able to.


I kept telling myself not to modify/re-program BIOS/UEFI for a long time. Why? I thought the stability of a motherboard is super important. If I did, could it break it? Besides, if the power gets shut down while flashing a new version of BIOS, I could permanently lose a motherboard. Do I have to buy a UPS before that? I'm not that rich to buy UPS without considering the cost. If you would like to sponsor one, please let me know.


These days, I'm playing some Supermicro motherboards. One of the most important reasons I like Supermicro is IPMI/BMC. With IPMI, I don't need to physically connect my monitor to the machine anymore. I can do anything, install a new operating system for the computer, change BIOS settings, or even upgrade the BIOS version remotely.


IPMI gives me confidence that I can play with BIOS now. Even if I flash with a corrupt BIOS file, then I can flash it back.  So there is nothing to worry about.

<!-- more -->

Now the only thing left is maybe a fuse, and now it comes today. I bought a [X9SCA-F](https://www.supermicro.com/products/motherboard/Xeon/C202_C204/X9SCA-F.cfm) for building my home NAS, a 10Gigabit NAS.


```
Motherboard: X9SCA-F
CPU: Xeon E3 1220 V2
RAM: 2x 8GB unbuffered ECC DIMM
SSD: 2x Samsung 970 Evo Plus NVME M.2 1TB
Network card: Mellanox dual 10Gb ConnectX-3
```

Looks good, right? The only problem is X9SCA-F doesn't support NVME M.2 because it's quite an old product from 2013, and now it's 2020, 7 years passed.


After doing some research, I find it's possible to MOD the motherboard BIOS to support NVME!


What I did is just following this post: <https://www.win-raid.com/t871f50-Guide-How-to-get-full-NVMe-support-for-all-Systems-with-an-AMI-UEFI-BIOS.html> and it's quite straight forward. With a tool called UEFITool (from CodeRush), I Mod a BIOS in about 15 minutes. Of course, I need to install Windows in VirtualBox beforehand.


Now I have an X9SCA-F motherboard with NVME support. Isn't that amazing?


Update: It turns out the X9SCA-F motherboard has a limit of 5Gbps bandwidth for its PCIE ports, so it's not possible to reach my goal of home NAS, ie 10Gb or even 20Gb. With that, I decide to upgrade my motherboard with a X10SLM+-F/X10SLL+-F or X10SRi-F/X10SRL-F/X10SRH-CF/X10SRH-CLN4F.

