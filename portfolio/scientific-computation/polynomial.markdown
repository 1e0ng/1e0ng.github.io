---
comments: true
date: 2008-04-16 16:07:34
layout: page
slug: polynomial
title: polynomial
---

{% highlight matlab linenos %}
%2008.4.16
clear;
t=[0.0 0.5 1.0 6.0 7.0 9.0]
y=[0.0 1.6 2.0 2.0 1.5 0.0]
for i=1:6
    for j=0:5
        A(i,j+1)=t(i)^j;
    end
end
x=A\y';
syms m n;
m=0;
for i=0:5
    m=m+x(i+1)*n^i;
end
m
n=0:.1:9;
m=subs(m);
plot(n,m);
%plot(t,y,'d');

{% endhighlight %}
