---
comments: true
date: 2012-02-16 23:51:58
layout: post
slug: pyramid-nginx-uwsgi-mysql
title: Pyramid + Nginx + uWSGI + MySQL
wordpress_id: 911
categories:
- Web
tags:
- MySQL
- Nginx
- Pyramid
- uWSGI
---

This article describes how to set an development and production environment for [Pyramid](http://pypi.python.org/pypi/pyramid) web framework on a Linux platform with [Nginx](http://nginx.org/), [uWSGI](http://projects.unbit.it/uwsgi/) and [MySQL](http://www.mysql.com/).

<!--more-->

Pyramid is a popular Python web framework, evolved with pylons(which is used as the main framework by Quora) and Repoze.bfg. Nginx is an excellent HTTP and reverse proxy server. uWSGI is a fast, self-healing and developer/sysadmin-friendly application container server coded in pure C. I use it to connect Nginx and Pyramid applications. MySQL is a most popular database.

### 1. Install Nginx

Simply run

    sudo apt-get install nginx


Fortunately, that will be OK. But if error happens, try to add the following line to your sources.list file (this is for Ubuntu lucid):





    deb http://nginx.org/packages/ubuntu/ lucid nginx





Then run





    sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com ABF5BD827BD9BF62
    sudo apt-get update
    sudo apt-get install nginx





If that still doesn't work, maybe you will have to download the [source code](http://nginx.org/) and compile it yourself. Don't forget to add the uWSGI support if you choose this way:





    ./configure --add-module=../uwsgi/nginx/





### 2. Install Pyramid


<!--more-->


    sudo apt-get install python-dev python-pip libjpeg62-dev





pip is a tool to install python packages. I prefer pip than easy_install. pip has the ability to uninstall packages. libjpeg62-dev is essential if you use PIL (Python Image Library) to handle jpeg images.





    sudo pip install virtualenvwrapper





virtualenvwrapper is a tool to setup a virtual python environment so as to isolate with system's python environment and also can be used to makeup different python environment for different projects. It's handy and useful.





    source /usr/local/bin/virtualenvwrapper.sh





Depend on your system, the path for this file maybe at /usr/bin/virtualenvwrapper.sh, so just find it. Also add the above line to you .bash_rc file so that you don't need to run this command each time you log in your system.





    mkvirtualenv env1
    workon env1





The mkvirtualenv command need to run once. The workon command need to run each time you get into this environment. You can make a variety of environments such env2, env3..., and you can use the workon command to switch between different environments:





    mkvirtualenv env2
    mkvirtualenv env3
    workon env2
    workon env3
    workon env1





Now get into env1 and install pyramid.





    pip install pyramid





To update instead of install pyramid, use the -U parameter:





    pip install -U pyramid





Note from now on, you need not to use sudo to install python packages, because you install python packages in your virtual environment, ie ~/.virtualenv/env1/





Read the document [SQLAlchemy + URL Dispatch Wiki Tutorial](http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/tutorials/wiki2/index.html) and setup your pyramid project.





### 3. Install uWSGI





    workon env1
    pip install uwsgi





Maybe you will encounter some errors, just resolve them. For example it maybe complains that there is no libxml2 library, just install it with:





    sudo apt-get install libxml2-dev





### 4. Install MySQL





    sudo install mysql-server python-myql libmysqlclient16





python-mysql is the python driver for mysql. libmysqlclient16 is needed as some python programe need the mysql_config file to work properly with mysql.





### 5. Configure MySQL





Edit /etc/mysql/my.cnf, adding the following lines under the [mysqld] tag:





    skip-character-set-client-handshake
    collation_server=utf8_unicode_ci
    character_set_server=utf8





This make mysql server to use utf8 character set. Restart mysql to make the configuration come into effect.





    sudo service mysql restart





### 6. Configure Nginx





Edit /etc/nginx/nginx.conf. Here is an example:





    user www-data;
    worker_processes  16;

    error_log  /var/log/nginx/error.log;
    pid        /var/run/nginx.pid;

    worker_rlimit_nofile 20480;
    events {
        use epoll;
        worker_connections  20480;
    }
    timer_resolution  500ms;


    http {
        include       mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr $host $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$request_length" "$upstream_response_time" "$request_time"';
        access_log  /var/log/nginx/access.log main;

        sendfile        on;

        keepalive_timeout  60;
        tcp_nodelay        on;

        gzip_disable "MSIE [1-6]\.(?!.*SV1)";
        gzip_buffers 16 8k;
        gzip_comp_level 1;
        gzip_min_length   0;
        gzip_types text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript;

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
    }





Add a file in /etc/nginx/sites-available/, for example named demo:





    server {
        listen          80;
        access_log      off;
        error_log       /var/log/nginx/http.error.log;

        charset         utf-8;
        location / {
            uwsgi_pass  unix:///tmp/uwsgi.sock;
            include     uwsgi_params;
        }
    }





The above code means Nginx accept requests from users on 80 port and forward them to uWSGI server via unix:///tmp/uwsgi.sock. And add a soft link to this file in folder /etc/nginx/sites-enabled:





    ln -sf /etc/nginx/sites-available/demo /etc/nginx/sites-enabled/demo





Now restart Nginx:





    sudo /etc/init.d/nginx restart





### 7. Configure uWSGI





Add the following lines to your production.ini/development.ini file:





    [uwsgi]
    socket = /tmp/uwsgi.sock
    master = true

    processes = 4

    harakiri = 60
    harakiri-verbose = true
    limit-post = 65536
    post-buffering = 8192

    daemonize = ./uwsgi.log
    pidfile = ./pid_5000.pid

    listen = 256

    max-requests = 1000

    reload-on-as = 128
    reload-on-rss = 96
    no-orphans = true

    log-slow = true

    virtualenv = /home/your_name/.virtualenvs/env1





This configure uWSGI to run in daemon mode logging errors to uwsgi.log file and the pid of the master process will be written to pid_5000.pid file.





Now start uWSGI through the command line:





    uwsgi --ini-paste-logged production.ini




The --ini-paste-logged option is only availabe in the development version. For the stable version(currently is  1.0.4), use --ini-paste instead.




use ps to make sure uWSGI is up:





    $ ps axu | grep uwsgi
    leon 16510 19.0  0.3  96072 30032 ?        S    18:06   0:00 uwsgi --ini-paste production.ini
    leon 16511  0.0  0.3  96072 26972 ?        S    18:06   0:00 uwsgi --ini-paste production.ini
    leon 16512  0.0  0.3  96072 26968 ?        S    18:06   0:00 uwsgi --ini-paste production.ini
    leon 16513  0.0  0.3  96072 26968 ?        S    18:06   0:00 uwsgi --ini-paste production.ini
    leon 16514  0.0  0.3  96072 26968 ?        S    18:06   0:00 uwsgi --ini-paste production.ini
    leon 16521  0.0  0.0   7620   908 pts/0    S+   18:06   0:00 grep --color=auto uwsgi





As you can see, the uWSGI server make up 1 master process and 4 worker processes.





View the uwsgi.log file to resolve errors.





To reload uWSGI, simply run:





    uwsgi --reload pid_5000.pid





To stop uWSGI, simply run:





    uwsgi --stop pid_5000.pid





### 8. Configure Pyramid





By default, the alchemy scaffold use sqlite database. Let's replace it with MySQL. Modify the development.ini/production.ini to modify the value of sqlalchemy.url:





    sqlalchemy.url = mysql://username:password@127.0.0.1/dbname?charset=utf8&use_unicode=0





### 9. System Tunning





Run the following commands:





    echo 3000 > /proc/sys/net/core/somaxconn
    echo 81920 > /proc/sys/net/ipv4/tcp_max_syn_backlog





That's all.
