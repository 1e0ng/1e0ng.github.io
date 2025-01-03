---
comments: true
date: 2011-09-08 23:36:17
layout: post
slug: send-email-with-php-in-utf-8
title: Send Email With PHP in UTF-8
wordpress_id: 755
categories:
- Web
tags:
- GBK
- HTML
- Linux
- Mail
- PHP
- UTF-8
---

In my previous article [Configure Mail Service with PHP Mail Function and Postfix](/posts/configure-mail-service-with-php-mail-function-and-postfix/), I described how to set up an environment to send mail with php on Linux.

Here, I will solve an issue which met by a lot of people, confused but don't know how to do: How to send mail in UTF-8? Here I will tell you how to send an email with not only a UTF-8 subject but also a UTF-8 content. It's simple. Just read the following code. Quote your subject with `'=?UTF-8?B?'` and `'?='`. You may choose to use HTML to edit your email content, just don't forget to declare UTF-8 character set. That's all.

<!-- more -->
``` php
<?php

/**
 * Created by Leon on 22, August, 2011
 * http://leons.im
 */

function sendmail($to, $code)
{
    $sender = "test@leons.im";
    list($user, $domain) = split("@", $to, 2);
    $subject = "测试主题";
    $subject = '=?UTF-8?B?'.base64_encode($subject).'?=';

    $from = "Test <${sender}>";
    $mime_boundary = "----Lite----".md5(time());

    $message = "--$mime_boundaryn";

    $message .= "Content-Type: text/html; charset=UTF-8n";
    $message .= "Content-Transfer-Encoding: 8bitnn";

    $message .= "<html><head></head><body>n";
    $message .= "你好！<br>n";
    $message .= "欢迎访问我的网站<a href=\"http://leons.im\" target=\"_blank\">http://leons.im</a><br>n";

    $message .= "</body></html>n";

    $message .= "--$mime_boundary--nn";

    //echo "message = $messagen";

    $headers = "From: Test <${sender}>n";
    $headers .= "Reply-To: Test <${sender}>n";
    $headers .= "MIME-Version: 1.0n";
    $headers .= "Content-Type: multipart/alternative; boundary=\"$mime_boundary\"\n";

    $addtional = "-f ${sender}";
    return mail($to, $subject, $message, $headers, $addtional);
}
?>

```
