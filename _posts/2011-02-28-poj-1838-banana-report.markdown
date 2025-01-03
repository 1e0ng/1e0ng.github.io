---
comments: true
date: 2011-02-28 16:29:31
layout: post
slug: poj-1838-banana-report
title: POJ 1838 Banana Report
wordpress_id: 347
categories:
- Problems
post_format:
- Gallery
tags:
- '1838'
- POJ
- Report
---

View this problem on POJ: [1838 Banana](http://poj.org/problem?id=1838).

This problem can be categorized as the Union-Find problem.

<!-- more -->

```
First, sort (xi,yi) by (x,y).
Find those has the same x,but y is 1 more than its precedence.
Find the roots of the two two-tuples.
Union the two roots.
Store the number of this set in the root node.

Second,sort (xi,yi) by (y,x).
Do the similar thing.

Third,find all the roots, and then sort them.
Find the first m roots.
Output the sum.
```


Here is my source code for this problem:

``` cpp POJ 1838 Banana
#include <iostream>
#include <algorithm>
using namespace std;
// Created by Leon in Feb 2011
int n,k;
int a[16010],x[16010],y[16010],b[16010];
bool cmp1(int i,int j){
    if(x[i]<x[j])return true;
    if(x[i]>x[j])return false;
    if(y[i]<y[j])return true;
    return false;
}
bool cmp2(int i,int j){
    if(y[i]<y[j])return true;
    if(y[i]>y[j])return false;
    if(x[i]<x[j])return true;
    return false;
}
int Find(int i){
    if(b[i]<0)return i;
    int p=Find(b[i]);
    b[i]=p;
    return p;
}
void Union(int i,int j){
    int x=Find(i);
    int y=Find(j);
    if(x==y)return;
    b[y]=b[x]+b[y];
    b[x]=y;
};
int main(){
    cin>>n>>k;
    int i;
    for(i=0;i<n;i++){
        scanf("%d%d",&x[i],&y[i]);
        a[i]=i;
        b[i]=-1;
    }
    sort(a,a+n,cmp1);
    for(i=1;i<n;i++){
        int t1=a[i],t2=a[i-1];
        if(x[t1]==x[t2]&&y[t1]==y[t2]+1)
            Union(t1,t2);
    }
    sort(a,a+n,cmp2);
    for(i=1;i<n;i++){
        int t1=a[i],t2=a[i-1];
        if(y[t1]==y[t2]&&x[t1]==x[t2]+1)
            Union(t1,t2);
    }
    int m=0;
    for(i=0;i<n;i++){
        if(b[i]<0){
            a[m++]=-b[i];
        }
    }
    sort(a,a+m);
    int s=0;
    for(i=0;i<k;i++){
        s+=a[m-1-i];
    }
    cout<<s;
    return 0;
}
```
