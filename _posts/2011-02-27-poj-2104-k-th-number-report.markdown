---
comments: true
date: 2011-02-27 12:24:49
layout: post
slug: poj-2104-k-th-number-report
title: POJ 2104 K-th Number Report
wordpress_id: 318
categories:
- Problems
post_format:
- Gallery
tags:
- '2104'
- POJ
- Report
---

View the problem description here: [ 2104 K-th Number ](http://poj.org/problem?id=2104).

To solve this problem, you need to learn the following knowledge first.
	
* Segment Tree
* Binary Search
* Merge Sort

If you know all the above, it's easy to solve this problem.

<!--more-->


Try to solve by yourself, and don't look my source code:

``` cpp POJ 2104 K-th Number
#include <iostream>
#include <cstdio>
#include <algorithm>
#include <memory.h>
#include <cstring>
using namespace std;
#define maxn 100010
#define maxm 20
int n,m;
int a[maxn];
int sorted[maxm][maxn];
struct node{
    int l,r,d;
    node* lc,*rc;
};
node mem[maxm*maxn];
int pos;
node *root;
int b,e,k;
node* maketree(int l,int r,int d){
    if(l>r)return 0;
    node* n1=&mem[pos++];
    n1->l=l,n1->r=r,n1->d=d;
    if(l==r){
        sorted[d][l]=a[l];
        return n1;
    }
    int mid=(l+r)/2;
    n1->lc=maketree(l,mid,d+1);
    n1->rc=maketree(mid+1,r,d+1);
    int i,j,k;
    i=l,j=mid+1,k=l;
    while(i<=mid&&j<=r){
        if(sorted[d+1][i]<sorted[d+1][j])
            sorted[d][k++]=sorted[d+1][i++];
        else
            sorted[d][k++]=sorted[d+1][j++];
    }
    while(i<=mid)sorted[d][k++]=sorted[d+1][i++];
    while(j<=r)sorted[d][k++]=sorted[d+1][j++];
    return n1;
}
int search2(int l,int r,int d,int u){
    if(l==r+1)return l;
    int mid=(l+r)/2;
    if(u<=sorted[d][mid])return search2(l,mid-1,d,u);
    else return search2(mid+1,r,d,u);
}
int query(int u,node *n1){
    if(b<=n1->l&&n1->r<=e){
        return search2(n1->l,n1->r,n1->d,u)-n1->l;
    }
    else{
        int ret=0;
        int mid=(n1->l+n1->r)/2;
        if(b<=mid)ret+=query(u,n1->lc);
        if(e>=mid+1)ret+=query(u,n1->rc);
        return ret;
    }
}
int search1(int l,int r){
    if(l==r+1){
        return r;
    }
    int mid=(l+r)/2;
    //cout<<"l="<<l<<",r="<<r<<endl;
    //cout<<"mid="<<mid<<endl;
    int x=query(sorted[1][mid],root);
    //cout<<"x="<<x<<endl;
    //cout<<"k="<<k<<endl;
    if(x<=k)return search1(mid+1,r);
    else return search1(l,mid-1);
}
int main(){
    scanf("%d%d",&n,&m);
    int i,j;
    for(i=1;i<=n;i++)scanf("%d",&a[i]);
    pos=0;
    root=maketree(1,n,1);
    /*for(i=1;i<=10;i++){
        for(j=1;j<=7;j++)
            printf("%d ",sorted[i][j]);
        cout<<endl;
    }*/
    for(i=1;i<=m;i++){
        scanf("%d%d%d",&b,&e,&k);
        k--;
        printf("%d\n",sorted[1][search1(1,n)]);
    }
}

```
