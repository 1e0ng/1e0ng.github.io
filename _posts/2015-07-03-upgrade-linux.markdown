---
layout: post
title: "Upgrade Linux"
date: 2015-07-03 15:50:03 +0800
comments: true
categories:
- Linux

---

### Gentoo

```
emerge --sync
emerge --update --deep --with-bdeps=y --newuse world
revdep-rebuild -ip
```

Don't forget to read news:

```
eselect news list
```


### Debian

```
apt-get update
apt-get upgrade
apt-get dist-upgrade
```


### Red hat

```
yum update
```
