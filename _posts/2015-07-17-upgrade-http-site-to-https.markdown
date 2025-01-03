---
layout: post
title: "Upgrade Http site to Https (For Free)"
date: 2015-07-17 20:18:47 +0800
comments: true
categories:
- Web
- Security

---

Even though the serieze of HeartBleeding bugs makes HTTPS (SSL) look vulnerable, I still believe after bugs fixed, HTTPS is more secure than HTTP. Actually we can archieve this in a few simple steps with technologies like OpenSSL, free certificate provider, nginx configuration.

<!--more-->

### Register an account at StartSSL

StartSSL is one of websites providing free digital certificates for websites and is my favourate one after experiencing several providers. Though the UI and UX are not so good, the function is good, and that's enough for free :-D

Open <https://www.startssl.com>, click `Control Panel` and `Sign-up` an account. Input some information to prove that you are a human being. Wait for some time, and you will receive an email that account get registered successfully.

### Back up p12 file

This is critical important. Back up a p12 file for the account in StartSSL. For Mac user, you need to export this via `Key Chain`.

### Email Address Validation

Return to StartSSL's control panel, and `authenticate` into it. Choose `Validation Wizard` tab. In the select box, choose `Email Address Validation` and complete this.

### Domain Name Validation

The same to the previous step except choose `Domain Name Validation` in the select box.

### Generate a CSR with OpenSSL

```
openssl genrsa -out ~/DOMAIN.key 2048
openssl req -new -sha256 -key ~/DOMAIN.key -out ~/DOMAIN.csr

```

### Retrieve certificate with CSR

Open StartSSL, and find `Certificate Wizard`. In Certifiate Target select box, choose `Web Server SSL/TLS Certifiate`. Skip the following step, because you have already generated a CSR. Submit the CSR, and download the certificate. Download intermediate and ca files as well.

Concate DOMAIN certificate, intermediate certificate and ca certificate.

```
sudo cat DOMAIN.crt intermediate.pem ca.pem > /etc/ssl/DOMAIN.crt
sudo mv ~/DOMAIN.key /ect/ssl/DOMAIN.key
```


### Configure nginx

```
sudo chmod 600 /etc/ssl/DOMAIN.*
sudo chown www-data:www-data /etc/ssl/DOMAIN.*
```

www-data is the user for nginx workers. If it's `nginx`, just replace to that.

Edit nginx configuration file.

```
server {
    listen 80;
    server_name DOMAIN;

    location / {
        rewrite ^ https://$server_name$request_uri? permanent;
    }
}

server {
    listen 443;
    server_name DOMAIN;

    ssl on;
    ssl_certificate /etc/ssl/DOMAIN.crt;
    ssl_certificate_key /etc/ssl/DOMAIN.key;

    ssl_stapling on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 5m;

    ssl_prefer_server_ciphers on;
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:ECDHE-RSA-RC4-SHA:ECDHE-ECDSA-RC4-SHA:RC4-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK';
    add_header Strict-Transport-Security "max-age=31536000;";

    if ($http_user_agent ~ "MSIE" ) {
        return 303 https://browser-update.org/update.html;
    }

    location / {
        proxy_pass http://localhost:3800;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade; # allow websockets
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header X-Forwarded-For $remote_addr; # preserve client IP
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
Here the location / is an example to use nginx as a reverse proxy. Substitude that with what you need.

Restart or reload nginx

```
sudo /etc/init.d/nginx configtest
sudo /etc/init.d/nginx restart

```
or if the configuration file already exists, just `reload` instead of `restart`

```
sudo /etc/init.d/nginx reload
```

### Open browser to test

Check and resolve errors.
