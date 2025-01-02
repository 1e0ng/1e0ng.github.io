---
layout: post
title: "Downgrade MongoDB from 3.0 to 2.6"
date: 2015-07-30 19:26:41 +0800
comments: true
categories: articles
tags:
- Server
- Database
- Operation

---

Due to a Meteor bug (actually it's a bug from MongoDB nodejs driver, but the bug has already been fixed by the nodejs driver, while the issue is Meteor is referencing an old version of this driver), I have to downgrade MongoDB from `3.0.5` to `2.6.10`. Normally this is a trival work, but it cost me a whole afternoon to do this, because there are serveral traps in there, so I decide to write this blog to help other people who meet the same issue with me.

The main problem is MongoDB 3.0 uses a new version of authentication algorithom `SCRAM-SHA-1`, while 2.6 uses an old version `MONGODB-CR`. Actually there are other methods besides these two. These two are the default configuration. If one upgrades MongoDB from 2.6 to 3.0, the authentication schema version can be upgraded by `authSchemaUpgrade` from 3 to 5, and in the same time the authentication algorithom will be upgraded from `MONGODB-CR` to `SCRAM-SHA-1`. However, when one downgrades MongoDB from 3.0 to 2.6, you can not use `authSchemaUpgrade` to downgrade the authentication schema, and it will remain in 5 and the authentication algorithm will remain in `SCRAM-SHA-1`, which are not supported by MongoDB 2.6. So yes, without additional work, you are not able to log into the database.

This article provides a method to solve this issue, which is not documented by MongoDB official website (and appearantly not documented in anywhere).

<!--more-->

### Preparation

First and most importantly, BACKUP all the database. It's easy for me --- just snapshot the Amazon EBS. But if that's not the case for you, just use `rsync` to backup all data files, journal files and oplogs after shutting down the database, or use `mongodump` tool if database is small.

According to MongoDB official site: `Once upgraded to MongoDB 3.0, you cannot downgrade to a version lower than 2.6.5.`, `If you upgrade to MongoDB 3.0 and have run authSchemaUpgrade, you cannot downgrade to the 2.6 series without disabling --auth.`

So first, choose a version of MongoDB 2.6. I choose `2.6.10` because currently it's highest in `2.6`.

According to official documentation, it's possible to maintain `secondary` set one by one, then do the `primary` set

### Downgrade

For each mongoDB instance one by one, do the following steps, in the order of `secondary` first, `primary` last.

1. Backup MongoDB configuration files.

2. Remove MongoDB 3.0

        apt-get --purge remove mongodb-org mongodb-org-*
        apt-get --purge autoremove

    Type `mongo` to test if Mongo is really removed. You should see `Command not exists`.

3. Install MongoDB 2.6

        sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
        echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
        sudo apt-get update
        apt-get install mongodb-org-server=2.6.10 mongodb-org-shell=2.6.10 mongodb-org-mongos=2.6.10 mongodb-org-tools=2.6.10

    Here you should note just run `apt-get install mongodb-org=2.6.10` doesn't work --- that will still install mongoDB 3.0 (The author of installing a group of packages must make a mistake here.)
    Check mongo version:

        $ mongo --version
        MongoDB shell version: 2.6.10
        $ mongod --version
        db version v2.6.10
        2015-07-31T02:38:44.808+0000 git version: 5901dbfb49d16eaef6f2c2c50fba534d23ac7f6c

4. Pin MongoDB packages version

        echo "mongodb-org-server hold" | sudo dpkg --set-selections
        echo "mongodb-org-shell hold" | sudo dpkg --set-selections
        echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
        echo "mongodb-org-tools hold" | sudo dpkg --set-selections

    Check if mongodb is pinned

        $dpkg --get-selections | grep mongo
        mongodb-org-server     hold
        mongodb-org-shell      hold
        mongodb-org-mongos     hold
        mongodb-org-tool       hold

5. Restore mongoDB configuration file.
6. Restart mongoDB

### Configuration

Add firewall rules to ban all access to MongoDB except from local and other repl sets. (This may cause web service down.)

Edit each replication set's configuration file, comment out the `keyFile` line, to disable authentication. (Or other authentication method is used, comment out them correspondingly)

Restart all MongoDB instances.

SSH to the primary db, and use `mongo` tool to log into the mongo shell. Without auth, a sing `mongo` command should work. No need to input username or password.

```
rs0:PRIMARY> use admin
switched to db admin
rs0:PRIMARY> db.system.users.find()
{ "_id" : "admin.oplogger", "user" : "oplogger", "db" : "admin", "credentials" : { "SCRAM-SHA-1" : { "iterationCount" : 10000, "salt" : "********", "storedKey" : "******", "serverKey" : "******" } }, "roles" : [ { "role" : "read", "db" : "local" } ] }
{ "_id" : "admin.siteUserAdmin", "user" : "siteUserAdmin", "db" : "admin", "credentials" : { "SCRAM-SHA-1" : { "iterationCount" : 10000, "salt" : "******", "storedKey" : "******", "serverKey" : "******" } }, "roles" : [ { "role" : "userAdminAnyDatabase", "db" : "admin" } ] }
...
```

Notice the credential method is `SCRAM-SHA-1`, first let's try drop a user and creat a new user.

```
rs0:PRIMARY> db.dropUser('siteUserAdmin')
2015-07-30T10:03:52.240+0000 E QUERY    Error: User and role management commands require auth data to have schema version 3 but found 5
    at Error (<anonymous>)
        at DB.dropUser (src/mongo/shell/db.js:1186:11)
            at (shell):1:4 at src/mongo/shell/db.js:1186

```

Oops, not able to drop a user. Why not Drop the collection?

```
rs0:PRIMARY> db.system.users.drop()
    2015-07-30T10:04:33.715+0000 E QUERY    Error: drop failed: {
        "ns" : "admin.system.users",
            "nIndexesWas" : 2,
            "ok" : 0,
            "errmsg" : "can't drop system ns",
            "code" : 20
    }

```

Failed again.

Notice the error message: `User and role management commands require auth data to have schema version 3 but found 5`. So try to use `authSchemaUpgrade` command to downgrade the schema version:

```
rs0:PRIMARY> db.getSiblingDB("admin").runCommand({authSchemaUpgrade: 3 });
{
    "ok" : 0,
    "errmsg" : "Do not know how to upgrade auth schema from version 5",
    "code" : 69
}
```

This doesn't work as well.

So at last the solution I find is:

```
rs0:PRIMARY> db.system.version.update({}, {$set:{currentVersion:3}})
```

Then recreate a user:

```
rs0:PRIMARY> db.dropUser('siteUserAdmin')
true
rs0:PRIMARY> db.createUser( {
        ...     user: "siteUserAdmin",
        ...     pwd: "******",
        ...     roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
        ...   });
Successfully added user: {
    "user" : "siteUserAdmin",
        "roles" : [
        {
            "role" : "userAdminAnyDatabase",
            "db" : "admin"
        }
    ]
}
```

It works.


Recreat all users.

Check `rs.status()`. Wait for all sync is complete, then shutdown all databases.

Restore the `keyFile` configuration (Or other auth configuration).

Start all database, and check `rs.status()`.

Restore firewall rule to allow web service to access mongoDB.
