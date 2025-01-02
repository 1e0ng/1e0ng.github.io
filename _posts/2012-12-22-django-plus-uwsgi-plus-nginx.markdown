---
layout: post
title: "Django + uWSGI + Nginx"
date: 2012-12-22 16:45
comments: true
categories: 
- Server
- Web
---

This is a brief introduction of production environment configuration for Django, uWSGI and Nginx.
If you haven't installed `virtualenv`, do it first.

<!--more-->
## Install Django, uWSGI, Nginx

### Create a virtual environment, and activate it

```
virtualenv en1
source en1/bin/activate
```

### Use pip to install Django and uWSGI

```
pip install django
pip install uwsgi
```

### Install Nginx

Use your package manager to install Nginx, like `apt-get install nginx`, `yum install nginx`, or `emerge nginx`.

## Configuration

### Django and uWSGI

Since Django is a WSGI already, it's easy to configure. What you need to do is creat a uwsgi.ini file. Here is an example.

```
[uwsgi]
socket=/var/run/uwsgi.sock
virtualenv=/home/leon/en1/
chdir=/home/leon/mysite
module=mysite.wsgi:application
master=True
workers=8
pidfile=/home/leon/mysite/uwsgi-master.pid
max-requests=5000
```
<!-- more -->

- `socket` is for communication with Nginx.
- `virtualenv` is the path of your virtual environment.
- `chdir` is you project folder. For this example, assume you have created a project called mysite in folder /home/leon (`django-admin startproject mysite`).
- `module` is the entrance to your application. If you use the current version of Django, the `django-admin startproject` command should have genereated a wsgi.py file for you with an `application` variable in it, so just substite `mysite` with your project name. 
- `master` means this uwsgi worker is master.
- `workers` is the number of uwsgi workers.
- `pidfile` is the pid of the running uwsgi process. You can use it to stop or reload your uWSGI server.

### uWSGI and Nginx

You may would like to use a port to connect uWSGI and Nginx, but in this example, let's use a socket, as it's very easy as well plus it don't need to occupy a port.(Someone says it's more efficient with socket than a port in some systems.)

For example we use `socket=/var/run/uwsgi.sock` in the uwsgi.ini file, we need to configure nginx like this:

```
user  leon;
worker_processes  1;

events {
    worker_connections  1024;
    use epoll;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log  main;
    sendfile        on;

    keepalive_timeout  65;
    gzip  on;

    server {
        listen       80;
        server_name  localhost;

        location /static/ {
            root /home/leon/mysite/;
        }

        location / {
            uwsgi_pass      unix:///var/run/uwsgi.sock;
            include         uwsgi_params;
            uwsgi_param     SCRIPT_NAME '';
        }

    }
}
```
- `user`: it's better to use the same user as the one for the uWSGI server.
- `usgi_pass`: the sock file to communicate with uWSGI.
- don't forget `include uwsgi_params;`

## Start uWSGI and Nginx

(The following commands are for Gentoo system.)

Configure Nginx to autostart with system.

```
rc-config add nginx default
```

Start Nginx.

```
/etc/init.d/nginx start
```

To start uWSGI, first use this command to test if all these work:

```
uwsgi --ini uwsgi.ini
```

If everything is OK, you need to find a daemon tool to monitor uWSGI servers and restart them if error happens, like `daemontools` or `supervisord`.
