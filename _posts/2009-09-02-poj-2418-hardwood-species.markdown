---
comments: true
date: 2009-09-02 15:50:12
layout: post
slug: poj-2418-hardwood-species
title: POJ 2418 Hardwood Species
wordpress_id: 292
categories:
- Problems
tags:
- '2418'
- POJ
- Report
---

This problem can be solved by at least 4 methods:

* Quick Sort
* Binary Search Tree
* Trie and Depth First Search
* Map

<!--more-->
Unfortunately, I only implemented the first two methods.
Here is the source code:

Use Quick Sort:

``` cpp POJ 2418 Hardwood Species (Use Quick Sort)
#include <iostream>
#include <cstring>
using namespace std;
int n;
struct tree{
    char key[31];
    int times;
    tree* l,* r;
};
tree* makeTree(char c[]){
    tree* t=new tree();
    t->l=0;
    t->r=0;
    t->times=1;
    strcpy(t->key,c);
    return t;
}
void Insert(tree* &t,char c[]){
    if(t==0){
        t=makeTree(c);
        return;
    }
    tree* tmp=t;
    tree* p;
    while(tmp!=0&&strcmp(tmp->key,c)!=0){
        p=tmp;
        if(strcmp(tmp->key,c)<0){
            tmp=tmp->r;
        }
        else{
            tmp=tmp->l;
        }
    }
    if(tmp==0){
        tmp=makeTree(c);
        if(strcmp(p->key,c)<0){
            p->r=tmp;
        }
        else{
            p->l=tmp;
        }
    }
    else{
        tmp->times++;
    }
}
void InOrder(tree* t){
    if(t!=0){
        InOrder(t->l);
        printf("%s %.4f\n",t->key,t->times*100.0/n);
        InOrder(t->r);
    }
}
int main(){
    freopen("in.txt","r",stdin);
    char c[31];
    tree* root=0;
    n=0;
    while(scanf("%[^\n]",c)!=EOF&&c[0]){
        n++;
        Insert(root,c);
        getchar();
        c[0]=0;
    }
    InOrder(root);
    return 0;
}
```

Use BST

``` cpp POJ 2418 Hardwood Species (Use Binary Search Tree)
#include <iostream>
#include <algorithm>
using namespace std;
#define N 1000000
char a[N][31];
int b[N];
int c[N];
double d[N];
bool cmp(int x,int y){
    int i;
    for(i=0;i<31;i++){
        if(a[x][i]!=a[y][i]||a[x][i]==0)
            break;
    }
    return a[x][i]<a[y][i];
}
int main(){
    //freopen("in.txt","r",stdin);
    int n=0;
    int i;
    while(scanf("%[^\n]",a[n])!=EOF&&a[n][0]){
        b[n]=n;
        n++;
        getchar();
    }
    sort(b,b+n,cmp);
    for(i=0;i<n;i++)
        c[i]=1;
    for(i=0;i<n-1;i++){
        int j1=b[i],j2=b[i+1];
        if(strcmp(a[j1],a[j2])==0){
            c[j2]+=c[j1];
            c[j1]=0;
        }
    }
    for(i=0;i<n;i++){
        if(c[i]>0){
            d[i]=100.0*c[i]/n;
        }
    }
    for(i=0;i<n;i++){
        int j=b[i];
        if(c[j]){
            printf("%s %.4f\n",a[j],d[j]);
        }
    }
    return 0;
}
```
