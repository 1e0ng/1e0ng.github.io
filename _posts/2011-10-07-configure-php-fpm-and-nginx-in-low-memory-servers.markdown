---
comments: true
date: 2011-10-07 00:02:48
layout: post
slug: configure-php-fpm-and-nginx-in-low-memory-servers
title: Configure PHP-FPM and Nginx in Low Memory Servers
wordpress_id: 783
categories: articles
tags:
- Server
tags:
- Configuration
- LNMP
- Nginx
- php-fpm
---

Recently, I registered an [Amazon EC2](http://aws.amazon.com/ec2/), ie Elastic Compute Cloud, with a free tier for the first year. The machine has only 600M memory. That is so few that it took me a few days to optimize my configuration files to make my blog and other web service run on this machine.

Before I use EC2, my blog is based on LAMP(Linux, Apache, MySQL, PHP). I decided to replace it with LNMP(Linux, Nginx, MySQL, PHP), since Nginx is said to be more efficient than Apache. To install all these is simple:
<!-- more -->

{% highlight bash linenos %}
# yum install php nginx mysql-server mysql-devel php-fpm
{% endhighlight %}

Now, let's concentrate on the configurations of php-fpm and Nginx.

This is the Nginx configuration:


```
#######################################################################
#
# This is the main Nginx configuration file.
#
# More information about the configuration options is available on
#   * the English wiki - http://wiki.nginx.org/Main
#   * the Russian documentation - http://sysoev.ru/nginx/
#
#######################################################################

# This configuration file is created by Leon in 2011
# http://nextspaceship.com

#----------------------------------------------------------------------
# Main Module - directives that cover basic functionality
#
#   http://wiki.nginx.org/NginxHttpMainModule
#
#----------------------------------------------------------------------

user              nginx;
worker_processes  2;

error_log  /var/log/nginx/error.log;
#error_log  /var/log/nginx/error.log  notice;
#error_log  /var/log/nginx/error.log  info;

pid        /var/run/nginx.pid;

#----------------------------------------------------------------------
# Events Module
#
#   http://wiki.nginx.org/NginxHttpEventsModule
#
#----------------------------------------------------------------------
worker_rlimit_nofile 10240;
events {
    use epoll;
    worker_connections  10240;
}
timer_resolution  500ms;

#----------------------------------------------------------------------
# HTTP Core Module
#
#   http://wiki.nginx.org/NginxHttpCoreModule
#
#----------------------------------------------------------------------

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server_name_in_redirect off;
    server_names_hash_bucket_size 128;
    server_tokens off;
    client_header_buffer_size 128;
    client_max_body_size 8m;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;
    sendfile        on;
    tcp_nopush     on;

    keepalive_timeout  65;
    tcp_nodelay     off;

    client_body_timeout 10;
    client_header_timeout 10;
    send_timeout 60;

    output_buffers 1 32k;
    postpone_output 1460;

    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 32k;
    fastcgi_buffers 4 32k;
    fastcgi_busy_buffers_size 32k;
    fastcgi_temp_file_write_size 32k;

    gzip  on;
    gzip_disable "MSIE [1-6]\.(?!.*SV1)";

    gzip_buffers 4 16k;
    gzip_http_version 1.0;

    gzip_comp_level 2;
    gzip_min_length   0;

    gzip_types text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_proxied expired no-cache no-store private auth;
    proxy_cache_path  /var/lib/nginx/cache  levels=1:2   keys_zone=staticfilecache:80m inactive=1d  max_size=2500m;
    proxy_temp_path /var/lib/nginx/proxy;
    proxy_connect_timeout 300;
    proxy_read_timeout 120;
    proxy_send_timeout 120;
    proxy_buffer_size  16k;
    proxy_buffers      4 16k;


    upstream wordpressnginx
    {
    server 127.0.0.1:9000 weight=1 fail_timeout=120s;
    }

    # Load config files from the /etc/nginx/conf.d directory
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

This is the configuration of php-fpm:

```
;;;;;;;;;;;;;;;;;;;;;
; FPM Configuration ;
; This configuration file is created by Leon in 2011
; http://nextspaceship.com
;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;
; Global Options ;
;;;;;;;;;;;;;;;;;;

[global]
error_log = /var/log/php-fpm.log
log_level = notice
emergency_restart_threshold = 5
emergency_restart_interval = 1m
process_control_timeout = 0
daemonize = yes

;;;;;;;;;;;;;;;;;;;;
; Pool Definitions ;
;;;;;;;;;;;;;;;;;;;;

[www]
listen = 127.0.0.1:9000
listen.backlog = -1
listen.allowed_clients = 127.0.0.1
listen.owner = nginx
listen.group = nginx
listen.mode = 0666

user = nginx
group = nginx

pm = static
pm.max_children = 8
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 35
pm.max_requests = 1024

request_terminate_timeout = 0
request_slowlog_timeout = 6s
slowlog = /var/log/$pool.log.slow

rlimit_files = 65536
rlimit_core = 0

catch_workers_output = yes
env[HOSTNAME] = $HOSTNAME
env[PATH] = /usr/local/bin:/usr/bin:/bin
env[TMP] = /tmp
env[TMPDIR] = /tmp
env[TEMP] = /tmp

php_flag[display_errors] = on
php_admin_value[error_log] = /var/log/fpm-php.www.log
php_admin_flag[log_errors] = on
php_admin_value[memory_limit] = 64M
```
