---
comments: true
date: 2011-08-28 18:06:00
layout: post
slug: configure-mail-service-with-php-mail-function-and-postfix
title: Configure Mail Service with PHP Mail Function and Postfix
wordpress_id: 745
categories:
- Web
tags:
- Arch
- Linux
- Mail
- PHP
- Postfix
- Ubuntu
---

This article describes how to use the php function mail to send a mail.

<!--more-->

PHP manual says  

{% quote %}
It is worth noting that the mail() function is not suitable for 
larger volumes of email in a loop. This function opens and closes an SMTP 
socket for each email, which is not very efficient. 

For the sending of large amounts of email, see the » PEAR::Mail, 
and » PEAR::Mail_Queue packages. 
{% endquote %}

Don't worry about that if you use postfix instead of MTA, because postfix handle all mails with a mail queue.


The PHP function mail is:

``` php    
bool mail(string $to, string $subject, string $message[, string $additional_headers[, string $additional_parameters]])
```

It depends on the system command sendmail. postfix is a portage contains the sendmail command. Though some other portages (like sendmail portage on Ubuntu) also work, I recomment postfix because it's secure, fast, easy to administer drop in replacement for Sendmail (MTA).

To install postfix on Arch, use this command:

{% highlight bash linenos %}
$ sudo pacman -Syu postfix 
{% endhighlight %}

Or, install it on Ubuntu, use this: 

{% highlight bash linenos %}
$ sudo apt-get install postfix 
{% endhighlight %}

If you have installed sendmail, you need to uninstall it at first: 
    
{% highlight bash linenos %}
$ sudo apt-get remove sendmail
{% endhighlight %}

That's all. Now write a test script to test. 

``` php    
<?php

/**
 * Created by Leon on 27, August, 2011
 * http://leons.im
 */

$to = "test@test.com";
$subject = "test";
$mime_boundary = "----test----".md5(time());
$message = "--$mime_boundaryn";

$message .= "Content-Type: text/html; charset=UTF-8n";
$message .= "Content-Transfer-Encoding: 8bitnn";
$message .= "Hello! Holla!n";
$message .= "--$mime_boundary--nn";

$sender = "test@test.org";
$headers = "From: test <${sender}>n";
$headers .= "Reply-To: test <${sender}>n";
$headers .= "MIME-Version: 1.0n";
$headers .= "Content-Type: multipart/alternative; boundary="$mime_boundary"n";

echo mail($to, $subject, $message, $headers);
?>
```

Postfix has a mail queue to handle your mail. This is fatabulous! 
    
{% highlight bash linenos %}
$ mailq
-Queue ID- --Size-- ----Arrival Time---- -Sender/Recipient-------
A774062A6E      157 Wed Aug 10 02:52:01  root
                                         root

C7E1362A6F     1220 Wed Aug 10 02:56:13  test@test.org
                                         test@test.com

-- 1 Kbytes in 2 Requests.
{% endhighlight %}
