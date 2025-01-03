---
comments: true
date: 2009-10-21 21:06:30
layout: post
slug: binary-search-tree-template
title: Binary-Search Tree Template
wordpress_id: 268
categories:
- Algorithm
- CPP

tags:
- Binary Search Tree
---

This is a Binary-Search Tree template written by Leon.

<!--more-->
``` cpp Binary Search Tree

#include <iostream>
#include <cstdio>
#include <cstring>
//Binary Search Tree
//Created by Leon
//Oct 19, 2009
using namespace std;

struct tree {
    int key;
    int value;
    tree *l, *r;
};

tree* Insert(tree* t, int c) {
    tree *nt = new tree();
    nt->l = 0, nt->r = 0, nt->value = 1;
    nt->key = c;
    if (t == 0) {
        return nt;
    }
    tree *tmp = t;
    tree *p;
    while (tmp != 0 && tmp->key != c) {
        p = tmp;
        if (tmp->key < c) {
            tmp = tmp->r;
        }
        else {
            tmp = tmp->l;
        }
    }
    if (tmp == 0) {
        tmp = nt;
        if (p->key < c) {
            p->r = tmp;
        }
        else {
            p->l = tmp;
        }
    }
    else {
        tmp->value++;
    }
    return t;
}

void InOrder(tree* t) {
    if (t != 0) {
        InOrder(t->l);
        printf("%d %dn", t->key, t->value);
        InOrder(t->r);
    }
}

int main() {
    tree* root = 0;
    root = Insert(root, 3);
    root = Insert(root, 19);
    root = Insert(root, 2);
    root = Insert(root, 5);
    root = Insert(root, 2);
    InOrder(root);
    return 0;
}

```
