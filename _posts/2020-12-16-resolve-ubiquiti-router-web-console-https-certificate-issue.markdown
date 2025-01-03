---
layout: post
title: "Resolve Ubiquiti Router Web Console HTTPS Certificate Issue"
date: 2020-12-16 21:20:29 +0800
comments: true
categories:
- Network
---

Having been bothered by Ubiquiti's HTTPS certificate issue for years, today I finally find some time to resolve this. There are multiple ways to resolve this, but I'm not able to find a perfect solution on the internet, so I write down my solution here.

I'm not going to use a public domain name, neither will I issue a certificate through a public issuer, for example, letencrypt, which I've been vasively used for my public websites. The reason is for me, I don't want my router to be exposed to the public internet, and the less exposion, the better. Setting up a letsencrypt certificate, most probably I need verify I own this domain name and the server, which means I will reveal my public IP address for my router, and that is not my intension.

With that, I'm going to generate a self signed certificate with a generated CA on a domain name I generated dedicated for my router (router.local). Then I will import my CA to my devices that need to access the router. Finally I'll redirect my router's local IP address to a local domain name (router.local).

<!-- more -->

Now I'm gonig to show you how to archive all the above step by step.


### Genaret CA and certifacte for the router

Here is the script. Copy and paste it into a file and run it on a Mac/Linux environment.

```
#!/bin/ksh

function CreateCertificateAuthority {

if [ -f ./ubntCA.key ]; then rm ./ubntCA.key; fi
if [ -f ./ubntCA.pem ]; then rm ./ubntCA.pem; fi

#
# Create the Root Key
#
openssl genrsa -out ubntCA.key 4096

#
# Now self-sign this certificate using the root key.
#
# CN: CommonName
# OU: OrganizationalUnit
# O: Organization
# L: Locality
# S: StateOrProvinceName
# C: CountryName
#
openssl req -x509 \
            -new \
            -nodes \
            -key ubntCA.key \
            -sha256 \
            -days 36500 \
            -subj "/C=US/ST=IS/L=TOTALLY/O=CONFUSED/OU=HERE/CN=LIANGSUN.ORG" \
            -out ubntCA.pem

print ""
print "Now install this cert (ubntCA.pem) in your workstations Trusted Root Authority."
print ""

}

function CreateServerCertificate {

if [ -f ./server.key ]; then rm ./server.key; fi
if [ -f ./server.csr ]; then rm ./server.csr; fi
if [ -f ./server.crt ]; then rm ./server.crt; fi

#
# Create A Certificate
#
openssl genrsa -out server.key 4096

#
# Now generate the certificate signing request.
#
openssl req -new \
            -key server.key \
            -subj "/C=US/ST=IS/L=ALSOTOTALLY/O=CONFUSED/OU=HERE/CN=ROUTER.LOCAL" \
            -out server.csr

#
# Now generate the final certificate from the signing request.
#
openssl x509 -req \
             -in server.csr \
             -CA ubntCA.pem \
             -CAkey ubntCA.key \
             -CAcreateserial \
             -extfile <(printf "subjectAltName=DNS:ROUTER.LOCAL,IP:172.10.0.1,IP:172.20.0.1,IP:172.30.0.1,IP:192.168.0.1,IP:192.168.1.1") \
             -out server.crt -days 36500 -sha256

}

function CreateServerPem {

cat server.crt  > server.pem
cat server.key >> server.pem

}

   CreateCertificateAuthority
   CreateServerCertificate
   CreateServerPem
```

This script will generate several files, and among them, there are 2 files are import to us, `ubntCA.pem` and `server.pem`. The file `ubntCA.pem` is the one we need to import into our devices that need to access the router.

As an exapmle, to import the CA to a Windows system, run this command on a Command line with Administrator access.

```
certutil -addstore -enterprise -f "Root" ubntCA.pem
```

### Install the generated certificate on the router

From the last step, we have generated a file called `server.pem`. This is the file we need to install onto the router.

We can use `scp` command to copy this file to the router, like this:

`scp server.pem USER@172.10.0.1:~/`

Here, USER is the username, and 172.10.0.1 is the IP address of the router.

Open a ssh connection to the router, and copy the the file to the lighttpd server configuration folder.


```
cd /etc/lighttpd
sudo mv server.pem server.pem.bk
sudo cp /home/USER/server.pem ./
```

Then restart the lighttpd server:

```
sudo  killall lighttpd
sudo /usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf
```

### Bind the domain name to the router's IP

Of course we can modify each client's hosts file to redirect the domain router.local into the IP of the router, in this case, it's 172.10.0.1, but I want to do this in a smarter way, so that each client doesn't need to manually modify the hosts file. I'm going to modify the router itself.

Again ssh into the router and run `configure` command to goin the configuration shell.

Then run the following command:

```
set system static-host-mapping host-name router.local inet 172.10.0.1
commit
save
```

Probably there is a way to configure this on the Web UI also, but since CLI can handle this faster, I don't want to find a way on the UI.

Now we can access the router on a client side without the certificate error. Just open <https://router.local> on a client that has imported the CA.

Last question is, what if a user open <https://172.10.0.1> which is the IP address of the router? They will still get a SSL certificate error.

To resolve the last problem and make this solution perfect, follow the next step.


### Redirect router IP to its domain name

Again ssh into the router and go to the folder `/etc/lighttpd/conf-enabled` and create a new file called `11-redirect.conf` with the following content.

```
$HTTP["scheme"] == "https" {
    $HTTP["host"] =~ "^\d+\.\d+\.\d+\.\d+$" {
        url.redirect = (
            "^(.*)$" => "https://router.local$1"
        )
    }
}

```

Then edit the file `/etc/lighttpd/lighttpd.conf` to include the above config file.


```
include "conf-enabled/10-ssl.conf"
include "conf-enabled/11-redirect"
include "conf-enabled/15-fastcgi-python.conf"
```

Add the second line, the same way as the existing `10-ssl.conf` and `15-fastcgi-python.conf` files.

Now restart the lighttpd server again.

```
sudo  killall lighttpd
sudo /usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf
```

Now, <https://172.10.0.1> will be redirectd to <https://router.local> without a certificate warning.

### Permanently save the cert file configuration for lighttpd

So far, everything works. But one day you reboot your router and find the server certificate is regenerated.
To resolve this issue, we need to save the configuration in a permanent way.

Login to the router by ssh and copy the `server.pem` file into folder `/config/auth/` and run the following command

```
configure
set service gui cert-file /config/auth/server.pem
commit
save
```

Run this command to show everything is good:

```
ubnt# show service gui
```

It will show the following:

```
 cert-file /config/auth/server.pem
 http-port 80
 https-port 443
 listen-address 172.20.0.1
 older-ciphers disable
```

By the way, you should always set the `listen-address` to a local IP address for both services `gui` and `ssh`. This will prevent the router from accessing from the public internet, which I see no point Ubiquiti not setting it as a default.

### Finally

Conguratulations, you find a perfect solution!

