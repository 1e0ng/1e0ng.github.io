---
layout: post
title: "Write LaTeX in Octopress with MathJax"
date: 2014-04-13 15:08:24 +0800
comments: true
categories:
- Web
- Math
---

The easiest method is to add by Mathjax CDN, but the drawback are it's not always stable and it doesn't work if you want to develop offline and want to preview via the `rake preview` command. So I have to embed a customized version of Mathjax into Octopress. With this method, I can preview equations offline and it's more stable -- it doesn't depend on the public CDN of Mathjax. OK, DIY start.

<!--more -->

## Install Mathjax

 Before doing this, it's a good idea to fork Octopress to your own repositories, so that you can make changes on it and save the configuration.


With Octopress, it is easy to custom the header file. Open the file `source/_includes/custom/head.html`, and add the following lines:

{% highlight html linenos %}
<script src="{{ root_url }}/mathjax/unpacked/MathJax.js"></script>
{% endhighlight %}


Then cd to the `source/` folder and add Mathjax as a submodule:

{% highlight sh linenos %}
git submodule add git://github.com/leonsim/MathJax.git mathjax
{% endhighlight %}


Here I use my forked MathJax repository, because I did some hack job ;-) Of course you can use the official repository, it's [here](git://github.com/mathjax/MathJax.git).

## Install rdiscount With LaTeX Support

The official rdiscount doesn't support LaTeX, while there are some other MarkDown rendering engines like kramdown, Pandoc etc, but these soltions either don't support the `$$ ` and ` $$` LaTex delimiters, which is my favourite writing style, or they only support the `$` or `$$` delimiters, and don't support the inline equation, which I can not endure, so I forked it and added LaTeX support. If you want to know how it works: [https://github.com/leonsim/rdiscount/commits/master](https://github.com/leonsim/rdiscount/commits/master).


{% highlight sh linenos %}
git clone git://github.com/leonsim/rdiscount.git
cd rdiscount
gem build rdiscount.gemspec
gem install rdiscount-*.gem
{% endhighlight %}

Open the `Gemfile` file and find this line

{% highlight yml linenos %}
gem 'rdiscount', '~> 2.0.7'
{% endhighlight %}

Replace with this line

{% highlight yml linenos %}
gem 'rdiscount', '9.0.0.0'
{% endhighlight %}

## Add rsync-exclude

Once you have successfully `rake deploy` your files to server, which will take some time because the mathjax folder is big, you can add a `rsync-exclude` file to exclude the mathjax folder in following deployments. Add a file named `rysnc-exclude` in the top folder of Octopress and put the following lines in it:

```
.git
.gitignore
mathjax
```

This will make the deploying speed as fast as without MathJax.

Also edit the `Rakefile` file, find this line,

```
FileList["#{args.source}/**/.*"].exclude("**/.", "**/..", "**/.DS_Store", "**/._*").each do |file|
```

and replace with this line,

```
FileList["#{args.source}/**/.*"].exclude("**/.", "**/..", "**/.DS_Store", "**/._*", "**/.git", "**/.gitignore").each do |file|
```

## Test

{% highlight latex linenos %}
Write an equation in $$ \TeX $$ now: $$ \frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} =
1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
{1+\frac{e^{-8\pi}} {1+\ldots} } } } $$, enjoy!
{% endhighlight %}
Write an equation in $$ \TeX $$ now: $$ \frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} =
1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
{1+\frac{e^{-8\pi}} {1+\ldots} } } } $$, enjoy!

{% highlight latex linenos %}
Another one: $$ \frac{\frac{a}{b}}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{b}}}}}}}}}}}} $$
{% endhighlight %}

Another one: $$ \frac{\frac{a}{b}}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{\frac{a}{b}}}}}}}}}}}} $$

{% highlight latex linenos %}
Maxwell's Equations: $$ \begin{split}\nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} & = \frac{4\pi}{c}\vec{\mathbf{j}} \\   \nabla \cdot \vec{\mathbf{E}} & = 4 \pi \rho \\ \nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} & = \vec{\mathbf{0}} \\ \nabla \cdot \vec{\mathbf{B}} & = 0 \end{split} $$
{% endhighlight %}

Maxwell's Equations: $$ \begin{split}\nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} & = \frac{4\pi}{c}\vec{\mathbf{j}} \\   \nabla \cdot \vec{\mathbf{E}} & = 4 \pi \rho \\ \nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} & = \vec{\mathbf{0}} \\ \nabla \cdot \vec{\mathbf{B}} & = 0 \end{split} $$
