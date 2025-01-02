---
comments: true
date: 2011-03-01 14:50:44
layout: post
slug: poj-1129-channel-allocation
title: POJ 1129 Channel Allocation Report
wordpress_id: 357
categories: articles
tags:
- Problems
tags:
- '1129'
- POJ
- Report
---

View this problem on POJ: [1129 Channel Allocation](http://poj.org/problem?id=1129)
This problem involves the following knowledge:
<!--more-->

* Four color theorem
* DFS (Depth First Search)

Any Greedy Method is wrong.
The test cases on POJ are so weak that some greedy methods can also be accepted.

Try this test case if you don't believe your greedy method is wrong:

```
2
A:
B:
4
A:BC
B:ACD
C:ABD
D:BC
4
A:BCD
B:ACD
C:ABD
D:ABC
6
A:BEF
B:AC
C:BD
D:CEF
E:ADF
F:ADE
0
```


Don't view my source code: 


``` cpp POJ 1129 Channel Allocation
#include <iostream>
#include <memory>
#include <cstring>
#include <algorithm>
using namespace std;
bool b[26][26];
char a[26];
int n,m;
void dfs(int d){
    int i,j;
    if(d==n){
        int mm=*max_element(a,a+n);
        if(mm<m)m=mm;
        return;
    }
    for(i=1;i<5;i++){
        bool ok=true;
        a[d]=i;
        for(j=0;j<n;j++){
            if(b[d][j]&&a[d]==a[j]&&d!=j){
                ok=false;
                break;
            }
        }
        if(ok){
            dfs(d+1);
        }
    }
}
int main(){
    freopen("in.txt","r",stdin);
    while(scanf("%d",&n)!=EOF&&n){
        char d[26];
        memset(a,0,sizeof(a));
        memset(b,0,sizeof(b));
        m=4;
        int i,j;
        for(i=0;i<n;i++){
            scanf("%s",d);
            for(j=2;j<strlen(d);j++){
                b[i][d[j]-'A']=1;
                b[d[j]-'A'][i]=1;
            }
        }
        dfs(0);
        if(m==1)
            printf("1 channel needed.\n");
        else
            printf("%d channels needed.\n",m);
    }
    return 0;
}
```
