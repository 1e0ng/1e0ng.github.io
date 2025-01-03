---
layout: post
title: "Automatically Backup MongoDB with AWS CLI"
date: 2015-07-24 10:54:31 +0800
comments: true
categories:
- AWS
- Database
- Op

---

After searching google, the information about backuping MongoDB is neither obselete or complicated. So this article is about a new practice on automatically backup MongoDB with AWS's offical tool AWS CLI. It's more straight forward and more compatable with the new Amazon S3 server (supporting the newest v4 signature).

Before that, let's review some existing methods. One method is use the open source project [s3cmd](https://github.com/s3tools/s3cmd). Originally it doesn't support the v4 signature, and after a long time, it finally supports v4 signature. The issue is it still doesn't support the China region S3 server. Due to the maintainer is only one person and he doesn't have enough time on this project, I guess it will another long period of time to fix this. Another method is to use [mongodb-s3-backup](https://github.com/RGBboy/mongodb-s3-backup). After a little modification, it can handle Chinese region S3 server well, but it doesn't support v4 signature.

So I just creat a new script: <https://github.com/leonsim/mongo-s3-backup>.

<!--more-->

### Usage

#### Install AWS CLI first

```
sudo apt-get install awscli
```

or

```
brew install awscli
```

```
sudo yum install awscli
```

#### Configure AWS CLI

```
aws configure
```
Input AWS Access Key, Secret Key and region.

#### Run Script

Edit file `backup.sh`, and input MongoDB credential infos and S3 bucket name.

```
./backup.sh
```

Or use crontab:

```
0 0 * * * ubuntu /bin/bash /home/ubuntu/backup.sh
```
