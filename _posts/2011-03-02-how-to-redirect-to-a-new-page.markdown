---
comments: true
date: 2011-03-02 17:09:56
layout: post
slug: how-to-redirect-to-a-new-page
title: How To Redirect to a New Page
wordpress_id: 406
categories:
- Web
tags:
- PHP
- Redirect
---

This is an example that shows how to redirect (forward) to a new page in PHP.

<!-- more -->
``` php PHP Redirect Code
<?php
    header("HTTP/1.1 301 Moved Permanently");
    header("Location: http://leons.im/about/");
?>
```

Note that with 301 error No., instead of 302 error No., your page is Search Engine Optimized, ie the search engine can retain the original page rank for your new page.
