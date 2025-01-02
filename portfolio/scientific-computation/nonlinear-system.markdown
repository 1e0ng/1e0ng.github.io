---
comments: true
date: 2008-05-22 16:07:34
layout: page
slug: nonlinear-system
title: Nonlinear System
---

{% highlight matlab linenos %}
%2008.5.22
clear;
x1=100;x2=100;x3=100;
for n=1:500
    if x1==0 && x2==1/3 && x3==0 
        break
    end
    n
    y1=-cos(x1)/81+ x2*x2/9+sin(x3)/3;
    y2=sin(x1)/3+cos(x3)/3;
    y3=-cos(x1)/9+x2/3+sin(x3)/6;
    x1=y1
    x2=y2
    x3=y3
end
J=[sin(x1)/81 x2*2/9 cos(x3)/3;cos(x1)/3 0 -sin(x3)/3;sin(x1)/9 1/3 cos(x3)/6];
max(eig(J))
x1=1;x2=3;x3=3;
for n=1:100
    if x1==0 && x2==1/3 && x3==0 
        break
    end
    n
    J=[sin(x1)/81-1 x2*2/9 cos(x3)/3;cos(x1)/3 -1 -sin(x3)/3;sin(x1)/9 1/3 cos(x3)/6-1];
    f=[cos(x1)/81+x1-x2*x2/9-sin(x3)/3;-sin(x1)/3+x2-cos(x3)/3;+cos(x1)/9-x2/3-sin(x3)/6+x3];
    s=J\f;
    x1=x1+s(1)
    x2=x2+s(2)
    x3=x3+s(3)
end
{% endhighlight %}
