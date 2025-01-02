---
comments: true
date: 2011-02-19 19:31:20
layout: post
slug: how-to-use-__int64
title: __int64 vs long long
categories: articles
tags:
- Windows

---

`long long` is a standard C++ type, so if you use gcc, you can use this type without any problem.
But on Windows, as some old Microsoft C++ compilers don't support the type `long long`, you have to use the non-standard type: `__int64`.

The following example shows how to input and output an `__int64` type of variable.

<!--more-->
```
__int64 a;
scanf("%I64d",&a);
printf("%I64d",a);
```
