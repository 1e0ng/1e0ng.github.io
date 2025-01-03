---
comments: true
date: 2011-12-27 23:43:00
layout: post
slug: do-not-use-inline-block-in-css
title: Do Not Use inline-block in CSS (Obsolete)
wordpress_id: 905
categories:
- Frontend
- CSS
tags:
- CSS
- display
- float
- inline-block
---

UPDATE: As Vensires mentions in the comment, this post is obsolete.

Usually, when we want to arrange some blocks horizontally with CSS, we may choose to use `float: left;` property, or `display: inline-block;` alternatively.

According to [http://www.quirksmode.org/css/display.html](http://www.quirksmode.org/css/display.html), inline-block is not supported by IE 5.5 and it's not completely supported by IE 6 and IE 7.

<!--more-->

[![](/uploads/2011-12-display.png)](/uploads/2011-12-display.png)

So, don't use `display: inline-block;`, it will mess up your page on some browsers. Use `float: left;` instead.

Here is an example:

Instead of using this,

``` css
.block1 {
    width: 100px;
    height: 30px;
    display: inline-block;
}
.block2 {
    width: 400px;
    height: 30px;
    display: inline-block;
}
```

we'd better to use use this,

``` css
.block1 {
    width: 100px;
    height: 30px;
    float: left;
    display: block;
}
.block2 {
    width: 400px;
    height: 30px;
    float: left;
    display: block;
}
```

Update: Don't forget to use `clear:both;` with `float:left;`.
