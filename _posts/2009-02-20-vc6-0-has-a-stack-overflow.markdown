---
comments: true
date: 2009-02-20 19:18:28
layout: post
slug: vc6-0-has-a-stack-overflow
title: VC6.0 has a stack overflow
wordpress_id: 240
categories: articles
tags:
- Windows
tags:
- Stack Overflow
- VC6
---

When VC6.0 breaks down due to a stack overflow, sometimes you can adjust the stack allocations to get around this problem.

Project->Settings->Link->Category->Output

Write the bytes you need in Stack allocations->Reserve.
