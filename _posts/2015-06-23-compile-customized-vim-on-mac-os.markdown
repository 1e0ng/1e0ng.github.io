---
layout: post
title: "Compile Customized Vim on Mac OS"
date: 2015-06-23 18:11:23 +0800
comments: true
categories:
- Tools
---

For Mac OS developers, it's essential to build your own arsenal.
For most Linux utilities missed on Mac OS, just use `homebrew` to install.
There is one exeption I make: Vim.

There is an integrated Vim on Mac OS, and also several brew version of Vim for choose.
However, sometimes you find you have to compile Vim by source code,
for getting the latest version of Vim, for customizing some configuration, for using some special features, or something else.

<!--more-->
After struggling with issues several times, I decide to write the process down.

First download the source code via `hg`

{% highlight bash linenos %}
git clone https://github.com/vim/vim.git

cd vim
git fetch
git merge
{% endhighlight %}

Then configure, make and install.

{% highlight bash linenos %}
make distclean
make clean
./configure --enable-rubyinterp --enable-python3interp  --enable-luainterp --with-lua-prefix=/usr/local --without-x --with-compiledby="Leon <i@leons.im>"
make
sudo make install
{% endhighlight %}

Done.
