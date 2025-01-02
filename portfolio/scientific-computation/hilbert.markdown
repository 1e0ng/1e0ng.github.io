---
comments: true
date: 2008-04-02 21:44:34
layout: page
slug: hilbert
title: hilbert
---

{% highlight matlab linenos %}
x=0;
A=0;
c=0;
for n=1:20
    n
for i=1:n
    for j=1:n
        A(i,j)=1/(i+j-1);
    end
    x(i)=1;
end
b=A*x';
%2008-04-02  21:44
B=A;
c=b;
for k=1:n-1
    p=k;
    for j=k+1:n
        if A(j,k)>A(p,k)
            p=j;
        end
    end
    if p~=k
        for j=1:n
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
    for i=k+1:n
        A(i,k)=A(i,k)/A(k,k);
    end
    for j=k+1:n
        for i=k+1:n
            A(i,j)=A(i,j)-A(i,k)*A(k,j);
        end
    end
end
for j=1:n
     y(j)=b(j);
     for i=j+1:n
         b(i)=b(i)-A(i,j)*y(j);
     end
end
for j=n:-1:1
    if A(j,j)==0
        break;
    end
    x(j)=y(j)/A(j,j);
    for i=1:j-1
        y(i)=y(i)-A(i,j)*x(j);
    end
end
x
r=max(c-B*x')
c(n)=cond(B);
c(n)
is=0;
for i=1:n
    x(i)=x(i)-1;
    if x(i)>1 
        is=1;
    end
end
if is==1
    break;
end

end
x=1:n;
%for i=1:n
%    c(i)
%end
plot(x ,c);
{% endhighlight %}
