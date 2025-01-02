---
comments: true
date: 2009-05-07 16:07:34
layout: page
slug: bezier
title: Bezier
---

{% highlight matlab linenos %}
%May,07,2009
clear all;
% Data Setting
r=[0 1 1.5 0];
w=[0.5 1 0.6 0.4];
n=4;
a=0;
b=1;
x=0:0.01:1;
m=length(x);
% Matrix Setting
Pn=zeros(1,m);
Rn=zeros(1,m);
Wn=zeros(1,m);
% Rational Bezier Curve
for j=1:m
    for i=1:n
        B(i)=nchoosek(n-1,i-1)*realpow(b-x(j),n-i)*realpow(x(j)-a,i-1);
        Pn(j)=Pn(j)+B(i)*w(i)*r(i);
        Wn(j)=Wn(j)+B(i)*w(i);
    end
    Rn(j)=Pn(j)/Wn(j);
end
%Calculate H_k
H(1:(2*n-3))=0;
for k=1:(2*n-3)
    for i=max(0,k-n+1)+1:fix((k-1)/2)+1
        H(k)=H(k)+(k-2*i+2)*nchoosek(n-1,i-1)*nchoosek(n-1,k-i+1)*w(i)*w(k-i+2)*(r(k-i+2)-r(i));
    end
end
% R'
R1(1:m)=0;
for j=1:m
    for k=1:(2*n-3)
        R1(j)=R1(j)+H(k)*realpow(b-x(j),2*n-3-k)*realpow(x(j)-a,k-1);
    end
end
R1=R1./Wn./Wn;
% Plot Graphic
plot(x,R1,'b');
legend('First Derivative of Rational Bezier Curve');
xlabel('t');
ylabel('R''(t)');
title(['First Derivative of Rational Bezier Curve']);
{% endhighlight %}


{% highlight matlab linenos %}
%May,09,2009
clear all;
% Data Setting
r=[0 1 1.5 0];
w=[0.5 1 0.6 0.4];
n=4;
a=0;
b=1;
x=0:0.01:1;
m=length(x);
% Matrix Setting
Pn=zeros(1,m);
Rn=zeros(1,m);
Wn=zeros(1,m);
% Rational Bezier Curve
for j=1:m
    for i=1:n
        B(i)=nchoosek(n-1,i-1)*realpow(b-x(j),n-i)*realpow(x(j)-a,i-1);
        Pn(j)=Pn(j)+B(i)*w(i)*r(i);
        Wn(j)=Wn(j)+B(i)*w(i);
    end
    Rn(j)=Pn(j)/Wn(j);
end
%Calculate H_k
H(1:(2*n-3))=0;
for k=1:(2*n-3)
    for i=max(0,k-n+1)+1:fix((k-1)/2)+1
        H(k)=H(k)+(k-2*i+2)*nchoosek(n-1,i-1)*nchoosek(n-1,k-i+1)*w(i)*w(k-i+2)*(r(k-i+2)-r(i));
    end
end
% R''
R3(1:m)=0;
for j=1:m
    z1=0;z2=0; z3=0; z4=0; z5=0; z6=0; z7=0;
    for i=1:n-1
        z1=z1+nchoosek(n-2,i-1)*realpow(b-x(j),n-i-1)*realpow(x(j)-a,i-1)*(w(i+1)-w(i));
    end
    for k=1:(2*n-3)
        z2=z2+realpow(b-x(j),2*n-3-k)*realpow(x(j)-a,k-1)*H(k);
    end
    for i=1:n-2
        z3=z3+nchoosek(n-3,i-1)*realpow(b-x(j),n-2-i)*realpow(x(j)-a,i-1)*(w(i+2)-2*w(i+1)+w(i));
    end
    for k=1:(2*n-3)
        z4=z4+H(k)*realpow(b-x(j),2*n-3-k)*realpow(x(j)-a,k-1);
    end
    for i=1:n-1
        z5=z5+nchoosek(n-2,i-1)*realpow(b-x(j),n-i-1)*realpow(x(j)-a,i-1)*(w(i)-w(i+1));
    end
    for k=1:(2*n-4)
        z6=z6+nchoosek(2*n-5,k-1)*realpow(b-x(j),2*n-4-k)*realpow(x(j)-a,k-1)*(H(k+1)/nchoosek(2*n-4,k)-H(k)/nchoosek(2*n-4,k-1));
    end
    for k=1:(2*n-5)
        z7=z7+nchoosek(2*n-5,k-1)*realpow(b-x(j),2*n-5-k)*realpow(x(j)-a,k-1)*(H(k+2)/nchoosek(2*n-4,k+1)-2*H(k+1)/nchoosek(2*n-4,k)+H(k)/nchoosek(2*n-4,k-1));
    end
    R3(j)=6*(n-1)*(n-1)*z1*z1*z2+2*(n-1)*(n-2)*Wn(j)*z3*z4+8*(n-1)*(n-2)*Wn(j)*z5*z6+(2*n-4)*(2*n-5)*Wn(j)*Wn(j)*z7;
end
R3=R3./Wn./Wn./Wn./Wn;
% Plot Graphic
plot(x,R3,'b');
legend('Third Derivative of Rational Bezier Curve');
xlabel('t');
ylabel('R''''''(t)');
title(['Third Derivative of Rational Bezier Curve']);
{% endhighlight %}
