---
comments: true
date: 2012-08-09 11:30:52
layout: post
slug: replace-strings-for-files-in-a-folder
title: Replace Strings For All Files In a Folder
wordpress_id: 983
categories:
- Python
---


In my previous blog, I wrote the code to replace all string in a file: [http://leons.im/2011/02/replace-all-strings-in-a-file/](http://leons.im/2011/02/replace-all-strings-in-a-file/). Today, I write a cooler code -- It can replace all strings in many files, actually it can replace all strings in files that are in a same folder.

<!--more-->

Save the following code to the folder that you want to replace strings, and name it like `replace.py`.

Modify parameters `from_str`, `to_str` and `files_to_replace` in the form of regular expression.
Then run `python replace.py`.


``` python Replace Strings for All Files in a Folder
#!/usr/bin/python
import sys, os, re
#Created by Leon on Aug 9, 2012

from_str = r'\t'
to_str = r'    '
files_to_replace = r'.(h|m|mm|cpp|inl|def|txt|php|tpl|css|js|py)$'

def replace(infile, outfile):
    f1 = open(infile)
    f0 = open(outfile, 'w')
    data = f1.readlines()
    for line in data:
        f0.write(re.sub(from_str, to_str, line))
    f1.close()
    f0.close()

def walk_folder(path):
    print "Current Path: " + path
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if re.search(files_to_replace, filename):
                print "----" + filename + "...."
                fi = open(os.path.join(dirpath, filename))
                fo = open(os.path.join(dirpath, filename + ".bk"), 'w')
                fo.write(fi.read())
                fo.close()
                fi.close()
                replace(os.path.join(dirpath, filename + ".bk"),
                          os.path.join(dirpath, filename))
                print "Done."
                os.remove(os.path.join(dirpath, filename + ".bk"))

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    walk_folder(path)
    print
    print "All files have been translated successfully."
    print
    print "Created for you by Leon on Aug 9, 2012."
    raw_input()
```

