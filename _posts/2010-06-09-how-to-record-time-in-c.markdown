---
comments: true
date: 2010-06-09 22:37:11
layout: post
slug: how-to-record-time-in-c
title: How to record time in C++?
wordpress_id: 218
categories: articles
tags:
- C
tags:
- C++
- Time
---

To record the time your program costs, you can use the function `clock()`, that is defined in `<ctime>`.
Here is an example showing how to use this function:

<!--more-->
``` cpp How To Record Time
#include <iostream>
#include <ctime>
using namespace std;
int main() {
	clock_t t1, t2;
	t1 = clock();
	int i, s = 0;
	for (i = 0; i < 100000000; i++)
	    s += i;
	t2 = clock();
	printf("%fn", (double)(t2 - t1) / CLOCKS_PER_SEC);
	return 0;
}

```
