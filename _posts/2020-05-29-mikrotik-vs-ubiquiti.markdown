---
layout: post
title: "MikroTik vs Ubiquiti"
date: 2020-05-29 21:19:23 +0800
comments: true
categories: Network
---

Talking about router and switch, we have 2 markets, the enterprise one, and the consumer one.
In the enterprise market, Cisco is a dominant player. Cisco devices are costly, but companies would like to pay for them, mostly for the service. Whenever an issue happens, a phone call gets human tech support at 24x7.
On the other side, in the consumer market, users have no intention to pay for such service, but would instead buy hardware and resolve issues by themselves.

Now today, I want to talk about equipment across the 2 markets, MikroTik and Ubiquiti. They have enterprise quality without real-time tech support, which is perfect for technical people who have a pursuit of quality and speed.

So what would you consider for choosing a router or switch? I don't know you, but I would consider (from most important to least important): Security > Reliability > Noise Level > Performance (Throughput) > Hardware Interface > Scalability > User Experience > Power Source > Power Cost > Technical Support >  Rack Mount

<!--more -->


## 1. Security

Security is more about routers than switches because routers are the ones that communicate with the internet directly while switches most times only reside inside an intranet.

Security Vulnerabilities Published In 2018 for MikroTik RouterOS: <https://www.cvedetails.com/vulnerability-list/vendor_id-12508/product_id-23641/year-2018/Mikrotik-Routeros.html>

Security Vulnerabilities Published In 2018 for Ubiquiti EdgeOS:
<https://www.cvedetails.com/vulnerability-list/vendor_id-12765/product_id-44469/year-2018/Ubnt-Edgeos.html>

Comparing these two, Ubiquiti is slightly better than MikroTik. There was one CVE from MikroTik [CVE-2018-7445 (Exec Code Overflow)](https://www.cvedetails.com/cve/CVE-2018-7445/) that scored as 10 (the highest vulnerability score) The detail of this CVE:

> A buffer overflow was found in the MikroTik RouterOS SMB service when processing NetBIOS session request messages. Remote attackers with access to the service can exploit this vulnerability and gain code execution on the system. The overflow occurs before authentication takes place, so an unauthenticated, remote attacker can exploit it. All architectures and all devices running RouterOS before versions `6.41.3`/`6.42rc27` are vulnerable.

I hope no one is using an internet-facing router to serve SMB service, because it's too risky to do that. A simple nmap exposes itself as an SMB server, and it's not that difficult to exploit a file sharing service like SMB. In other words, we should always put a file sharing service on a switch. But unfortunately, for MikroTik switches, there isn't one switch that supports NVME m.2 interface like their high-end routers, so this feature seems useless for high-speed local storage service. Even there exists, their SMB service only supports Samba 1.0, and only Samba 3.0 or above has the feature to aggregate bandwidth from different links. So I would suggest MikroTik focus on what a router is supposed to do and let end users build their own professional high-speed local NAS. Ubiquiti doesn't have this feature at all; neither do they support an NVME storage in their router.  Thus no such issues for Ubiquiti.

For switches, the security is less critical because we usually access them from inside a network. Still a minus point to `SwOS` because it doesn't support to modify the default admin user name. I know most new MikroTik switches (`CRS` Cloud Router Switch series) support both `SwOS` and `RouterOS`, and `RouterOS` doesn't have this issue, but still, someone would prefer the old and more cost-effective `CSS` (Cloud Smart Switch) series. Ubiquiti's UI does support this but not so apparent to end-users. We need to switch to the legacy UI to do so rather than the default new UI or use the CLI.

## 2. Reliability

From my personal experience, MikroTik is slightly better than Ubiquiti on this. It might because I purchased an Edge Switch 2 years ago, and before the new `v1.8.3` release, I was hit several times by this issue:

https://community.ui.com/questions/Losing-access-to-switches-Regulary-Regreting-buying-Ubiquiti/5202e750-f497-40d0-a00d-908c8c2a3d0a

With the `v1.8.3` release, they have added some methods to mitigate this issue but have not yet 100% resolved it after 2 years. It seems the root cause is still not found.
MikroTik's SwOS v2.5 in 2017 was infamous on the CxS326 platform, as there were issues with the 10GbE port performance. The fix was simple, downgrading to `v2.4`. These issues have been fixed.

Ubiquiti's EdgeRouter ER-X also had some reliability issues with their firmware in `v2.x`. I downgraded to `v1.x`, and so far, it's OK for half a year. Now if you check their firmware downloading page, you find 2 versions (as of writing on 29 May 2020):

<https://www.ui.com/download/edgemax/edgerouter-x/default/edgerouter-er-xer-x-sfpep-r6-firmware-v11011>

<https://www.ui.com/download/edgemax/edgerouter-x/default/edgerouter-er-xer-x-sfpep-r6er-10x-firmware-v208-hotfix1>

I assume the `v2` is still not stable because there is a hotfix suffix in that build name, which means there was a critical bug before that build.

Right now, I stick with `v1.10.11` for ER-X and not go for `v2` for a long time and `v1.8.5` for EdgeSwitch and not go for `v1.9` for a long time.

Users also complain about the version naming for Ubiquiti's firmware. Instinctually people would think `v2` is better than `v1`, but that's not the case for Ubiquiti. `v2` is experimental, while `v1` is the stable version for the case ER-X. This issue doesn't happen for MikroTik, which separates their versions into 4 segments: `long-term`, `stable`, `testing`, and `development`. I always choose `stable` or `long-term` versions for RouterOS.

## 3. Noise Level

It all depends on where you put your equipment. If it's for a home lab, for sure, you don't want a MikroTik CRS354-48G-4S+2Q+RM because it's too noisy unless you have a good rack cabinet and put it somewhere far from your living and working place.

Both Ubiquiti and MikroTik have quiet/fanless solutions. We only need to choose the right models. For POE switches, of course, we need fans, and if you are searching for solutions to modify the fans with some quiet ones,  I don't have any experience to share with you. Good luck!

## 4. Performance (Throughput)


MikroTik has a much higher performance than Ubiquiti for products in the same price segments. A few examples:

### Ubiquiti ER-12 (suggested price $249) and MikroTik RB4011iGS+RM (suggested price $199)

<table><thead><tr><td colspan="2">Ubiquiti ER-12</td><td colspan="6">measured with firmware v1.9.7</td></tr>
<tr><td rowspan="2">Mode</td><td rowspan="2">Configuration</td><td colspan="2">1518 byte</td><td colspan="2">512 byte</td><td colspan="2">64 byte</td></tr><tr><td>kpps</td><td>Mbps</td><td>kpps</td><td>Mbps</td><td>kpps</td><td>Mbps</td></tr></thead>
<tbody><tr>
<td>Routing</td><td>none (fast path)</td><td>650</td><td>8,000</td><td></td><td></td><td>3,400</td><td>1,800</td>
</tr></tbody></table>

<small> Data source: https://www.ui.com/edgemax/comparison/ </small>

<table><thead><tr><td colspan="2">RB4011iGS+RM</td><td colspan="6">AL21400 1G/S+ all port test</td></tr><tr><td rowspan="2">Mode</td><td rowspan="2">Configuration</td><td colspan="2">1518 byte</td><td colspan="2">512 byte</td><td colspan="2">64 byte</td></tr><tr><td>kpps</td><td>Mbps</td><td>kpps</td><td>Mbps</td><td>kpps</td><td>Mbps</td></tr></thead>
<tbody><tr><td>Bridging</td><td>none (fast path)</td><td>806</td><td>9,792</td><td>2,312</td><td>9,473</td><td>5,509</td><td>2,821</td></tr><tr><td>Bridging</td><td>25 bridge filter rules</td><td>806</td><td>9,792</td><td>1,037</td><td>4,249</td><td>1,153</td><td>590</td></tr><tr><td>Routing</td><td>none (fast path)</td><td>806</td><td>9,792</td><td>1923</td><td>7,877</td><td>5,092</td><td>2,607</td></tr><tr><td>Routing</td><td>25 simple queues</td><td>806</td><td>9,792</td><td>1,046</td><td>4,286</td><td>960</td><td>491</td></tr><tr><td>Routing</td><td>25 ip filter rules</td><td>593</td><td>7,209</td><td>625</td><td>2,560</td><td>564</td><td>289</td></tr></tbody></table>

<small> Data source: https://mikrotik.com/product/rb4011igs_rm with corrections on some data. </small>

I don't understand why MikroTik made some basic mistakes on some `,` and `.` notation in their test data, so I have to make some corrections to make them add up.
Please also note the throughput value in Mbps used above for Ubiquiti seems the real data excluding the packet overhead, while for MikroTik data, the packet overhead is included.
Even considering all those overhead and mistakes, MikroTik still has a higher performance.

### Ubiquiti ES-24-LITE (suggested price $240) and MikroTik CRS326-24G-2S+RM (suggested price $199)

ES-24-LITE has a throughput of 26Gbps and CRS326-24G-2S+RM has a throughput of 33Gbps+.
That simple comparison may be not fair.

## 5. Hardware Interface

In terms of hardware interface, MikroTik is much more aggressive, and Ubiquiti looks conservative in general. You would see more SFP+ ports used in MikroTik products, while Ubiquiti only has SFP ports in the same price segmentations.

One example is the comparison between CRS326-24G-2S+RM and ES-24-LITE we just talked about above.

Another example is MikroTik CRS354-48G-4S+2Q+RM (suggested price $499) and Ubiquiti ES-48-LITE (suggested price $460). CRS354-48G-4S+2Q+RM has 48 Gigabit Ethernet ports, 4 10-Gigabit SFP+ ports, and 2 40-Gigabit QSFP ports. In comparison, ES-48-LITE only has 48 Gigabit Ethernet ports, 2 Gigabit SFP ports and 2 10-Gigabit SFP+ ports.

There is also one product I have found that Ubiquiti has an advantage over MikroTik. MikroTik CRS312-4C+8XG-RM (suggested price $599) and Ubiquiti US‑16‑XG ($599 but out of stock at the moment 30 May 2020). CRS312-4C+8XG-RM has 4 Combo 10-Gigabit Ethernet/SFP+ ports (for each of the Combo port, users can choose to use a 10-Gigabit Ethernet port, or a 10-Gigabit SFP+ port), and 8 10-Gigabit Ethernet ports. In comparison, US‑16‑XG has 12 10-Gigabit SFP+ ports and 4 10-Gigabit Ethernet ports.

## 6. Scalability

MikroTik has very limited scalabilities, but Ubiquiti is doing quite well on this.

Ubiquiti develops a centralized management software called UNMS ( Ubiquiti Network Management System). It provides 2 options. Users can either host the UNMS by themselves or use the free UNMS provided by Ubiquiti if they have at least 10 Ubiquiti devices. With UNMS, we can manage thousands of UniFi devices across multiple sites, and scale network as needed without any ongoing licensing fees. For UniFi series devices, we can also use UniFi Controller, another centralized tool to manage devices.

When you have more than 10 devices, including routers, switches, and wireless APs, I would strongly suggest you use Ubiquiti products rather than MikroTik.

For example, you have 3 apartments, and each one installs one router, one switch, 2 wireless AP, then it could be a burden for you to manage those devices. You would want to upgrade the firmware by one click remotely. Or maybe you have one big detached house, and you need to install 10 wireless APs, then again, better to choose Ubiquiti. Of course, it may not be that often to upgrade firmware for network devices that we expect to run for a reasonably long time. Another benefit for a centralized management system is that when issues happen, we can quickly have a basic idea which part of the system goes wrong and most probably come up with a fast solution.

On the other hand, if you are sure that you won't have many devices and scalability is not an issue to you, or you think everything is still manageable, then maybe MikroTik is not a bad choice.


### 7. User Experience

Ubiquiti is slightly better than MikroTik in terms of user experience.

MikroTik provides a native desktop app called WinBox, but sadly it only supports Windows, and it won't work on a Mac OS, especially for the newer versions even the Wine solution won't work. WinBox is very useful when sometimes users make some stupid mistakes on IP addresses. It can connect to routers/switches without an IP address! How? It connects directly with MAC addresses. That's a feature that Ubiquiti doesn't provide. For Ubiquiti devices, in case we mess up with IP addresses, the only way is to reset to factory settings and start over again. Professional network engineers probably make IP mistakes very rarely, but as a non-professional engineer, I made such mistakes several times.

Both MikroTik and Ubiquiti provide Web and CLI (Command-Line Interface) management. MikroTik UI is more straight forward while Ubiquiti UI looks well designed by UI/UX designers and maybe also product managers instead of coming out from software engineers alone.

Again, the UNMS is more user friendly when managing more than 10 devices. UNMS is fantastic, and once you tried, maybe you would never want to go back to the old days. UNMS itself makes Ubiquiti's user experience better than MikroTik.

Some MikroTik devices, for instance, RB400iGS+RM, have a way too bright LED for power status, which is complained by many users, but it seems MikroTik doesn't bother to care about it at all. On the contrary, Ubiquiti devices look more decent.

### 8. Power Source

MikroTik products tend to provide redundancies in power sources. As an example, CSS326-24G-2S+RM has a DC input and also a POE in. Technically, this makes this a dual power supply switch, and the PoE side can be latched and come from a higher-quality power source. Ubiquiti UnifiSwitch-24 only has one AC input, so does Ubiquiti EdgeSwitch 24.

As an extreme example, MikroTik CRS305-1G-4S+IN even has 2 DC inputs and also a POE in, which technically makes it a triple power supply switch.

Sometimes, the preference of the power method depends on whether we put the device into a rack. Usually, for a rack-mountable device, we prefer an AC power than a DC, because with a DC power, the adapter is quite big and it's not that easy to find a place to plug it into a rack. However, for none-rack-mount devices, a DC power is more cost-effective.

UnifiSwitch-24 has one AC input, which is better than CSS326-24G-2S+RM, but the later has a POE in, which the former doesn't have.

I can't say which is better, but it depends on what you need and what you prefer.

### 9. Power Cost

We don't need to consider power cost for a home lab because we are not running thousands of devices at the same time, and for devices running in less than 100W, we just don't care.


### 10. Technical Support

Both MikroTik and Ubiquiti have limited technical support. Most of the time, we depend on their forums for answers, and that is the fun part, is it?

### 11. Rack Mount

Ubiquiti's most devices are rack-mountable, with an additional rack mount kit, which they sell it separately. MikroTik has rack-mount versions for their products, with an RM in the affix in the product name, for example, RB4011iGS+RM; and also, it has none-rack-mount versions, for example, CCR1009-7G-1C-PC.

