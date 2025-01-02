---
comments: true
date: 2011-03-04 16:13:51
layout: post
slug: poj-1260-pearls-report
title: POJ 1260 Pearls Report
wordpress_id: 421
categories:
- Problems
tags:
- '1260'
- POJ
- Report
---

View the [problem](http://poj.org/problem?id=1260) at POJ.
It's a problem from a contest in Northwestern Europe, 2002.

This is a classical Dynamic-Programing problem.
The sate transformation equation is:

<!-- more -->
```
f(i)=min{ f(i - k) + [a(i - k + 1) + a(i - k + 2) + ... + a(i) + 10 ] * p(i) };  (1<=k<=i, 1<=i<=c)
```

`f(i)` means the lowest possible price needed to buy pearls from class 1 to class `i`;
`a(i)` means the number of pearls needed to buy in class `i`;
`p(i)` menas the price of each peal in class `i`;
`c` means the number of categories.

The initial condition is:

```
f(0) = 0;
```

The answer to this problem is:
`f(c)`

You can iteratively calculate `f(i)`, ie from `f(1)` to `f(c)`, or recursively calculate `f(i)`, with recording which `f(i)` has been calculated.

If you want to prove the correctness of the state transformation, continue to the following parts.

1. All pearls in the same class should be bought in a unit.
Prove: Assume we break them into two parts, and buy one part in class `i`, and buy another in class `j`. Without lost of generous, let `i < j`, if we buy all of them in class `i`, we will pay less money. So this is not the best plan, and we should buy all pearls in the same class in one class.

2. If we buy pearls, which is originally in class `i`, in a higher class `j`, then we must buy all pearls originally in class `k (i < k < j)` in class `j`.
Prove: Assume there exists some pearls in class k (i < k < j) that is not bought in class `j`. Then they must be bought in class `k`, or in class `p (k< p < j)`, or in class `q (q > j)`.
If they are bought in class `k`, then if the pearls in class `i` are bought in class `k`, we will pay less money. So this is not a best plan.
If they are bought in class `q`, then if they are bought in class `j`, we will pay less money, so this is not an optimistic plan, either.
If they are bought in class `p`, then there exists some pearls in class `p (k < p < j)` that is not bought in class `j`, and then we replace `i` with `k` replace `k` with `p`, we get the same proposition as the original proposition. Iteratively prove this proposition, and finally this case will falls into one of the above two cases. (Because `p` is monotone increasing and `j` is a limited number, so it's convergence.)
As all above cases results a contradiction, the assume is not true. Hence it is proved.


Source Code to resolve this problem:

``` cpp POJ 1260 Pearls
#include <iostream>
#include <cstdio>
using namespace std;

#define N 110

int a[N], p[N], f[N];
int c;

void solve() {
    f[0] = (a[0] + 10) * p[0];
    for (int i = 1; i < c; ++i) {
        int m = 100000000;
        for (int j = 0; j <= i; ++j) {
            int sum = 10;
            for (int k = j; k <= i ; ++k) {
                sum += a[k];
                //printf("---sum = %d\n", sum);
            }
            //printf("sum = %d\n", sum);
            int tmp = j > 0 ? f[j - 1] : 0;
            tmp += sum * p[i];
            if (tmp < m) {
                m = tmp;
            }
        }
        f[i] = m;
        //printf("f[%d] = %d\n", i, f[i]);
    }
    printf("%d\n", f[c - 1]);
}

int main() {
    int t;
    scanf("%d", &t);
    while (t--) {
        scanf("%d", &c);
        for (int i = 0; i < c; ++i) {
            scanf("%d%d", &a[i], &p[i]);
        }
        solve();
    }
    return 0;
}

```

