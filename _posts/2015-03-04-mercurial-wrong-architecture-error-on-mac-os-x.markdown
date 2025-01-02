---
layout: post
title: "Mercurial wrong architecture error on Mac OS X"
date: 2015-03-04 20:24:47 +0800
comments: true
categories: articles
tags: 
---

If you install Mercurial(hg) via `brew install mercurial`, it succeeds to install, but when you run `hg` command, it fails with the following error message:

<!--more-->

```
leon@ls-mbp$  hg
Traceback (most recent call last):
  File "/usr/local/bin/hg", line 41, in <module>
    mercurial.util.setbinary(fp)
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/demandimport.py", line 106, in __getattribute__
    self._load()
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/demandimport.py", line 78, in _load
    mod = _hgextimport(_import, head, globals, locals, None, level)
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/demandimport.py", line 47, in _hgextimport
    return importfunc(name, globals, *args)
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/util.py", line 70, in <module>
    statfiles = getattr(osutil, 'statfiles', platform.statfiles)
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/demandimport.py", line 106, in __getattribute__
    self._load()
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/demandimport.py", line 78, in _load
    mod = _hgextimport(_import, head, globals, locals, None, level)
  File "/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/demandimport.py", line 47, in _hgextimport
    return importfunc(name, globals, *args)
ImportError: dlopen(/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/osutil.so, 2): no suitable image found.  Did find:
	/usr/local/Cellar/mercurial/3.3/lib/python2.7/site-packages/mercurial/osutil.so: mach-o, but wrong architecture
```

Then your Python most likely runs in 32-bit mode. To force Python to run in 64-bit mode, run this command:

```
defaults write com.apple.versioner.python Prefer-32-Bit -bool no
```
