---
comments: true
date: 2012-10-10 00:48:46
layout: post
slug: how-to-add-pinterest-google-1-facebook-like-tweet-to-prestashop
title: How To Add Pinterest, Google +1, Facebook Like, Tweet to Prestashop
wordpress_id: 1071
categories: articles
tags:
- Frontend
- Javascript
- Web

tags:
- Facebook like
- Google +1
- Pin it
- Prestashop
- Tweet
---

Connecting prestashop to social network will bring more customers and draw more attentions. Which social network is best for a website? My answer is why not add them all.
<!-- more -->
First, add the following code to where you want to show Pin it button, Google +1 button, Facebook like button and Tweet button (for example, in the product.tpl file): 

{% highlight html linenos %}
<!-- Pinterest Pin it button -->
<div>
    <a href="<a href="http://pinterest.com/pin/create/button/?url={">http://pinterest.com/pin/create/button/?url={</a>$link->getProductLink($product->id, $product->link_rewrite)}&media={$link->getImageLink($product->link_rewrite, $cover.id_image, 'large')}&description={$product->name|escape:'htmlall':'UTF-8'}" class="pin-it-button" count-layout="horizontal" always-show-count="true"><img border="0" src="//assets.pinterest.com/images/PinExt.png" title="Pin It" /></a>
</div>

<!-- Facebook like button -->
<div>
    <div class="fb-like" data-href="{$link->getProductLink($product->id, $product->link_rewrite)}" data-send="false" data-layout="button_count" data-width="100" data-show-faces="true"></div>
</div>
<!-- Twitter tweet button -->
<div>
    <a href="<a href="https://twitter.com/share"">https://twitter.com/share"</a> class="twitter-share-button" data-lang="en" data-url="{$link->getProductLink($product->id, $product->link_rewrite)}" data-text="{$product->name}">Tweet</a>
</div>
<!-- Google +1 button -->
<div>
    <g:plusone href="{$link->getProductLink($product->id, $product->link_rewrite)}" size="medium"></g:plusone>
</div>
{% endhighlight %}



Second, add the following code to the place right before </body> tag in same file(in this case, the product.tpl file): 

``` javascript    
<!-- Pinterest js file -->
<script type="text/javascript" src="//assets.pinterest.com/js/pinit.js">
</script>

<p><!-- Google +1 js file --> 
<script type="text/javascript"> 
    window.___gcfg = { 
        lang: 'en-US' 
    };
(function() { 
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true; 
    po.src = '<a href="https://apis.google.com/js/plusone.js';">https://apis.google.com/js/plusone.js';</a> 
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s); 
})(); 
</script>
<!-- Twitter js file --> 
<script> 
    !function(d,s,id){ 
        var js,fjs=d.getElementsByTagName(s)[0]; 
        if(!d.getElementById(id)){ 
            js=d.createElement(s); 
            js.id=id; 
            js.src="//platform.twitter.com/widgets.js"; 
            fjs.parentNode.insertBefore(js,fjs); 
        } 
    }(document,"script","twitter-wjs"); 
</script>
<!-- Facebook js file --> 
<div id="fb-root"></div> 
<script>(function(d, s, id) { 
    var js, fjs = d.getElementsByTagName(s)[0]; 
    if (d.getElementById(id)) return; 
    js = d.createElement(s); js.id = id; 
    js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=174052042732019"; 
    fjs.parentNode.insertBefore(js, fjs); 
}(document, 'script', 'facebook-jssdk')); 
  </script>
```

