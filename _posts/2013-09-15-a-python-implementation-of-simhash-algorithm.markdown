---
layout: post
title: "A Python Implementation Of Simhash Algorithm"
date: 2013-09-15 00:10
comments: true
categories:
- Algorithm

---

Recently I'm reading an exellent paper: [Detecting Near-Duplicates for Web Crawling](http://www.wwwconference.org/www2007/papers/paper215.pdf), by Gurmeet Singh Manku, Arvind Jain and Anish Das Sarma.

The interesting of simhash algorithm is its two properties:
{% quote %}
Properties of simhash: Note that simhash possesses two conicting properties: (A) The fingerprint of a document is a "hash" of its features, and (B) Similar documents have similar hash values.
{% endquote %}

Maybe it's because of the beauty of the algorithm, I find myself implementing it. <https://github.com/leonsim/simhash>

<!--more-->

## Getting Started

```
pip install simhash
(or: easy_install simhash)
```


View simhash value:

```python
import re
from simhash import Simhash
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

print '%x' % Simhash(get_features('How are you? I am fine. Thanks.')).value
print '%x' % Simhash(get_features('How are u? I am fine.     Thanks.')).value
print '%x' % Simhash(get_features('How r you?I    am fine. Thanks.')).value

```

Get distance of two simhash:

```python
from simhash import Simhash
print Simhash('aa').distance(Simhash('bb'))
print Simhash('aa').distance(Simhash('aa'))
```

## Use the Simhash Index

Use the SimhashIndex to query near duplicates objects in a very efficient way.

```python
import re
from simhash import Simhash, SimhashIndex
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

data = {
    1: u'How are you? I Am fine. blar blar blar blar blar Thanks.',
    2: u'How are you i am fine. blar blar blar blar blar than',
    3: u'This is simhash test.',
}
objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
index = SimhashIndex(objs, k=3)

print index.bucket_size()

s1 = Simhash(get_features(u'How are you i am fine. blar blar blar blar blar thank'))
print index.get_near_dups(s1)

index.add('4', s1)
print index.get_near_dups(s1)
```


## Source Code

View [Source Code](https://github.com/leonsim/simhash) at GitHub.
