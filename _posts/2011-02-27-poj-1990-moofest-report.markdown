---
comments: true
date: 2011-02-27 14:10:16 +0800
layout: post
slug: poj-1990-moofest-report
title: POJ 1990 MooFest Report
wordpress_id: 342
categories: articles
tags:
- Problems
post_format:
- Gallery
tags:
- '1990'
- POJ
- Report
---

View this problem on POJ: [1990 MooFest](http://poj.org/problem?id=1990).


Here is my resolution:

<!-- more -->

First, sort cows by v value.

Then, for each cow in ascend order,

calculate  DS : the sum of the differences of distances between this cow and each of the dealted cows.
The answer is $$ \sum_i{DS_i v_i} $$

How to calculate DS? Use Tree-Structure Array.

Tree-Structure Array may be used to

* store the number of cows that has a smaller $$ x $$ value as $$ N_i $$ for the $$ i $$-th cow.
* store the sum of $$ x $$ values which is smaller than the $$ x $$ value of the current cow as $$ S_i $$ for the $$ i $$-th cow.

The sum of all $$ x $$ values when dealing the $$ i $$-th cow can be calculated, which we denote as $$ T_i $$.

Then $$ DS_i = (x_i N_i - S_i) + [(T_i - S_i) - (i - 1 - N_i)  x_i] $$

The sort costs $$ O(n log(n)) $$ (if you use quick sort), or $$ O(n) $$ (if you use radix sort).

For each cow, we need $$ O(log(n)) $$ to calculate the DS(i), this is decided by the algorithm of Tree-Structure Array.

So, the total complexity of this algorithm is $$ O(n log(n)) $$.[^1]

[^1]: For this problem, the answer may exceed the scope of 32-bit integer , so you may use int64 or long long in C++ language, or BigInteger in Java.


``` cpp POJ 1990 Moo Fest
#include <stdio.h>
#include <memory.h>
#include <algorithm>
#define N 20001
using namespace std;
int ln[N],lsum[N],v[N],x[N],p[N],l[N];
int n,m;
__int64 result;
int query(int a[],int pos){
    int sum=0;
    while(pos>0){
        sum+=a[pos];
        pos-=l[pos];
    }
    return sum;
}
void modify(int a[],int pos,int num){
    while(pos<=m){
        a[pos]+=num;
        pos+=l[pos];
    }
}
bool cmp(int a,int b){
    return v[a]<v[b];
}
int main(){

    scanf("%d",&n);
    int i;
    m=0;
    for(i=0;i<n;i++){
        scanf("%d%d",&v[i],&x[i]);
        p[i]=i;
        if(x[i]>m)
            m=x[i];
    }
    for(i=0;i<=m;i++)
        l[i]=i&(i^(i-1));
    sort(p,p+n,cmp);
    memset(ln,0,sizeof(ln));
    memset(lsum,0,sizeof(lsum));
    modify(ln,x[p[0]],1);
    modify(lsum,x[p[0]],x[p[0]]);
    int total=x[p[0]];
    result=0;
    for(i=1;i<n;i++){
        int xx=x[p[i]];
        int lnn=query(ln,xx);
        int lss=query(lsum,xx);
        __int64 distance=(2*lnn-i)*xx-2*lss+total;
        result+=distance*v[p[i]];
        total+=xx;
        modify(ln,xx,1);
        modify(lsum,xx,xx);
    }
    printf("%I64d\n",result);
    return 0;
}
```
