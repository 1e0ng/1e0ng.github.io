---
comments: true
date: 2008-04-30 16:07:34
layout: page
slug: squares
title: squares
---

{% highlight matlab linenos %}
clear;
%2008.4.30
t=[0.0;1.0;2.0;3.0;4.0;5.0];
y=[1.0;2.7;5.8;6.6;7.5;9.9];
n=5;
for i=1:6
    for j=0:n
        A(i,j+1)=t(i)^j;
    end
end
B=A'*A;
q=A'*y;
x=B\q;
syms b m;
b=0;
for i=1:n+1
   b=b+x(i)*m^(i-1);
end
m=-1:.05:6;
b=subs(b);
plot(t,y,'o',m,b);

{% endhighlight %}
