---
comments: true
date: 2011-03-01 12:36:04
layout: post
slug: poj-2001-shortest-prefixes-report
title: POJ 2001 Shortest Prefixes Report
wordpress_id: 321
categories:
- Problems
tags:
- '2001'
- POJ
- Report
---

[View](http://poj.org/problem?id=2001) the Problem.

This problem can be solved by 2 methods.
<!-- more -->
* Trie
* Quick Sort

To get a quick coding, choose the `Quick Sort` method.
To get a good performance, choose the `Trie` method.


1.

``` cpp POJ 2001 Shortest Prefixes (Trie)
#include <iostream>
#include <string.h>
using namespace std;
#define N 26
#define B 'a'

struct Trie{
    int num;
    Trie* child[N];
};
Trie* NewTrie(){
    Trie* tmp=new Trie();
    tmp->num=1;
    int i;
    for(i=0;i<N;i++){
        tmp->child[i]=NULL;
    }
    return tmp;
}

void Insert(Trie* tr,char* c,int l){
    int i;
    Trie* tmp=tr;
    for(i=0;i<l;i++){
        if(tmp->child[c[i]-B]==NULL){
            tmp->child[c[i]-B]=NewTrie();
        }
        else{
            tmp->child[c[i]-B]->num++;
        }
        tmp=tmp->child[c[i]-B];
    }
}
void Delete(Trie* tr){
    int i;
    for(i=0;i<N;i++){
        if(tr->child[i]) Delete(tr->child[i]);
    }
    delete tr;
    tr=0;
}
void Find(Trie* tr,char* c,int l){
    int i;
    printf("%s ",c);
    Trie* tmp=tr;
    for(i=0;i<l;i++){
        printf("%c",c[i]);
        if(tmp->child[c[i]-B]->num==1)
            break;
        tmp=tmp->child[c[i]-B];
    }
    printf("\n");
}
Trie* t;
char s[1001][21];
int main(){
    freopen("in.txt","r",stdin);
    freopen("out.txt","w",stdout);
    t=NewTrie();
    int i=0,j;
    while(scanf("%s",s[i])!=EOF){
        Insert(t,s[i],strlen(s[i]));
        i++;
    }
    for(j=0;j<i;j++){
        Find(t,s[j],strlen(s[j]));
    }
    Delete(t);
    return 0;
}
```

2.

``` cpp POJ 2001 Shortest Prefixes (Quick Sort)

#include <iostream>
#include <algorithm>
#include <memory.h>
#include <string.h>
#define M 1100
using namespace std;
char c[M][30];
int d[M],l[M];
int n;
bool cmp(int x,int y){
    int i=0;
    while(c[x][i]==c[y][i]&&c[x][i]&&c[y][i])
        i++;
    return c[x][i]<c[y][i];
}
int main(){
    freopen("in.txt","r",stdin);
    freopen("out.txt","w",stdout);
    int i,j,k,j2;
    n=0;
    while(scanf("%s",c[n])!=EOF){
        d[n]=n;
        n++;
    }
    sort(d,d+n,cmp);
    memset(l,0,sizeof(l));
    for(i=0;i<n-1;i++){
        int j=d[i];j2=d[i+1];
        k=0;
        while(c[j][k]==c[j2][k]&&c[j][k]&&c[j2][k])
            k++;
        if(k>l[j])l[j]=k;
        if(k>l[j2])l[j2]=k;
    }
    for(i=0;i<n;i++){
        if(c[i][0]){
            printf("%s ",c[i]);
            for(j=0;j<l[i];j++)
                printf("%c",c[i][j]);
            if(c[i][j]!=0)
                printf("%c",c[i][j]);
        }
        printf("\n");
    }
    return 0;
}
/*

#include<iostream>
#include<stdlib.h>
#include<string.h>
#include<algorithm>
#include<assert.h>
using namespace std;
int k[1000],l[1000];
char str1[1000][22];
int cmp1(int a,int b)
{
    int i=0;
    while(str1[a][i]==str1[b][i]&&str1[a][i]){
        i++;
    }
    return str1[a][i]<str1[b][i];
}
int main()
{
    freopen("in.txt","r",stdin);
    freopen("out.txt","w",stdout);
    int i=0,m1=0,m2=0,j,len,min;
    while (cin>>str1[i])
    {
          k[i]=i;
          i++;
    }
    len=i;
    sort(k,k+len,cmp1);
    for (i=0;i<len-1;i++)
    {
        j=0;
        while(str1[k[i]][j]&&str1[k[i+1]][j]&&str1[k[i]][j]==str1[k[i+1]][j])
            j++;
        if(j>l[k[i]])l[k[i]]=j;
        if(j>l[k[i+1]])l[k[i+1]]=j;
    }
    for (i=0;i<len;i++){
        cout<<str1[i]<<" ";
        for(j=0;j<l[i];j++){
            printf("%c",str1[i][j]);
        }
        if(str1[i][l[i]])printf("%c",str1[i][l[i]]);
        cout<<endl;
    }
    return 0;  
}

*/
```
