---
comments: true
date: 2011-05-03 12:12:19
layout: post
slug: calling-non-const-member-functions-from-const-member-functions
title: Calling Non-const Member Functions from Const Member Functions
wordpress_id: 641
categories: articles
tags:
- C
---

Compare the following two segments of codes. Which do you think is better?

<!--more-->

{% highlight cpp linenos %}
class Array{
private:
       int a[100];
public:
       Array(){}
       int & at(int index){
           return a[index];
       }
       const int & at(int index) const  {
             return const_cast<Array*>(this)->at(index);
       }
};
{% endhighlight %}

{% highlight cpp linenos %}
class Array{
private:
       int a[100];
public:
       Array(){}
       const int & at(int index)const {
             return a[index];
       }
       int & at(int index){
           return const_cast<int&>(
                  const_cast<const Array *>(this)->at(index));
       }
};
{% endhighlight %}
