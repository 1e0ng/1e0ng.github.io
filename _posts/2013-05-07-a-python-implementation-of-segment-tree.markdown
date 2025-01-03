---
layout: post
title: "A Python Implementation of Segment Tree"
date: 2013-05-07 00:26
comments: true
categories:
- Algorithm


---

Today I need to use a data structure called [Segment Tree](http://en.wikipedia.org/wiki/Segment_tree).
A segment tree for a set I of n intervals uses $$ O(n \log{n}) $$ storage and can be built in $$ O(n \log{n}) $$ time.
Segment trees support searching for all the intervals that contain a query point in $$ O(\log{n} + k) $$, k being the number of retrieved intervals or segments.

While I search for a Python implementation of segment tree, there is no good ones. So I write one.

<!-- more -->

It's open sourced on [github](https://github.com/leonsim/segmenttree)

## How to install

```
pip install segmenttree
```

## How to use

{% highlight python linenos %}
from segmenttree import SegmentTree
segtree = SegmentTree(1, 8)
segtree.add(1, 3, 1)
segtree.add(3, 4, 1)
segtree.add(4, 5, 1)
segtree.add(3, 6, 2)
segtree.add(1, 71)
print(segtree.query_max(2, 5)) #This should print 5
print(segtree.query_len(2, 5)) #This should print 4
print(segtree.query_sum(2, 5)) #This should print 16

segtree = SegmentTree(0, 8)
segtree.add(1, 1, 1)
segtree.add(8, 8, 1)
print(segtree.query_max(0, 8)) #1
print(segtree.query_len(0, 8)) #2
print(segtree.query_sum(0, 8)) #2

{% endhighlight %}
