---
layout: post
title: "POJ 3264 Balanced Lineup"
date: 2014-10-25 23:15:03 +0800
comments: true
categories:
- Problems

---

This is a classic range minimum query and range maximum query problem.

Segment tree, with $$ O(\log_2{n}) $$ updating complexity and  $$ O(\log_2{n}) $$ query complexity, is a perfect data structure for this problem.

Actually this is really easy once segment tree is imported.

Source code:
<!--more-->

``` c++

#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;

#define H 1000000
#define N 50010

int n, q;
int h[N];
int c_min[1 << 22],c_max[1<<22];

void update(int ii,int s,int t,int ss,int tt) {
    if(ss>tt) return; int mid((s+t)/2);
    if(s==ss && t==tt){ c_min[ii]=c_max[ii]=h[ss]; return;}
    update(ii*2,s,mid,ss, min(mid,tt));
    update(ii*2+1,mid+1,t, max(mid+1,ss),tt);
    c_min[ii]=min(c_min[ii*2],c_min[ii*2+1]);
    c_max[ii]=max(c_max[ii*2],c_max[ii*2+1]);
}

int min_query(int ii,int s,int t,int ss,int tt) {
    if(ss>tt) return H+1; int mid((s+t)/2);
    if(s==ss&&t==tt) return c_min[ii];
    return min(min_query(ii*2,s,mid,ss, min(mid,tt)),
        min_query(ii*2+1,mid+1,t, max(mid+1,ss),tt));
}

int max_query(int ii,int s,int t,int ss,int tt) {
    if(ss>tt) return -1; int mid((s+t)/2);
    if(s==ss&&t==tt) return c_max[ii];
    return max(max_query(ii*2,s,mid,ss, min(mid,tt)),
        max_query(ii*2+1,mid+1,t, max(mid+1,ss),tt));
}

int main() {
    scanf("%d", &n);
    scanf("%d", &q);
    memset(c_min, 0, sizeof(c_min)/sizeof(int));
    memset(c_max, 0, sizeof(c_max)/sizeof(int));
    for (int i = 1; i <= n; ++i){
        scanf("%d", &h[i]);
        update(1, 1, H, i, i);
    }
    for (int i = 0; i < q; ++i) {
        int a, b;
        scanf("%d", &a);
        scanf("%d", &b);
        printf("%d\n", max_query(1, 1, H, a, b) - min_query(1, 1, H, a, b));
    }
    return 0;
}
```
