---
layout: post
title: "Setting Up MongoDB Replication on EC2 with Ubuntu 14.02"
date: 2015-07-10 15:30:03 +0800
comments: true
categories: articles
tags:
 - Server
 - DB

---

To setup a meteor production environment on EC2, we need to install mongoDB as the main database.
To use the MUP(Meteor Up tool), it's easier to use Ubuntu operating system.

This article is about how to setup mongoDB replication on EC2 with Ubuntu 14.02 LTS. Basically, it's the combination of the following articles:

<!--more-->

mongoDB Replication Doc: <http://docs.mongodb.org/manual/replication/>

mongoDB official doc for platform Amazon EC2: <http://docs.mongodb.org/ecosystem/platforms/amazon-ec2/>

Install mongoDB on Ubuntu: <http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/>

An old article about setting up mongoDB replication on EC2: <https://medium.com/cs-math/settings-up-mongodb-replica-sets-on-ec2-with-ubuntu-natty-11-04-c6f300502c5f>

Configure MUP: <https://github.com/arunoda/meteor-up#accessing-the-database>

Oplog Observe Driver: <https://github.com/meteor/meteor/wiki/Oplog-Observe-Driver>

### Storage Considerations

EC2 instances can be configured with either ephemeral storage or persistent storage using the Elastic Block Store (EBS). Ephemeral storage is lost when instances are terminated, so it is generally not recommended unless you understand the data loss implications.

For almost all deployments EBS will be the better choice. For production systems we recommend using

- EBS-optimized EC2 instances
- Provisioned IOPS (PIOPS) EBS volumes

It is recommended to use individual PIOPS EBS volumes for data (1000 IOPS), journal (250 IOPS), and log (100 IOPS).

So first launch three new EC2 instance and create 3 new EBS volumes for each EC2 instances, and then associates volumes to corresponding EC2 instances.

### Install mongoDB

For each EC2 instance:

```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
$ echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
```

After successfully installed mongoDB, check mongoDB version:

```
$ mongo --version
MongoDB shell version: 3.0.4
```

### Configure EC2 Security Groups

Create a security group named `mongodb`, and add a rule:

```
Custom TCP role, TCP, 27017, 172.31.0.0/16
SSH, TCP, 22, 0.0.0.0/0
```

Here `172.31.0.0/16` depends on the network of all instances. 
Make sure all EC2 instances can connect to each other, and the web/app server can connect the primary database server.

Associate the security group to each EC2 instance.

### Configure hostnames

For each instance, give it a hostname.

```
$ sudo hostnamectl set-hostname alice
$ sudo hostnamectl set-hostname bob
$ sudo hostnamectl set-hostname eve
```

Append the following lines to `/etc/hosts`:

```
172.16.0.1 alice
172.16.0.2 bob
172.16.0.3 eve
```

Replace the `172.16.0.x` with the real IPs. It's better to use intranet addresses.

Reboot all instances.

### Create disk partitions

```
$ sudo mkdir /data /log /journal

$ sudo mkfs.ext4 /dev/xvdf
$ sudo mkfs.ext4 /dev/xvdg
$ sudo mkfs.ext4 /dev/xvdh

$ echo '/dev/xvdf /data ext4 defaults,auto,noatime,noexec 0 0
/dev/xvdg /journal ext4 defaults,auto,noatime,noexec 0 0
/dev/xvdh /log ext4 defaults,auto,noatime,noexec 0 0' | sudo tee -a /etc/fstab

$ sudo mount /data
$ sudo mount /journal
$ sudo mount /log

$ sudo chown mongodb:mongodb /data /journal /log

$ sudo ln -s /journal /data/journal
```

### System configuartion for mongoDB production environment

```
$ sudo nano /etc/security/limits.conf
* soft nofile 64000
* hard nofile 64000
* soft nproc 32000
* hard nproc 32000

$ sudo nano /etc/security/limits.d/90-nproc.conf
* soft nproc 32000
* hard nproc 32000
```

```
$ sudo blockdev --setra 32 /dev/xvdf
$ sudo blockdev --setra 32 /dev/xvdg
$ sudo blockdev --setra 32 /dev/xvdh

$ echo 'ACTION=="add", KERNEL=="xvdf", ATTR{bdi/read_ahead_kb}="32"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules
$ echo 'ACTION=="add", KERNEL=="xvdg", ATTR{bdi/read_ahead_kb}="32"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules
$ echo 'ACTION=="add", KERNEL=="xvdh", ATTR{bdi/read_ahead_kb}="32"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules
```

```
if test -f /sys/kernel/mm/transparent_hugepage/khugepaged/defrag; then
  echo 0 > /sys/kernel/mm/transparent_hugepage/khugepaged/defrag
fi
if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
  echo never > /sys/kernel/mm/transparent_hugepage/defrag
fi
if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
  echo never > /sys/kernel/mm/transparent_hugepage/enabled
fi
```

Reboot all instances.

### Configure mongoDB

Choose one instance as the primary mongoDB, say `alice`.

Login `alice`, start `mongod` with `auth` disabled.

Edit `/etc/mongod.conf`. Comment out `bind_ip = 127.0.0.1` line. Edit `dbpath`, `logpath` and `replSet`.

```
dbpath=/data
logpath=/log/mongod.log
logappend=true

#bind_ip = 127.0.0.1

```

```
sudo service mongod start
```

Create administative users:

```
mongo
use admin
db.createUser( {
    user: "siteUserAdmin",
    pwd: "<password>",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  });
db.createUser( {
    user: "siteRootAdmin",
    pwd: "<password>",
    roles: [ { role: "root", db: "admin" } ]
  });
```

Stop `mongod`

```
sudo service mongod stop
```

Create the key file to be used by each member of the replica set.

```
openssl rand -base64 741 > mongodb-keyfile
sudo mv mongodb-keyfile /etc/mongodb-keyfile
sudo chown mongodb:mongodb /etc/mongodb-keyfile
sudo chmod 600 /etc/mongodb-keyfile
```

Edit `/etc/mongod.conf` again.

```
replSet=rs0
keyFile=/etc/mongodb-keyfile
```

Copy `mongod.conf` to all other instances.

Copy `/etc/mongodb-keyfile` to all other instances.


### Start mongoDB


Start mongoDB on `alice` first.

```
sudo service mongod restart
```


```
mongo

use admin
db.auth("siteRootAdmin", "<password>");

rs.initiate()
rs.conf()
rs.add("bob:27017")
rs.add("eve:27017")
```

Check status:

```
rs.status()
```

### Adjust Priority for Replica Set Member

```
cfg = rs.conf()
cfg.members[0].priority = 0.5
cfg.members[1].priority = 2
cfg.members[2].priority = 2
rs.reconfig(cfg)
```

### Create additional users to address operational requirements.

For example, the following creates a database administrator for the products database:

```
use products
db.createUser(
  {
    user: "productsDBAdmin",
    pwd: "password",
    roles:
    [
      {
        role: "dbOwner",
        db: "products"
      }
    ]
  }
)
```

### Creat oplogger user

```
mongo
cluster:PRIMARY> use admin
cluster:PRIMARY> db.createUser({user: "oplogger", pwd: "PasswordForOplogger", roles: [{role: "read", db: "local"}]})
```

### Configure MUP

Edit `mup.json` file. Here I use `nearest` read preference and `majority` write concern.


```
{
  ...
  // Configure environment
  "env": {
    "PORT": 3800,
    "ROOT_URL": "http://example.com",
    "MONGO_URL": "mongodb://productsDBAdmin:password@alice:27017,bob:27017,eve:27017/product?replicaSet=rs0&readPreference=nearest&w=majority",
    "MONGO_OPLOG_URL": "mongodb://oplogger:PassswordForOplogger@alice:27017,bob:27017,eve:27017/local?authSource=admin"
  },
  ...
}

```



