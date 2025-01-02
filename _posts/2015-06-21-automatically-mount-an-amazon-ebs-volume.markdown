---
layout: post
title: "Automatically mount an Amazon EBS volume"
date: 2015-06-21 01:51:29 +0800
comments: true
categories: articles
tags:
- Server
- Linux
---

After you attach an Amazon EBS volume to your instance, it is exposed as a block device. You can format the volume with any file system and then mount it. After you make the EBS volume available for use, you can access it in the same ways that you access any other volume. Any data written to this file system is written to the EBS volume and is transparent to applications using the device.

Note that you can take snapshots of your EBS volume for backup purposes or to use as a baseline when you create another volume. For more information, see Amazon EBS Snapshots.

Use the following procedure to make the volume available. Note that you can get directions for volumes on a Windows instance from Making the Volume Available on Windows in the Amazon EC2 User Guide for Microsoft Windows Instances.

<!-- more -->


1. Connect to your instance using SSH. For more information, see Connect to Your Instance.

2. Depending on the block device driver of the kernel, the device might be attached with a different name than what you specify. For example, if you specify a device name of /dev/sdh, your device might be renamed /dev/xvdh or /dev/hdh by the kernel; in most cases, the trailing letter remains the same. In some versions of Red Hat Enterprise Linux (and its variants, such as CentOS), even the trailing letter might also change (where /dev/sda could become /dev/xvde). In these cases, each device name trailing letter is incremented the same number of times. For example, /dev/sdb would become /dev/xvdf and /dev/sdc would become /dev/xvdg. Amazon Linux AMIs create a symbolic link with the name you specify at launch that points to the renamed device path, but other AMIs might behave differently.

    Use the `lsblk` command to view your available disk devices and their mount points (if applicable) to help you determine the correct device name to use.

    {% highlight bash linenos %}
[ec2-user ~]$ lsblk
NAME  MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
xvdf  202:80   0  100G  0 disk
xvda1 202:1    0    8G  0 disk /
    {% endhighlight %}

    The output of lsblk removes the /dev/ prefix from full device paths. In this example, /dev/xvda1 is mounted as the root device (note the MOUNTPOINT is listed as /, the root of the Linux file system hierarchy), and /dev/xvdf is attached, but it has not been mounted yet.

3. Determine whether you need to create a file system on the volume. New volumes are raw block devices, and you need to create a file system on them before you can mount and use them. Volumes that have been restored from snapshots likely have a file system on them already; if you create a new file system on top of an existing file system, the operation overwrites your data. Use the sudo file -s device command to list special information, such as file system type.

    ```
[ec2-user ~]$ sudo file -s /dev/xvdf
/dev/xvdf: data
    ```

    If the output of the previous command shows simply data for the device, then there is no file system on the device and you need to create one. You can go on to Step 4. If you run this command on a device that contains a file system, then your output will be different.

    ```
[ec2-user ~]$ sudo file -s /dev/xvda1
/dev/xvda1: Linux rev 1.0 ext4 filesystem data, UUID=1701d228-e1bd-4094-a14c-8c64d6819362 (needs journal recovery) (extents) (large files) (huge files)
    ```

    In the previous example, the device contains Linux rev 1.0 ext4 filesystem data, so this volume does not need a file system created (you can skip Step 4 if your output shows file system data).

4. (Conditional) Use the following command to create an ext4 file system on the volume. Substitute the device name (such as /dev/xvdf) for device_name. Depending on the requirements of your application or the limitations of your operating system, you can choose a different file system type, such as ext3 or XFS.

    Caution

    This step assumes that you're mounting an empty volume. If you're mounting a volume that already has data on it (for example, a volume that was restored from a snapshot), don't use mkfs before mounting the volume (skip to the next step instead). Otherwise, you'll format the volume and delete the existing data.

    ```
[ec2-user ~]$ sudo mkfs -t ext4 device_name
    ```

5. Use the following command to create a mount point directory for the volume. The mount point is where the volume is located in the file system tree and where you read and write files to after you mount the volume. Substitute a location for mount_point, such as /data.

    ```
[ec2-user ~]$ sudo mkdir mount_point
    ```

6. To mount this EBS volume on every system reboot, add an entry for the device to the /etc/fstab file.

    a. Create a backup of your /etc/fstab file that you can use if you accidentally destroy or delete this file while you are editing it.

        ```
[ec2-user ~]$ sudo cp /etc/fstab /etc/fstab.orig
        ```

    b. Open the /etc/fstab file using any text editor, such as nano or vim.

        Note

        You need to open the file as root or by using the sudo command.

    c. Add a new line to the end of the file for your volume using the following format.

        ```
device_name  mount_point  file_system_type  fs_mntops  fs_freq  fs_passno  
        ```

        The last three fields on this line are the file system mount options, the dump frequency of the file system, and the order of file system checks done at boot time. If you don't know what these values should be, then use the values in the example below for them (defaults,nofail 0 2). For more information on /etc/fstab entries, see the fstab manual page (by entering man fstab on the command line). For example, to mount the ext4 file system on the device /dev/xvdf at the mount point /data, add the following entry to /etc/fstab.

        Note
        If you ever intend to boot your instance without this volume attached (for example, so this volume could move back and forth between different instances), you should add the nofail mount option that allows the instance to boot even if there are errors in mounting the volume. Debian derivatives, such as Ubuntu, must also add the nobootwait mount option.

        ```
/dev/xvdf       /data   ext4    defaults,nofail        0       2
        ```

    d. After you've added the new entry to /etc/fstab, you need to check that your entry works. Run the sudo mount -a command to mount all file systems in /etc/fstab.

        ```
[ec2-user ~]$ sudo mount -a
        ```

        If the previous command does not produce an error, then your /etc/fstab file is OK and your file system will mount automatically at the next boot. If the command does produce any errors, examine the errors and try to correct your /etc/fstab.

        Warning

        Errors in the /etc/fstab file can render a system unbootable. Do not shut down a system that has errors in the /etc/fstab file.

    e. (Optional) If you are unsure how to correct /etc/fstab errors, you can always restore your backup /etc/fstab file with the following command.

        ```
[ec2-user ~]$ sudo mv /etc/fstab.orig /etc/fstab
        ```

7. Review the file permissions of your new volume mount to make sure that your users and applications can write to the volume.
