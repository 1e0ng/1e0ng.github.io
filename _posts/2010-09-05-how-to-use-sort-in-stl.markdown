---
comments: true
date: 2010-09-05 16:40:16 +0800
layout: post
slug: how-to-use-sort-in-stl
title: How to use STL Sort?
wordpress_id: 230
categories:
- C
tags:
- Sort
- STL
---

By now, the fastest comparison sorting algorithm is $$ Ο(N\log N) $$. The `sort()` function in STL implemented with an optimized quicksort, which is always $$ O(N\log N) $$.

Here is an example:

<!--more-->

``` cpp How To Use STL Sort
#include <algorithm>
using namespace std;
#define N 20
int a[N];
bool cmp(int x, int y){
    return x < y;
}
int main() {
    sort(a, a + N, cmp);
    return 0;
}
```
