---
comments: true
date: 2008-04-02 21:44:34
layout: page
slug: gaussian
title: gaussian
---

{% highlight matlab linenos %}
A=[21.0 67.0 88.0 73.0;
76.0 63.0 7.0 20.0;
0.0 85.0 56.0 54.0;
19.3 43.0 30.2 29.4];
b=[141.0;109.0;218.0;93.7];
%2008-04-02  21:44
B=A;
c=b;
for k=1:length(A)-1
    p=k;
    for j=k+1:length(A)
        if A(j,k)>A(p,k)
            p=j;
        end
    end
    if p~=k
        for j=1:length(A)
            t=A(p,j);
            A(p,j)=A(k,j);
            A(k,j)=t;
        end
        t=b(p);
        b(p)=b(k);%At the same time ,this should be changed.
        b(k)=t;
    end
    if A(k,k)==0
        continue;
    end
    for i=k+1:length(A)
        A(i,k)=A(i,k)/A(k,k);
    end
    for j=k+1:length(A)
        for i=k+1:length(A)
            A(i,j)=A(i,j)-A(i,k)*A(k,j);
        end
    end
end
for j=1:length(A)
     y(j)=b(j);
     for i=j+1:length(A)
         b(i)=b(i)-A(i,j)*y(j);
     end
end
for j=length(A):-1:1
    if A(j,j)==0
        break;
    end
    x(j)=y(j)/A(j,j);
    for i=1:j-1
        y(i)=y(i)-A(i,j)*x(j);
    end
end

x=x'
r=single(c-B*x)
{% endhighlight %}
