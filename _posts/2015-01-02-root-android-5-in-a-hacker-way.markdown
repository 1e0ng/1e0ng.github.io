---
layout: post
title: "Root Android 5 in a Hacker Way"
date: 2015-01-02 11:31:57 +0800
comments: true
categories:
- Android
---

So why bother to root an Android device?

Because Android's permission control system is so weak and unsatisfied. Any app may apply more permissions than need, and if you really need some apps but don't like to give them some permissions, there is no way to use them with selected permissions unless to root the device. Aother drawback is the battery usage. Apps like to live as long as they can. They don't want to die or be killed. In my experience, the battery usage for a constant time increases almost linearly for the number of apps installed. So to save battery and make a fair enviroment for all apps installed, you need manual control of apps, which needs a root access of a device.

Before ROOTing, install `adb` and `fastboot` from Android's official website.
<!--more-->

### Backup

Backup everything important.

### Activate developer options and enable usb debugging.

Open `Settings`->`About phone`, Touch `Build number` 7 times. This makes you a developer :D

Open `Settings`->`Developer options`, Check `USB debugging`.

### Unlock

Connect android device to computer. (For this instance, I connect Nexus 4 to a Macbook)

```
adb reboot bootloader
```

Wait for bootloader.

```
fastboot oem unlock
```

### Install TWRP


Download twrp image from official website to computer. (For my device, it's `twrp-2.8.7.1-hammerhead.img`)

Do step 2 (Activate developer options and enable usb debugging) again.

```
adb reboot bootloader
```

Wait for bootloader.

```
fastboot flash recovery twrp-2.8.7.1-hammerhead.img
```

### Install Supersu

Supersu is integrated into TWRP, so just select `Recovery mode` with volume up/down button and press power button.

Open `Reboot` -> `System`, it will remind you to install `Supersu`.

### Lock

```
adb reboot bootloader
fastboot oem lock
fastboot reboot
```

### Install Supersu GUI

Open `Play Store` and update `Supersu`.

### Install App Ops

Install `App Ops` on `Play Store`. With `App Ops`, do permission control for each app.
