---
layout: post
title: "Solve AutoCAD Chinese question mark issue"
date: 2016-06-15 18:28:52 +0800
comments: true
categories:
- Design
- Tools
---

This article describes a complicated issue when using AutoCAD, Chinese text shows as a question mark, and two common causes and a perfect solution.
<!--more-->

### Issue:

Chinese text shows as a question mark (?) when opening the file in AutoCAD as opposed to the actual symbols


### Causes:

Often this is caused by a missing font file (.shx). Actually I do have this problem, so I search and find the missing shx called `HZTXT.shx`, and put it under `shx` folder. However, this only solved part of the problem, and some Chinese text still shows as a question mark (?).

Another cause is the TEXT objects.  These objects cannot support multiple langues.  Within the Chinese version of Windows, the one and only language is Chinese.  On this platform, the TEXT object will display the proper characters.  When the file is opened on a non-Chinese operating system, the limitation is encountered.  When there is more than one language on the Windows Operating System, the TEXT object is still set to a different language.

### Solution:

MTEXT objects are able to support multiple languages.  You will want to use the TXT2MTXT (Express Tools) command to convert the TEXT objects to MTEXT objects.  If the TEXT objects are within a block, you will want to first enter the BLOCK EDITOR and then use the TXT2MTXT command.

### Convert multiple text individually

{% highlight lisp linenos %}
;changes text to individual mtext by Carl B.

(princ "\nType T2M to start")
(defun c:t2m ()
(setq Tset (ssget '((0 . "*TEXT")))) ;filter text in selection set
(setq	Setlen (sslength Tset) ;setq number of entties in selection set, setq count(er) to 0
Count 0
) ;setq
(repeat SetLen ;repeat setlen times
(setq Ename (ssname Tset Count)) ;setq ename to be the "0..." entity in selection set Tset
(command "_txt2mtxt" Ename "")
(setq Count (+ 1 Count)) ; add 1 to Count(er)
)	; Repeat	
(princ)
)
{% endhighlight %}

Copy the above code and paste to a file named `t2m.lsp`.


Add this file to startup suite contents.

Now you can use `T2M` command to process multiple TEXT to MTEXT individually.

