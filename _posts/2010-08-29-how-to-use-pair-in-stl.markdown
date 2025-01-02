---
comments: true
date: 2010-08-29 08:47:52
layout: post
slug: how-to-use-pair-in-stl
title: How to use "pair" in STL?
wordpress_id: 226
categories: articles
tags:
- CPP

tags:
- Pair
- STL
---

In Python, we have tuple, and in Java, we have Map, but in C++, the language itself doesn't contain anything equivalent. Nevertheless, we can use STL - the Standard Template Library - to construct the data structure.

Of course, we can construct this by ourself, and it's not complex, but as we will see, with "pair" we can make it easier and simpler.

This is an example:

<!--more-->
``` cpp How To Use Pair In C++
 #include <utility>

 pair<int,int> p;
 p.first=1;
 p.second=2;
 p=make_pair(3,4);
```
