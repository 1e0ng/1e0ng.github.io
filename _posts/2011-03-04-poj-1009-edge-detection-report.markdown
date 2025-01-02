---
comments: true
date: 2011-03-04 16:08:09
layout: post
slug: poj-1009-edge-detection-report
title: POJ 1009 Edge Detection Report
wordpress_id: 422
categories: articles
tags:
- Problems
tags:
- '1009'
- POJ
- Report
---

View the problem at POJ: [1009 Edge Detection](http://poj.org/problem?id=1009).

The answer should be in format of Run Time Encoding. Let val[i] be the value, and len[i] be the length of the i-th pair. There is a corresponding location for each pair, ie the start point, and let row[i] be the row, and col[i] be the column of the start point for the i-th pair.

<!-- more -->
First, let's prove this proposition: Each start point to output is adjacent to at least one start point from input.

(Here adjacent means the difference between their compressed location is WIDTH - 1, WIDTH + 1, 1, -1, 0. Here compressed location of a point means the row of the point multiplied by WIDTH and plus the column of the point. "WIDTH" is the variable "width" from input.)

Well, to prove the proposition directly is not easy, so let's prove the contraposition, ie if a point is not adjacent to any start point from input, then the point is not a start point to output.

Assume x is such a point, as the following shows.

```
................
...a  b  c...
...d  x  e...
...f   g  h...
................

```

As x is not adjacent to any start point from input, a must be equal to b. (Because if not, b should be a start point from input, and x is adjacent to b.) Similarly, b must be equal to c, and d must be equal to x and e, and f must be equal to g and h. So the above image can be displayed below:

```
................
...a  a  a...
...d  x  d...
...f   f   f...
.................

(x = d)
```

The character precedent to the first "a" should also be "a", because if not the first a showing in above picture is a start point, and x is adjacent to it. Similarly, d and f should also has a precent equal to itself.

So, let's expand the picture:

```
.......................
...a  a   a   a...
...d  d  x   d...
...f   f   f    f...
.....................
```

Now we can calculate the value of the "d" adjacent to "x".

The value of "d" adjacent to "x" = max { |a - d|, |d - f| }.

We can also calculate the value of "x".(Note x = d.)

The value of "x" = max { |a - d|, |d - f| }.

So, the value of "x" = the value of "d" adjacent to "x", and therefore "x" is not a start point to output. (A start point must have a different value from its precedent.)

Hence we prove the proposition.

Also note some cases when "x" is at column 1, as following shows.

```
.......
a  ...
x  ...
f  ...
.......
```

You will find these cases can also be proved as soon as you proved the above common cases. :)


Source Code:


``` cpp POJ 1009 Edge Detection

#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <cmath>
using namespace std;

#define N 1010
int inData[N][2];
struct node{
    int val, pos;
} outData[N * 9];

int inNum, outNum, total, width;

bool cmp(const node &n1, const node &n2) {
    return n1.pos < n2.pos;
}

int getValue(int loc) {
    int low = 0, high = inNum - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (inData[mid][1] <= loc) {
            low = mid + 1;
        }
        else {
            high = mid - 1;
        }
    }
    //printf("high = %dn", high);
    return inData[high][0];
}

int cal(int loc) {
    int row, col, i, j, ret = 0;
    row = loc / width;
    col = loc % width;
    for (i = row - 1; i <= row + 1; ++i) {
        for (j = col - 1; j <= col + 1; ++j) {
            int p = i * width + j;
            if (i < 0 || j < 0 || j >= width || p >= total || p == loc) {
                continue;
            }
            int q = abs(getValue(p) - getValue(loc));
            //printf("q = %d, p = %d, loc = %d,n", q, p, loc);
            if (q > ret) {
                ret = q;
            }
        }
    }
    return ret;
}

void solve() {
    int i, j, k, row, col;
    outNum = 0;
    for (i = 0; i <= inNum; ++i) {
        row = inData[i][1] / width;
        col = inData[i][1] % width;
        for (j = row - 1; j <= row + 1; ++j) {
            for (k = col - 1; k <= col + 1; ++k) {
                int p = j * width + k;
                if (j < 0 || p >= total || p < 0) {
                    continue;
                }
                outData[outNum].val = cal(p);
                outData[outNum].pos = p;
                ++outNum;
            }
        }
    }
    for (i = 0; i < outNum; ++i) {
        //printf("%d, %d\n", outData[i].val, outData[i].pos);
    }
    sort(outData, outData + outNum, cmp);
    node cur = outData[0];
    for (i = 0; i < outNum; ++i) {
        if (cur.val == outData[i].val) {
            continue;
        }
        printf("%d %d\n", cur.val, outData[i].pos - cur.pos);
        cur = outData[i];
    }
    printf("%d %d\n", cur.val, total - cur.pos);
    printf("0 0\n");
}

int main() {
    //freopen("in.txt", "r", stdin);
    while (scanf("%d", &width) != EOF && width) {
        printf("%d\n", width);
        int i = 0, j;
        total = 0;
        while (scanf("%d%d", &inData[i][0], &inData[i][1]) != EOF) {
            j = inData[i][1];
            inData[i][1] = total;
            total += j;
            if (0 == j) break;
            ++i;
        }
        inNum = i;
        solve();
    }
    printf("0\n");
    return 0;
}
```

