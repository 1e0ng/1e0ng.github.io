---
layout: post
title: "POJ 3468 A Simple Problem with Integers"
date: 2014-10-26 00:27:24 +0800
comments: true
categories:
- Problems

---

Like [POJ 3264 Balanced Lineup](/posts/poj-3264-balanced-lineup/), segment tree is used.

The point is not to push down delta value to descendents, just keeping it on current node if the addition is for all its descendents.

Source code:

<!--more-->

``` c++
#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;

int n, q;
long long cc[1 << 22];
long long dd[1 << 22];

void update(int ii,int s,int t,int ss,int tt, int c) {
    if(ss>tt) return; int mid((s+t)/2);
    if(s==ss&&t==tt) {dd[ii]+=c; return;}
    update(ii*2,s,mid,ss, min(mid,tt), c);
    update(ii*2+1,mid+1,t, max(mid+1,ss),tt,c);
    cc[ii] = cc[ii*2] + cc[ii*2+1] + dd[ii*2]*(mid-s+1) + dd[ii*2+1]*(t-mid);
}

long long query(int ii,int s,int t,int ss,int tt) {
    if(ss>tt) return 0; int mid((s+t)/2);
    if (s==ss&&t==tt){
        return cc[ii] + dd[ii]*(tt-ss+1);
    }
    return query(ii*2,s,mid,ss, min(mid,tt))
        +query(ii*2+1,mid+1,t, max(mid+1,ss),tt) + dd[ii]*(tt-ss+1);
}

int main() {
    scanf("%d", &n);
    scanf("%d", &q);
    memset(cc, 0, sizeof(cc)/sizeof(long long));
    memset(dd, 0, sizeof(dd)/sizeof(long long));
    for (int i = 1; i <= n; ++i){
        int a;
        scanf("%d", &a);
        update(1, 1, n, i, i, a);
    }
    for (int i = 0; i < q; ++i) {
        char o[2];
        int a, b, c;
        scanf("%1s", o);
        if (o[0] == 'C') {
            scanf("%d", &a);
            scanf("%d", &b);
            scanf("%d", &c);
            update(1, 1, n, a, b, c);
        }
        else {
            scanf("%d", &a);
            scanf("%d", &b);
            printf("%lld\n", query(1, 1, n, a, b));
        }
    }
    return 0;
}
```
