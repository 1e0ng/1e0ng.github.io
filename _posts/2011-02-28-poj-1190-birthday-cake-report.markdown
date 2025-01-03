---
comments: true
date: 2011-02-28 18:32:51
layout: post
slug: poj-1190-birthday-cake-report
title: POJ 1190 Birthday Cake Report
wordpress_id: 352
categories:
- Skills
tags:
- '1190'
- POJ
- Report
---

View this problem on POJ: [1190 Birthday Cake (生日蛋糕)](http://poj.org/problem?id=1190)

There is no good methods, maybe dynamic programing is feasible, but it's too complex for me to construct the transformation equation.

I have to use DFS (Depth First Search) to solve this problem. After the TLE (Time Limit Exceeds) appeared enough times, I worked it out. Pruning is very important for this problem.

<!-- more -->

My source code:

``` cpp POJ 1190 Birthday Cake
#include <iostream>
#include <cmath>
using namespace std;
int n,m;
int q[11000];
int p[11000];
unsigned int result;
void dfs(int l,int v,int r,int h,int s){
    if(v<0)return;
    if(l>m+1)return;
    if(s+p[m-l+1]>result)return;
    if(v<q[m-l+1])return;
    if(v>r*r*h*(m-l+1))return;
    if(l==m+1&&v==0){
        if(s<result)result=s;
    }
    int ri,hi;
    for(ri=r;ri>0;ri--){
        if(2*v/ri>=result-s)break;
        for(hi=h;hi>0;hi--){
            int t=s+2*ri*hi;
            if(l==1)t+=ri*ri;
            dfs(l+1,v-ri*ri*hi,ri-1,hi-1,t);
        }
    }
}
int main(){
    cin>>n>>m;
    result=-1;
    int i;
    for(i=0;i<11000;i++){
        q[i]=i*i*i;
        p[i]=2*i*i;
    }
    for(i=1;i<11000;i++){
        q[i]+=q[i-1];
        p[i]+=p[i-1];
    }
    dfs(1,n,(int)(sqrt((double)n)),n,0);
    if(result==-1)cout<<"0";
    else
        cout<<result;
    return 0;
}
```
