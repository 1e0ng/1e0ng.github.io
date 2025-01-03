---
layout: post
title: "Tune Supmermicro Board Fun Speed With ipmitool"
date: 2025-01-01 22:54:38 +0800
comments: true
categories:
- Server
---

On this year's Christmas holiday, I was planning to do some maintainess with my home server, which is a Super Micro SYS-7048GR-TR (or X10DRG-Q if folks are more familar with the motherboard model). Then supprise came, when I tried to do something real, every time. I wasn't able to connect to the server by IPMI web portal! The Chrome browser showed an error of ERR_ADDRESS_UNREACHABLE, which means the connection was rejected. First thing came to my mind is I got hacked. <!-- more -->

The first mistake I made was I didn't even try with another browser. I tried with the ipmitool command line tool, and it was successful. I quickly figured out 2 solutions:

1. Connect a monitor to that ancient VGA onboard graphic card interface. I did searched my home lab for anything about VGA, no found any adaptor from VGA to HDMI, or any cable with VGA. Only found one DVI to VGA adaptor, but that is useless for this case. This search took me almost one hour.

2. Fix the IPMI. Since I'm not able to find any way to connect a monitor, then the only feasible way for me to fix the IPMI on the board. I  don't want to search Carousel for an adaptor on Christmas eve. Given the fact I was still to connect with the ipmitool CLI, then maybe I can factory reset the BMC? The BMC IP is retrieved from DHCP service of my router, so that means the IP address for the IPMI wouldn't be changed. What else? Maybe some configurations, either way I can configure them one more time since I already did it before.

Comparing with the pros and cons or not needing to compare at all, option 2 is my last straw.

I quickly did a factory reset of the BMC. It worked, because I wasn't able to connect to it with the previous IPMI password I set, but with the default password. I quickly modified the password to new one, in the fare of the potential hacker could take over my access to server in the short period of time. Now the weird thing happened: The same error on the Chrome browser. This confused me a lot, as I was expecting everything back to normal after a factory reset of the BMC, which is a really heavy and serious operation. Could it because the hardware chip got corrupted? I did change the fans to Noctua ones, but nothing big change. Then I kind of lost thread.

Since I just re-wired my home network before that, I highly doubt some firewall settings I set could be wrong, which blocked me out of the IPMI web portal. First I checked the router configuration, all looks normal. Then I wanted to check the switch portal for any port isolation. I got the same error ERR_ADDRESS_UNREACHABLE when I tried to access my switch portal.
Now I realised maybe I was on the wrong direction. It wasn't anything about IPMI, but maybe about the browser? I tried with Safari once and magically it worked! Then I started to blame Chrome silently. It could be because one upgrade that caused this bug. After Google search a while, I found I was wrong again. It was actually because I didn't grant the local network access on the Mac OS system. This [answer](https://support.google.com/chrome/thread/300649124/i-got-err-address-unreachable-error-message-while-safari-is-ok?hl=en) saved my life. To copy it here: MAC OS System Settings > Privacy and Security. Then scroll to find Local Network. Make sure it is enabled for Google Chrome.

What can I say for my whole day investigation to late night? Thank you Apple for your recent upgrade.

There is more: since I factory reset BMC, the server fan started to run full speed every minute or two. I know this is because I swapped the original fans with Noctua ones. Thankfully I have the earlier script to set the fan speed.

To view the current temperature settings of all fans:

```
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor list | grep -i temp | grep -v na
```

To set speed for all fans in my case:

```
for i in 1 2 3 4 5 6 A B C D; do ipmitool -H 172.30.0.x \
                      -U username -f ./.ipmi-supermicro-bmc -I lanplus \
                      sensor thresh FAN${i} lower 0 100 200;done



#### deleted: NF-A14 PWM; RPM 1500
# GT 2150 PWM; RPM 2150
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FAND lower 0 1500 1800
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FAND upper 2400 2500 2600


# NF-A8 PWM; RPM 2200
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FAN3 upper 2400 2500 2600
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FAN4 upper 2400 2500 2600
### deleted: ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FANC upper 2400 2500 2600


# NF-F12 industrialPPC-3000 PWM; RPM 3000
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FAN1 upper 3200 3300 3400
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FAN2 upper 3200 3300 3400


# NF-A14 industrialPPC-3000 PWM; RPM 3000
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor thresh FANA upper 3200 3300 3400



# Verify
ipmitool -H 172.30.0.x -U username -f ./.ipmi-supermicro-bmc -I lanplus sensor list | grep ^FAN
```


