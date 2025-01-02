---
comments: true
date: 2011-08-24 23:27:00
layout: post
slug: resolve-hg-conflicts-manually
title: Resolve Hg Conflicts Manually
wordpress_id: 729
categories: articles
tags:
- Skills
- Hg

---

This artical tells about a simple method to resolve Hg conflicts. It doesn't use any 3-party tool to merge your code, but only use emacs to edit your conflicts file and tag a resolved tag. So don't apply it to merge big files with a lot of conflicts.

<!--more-->
When you pull code from the hg server, you get new changesets. 

``` bash    
$ hg pull
--------------------------------------------
pulling from http://***/hg_server
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
(run 'hg update' to get a working copy)
```

It notifies you to run `hg update`. 

{% highlight bash linenos %}
$ hg up
----------------------------------------
merging ***
warning: conflicts during merge.
merging a.php failed!
0 files updated, 0 files merged, 0 files removed, 1 files unresolved
{% endhighlight %}

Conflict happens. That means another guy modified the same file and he or she has pushed the file into the hg server. Don't worry, let's edit the file to make it right. 

``` bash    
$ emacs a.php
```

After that, we should let hg know we have resolved the conflict file. 

``` bash    
$ hg resolve -m test.php
```

OK, that' all. You can commit and push your code to hg server now. 

``` bash    
$ hg st
--------------------
M test.php
$ hg ci -m 'Add a test script.'
-------------------------------------
$ hg push
----------------------------------
pushing to http://***/hg_server
searching for changes
remote: adding changesets
remote: adding manifests
remote: adding file changes
remote: added 1 changesets with 1 changes to 1 files
```
