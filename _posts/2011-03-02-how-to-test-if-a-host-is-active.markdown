---
comments: true
date: 2011-03-02 23:05:54
layout: post
slug: how-to-test-if-a-host-is-active
title: How To Test If A Host Is Active
wordpress_id: 385
categories:
- Mac OS
- Network
tags:
- Active
- Cocoa
- Host
- iMac
---

Sometimes, we would like to check if a remote host is reachable before we establish a connection. This is much like the function of the `ping` command in terminal. Well in Cocoa programing, you can use the function `SCNetworkReachabilityCreateWithName()`.

Here is the code:

<!--more-->
``` objc Test If A Host Is Active
bool success = false;
const char *host_name = [ip cStringUsingEncoding:NSASCIIStringEncoding];
SCNetworkReachabilityRef reachability = SCNetworkReachabilityCreateWithName(NULL, host_name);
SCNetworkConnectionFlags flags;
success = SCNetworkReachabilityGetFlags(reachability, &flags);
bool isAvailable = success && (flags & kSCNetworkFlagsReachable) &&
!(flags & kSCNetworkFlagsConnectionRequired);if (isAvailable) {
    NSLog(@"Host is reachable: %d", flags);
}
else {
    NSLog(@"Host is unreachable");
}
```
