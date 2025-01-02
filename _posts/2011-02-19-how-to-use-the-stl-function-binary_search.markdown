---
comments: true
date: 2011-02-19 21:46:49
layout: post
slug: how-to-use-the-stl-function-binary_search
title: 'STL Function: binary_search()'
categories: articles
tags:
- Algorithm
- CPP

---

In some cases, we just want to if an element exists in a sorted list, then we can use the STL function: `binary_search()`.
To use this function, you must include the header `<algorithm>`.
Note before we use `binary_search()`, the list must be sorted, either in ascending order or in descending order.
......
Here is a simpler example explaining how to use this function.

<!--more-->
```
#include <algorithm>
#include <iostream>
#include <utility>
using namespace std;
#define N 20
int a[N];
int main() {
    sort(a, a + N);
    if (binary_search(a, a + N, 1)) {
        cout << "OK";
    }
}
```
