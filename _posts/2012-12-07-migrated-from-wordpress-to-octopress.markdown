---
layout: post
title: "Migrated From Wordpress to Octopress"
date: 2012-12-07 22:57
comments: true
categories:
- Web
---

This blog has migrated from Wordpress to Octopress.
Compared with Wordpress, Octopress has a lot of overwhelming advantages.

<!--more-->
* No database, so you don't need to back up database, and you can use github or bitbucket to control your all files.
* No dymaic page, so you don't PHP server. All you need is to set up Nginx. This allows more concurrent access to your website.
* Posting more effitiently. I like the process and interaction of posting an article with Octopress. Use command `rake new_post["BLOG TITLE"]` to generate a template, and with any editor like `emacs` or `vim` to edit my article. Use `rake generate` to generate html file according to the source file, and then `rake deploy` to deploy to the server. Don't you think that's so cool? Don't forget to commit to your version control system.
* Markdown format. This is a format easier to write and read than html for human being. Use it. Trust me.

## How?

If you start a new blog, just use Octopress, but if you already have a wordpress blog like me, it's not so easy to migrate to Octopress. At least don't forget to do the following things:

* Use [exitwp](https://github.com/thomasf/exitwp) to convert the XML file, which is exported from wordpress, to Markdown format files.
* Use [Disqus](http://www.disqus.com/) to manage comments in your blog.
* Modify code block. [http://octopress.org/docs/blogging/code/](http://octopress.org/docs/blogging/code/)
* Define each post with at most one category, if you prepare to configure your blog urls with categories as a part.
* Write a script to check each link in your blog valid. Use [Nginx rewrite](http://wiki.nginx.org/HttpRewriteModule) to forward old links to new links. Also write a URL Maper file (mapping from old links to new links) and submit it to Disqus, where there is a [migratino tool](http://www.disqus.com/admin/tools/migrate/) to do such things.
* Use [Google Analytics](http://www.google.com/analytics/) and [Google Webmaster Tools](https://www.google.com/webmasters/tools/) to minitor your website. Correct warnings and errors they inform you.
