---
comments: true
date: 2008-05-14 16:07:34
layout: page
slug: newton-iteration
title: Newton Iteration
---

{% highlight matlab linenos %}
%2008.5.14
clear;
syms y x z;
y=x^2-1;
z=x-y/diff(y);
t=10^6
for i=1:30
    i
    t=subs(z,x,t)
    if t==1
        break;
    end
end
{% endhighlight %}

{% highlight matlab linenos %}
%2008.5.14
clear;
syms y x z;
y=(x-1)^4;
z=x-y/diff(y);
t=10
for i=1:50
    i
    t=subs(z,x,t)
    if t==1
        break;
    end
end
{% endhighlight %}
