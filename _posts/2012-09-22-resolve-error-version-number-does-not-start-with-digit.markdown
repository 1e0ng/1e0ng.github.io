---
comments: true
date: 2012-09-22 22:43:52
layout: post
slug: resolve-error-version-number-does-not-start-with-digit
title: Resolve Error "version number does not start with digit
wordpress_id: 1063
categories:
- Linux
tags:
- Deb
- Linux QQ
- version number
---

Today, I download a Linux version of QQ, a Deb file, but when I install it, I get an error : "version number does not start with digit".

I search the internet and Google tells me the solution.

<!--more-->

1. cd to the directory of linuxqq_v1.0.2-beta1_i386.deb

2. 


	```    
	dpkg-deb -R linuxqq_v1.0.2-beta1_i386.deb linuxqq
	```
3. 

	```    
	vi linuxqq/DEBIAN/control
	```


	change the line "Version: v1.0.2-beta1" to "Version: 1.0.2-beta1", ie remove the letter "v".
	
	save and exit.

4. 

	```  
	dpkg-deb -b linuxqq/ linuxqq.deb
	```

The new package linuxqq.deb can be installed successfully now.


