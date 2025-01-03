---
comments: true
date: 2011-07-22 17:13:40
layout: page
slug: nsis-plugin-litefirewall
title: NSIS Plugin --- liteFirewall
wordpress_id: 7382
---

### Background


There have been 3 firewall plugin for NSIS: Firewall-Disabler Plugin, NSIS Simple Firewall Plugin and NsisFirewall Plugin. But each of them has some shortcomings, so I just write one: liteFirewall. It's based on nsisFirewall. Thanks to its author.



	
  * [Firewall-Disbler plugin](http://nsis.sourceforge.net/Firewall-Disabler_plug-in): No one will use it.

	
  * [NsisFirewall plug-in](http://nsis.sourceforge.net/NsisFirewall_plug-in): It doesn't support firewall profiles (private, domain or public) on Vista/Windows 7.

	
  * [NSIS Simple Firewall Plugin](http://nsis.sourceforge.net/NSIS_Simple_Firewall_Plugin): It doesn't support Unicode NSIS.

	
  * [liteFirewall plug-in](http://nsis.sourceforge.net/LiteFirewall_Plugin): It supports both Unicode NSIS and firewall profiles.




### Presentation


liteFirewall is based on nsisFirewall, and it also allows you to perform easily 2 tasks:



	
  * Add an application to Windows Firewall exception list

	
  * Remove an application from Windows Firewall exception list


The advantage of liteFirewall compared to nsisFirewall is it can automatically figure out the current profile of windows firewall, and add a corresponding rule for your application.


### Download


[liteFirewall.zip](https://bitbucket.org/lsun/litefirewall/downloads/2011-07-liteFirewall.zip)

ZIP archive contains the plug-in DLL as well as documentation, source code and sample script.


### Usage




    liteFirewall::AddRule "<application path>" "<rule name>"
    liteFirewall::RemoveRule "<application path>" "<rule name>"


<application path>is the full path to the application you want to be authorized to access the network (or accept incoming connections). <rule name>is the title that will be given to this exception entry in the firewall control panel list.


### Examples




    ; Add NOTEPAD to the authorized list
    liteFirewall::AddRule "$WINDIRNotepad.exe" "liteFirewall Test"
    Pop $0
    ; Remove NOTEPAD from the authorized list
    liteFirewall::RemoveRule "$WINDIRNotepad.exe" "liteFirewall Test"
    Pop $0

### Source Code

This project is an open source project. You may compile the source code at <https://bitbucket.org/lsun/litefirewall/>.
