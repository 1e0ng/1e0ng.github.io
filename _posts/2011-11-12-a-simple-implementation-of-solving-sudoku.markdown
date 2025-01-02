---
comments: true
date: 2011-11-12 21:10:07
layout: post
slug: a-simple-implementation-of-solving-sudoku
title: A Simple Implementation of Solving Sudoku
wordpress_id: 873
categories: articles
tags:
- Algorithm
- CPP
tags:
- Search
- Sudoku
---

[Sudoku](http://en.wikipedia.org/wiki/Sudoku) is a popular game. Howerver, solving Sudoku is sometimes not so easy, so I wrote a program to help me do this job. 

<!-- more -->

``` cpp Solving Suduku    

// Created by Leon in 2011
// http://leons.im

#include <iostream>
#include <cstdio>
#include <vector>
#include <utility>
using namespace std;

int in[9][9] = { {9, 0, 0, 0, 5, 0, 7, 0, 0},
                 {0, 7, 0, 6, 0, 3, 9, 0, 8},
                 {0, 8, 3, 0, 0, 4, 0, 0, 2},

                 {8, 0, 5, 2, 0, 9, 0, 7, 0},
                 {1, 0, 0, 0, 6, 0, 0, 0, 3},
                 {0, 9, 0, 3, 0, 0, 1, 0, 5},
                  
                 {7, 0, 0, 4, 0, 0, 5, 2, 0},
                 {3, 0, 4, 5, 0, 1, 0, 6, 0},
                 {0, 0, 9, 0, 8, 0, 0, 0, 1} };
int out[9][9];
int pos[9][9];

bool solve(int d) {
    //printf("d=%d\n", d);
    if (81 == d) {
        return true;
    }
    unsigned i = d / 9, j = d % 9;
    if (in[i][j] > 0) {
        return solve(d + 1);
    }
    for (unsigned k = 1; k <= 9; ++k) {
        if (!(pos[i][j] & (1 << k))) {
            //printf("k=%d\n", k);
            out[i][j] = k;
            int m = 1 << k;
            vector<pair<int, int> > v;
            for (unsigned p = 0; p < 9; ++p) {
                if (!(pos[i][p] & m)) {
                    pos[i][p] |= m;
                    v.push_back(make_pair(i, p));
                }
                if (!(pos[p][j] & m)) {
                    pos[p][j] |= m;
                    v.push_back(make_pair(p, j));
                }
            }
            unsigned si = i / 3 * 3, sj = j / 3 * 3;
            for (unsigned p = 0; p < 3; ++p) {
                for (unsigned q = 0; q < 3; ++q) {
                    if (!(pos[si + p][sj + q])) {
                        pos[si + p][sj + q] |= m;
                        v.push_back(make_pair(si + p, sj + q));
                    }
                }
            }
            if (solve(d + 1)) {
                return true;
            }
            //printf("-------\n");
            for (unsigned p = 0; p < v.size(); ++p) {
                pos[v[p].first][v[p].second] &= ~m;
            }
        }
    }
    return false;
}

int main() {
    for (unsigned i = 0; i < 9; ++i) {
        for (unsigned j = 0; j < 9; ++j) {
            printf("%d, ", in[i][j]);

            if (in[i][j] > 0) {
                out[i][j] = in[i][j];
                int m = 1 << in[i][j];
                for (unsigned k = 0; k < 9; ++k) {
                    pos[i][k] |= m;
                    pos[k][j] |= m;
                }
                unsigned si = i/3 * 3, sj = j/3 * 3;
                for (unsigned k = 0; k < 3; ++k) {
                    for (unsigned p = 0; p < 3; ++p) {
                        pos[si + k][sj + p] |= m;
                    }
                } 
            }
        }
        printf("\n");
    }
    /*
    for (unsigned i = 0; i < 9; ++i) {
        for (unsigned j = 0; j < 9; ++j) {
            if (0 == in[i][j]) {
                for (unsigned k = 1; k <= 9; ++k) {
                    if (!(pos[i][j] & (1 << k))) {
                        printf("%d,", k);
                    }
                }
            }
            printf("; ");
        }
        printf("\n");
    }
    */
    printf("-----------------\n");
    if (solve(0)) {
        for (unsigned i = 0; i < 9; ++i) {
            for (unsigned j = 0; j < 9; ++j) {
                printf("%d, ", out[i][j]);
            }
            printf("\n");
        }
    }
    else {
        printf("No solution.");
    }
    return 0;
}
```
