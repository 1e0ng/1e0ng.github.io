---
layout: post
title: "Modify Java .class in a .jar"
date: 2015-12-19 01:38:11 +0800
comments: true
categories: articles
tags:
- Security
- Java
---

Sometimes I need to know what's inside to figure out a best solution, like modifying a Java `.class` file in a `.jar` file.
After searching google and stack overflow for a while, I found this question is little cared, and almost all information is not complete.
So I wrap them up and make the whole process runnable.

<!-- more -->

Use luyten (or JD GUI if you don't care its bugs) to decompile the jar, and save all files to folder `srcdir`

Modify a java file, then compile it to `.class` file.


```
cd srcdir
vi com/.../A.java
cp some_folder/original.jar ./
javac -cp "original.jar" com/.../A.java
```

The last command will generate a file named `A.class` in the same folder as `A.java`

Use luyten to check if the file `A.class` is modified.

```
jar -uf original.jar com/.../A.class
mv original.jar modified.jar
```

This will generate a `modified.jar`. Use luyten to check again if it's modified.

Note: If `A.java` depends other external jars other than `original.jar`, Add them to classpath by

```
javac -cp "original.jar;lib/*" com/.../A.java
```

It's important to use `lib/*` rather than `lib/*.jar` because the later will not work.
