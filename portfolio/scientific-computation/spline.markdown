---
comments: true
date: 2008-04-24 16:07:34
layout: page
slug: spline
title: Spline
---

{% highlight matlab linenos %}
clear;
%2008.4.24
t=[-2 0 1];
A=[1 t(1) t(1)^2 t(1)^3 0 0 0 0;
   1 t(2) t(2)^2 t(2)^3 0 0 0 0;
   0 0 0 0 1 t(2) t(2)^2 t(2)^3;
   0 0 0 0 1 t(3) t(3)^2 t(3)^3;
   0 1 2*t(2) 3*t(2)^2 0 -1 -2*t(2) -3*t(2)^2;
   0 0 2 6*t(2) 0 0 -2 -6*t(2);
   0 0 2 6*t(1) 0 0 0 0;
   0 0 0 0 0 0 2 6*t(3)];
y=[-27;-1;-1;0;0;0;0;0];
x=A\y
syms t1 t2 p1 p2;
p1=0;p2=0;
for i=0:3
    p1=p1+x(i+1)*t1^i;
    p2=p2+x(i+5)*t2^i;
end
p1
p2
p3=diff(p1);
p4=diff(p2);
p5=diff(p3);
p6=diff(p4);
t1=-2:.1:0;
t2=0:.1:1;
p1=subs(p1);
p2=subs(p2);
p3=subs(p3);
p4=subs(p4);
p5=subs(p5);
p6=subs(p6);
y=[-27 -1 0];
plot(t1,p1,t1,p3,t1,p5,t2,p2,t2,p4,t2,p6,t,y,'o');
{% endhighlight %}
