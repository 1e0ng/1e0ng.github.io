---
comments: true
date: 2011-07-08 10:18:09
layout: post
slug: check-if-a-string-contains-chinese-characters
title: Check If a String Contains Chinese Characters
wordpress_id: 678
categories:
- Python
tags:
- Character
- Chinese
- GBK
- Python
- Unicode
- UTF-8
---

Transfer the string to Unicode and since Chinese is between 0x4e00 and 0x9fff, just check if there is a character in this range.

<!--more-->

``` python Check If a String Contains Chinese Characters
#coding=utf-8
#!/usr/bin/python

#This code is intended for Python 2.7

#Copy this file in the folder where
#you want to abstract Chinese from files

#Created by Leon on July, 7, 2011
#http://leons.im

import sys, os, codecs, glob, re

fout = codecs.open("out.txt", "wb", "gbk")
num = 1
def record(bn, ln, line):
	global num
	for i in line:
		if ord(i) >= 0x4e00 and ord(i) <= 0x9fff:
			print line
			fout.write('%d:%s:%d:%s\r\n' % (num, bn, ln, line))
			num = num + 1
			break

def transcode(infile):
    print "infile = " + infile

    fin = codecs.open(infile, "rb", "gbk")
    ln = 1
    bn = os.path.basename(infile)
    try:
    	for line in fin.readlines():
    		m = re.search(r'^s*//', line)
    		if m:
    			continue
    		m = re.search(r'_T("([^)]*)")', line)
    		if m and len(m.group(1)) > 0:
    			record(bn, ln, m.group(0))
        	m = re.search(r'L"([^"]*)"', line)
        	if m and len(m.group(1)) > 0:
        		record(bn, ln, m.group(0))
        	ln = ln + 1
    except:
    	print "error."
    fin.close()

path = os.path.abspath(os.path.dirname(sys.argv[0]))
print "Current Path: " + path

for dirpath, dirs, files in os.walk(path):
    for filename in files:
        if re.search(r".(h|m|mm|cpp|inl|def|txt)$", filename):
            print "----" + filename + "...."
            transcode(os.path.join(dirpath, filename))
            print "Done."
print
print "Created for you by Leon on July, 7, 2011."
fout.close()
raw_input()
```
