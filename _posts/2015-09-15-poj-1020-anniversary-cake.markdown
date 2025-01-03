---
layout: post
title: "POJ 1020 Anniversary Cake"
date: 2015-09-15 23:42:56 +0800
comments: true
categories:
- Problems
---

This is a simple search problem. With some pruning job it's sufficient to pass test cases.

The biggest possible area of cake is $$ 16 \times 10 \times 10 $$, so the biggest possbile side of cake is $$ 40 $$.

Image a cake as a matrix with rows and colums. Each element of this matrix is a 1x1 cell. The problem can be translated to if there exists a method to fill this matrix with squares.

Now fill the matrix in this order: find the lowest leftmost empty cell $$ C_{i,j} $$.
Find successive cells $$ C_{i,j}, C_{i, j+1}, \dots, C_{i, j+w} $$ with the same height as $$ C_{i,j} $$.

Choose a square and put it into an area with left upper cell as $$ C_{i, j} $$. If this can not construct a solution, backtrack to use another squre, otherwise continue to the end and get a solution.

<!--more-->

Source code in C++:

{% highlight cpp linenos %}
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

int s, n;
char cs[11], lens[41];

bool dfs(int x) {
    if (x == n) {
        return true;
    }
    int m = 1, w = 1, suc = 1;
    for (int i = 2; i <= s; ++i) {
        if (lens[i] < lens[m]) {
            m = i, w = 1, suc = 1;
        }
        else if (lens[i] == lens[m] && suc) {
            ++w;
        }
        else {
            suc = 0;
        }
    }

    for (int i = min(10, w); i >= 1; --i) {
        if (cs[i] > 0 && lens[m] + i <= s) {
            cs[i]--;
            for (int j = m; j < m + i; ++j) {
                lens[j] += i;
            }
            if (dfs(x+1)) {
                return true;
            }
            for (int j = m; j < m + i; ++j) {
                lens[j] -= i;
            }
            cs[i]++;
        }
    }
    return false;
}

bool solve() {
    cin >> s >> n;
    memset(cs, 0, sizeof(cs));
    memset(lens, 0, sizeof(lens));

    int sum = 0, tmp;
    for (int i = 0; i < n; ++i) {
        cin >> tmp;
        cs[tmp]++;
        sum += tmp*tmp;
    }
    if (sum != s*s) {
        return false;
    }
    return dfs(0);
}

int main() {
    int t;
    cin >> t;
    while(t--) {
        if (solve()) {
            cout << "KHOOOOB!" << endl;
        }
        else {
            cout << "HUTUTU!" << endl;
        }
    }
}
{% endhighlight %}
