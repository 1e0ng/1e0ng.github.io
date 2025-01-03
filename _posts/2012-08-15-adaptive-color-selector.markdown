---
comments: true
date: 2012-08-15 15:42:00
layout: post
slug: adaptive-color-selector
title: Adaptive Color Selector
wordpress_id: 987
categories:
- Frontend
- Javascript

tags:
- Adaptive Color Selector
- Dark Color
- JS
- Light Color
- Luminance

---

This is an adaptive color selector. It can dynamically choose which color of checkmark to use. When a light color is chosen, a black checkmark display; while when dark color is chosen, a white checkmark display.

Here is a screenshot.
<!-- more --> 

[![](/uploads/2012-08-color-selector.png)](/uploads/2012-08-color-selector.png)

To implement this feature, I calculte the luminance of the color and then decide which color of checkmark to use. According to [Wikipedia](http://en.wikipedia.org/wiki/Luminance_(relative)), the formula of lumaninace for RGB color is:
$$
Y = 0.2126 R + 0.7152 G + 0.0722 B
$$
An example of segment of html code:

{% highlight html linenos %}
<!-- An example of segment of html code -->
<div class="color-tag on" style="background:#ccc;">
    <img src="/static/select_white.png">
</div>
<div class="color-tag on" style="background:#353fd9;">
    <img src="/static/select_white.png">
</div>
<div class="color-tag on" style="background:#f60409;">
    <img src="/static/select_white.png">
</div>
{% endhighlight %}

{% highlight javascript linenos %}
<script>
$(function(){
        $('.color-tag.on').each(function(){
            var rgb = $(this).prev().css('background-color');
            rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
            var luminance = parseInt(rgb[1])*0.2126 + parseInt(rgb[2])*0.7152 + parseInt(rgb[3])*0.0722;
            if (luminance > 192) {
                $(this).html('<img src="/static/select_black.png">');
            }
        });
});
</script>
{% endhighlight %}
