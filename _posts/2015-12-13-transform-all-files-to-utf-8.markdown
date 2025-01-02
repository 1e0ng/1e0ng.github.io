---
layout: post
title: "Transform all files to UTF-8"
date: 2015-12-13 17:59:33 +0800
comments: true
categories:
- Python
---

I wrote a [blog](/posts/python-script-to-transform-shift-jis-to-utf-8-encoding/) several years ago about transform all files in a folder recursively from one encoding to another. Today I decide to solve this issue more completely.


I wrap all this to a Python egg package, upload it to PyPi, and everyone who want to use this don't need to copy & paste code any more. Just install it and use it.


```
pip install toutf8
```

This ships with a shell command, so after installing, just type

```
toutf8 FILENAME
```
to transform a single file to UTF-8 encoding, or

```
toutf8 PATHNAME
```

<!-- more -->

to transform all files in folder PATHNAME to UTF-8 encoding.

The script can detect the source encoding, so whether it being GBK, GB2312, GB18030, CP936 or Shift-jis, all will be transformed to UTF-8.

```
GBK        --> UTF-8
GB2312     --> UTF-8
GB18030    --> UTF-8
CP936      --> UTF-8
Shift-jis  --> UTF-8
Euc-jp     --> UTF-8
Korean     --> UTF-8
Vietnamese --> UTF-8
UTF-16LE   --> UTF-8
UTF-16BE   --> UTF-8
UTF-32     --> UTF-8
```

### Advance usage

Use a regular expression to filter out which kinds of files should be transformed.

```
toutf8 PATHNAME .*txt
```
