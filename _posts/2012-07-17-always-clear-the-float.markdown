---
comments: true
date: 2012-07-17 16:15:34
layout: post
slug: always-clear-the-float
title: Always "Clear" The "Float"
wordpress_id: 974
categories:
- Frontend
- CSS

---

Unless you really want to use Block Formatting Context, it's usually a good idea to clear the float.

<!--more-->

Look at the following html code:


{% highlight html linenos %}
<ul class="list">
    <li>
        One
    </li>
    <li>
        Two
    </li>
</ul>
{% endhighlight %}

And the corresponding css code:

{% highlight css linenos %}
ul.list{
    background-color:#369;
}
ul.list li{
    float:left;
}
{% endhighlight %}


The background-color style of the ul.list won't work at all.
Because the height of ul.list is 0.
Just add a "clear" div will fix this tricky.
Here is the right html code:

{% highlight html linenos %}
<ul class="list">
    <li>
        One
    </li>
    <li>
        Two
    </li>
    <div class="clear">
    </div>
</ul>
{% endhighlight %}


And add the following code to the css file:

{% highlight css linenos %}
.clear{
    clear:both;
}
{% endhighlight %}
