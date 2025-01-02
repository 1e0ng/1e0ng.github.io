---
comments: true
date: 2011-05-01 23:32:27
layout: post
slug: a-discrete-cosine-transform-demo
title: A Discrete Cosine Transform Demo
wordpress_id: 614
categories: articles
tags:
- Math
---

The Discrete Cosine Transform ([DCT](http://en.wikipedia.org/wiki/Discrete_cosine_transform)) algorithm constitutes an integral component of contemporary image/video processing applications.

The formal definition of DCT is:

$$ X_k = \sum\limits_{n=0}^{N-1}{x_n}\cos{\left[\dfrac{\pi}{N}\left(n+\dfrac12\right)k\right]}\quad k=0,\ldots,N-1. $$

<!--more-->

In [JPEG](http://en.wikipedia.org/wiki/JPEG) standard, DCT algorithm is used to transform images to a set of independent parts (to reduce the [entropy](http://en.wikipedia.org/wiki/Entropy)), and only after that can the image be quantized to decrease the number of bits to represent the image.

Note that DCT is a lossless transformation, and only the quantization remove some less important data.

The following demo, which is written in Matlab, demonstrates that DCT is lossless, because data is transformed and then restored to original data.

``` matlab    
%DCT Demo
%Created by Leon
%http://leons.im
%May,1,2011
N=8;
fx=[3 89 23 11 0 82 854 23];
a0=sqrt(1/N);
a1=sqrt(2/N);
au=[a0 a1 a1 a1 a1 a1 a1 a1];
cosu=cos(((2*linspace(0,N-1,N)+1)*acos(-1)/2/N)'*linspace(0,N-1,N));
cu=au.*(fx*cosu)
gx=(au.*cu)*(cosu')
```

The result is:

``` matlab    
gx =

    3.0000   89.0000   23.0000   11.0000    0.0000   82.0000  854.0000   23.0000
```

As you can see, `gx=fx`, therefore DCT is lossless.

If you want to learn DCT, this is best tutorial book: [The Discrete Cosine Transform (DCT): Theory and Application](http://www.wisnet.seecs.edu.pk/publications/tech_reports/DCT_TR802.pdf)
