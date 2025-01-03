---
comments: true
date: 2011-02-22 23:21:57
layout: post
slug: poj-2184-cow-exhibition
title: POJ 2184 Cow Exhibition
wordpress_id: 309
categories:
- Problems
post_format:
- Gallery
tags:
- '2184'
- POJ
- Report
---

This problem can be solved by two methods
	
* Deepth First Search (DFS)
* Dynamic Programming (DP)

<!-- more -->
As I don't know how to pruning, the first method will lead to Time Limit Exceed.

So, … this is my DP method:

```
State Transformation Equation:
    f(i, j) =
        max(f(i-1, j), f(i-1, j-a(i)) + b(i))), if color(i-1, j) is BLACK and color(i - 1, j - a(i)) is BLACK,
        f(i-1,j-a(i))+b(i), if color(i-1,j) is WHITE and color(i-1,j-a(i)) is BLACK
    color(i, j) =
    	BLACK, if color(i-1, j) is BLACK or color(i-1, j-a(i)) is BLACK or (j-a(i)) = 0,
    	WHITE, if color(i-1, j) is WHITE and color(i-1, j-a(i)) is WHITE

```

Here is the source code:


``` cpp POJ 2184 Cow Exhibition
#include <iostream>
#include <cstdio>
using namespace std;
int n,a[1010],b[1010];
#define N 200000
#define M 100000
int f[N+10],color[N+10];
int max(int x,int y){
    return (x>y)?x:y;
}
int main(){
    scanf("%d",&n);
    int i,j;
    for(i=0;i<n;i++){
        scanf("%d%d",&a[i],&b[i]);
        if(a[i]<0&&b[i]<0)continue;
        if(a[i]>=0){
            for(j=N-a[i];j>=0;j--){
                if(color[j]){
                    if(color[j+a[i]])
                        f[j+a[i]]=max(f[j+a[i]],f[j]+b[i]);
                    else
                        f[j+a[i]]=f[j]+b[i];
                    color[j+a[i]]=1;
                }
            }
        }
        else{
            for(j=-a[i];j<=N;j++){
                if(color[j]){
                    if(color[j+a[i]])
                        f[j+a[i]]=max(f[j+a[i]],f[j]+b[i]);
                    else
                        f[j+a[i]]=f[j]+b[i];
                    color[j+a[i]]=1;
                }
            }
        }
        if(color[a[i]+M]==0){
            color[a[i]+M]=1;
            f[a[i]+M]=b[i];
        }
    }
    j=0;
    for(i=M;i<=N;i++){
        if(color[i]&&f[i]>=0&&f[i]+i-M>j){
            j=f[i]+i-M;
        }
    }
    printf("%d\n",j);
    return 0;
}

```

