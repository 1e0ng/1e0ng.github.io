---
comments: true
date: 2008-03-20 16:07:34
layout: page
slug: cholesky
title: Cholesky
---

{% highlight matlab linenos %}
n=3;
x=0;
for i=1:n
    for j=1:n
        A(i,j)=1/(i+j-1);
    end
    x(i)=1;
end
x=x';
b=A*x;
c=b;
B=A;
A
b
for k=1:length(A)
    A(k,k)=sqrt(A(k,k));
    for i=k+1:length(A)
        A(i,k)=A(i,k)/A(k,k);
    end
    for j=k+1:length(A)
        for i=k+1:length(A)
            A(i,j)=A(i,j)-A(i,k)*A(j,k);
        end
    end
end
for i=1:length(A)
    for j=i+1:length(A)
        A(j,i)=A(i,j);
    end
end
A

for j=1:length(A)
     y(j)=b(j)/A(j,j);
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
x
r=single(c-B*x)
{% endhighlight %}
