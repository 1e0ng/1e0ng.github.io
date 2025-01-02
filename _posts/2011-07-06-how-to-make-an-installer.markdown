---
comments: true
date: 2011-07-06 19:59:07
layout: post
slug: how-to-make-an-installer
title: How To Make a Windows Installer
wordpress_id: 674
categories: articles
tags:
- Software
tags:
- Install Package
- Installer
- NSIS
- Pidgin
- Unicode
---

## Introduction

There are many tools which can be used to make an installer, like NSIS, Install Shield, Advanced Installer, WiX, InnoSetup and even Visual Studio. Here I just show you how to make an installer by NSIS. NSIS (Nullsoft Scriptable Install System) is a professional open source system to create Windows installers. NSIS is script-based, which means you configure your installer by a script. That makes it small and flexible.

<!--more-->

You can download NSIS at the official website: http://nsis.sourcefore.net, but I recommend you download the Unicode version of NSIS here: http://www.scratchpaper.com, because if your installer is not in English, it will not correctly displayed in some circumstances, for example, your installer is in Chinese, but you want to install it in a English-version Windows, you may see garbled fonts.

## UAC Problem

On Vista and Windows 7 systems, you should met the UAC problem when you make your installer with NSIS. There IS a NSIS UAC plug-in, and you may download here: http://nsis.sourceforge.net/UAC_plug-in. But in my opinion, this plug-in is not elegant, as it creates a new progress when it elevate privileges, which makes the decompress process appears 2 times, one for each progress.

The installer of GTalk doesn’t use UAC and it doesn’t need administrative privilege at all! While the installer of QQ (another instant messenger), needs administrative privilege and it can’t install without the privilege. Both of the above installers doesn’t use UAC plugin, assuming they are made with NSIS.

Is there a way between GTalk and QQ? I don’t know. I’m finding a way that if both low and high privilege users can install my software without the ugly UAC plugin.

## Use 7z to Reduce the Size of the Installer

My test shows the size of my installer reduces about 20 percent when I use 7z to compress my installer. To do this, you need to use this plugin to extract 7z package: http://nsis.sourceforge.net/Nsis7z_plug-in. You have to write another script to compress your program package with 7z. In addition, you need to adjust the information for the size of volume needed to install during the installing process.

## An NSIS Bug

You would loose the focus of your program if you keep dragging the installer window while the progress bar is running until the next window appears.

## NSIS Is Not Cool Enough?

Maybe not.

## Example

To learn how to use NSIS, you can reference the official document http://nsis.sourceforge.net/Docs/, while there is an easier way, to read an example. This is the NSIS script for Pidgin (from http://nsis.sourceforge.net/Pidgin). Though it’s not excellent code, you will learn a lot if you are a newbie to make installers.

pidgin-installer.nsi:

```
; Installer script for win32 Pidgin
; Original Author: Herman Bloggs 
; Updated By: Daniel Atallah 
 
; NOTE: this .NSI script is intended for NSIS 2.27
;
 
;--------------------------------
;Global Variables
Var name
Var GTK_FOLDER
Var ISSILENT
Var STARTUP_RUN_KEY
Var SPELLCHECK_SEL
 
;--------------------------------
;Configuration
 
;The name var is set in .onInit
Name $name
 
!ifdef WITH_GTK
OutFile "pidgin-${PIDGIN_VERSION}.exe"
!else
!ifdef DEBUG
OutFile "pidgin-${PIDGIN_VERSION}-debug.exe"
!else
OutFile "pidgin-${PIDGIN_VERSION}-no-gtk.exe"
!endif
!endif
 
SetCompressor /SOLID lzma
ShowInstDetails show
ShowUninstDetails show
SetDateSave on
 
; $name and $INSTDIR are set in .onInit function..
 
!include "MUI.nsh"
!include "Sections.nsh"
!include "WinVer.nsh"
!include "LogicLib.nsh"
 
!include "FileFunc.nsh"
!insertmacro GetParameters
!insertmacro GetOptions
!insertmacro GetParent
 
!include "WordFunc.nsh"
!insertmacro VersionCompare
!insertmacro WordFind
!insertmacro un.WordFind
 
;--------------------------------
;Defines
 
!define PIDGIN_NSIS_INCLUDE_PATH		"."
!define PIDGIN_INSTALLER_DEPS			"........win32-devpidgin-inst-deps"
 
; Remove these and the stuff that uses them at some point
!define OLD_GAIM_REG_KEY			"SOFTWAREgaim"
!define OLD_GAIM_UNINSTALL_KEY			"SOFTWAREMicrosoftWindowsCurrentVersionUninstallGaim"
!define OLD_GAIM_UNINST_EXE			"gaim-uninst.exe"
 
!define PIDGIN_REG_KEY				"SOFTWAREpidgin"
!define PIDGIN_UNINSTALL_KEY			"SOFTWAREMicrosoftWindowsCurrentVersionUninstallPidgin"
 
!define HKLM_APP_PATHS_KEY			"SOFTWAREMicrosoftWindowsCurrentVersionApp Pathspidgin.exe"
!define STARTUP_RUN_KEY				"SOFTWAREMicrosoftWindowsCurrentVersionRun"
!define PIDGIN_UNINST_EXE			"pidgin-uninst.exe"
 
!define GTK_MIN_VERSION				"2.6.10"
!define GTK_REG_KEY				"SOFTWAREGTK2.0"
!define PERL_REG_KEY				"SOFTWAREPerl"
!define PERL_DLL				"perl510.dll"
!define GTK_DEFAULT_INSTALL_PATH		"$COMMONFILESGTK2.0"
!define GTK_RUNTIME_INSTALLER			"........gtk_installergtk-runtime*.exe"
 
!define ASPELL_REG_KEY				"SOFTWAREAspell"
!define DOWNLOADER_URL				"http://pidgin.im/win32/download_redir.php"
 
;--------------------------------
;Version resource
VIProductVersion "${PIDGIN_PRODUCT_VERSION}"
VIAddVersionKey "ProductName" "Pidgin"
VIAddVersionKey "FileVersion" "${PIDGIN_VERSION}"
VIAddVersionKey "ProductVersion" "${PIDGIN_VERSION}"
VIAddVersionKey "LegalCopyright" ""
!ifdef WITH_GTK
VIAddVersionKey "FileDescription" "Pidgin Installer (w/ GTK+ Installer)"
!else
!ifdef DEBUG
VIAddVersionKey "FileDescription" "Pidgin Installer (Debug Version)"
!else
VIAddVersionKey "FileDescription" "Pidgin Installer (w/o GTK+ Installer)"
!endif
!endif
 
;--------------------------------
;Reserve files used in .onInit
;for faster start-up
ReserveFile "${NSISDIR}PluginsSystem.dll"
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS
!insertmacro MUI_RESERVEFILE_LANGDLL
 
;--------------------------------
;Modern UI Configuration
 
  !define MUI_ICON				".pixmapspidgin-install.ico"
  !define MUI_UNICON				".pixmapspidgin-install.ico"
  !define MUI_WELCOMEFINISHPAGE_BITMAP		".pixmapspidgin-intro.bmp"
  !define MUI_HEADERIMAGE
  !define MUI_HEADERIMAGE_BITMAP		".pixmapspidgin-header.bmp"
 
  ; Alter License section
  !define MUI_LICENSEPAGE_BUTTON		$(PIDGIN_LICENSE_BUTTON)
  !define MUI_LICENSEPAGE_TEXT_BOTTOM		$(PIDGIN_LICENSE_BOTTOM_TEXT)
 
  !define MUI_LANGDLL_REGISTRY_ROOT "HKCU"
  !define MUI_LANGDLL_REGISTRY_KEY ${PIDGIN_REG_KEY}
  !define MUI_LANGDLL_REGISTRY_VALUENAME "Installer Language"
 
  !define MUI_COMPONENTSPAGE_SMALLDESC
  !define MUI_ABORTWARNING
 
  ;Finish Page config
  !define MUI_FINISHPAGE_NOAUTOCLOSE
  !define MUI_FINISHPAGE_RUN			"$INSTDIRpidgin.exe"
  !define MUI_FINISHPAGE_RUN_NOTCHECKED
  !define MUI_FINISHPAGE_LINK			$(PIDGIN_FINISH_VISIT_WEB_SITE)
  !define MUI_FINISHPAGE_LINK_LOCATION		"http://pidgin.im"
 
;--------------------------------
;Pages
 
  !define MUI_PAGE_CUSTOMFUNCTION_PRE		preWelcomePage
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE			"../../../COPYING"
  !insertmacro MUI_PAGE_COMPONENTS
 
!ifdef WITH_GTK
  ; GTK+ install dir page
  !define MUI_PAGE_CUSTOMFUNCTION_PRE		preGtkDirPage
  !define MUI_PAGE_CUSTOMFUNCTION_LEAVE		postGtkDirPage
  !define MUI_DIRECTORYPAGE_VARIABLE		$GTK_FOLDER
  !insertmacro MUI_PAGE_DIRECTORY
!endif
 
  ; Pidgin install dir page
  !insertmacro MUI_PAGE_DIRECTORY
 
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH
 
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH
 
;--------------------------------
;Languages
 
  ;; English goes first because its the default. The rest are
  ;; in alphabetical order (at least the strings actually displayed
  ;; will be).
 
  !insertmacro MUI_LANGUAGE "English"
 
  !insertmacro MUI_LANGUAGE "Afrikaans"
  !insertmacro MUI_LANGUAGE "Albanian"
  !insertmacro MUI_LANGUAGE "Arabic"
  !insertmacro MUI_LANGUAGE "Basque"
  !insertmacro MUI_LANGUAGE "Bulgarian"
  !insertmacro MUI_LANGUAGE "Catalan"
  !insertmacro MUI_LANGUAGE "Czech"
  !insertmacro MUI_LANGUAGE "Danish"
  !insertmacro MUI_LANGUAGE "SimpChinese"
  !insertmacro MUI_LANGUAGE "TradChinese"
  !insertmacro MUI_LANGUAGE "German"
  !insertmacro MUI_LANGUAGE "Spanish"
  !insertmacro MUI_LANGUAGE "Farsi"
  !insertmacro MUI_LANGUAGE "Finnish"
  !insertmacro MUI_LANGUAGE "French"
  !insertmacro MUI_LANGUAGE "Hebrew"
  !insertmacro MUI_LANGUAGE "Italian"
  !insertmacro MUI_LANGUAGE "Japanese"
  !insertmacro MUI_LANGUAGE "Korean"
  !insertmacro MUI_LANGUAGE "Kurdish"
  !insertmacro MUI_LANGUAGE "Lithuanian"
  !insertmacro MUI_LANGUAGE "Hungarian"
  !insertmacro MUI_LANGUAGE "Dutch"
  !insertmacro MUI_LANGUAGE "Norwegian"
  !insertmacro MUI_LANGUAGE "Polish"
  !insertmacro MUI_LANGUAGE "PortugueseBR"
  !insertmacro MUI_LANGUAGE "Portuguese"
  !insertmacro MUI_LANGUAGE "Romanian"
  !insertmacro MUI_LANGUAGE "Russian"
  !insertmacro MUI_LANGUAGE "Serbian"
  !insertmacro MUI_LANGUAGE "Slovak"
  !insertmacro MUI_LANGUAGE "Slovenian"
  !insertmacro MUI_LANGUAGE "Swedish"
 
;--------------------------------
;Translations
 
  !define PIDGIN_DEFAULT_LANGFILE "${PIDGIN_NSIS_INCLUDE_PATH}translationsenglish.nsh"
 
  !include "${PIDGIN_NSIS_INCLUDE_PATH}langmacros.nsh"
 
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "AFRIKAANS"	"${PIDGIN_NSIS_INCLUDE_PATH}translationsafrikaans.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "ALBANIAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsalbanian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "ARABIC"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsarabic.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "BASQUE"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsbasque.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "BULGARIAN"	"${PIDGIN_NSIS_INCLUDE_PATH}translationsbulgarian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "CATALAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationscatalan.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "CZECH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsczech.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "DANISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsdanish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "DUTCH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsdutch.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "ENGLISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsenglish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "FARSI"		"${PIDGIN_NSIS_INCLUDE_PATH}translationspersian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "FINNISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsfinnish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "FRENCH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsfrench.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "GERMAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsgerman.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "HEBREW"		"${PIDGIN_NSIS_INCLUDE_PATH}translationshebrew.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "HUNGARIAN"	"${PIDGIN_NSIS_INCLUDE_PATH}translationshungarian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "ITALIAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsitalian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "JAPANESE"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsjapanese.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "KOREAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationskorean.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "KURDISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationskurdish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "LITHUANIAN"	"${PIDGIN_NSIS_INCLUDE_PATH}translationslithuanian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "NORWEGIAN"	"${PIDGIN_NSIS_INCLUDE_PATH}translationsnorwegian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "POLISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationspolish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "PORTUGUESE"	"${PIDGIN_NSIS_INCLUDE_PATH}translationsportuguese.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "PORTUGUESEBR"	"${PIDGIN_NSIS_INCLUDE_PATH}translationsportuguese-br.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "ROMANIAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsromanian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "RUSSIAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsrussian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "SERBIAN"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsserbian-latin.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "SIMPCHINESE"	"${PIDGIN_NSIS_INCLUDE_PATH}translationssimp-chinese.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "SLOVAK"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsslovak.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "SLOVENIAN"	"${PIDGIN_NSIS_INCLUDE_PATH}translationsslovenian.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "SPANISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsspanish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "SWEDISH"		"${PIDGIN_NSIS_INCLUDE_PATH}translationsswedish.nsh"
  !insertmacro PIDGIN_MACRO_INCLUDE_LANGFILE "TRADCHINESE"	"${PIDGIN_NSIS_INCLUDE_PATH}translationstrad-chinese.nsh"
 
;--------------------------------
;Reserve Files
  ; Only need this if using bzip2 compression
 
  !insertmacro MUI_RESERVEFILE_INSTALLOPTIONS
  !insertmacro MUI_RESERVEFILE_LANGDLL
  ReserveFile "${NSISDIR}PluginsUserInfo.dll"
 
 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Start Install Sections ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 
;--------------------------------
;Uninstall any old version of Pidgin (or Gaim)
 
Section -SecUninstallOldPidgin
  ; Check install rights..
  Call CheckUserInstallRights
  Pop $R0
 
  ;First try to uninstall Pidgin
  StrCpy $R4 ${PIDGIN_REG_KEY}
  StrCpy $R5 ${PIDGIN_UNINSTALL_KEY}
  StrCpy $R6 ${PIDGIN_UNINST_EXE}
  StrCpy $R7 "Pidgin"
 
  start_comparison:
  ;If pidgin is currently set to run on startup,
  ;  save the section of the Registry where the setting is before uninstalling,
  ;  so we can put it back after installing the new version
  ClearErrors
  ReadRegStr $STARTUP_RUN_KEY HKCU "${STARTUP_RUN_KEY}" $R7
  IfErrors +3
  StrCpy $STARTUP_RUN_KEY "HKCU"
  Goto +5
  ClearErrors
  ReadRegStr $STARTUP_RUN_KEY HKLM "${STARTUP_RUN_KEY}" $R7
  IfErrors +2
  StrCpy $STARTUP_RUN_KEY "HKLM"
 
  StrCmp $R0 "HKLM" compare_hklm
  StrCmp $R0 "HKCU" compare_hkcu done
 
  compare_hkcu:
      ReadRegStr $R1 HKCU $R4 ""
      ReadRegStr $R2 HKCU $R4 "Version"
      ReadRegStr $R3 HKCU "$R5" "UninstallString"
      Goto try_uninstall
 
  compare_hklm:
      ReadRegStr $R1 HKLM $R4 ""
      ReadRegStr $R2 HKLM $R4 "Version"
      ReadRegStr $R3 HKLM "$R5" "UninstallString"
 
  ; If a previous version exists, remove it
  try_uninstall:
    StrCmp $R1 "" no_version_found
      ; Version key started with 0.60a3. Prior versions can't be
      ; automatically uninstalled.
      StrCmp $R2 "" uninstall_problem
        ; Check if we have uninstall string..
        IfFileExists $R3 0 uninstall_problem
          ; Have uninstall string, go ahead and uninstall.
          SetOverwrite on
          ; Need to copy uninstaller outside of the install dir
          ClearErrors
          CopyFiles /SILENT $R3 "$TEMP$R6"
          SetOverwrite off
          IfErrors uninstall_problem
            ; Ready to uninstall..
            ClearErrors
            ExecWait '"$TEMP$R6" /S _?=$R1'
            IfErrors exec_error
              Delete "$TEMP$R6"
            Goto done
 
            exec_error:
              Delete "$TEMP$R6"
              Goto uninstall_problem
 
        no_version_found:
          ;We've already tried to fallback to an old gaim instance
          StrCmp $R7 "Gaim" done
          ; If we couldn't uninstall Pidgin, try to uninstall Gaim
          StrCpy $STARTUP_RUN_KEY "NONE"
          StrCpy $R4 ${OLD_GAIM_REG_KEY}
          StrCpy $R5 ${OLD_GAIM_UNINSTALL_KEY}
          StrCpy $R6 ${OLD_GAIM_UNINST_EXE}
          StrCpy $R7 "Gaim"
          Goto start_comparison
 
        uninstall_problem:
          ; We can't uninstall.  Either the user must manually uninstall or we ignore and reinstall over it.
          MessageBox MB_OKCANCEL $(PIDGIN_PROMPT_CONTINUE_WITHOUT_UNINSTALL) /SD IDOK IDOK done
          Quit
  done:
SectionEnd
 
 
;--------------------------------
;GTK+ Runtime Install Section
 
!ifdef WITH_GTK
Section $(GTK_SECTION_TITLE) SecGtk
 
  Call CheckUserInstallRights
  Pop $R1
 
  SetOutPath $TEMP
  SetOverwrite on
  File /oname=gtk-runtime.exe ${GTK_RUNTIME_INSTALLER}
  SetOverwrite off
 
  Call DoWeNeedGtk
  Pop $R0
  Pop $R6
 
  StrCmp $R0 "0" have_gtk
  StrCmp $R0 "1" upgrade_gtk
  StrCmp $R0 "2" upgrade_gtk
  ;StrCmp $R0 "3" no_gtk no_gtk
 
  ;no_gtk:
    StrCmp $R1 "NONE" gtk_no_install_rights
    ClearErrors
    ExecWait '"$TEMPgtk-runtime.exe" /L=$LANGUAGE $ISSILENT /D=$GTK_FOLDER'
    IfErrors gtk_install_error done
 
  upgrade_gtk:
    StrCpy $GTK_FOLDER $R6
    StrCmp $R0 "2" +2 ; Upgrade isn't optional
    MessageBox MB_YESNO $(GTK_UPGRADE_PROMPT) /SD IDYES IDNO done
    ClearErrors
    ExecWait '"$TEMPgtk-runtime.exe" /L=$LANGUAGE $ISSILENT /D=$GTK_FOLDER'
    IfErrors gtk_install_error done
 
    gtk_install_error:
      Delete "$TEMPgtk-runtime.exe"
      MessageBox MB_OK $(GTK_INSTALL_ERROR) /SD IDOK
      Quit
 
  have_gtk:
    StrCpy $GTK_FOLDER $R6
    StrCmp $R1 "NONE" done ; If we have no rights, we can't re-install
    ; Even if we have a sufficient version of GTK+, we give user choice to re-install.
    ClearErrors
    ExecWait '"$TEMPgtk-runtime.exe" /L=$LANGUAGE $ISSILENT'
    IfErrors gtk_install_error
    Goto done
 
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; end got_install rights
 
  gtk_no_install_rights:
    ; Install GTK+ to Pidgin install dir
    StrCpy $GTK_FOLDER $INSTDIR
    ClearErrors
    ExecWait '"$TEMPgtk-runtime.exe" /L=$LANGUAGE $ISSILENT /D=$GTK_FOLDER'
    IfErrors gtk_install_error
      SetOverwrite on
      ClearErrors
      CopyFiles /FILESONLY "$GTK_FOLDERbin*.dll" $GTK_FOLDER
      SetOverwrite off
      IfErrors gtk_install_error
        Delete "$GTK_FOLDERbin*.dll"
        Goto done
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; end gtk_no_install_rights
 
  done:
    Delete "$TEMPgtk-runtime.exe"
SectionEnd ; end of GTK+ section
!endif
 
;--------------------------------
;Pidgin Install Section
 
Section $(PIDGIN_SECTION_TITLE) SecPidgin
  SectionIn 1 RO
 
  ; Check install rights..
  Call CheckUserInstallRights
  Pop $R0
 
  ; Get GTK+ lib dir if we have it..
 
  StrCmp $R0 "NONE" pidgin_none
  StrCmp $R0 "HKLM" pidgin_hklm pidgin_hkcu
 
  pidgin_hklm:
    ReadRegStr $R1 HKLM ${GTK_REG_KEY} "Path"
    WriteRegStr HKLM "${HKLM_APP_PATHS_KEY}" "" "$INSTDIRpidgin.exe"
    WriteRegStr HKLM "${HKLM_APP_PATHS_KEY}" "Path" "$R1bin"
    WriteRegStr HKLM ${PIDGIN_REG_KEY} "" "$INSTDIR"
    WriteRegStr HKLM ${PIDGIN_REG_KEY} "Version" "${PIDGIN_VERSION}"
    WriteRegStr HKLM "${PIDGIN_UNINSTALL_KEY}" "DisplayName" "Pidgin"
    WriteRegStr HKLM "${PIDGIN_UNINSTALL_KEY}" "DisplayVersion" "${PIDGIN_VERSION}"
    WriteRegStr HKLM "${PIDGIN_UNINSTALL_KEY}" "HelpLink" "http://developer.pidgin.im/wiki/Using Pidgin"
    WriteRegDWORD HKLM "${PIDGIN_UNINSTALL_KEY}" "NoModify" 1
    WriteRegDWORD HKLM "${PIDGIN_UNINSTALL_KEY}" "NoRepair" 1
    WriteRegStr HKLM "${PIDGIN_UNINSTALL_KEY}" "UninstallString" "$INSTDIR${PIDGIN_UNINST_EXE}"
    ; Sets scope of the desktop and Start Menu entries for all users.
    SetShellVarContext "all"
    Goto pidgin_install_files
 
  pidgin_hkcu:
    ReadRegStr $R1 HKCU ${GTK_REG_KEY} "Path"
    StrCmp $R1 "" 0 +2
      ReadRegStr $R1 HKLM ${GTK_REG_KEY} "Path"
 
    WriteRegStr HKCU ${PIDGIN_REG_KEY} "" "$INSTDIR"
    WriteRegStr HKCU ${PIDGIN_REG_KEY} "Version" "${PIDGIN_VERSION}"
    WriteRegStr HKCU "${PIDGIN_UNINSTALL_KEY}" "DisplayName" "Pidgin"
    WriteRegStr HKCU "${PIDGIN_UNINSTALL_KEY}" "DisplayVersion" "${PIDGIN_VERSION}"
    WriteRegStr HKCU "${PIDGIN_UNINSTALL_KEY}" "HelpLink" "http://developer.pidgin.im/wiki/Using Pidgin"
    WriteRegDWORD HKCU "${PIDGIN_UNINSTALL_KEY}" "NoModify" 1
    WriteRegDWORD HKCU "${PIDGIN_UNINSTALL_KEY}" "NoRepair" 1
    WriteRegStr HKCU "${PIDGIN_UNINSTALL_KEY}" "UninstallString" "$INSTDIR${PIDGIN_UNINST_EXE}"
    Goto pidgin_install_files
 
  pidgin_none:
    ReadRegStr $R1 HKLM ${GTK_REG_KEY} "Path"
 
  pidgin_install_files:
    SetOutPath "$INSTDIR"
    ; Pidgin files
    SetOverwrite on
 
    ;Delete old liboscar and libjabber since they tend to be problematic
    Delete "$INSTDIRpluginsliboscar.dll"
    Delete "$INSTDIRpluginslibjabber.dll"
 
    File /r ......${PIDGIN_INSTALL_DIR}*.*
    !ifdef DEBUG
    File "${PIDGIN_INSTALLER_DEPS}exchndl.dll"
    !endif
 
    ; Install shfolder.dll if need be..
    SearchPath $R4 "shfolder.dll"
    StrCmp $R4 "" 0 got_shfolder
      SetOutPath "$SYSDIR"
      File "${PIDGIN_INSTALLER_DEPS}shfolder.dll"
      SetOutPath "$INSTDIR"
    got_shfolder:
 
    ; Check if Perl is installed, if so add it to the AppPaths
    ReadRegStr $R2 HKLM ${PERL_REG_KEY} ""
    StrCmp $R2 "" 0 perl_exists
      ReadRegStr $R2 HKCU ${PERL_REG_KEY} ""
      StrCmp $R2 "" perl_done perl_exists
 
      perl_exists:
        IfFileExists "$R2bin${PERL_DLL}" 0 perl_done
        StrCmp $R0 "HKLM" 0 perl_done
          ReadRegStr $R3 HKLM "${HKLM_APP_PATHS_KEY}" "Path"
          WriteRegStr HKLM "${HKLM_APP_PATHS_KEY}" "Path" "$R3;$R2bin"
 
    perl_done:
 
    ; If this is under NT4, delete the SILC support stuff
    ; there is a bug that will prevent any account from connecting
    ; See https://lists.silcnet.org/pipermail/silc-devel/2005-January/001588.html
    ; Also, remove the GSSAPI SASL plugin and associated files as they aren't
    ; compatible with NT4.
    ${If} ${IsNT}
    ${AndIf} ${IsWinNT4}
      ;SILC
      Delete "$INSTDIRpluginslibsilc.dll"
      Delete "$INSTDIRlibsilcclient-1-1-2.dll"
      Delete "$INSTDIRlibsilc-1-1-2.dll"
      ;GSSAPI
      Delete "$INSTDIRsasl2saslGSSAPI.dll"
    ${EndIf}
 
    SetOutPath "$INSTDIR"
 
    ; If we don't have install rights we're done
    StrCmp $R0 "NONE" done
    SetOverwrite off
 
    ; write out uninstaller
    SetOverwrite on
    WriteUninstaller "$INSTDIR${PIDGIN_UNINST_EXE}"
    SetOverwrite off
 
    ; If we previously had pidgin set up to run on startup, make it do so again
    StrCmp $STARTUP_RUN_KEY "HKCU" +1 +2
    WriteRegStr HKCU "${STARTUP_RUN_KEY}" "Pidgin" "$INSTDIRpidgin.exe"
    StrCmp $STARTUP_RUN_KEY "HKLM" +1 +2
    WriteRegStr HKLM "${STARTUP_RUN_KEY}" "Pidgin" "$INSTDIRpidgin.exe"
 
  done:
SectionEnd ; end of default Pidgin section
 
;--------------------------------
;Shortcuts
 
SectionGroup /e $(PIDGIN_SHORTCUTS_SECTION_TITLE) SecShortcuts
  Section /o $(PIDGIN_DESKTOP_SHORTCUT_SECTION_TITLE) SecDesktopShortcut
    SetOverwrite on
    CreateShortCut "$DESKTOPPidgin.lnk" "$INSTDIRpidgin.exe"
    SetOverwrite off
  SectionEnd
  Section $(PIDGIN_STARTMENU_SHORTCUT_SECTION_TITLE) SecStartMenuShortcut
    SetOverwrite on
    CreateShortCut "$SMPROGRAMSPidgin.lnk" "$INSTDIRpidgin.exe"
    SetOverwrite off
  SectionEnd
SectionGroupEnd
 
;--------------------------------
;URI Handling
 
!macro URI_SECTION proto
  Section /o "${proto}:" SecURI_${proto}
    Push "${proto}"
    Call RegisterURIHandler
  SectionEnd
!macroend
SectionGroup /e $(URI_HANDLERS_SECTION_TITLE) SecURIHandlers
  !insertmacro URI_SECTION "aim"
  !insertmacro URI_SECTION "msnim"
  !insertmacro URI_SECTION "myim"
  !insertmacro URI_SECTION "ymsgr"
SectionGroupEnd
 
;--------------------------------
;Spell Checking
 
SectionGroup /e $(PIDGIN_SPELLCHECK_SECTION_TITLE) SecSpellCheck
  Section /o $(PIDGIN_SPELLCHECK_BRETON) SecSpellCheckBreton
    Push ${SecSpellCheckBreton}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_CATALAN) SecSpellCheckCatalan
    Push ${SecSpellCheckCatalan}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_CZECH) SecSpellCheckCzech
    Push ${SecSpellCheckCzech}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_WELSH) SecSpellCheckWelsh
    Push ${SecSpellCheckWelsh}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_DANISH) SecSpellCheckDanish
    Push ${SecSpellCheckDanish}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_GERMAN) SecSpellCheckGerman
    Push ${SecSpellCheckGerman}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_GREEK) SecSpellCheckGreek
    Push ${SecSpellCheckGreek}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_ENGLISH) SecSpellCheckEnglish
    Push ${SecSpellCheckEnglish}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_ESPERANTO) SecSpellCheckEsperanto
    Push ${SecSpellCheckEsperanto}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_SPANISH) SecSpellCheckSpanish
    Push ${SecSpellCheckSpanish}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_FAROESE) SecSpellCheckFaroese
    Push ${SecSpellCheckFaroese}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_FRENCH) SecSpellCheckFrench
    Push ${SecSpellCheckFrench}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_ITALIAN) SecSpellCheckItalian
    Push ${SecSpellCheckItalian}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_DUTCH) SecSpellCheckDutch
    Push ${SecSpellCheckDutch}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_NORWEGIAN) SecSpellCheckNorwegian
    Push ${SecSpellCheckNorwegian}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_POLISH) SecSpellCheckPolish
    Push ${SecSpellCheckPolish}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_PORTUGUESE) SecSpellCheckPortuguese
    Push ${SecSpellCheckPortuguese}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_ROMANIAN) SecSpellCheckRomanian
    Push ${SecSpellCheckRomanian}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_RUSSIAN) SecSpellCheckRussian
    Push ${SecSpellCheckRussian}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_SLOVAK) SecSpellCheckSlovak
    Push ${SecSpellCheckSlovak}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_SWEDISH) SecSpellCheckSwedish
    Push ${SecSpellCheckSwedish}
    Call InstallAspellAndDict
  SectionEnd
  Section /o $(PIDGIN_SPELLCHECK_UKRAINIAN) SecSpellCheckUkrainian
    Push ${SecSpellCheckUkrainian}
    Call InstallAspellAndDict
  SectionEnd
SectionGroupEnd
 
;--------------------------------
;Uninstaller Section
 
 
Section Uninstall
  Call un.CheckUserInstallRights
  Pop $R0
  StrCmp $R0 "NONE" no_rights
  StrCmp $R0 "HKCU" try_hkcu try_hklm
 
  try_hkcu:
    ReadRegStr $R0 HKCU ${PIDGIN_REG_KEY} ""
    StrCmp $R0 $INSTDIR 0 cant_uninstall
      ; HKCU install path matches our INSTDIR so uninstall
      DeleteRegKey HKCU ${PIDGIN_REG_KEY}
      DeleteRegKey HKCU "${PIDGIN_UNINSTALL_KEY}"
      Goto cont_uninstall
 
  try_hklm:
    ReadRegStr $R0 HKLM ${PIDGIN_REG_KEY} ""
    StrCmp $R0 $INSTDIR 0 try_hkcu
      ; HKLM install path matches our INSTDIR so uninstall
      DeleteRegKey HKLM ${PIDGIN_REG_KEY}
      DeleteRegKey HKLM "${PIDGIN_UNINSTALL_KEY}"
      DeleteRegKey HKLM "${HKLM_APP_PATHS_KEY}"
      ; Sets start menu and desktop scope to all users..
      SetShellVarContext "all"
 
  cont_uninstall:
    ; The WinPrefs plugin may have left this behind..
    DeleteRegValue HKCU "${STARTUP_RUN_KEY}" "Pidgin"
    DeleteRegValue HKLM "${STARTUP_RUN_KEY}" "Pidgin"
    ; Remove Language preference info
    DeleteRegValue HKCU "${PIDGIN_REG_KEY}" "Installer Language"
 
    ; Remove any URI handlers
    ; I can't think of an easy way to maintain a list in a single place
    Push "aim"
    Call un.UnregisterURIHandler
    Push "msnim"
    Call un.UnregisterURIHandler
    Push "myim"
    Call un.UnregisterURIHandler
    Push "ymsgr"
    Call un.UnregisterURIHandler
 
    Delete "$INSTDIRca-certsCAcert_Class3.pem"
    Delete "$INSTDIRca-certsCAcert_Root.pem"
    Delete "$INSTDIRca-certsEquifax_Secure_CA.pem"
    Delete "$INSTDIRca-certsGTE_CyberTrust_Global_Root.pem"
    Delete "$INSTDIRca-certsMicrosoft_Internet_Authority.pem"
    Delete "$INSTDIRca-certsMicrosoft_Secure_Server_Authority.pem"
    Delete "$INSTDIRca-certsStartCom_Free_SSL_CA.pem"
    Delete "$INSTDIRca-certsVerisign_Class3_Primary_CA.pem"
    Delete "$INSTDIRca-certsVeriSign_Class_3_Public_Primary_Certification_Authority_-_G5.pem"
    Delete "$INSTDIRca-certsVeriSign_International_Server_Class_3_CA.pem"
    Delete "$INSTDIRca-certsVerisign_RSA_Secure_Server_CA.pem"
    RMDir "$INSTDIRca-certs"
    RMDir /r "$INSTDIRlocale"
    RMDir /r "$INSTDIRpixmaps"
    RMDir /r "$INSTDIRperlmod"
    Delete "$INSTDIRpluginsautoaccept.dll"
    Delete "$INSTDIRpluginsbuddynote.dll"
    Delete "$INSTDIRpluginsconvcolors.dll"
    Delete "$INSTDIRpluginsextplacement.dll"
    Delete "$INSTDIRpluginsgtkbuddynote.dll"
    Delete "$INSTDIRpluginshistory.dll"
    Delete "$INSTDIRpluginsiconaway.dll"
    Delete "$INSTDIRpluginsidle.dll"
    Delete "$INSTDIRpluginsjoinpart.dll"
    Delete "$INSTDIRpluginslibaim.dll"
    Delete "$INSTDIRpluginslibbonjour.dll"
    Delete "$INSTDIRpluginslibgg.dll"
    Delete "$INSTDIRpluginslibicq.dll"
    Delete "$INSTDIRpluginslibirc.dll"
    Delete "$INSTDIRpluginslibmsn.dll"
    Delete "$INSTDIRpluginslibmyspace.dll"
    Delete "$INSTDIRpluginslibnapster.dll"
    Delete "$INSTDIRpluginslibnovell.dll"
    Delete "$INSTDIRpluginslibqq.dll"
    Delete "$INSTDIRpluginslibsametime.dll"
    Delete "$INSTDIRpluginslibsilc.dll"
    Delete "$INSTDIRpluginslibsimple.dll"
    Delete "$INSTDIRpluginslibtoc.dll"
    Delete "$INSTDIRpluginslibyahoo.dll"
    Delete "$INSTDIRpluginslibxmpp.dll"
    Delete "$INSTDIRpluginslog_reader.dll"
    Delete "$INSTDIRpluginsmarkerline.dll"
    Delete "$INSTDIRpluginsnewline.dll"
    Delete "$INSTDIRpluginsnotify.dll"
    Delete "$INSTDIRpluginsofflinemsg.dll"
    Delete "$INSTDIRpluginsperl.dll"
    Delete "$INSTDIRpluginspidginrc.dll"
    Delete "$INSTDIRpluginspsychic.dll"
    Delete "$INSTDIRpluginsrelnot.dll"
    Delete "$INSTDIRpluginssendbutton.dll"
    Delete "$INSTDIRpluginsspellchk.dll"
    Delete "$INSTDIRpluginsssl-nss.dll"
    Delete "$INSTDIRpluginsssl.dll"
    Delete "$INSTDIRpluginsstatenotify.dll"
    Delete "$INSTDIRpluginstcl.dll"
    Delete "$INSTDIRpluginsticker.dll"
    Delete "$INSTDIRpluginstimestamp.dll"
    Delete "$INSTDIRpluginstimestamp_format.dll"
    Delete "$INSTDIRpluginswin2ktrans.dll"
    Delete "$INSTDIRpluginswinprefs.dll"
    Delete "$INSTDIRpluginsxmppconsole.dll"
    RMDir "$INSTDIRplugins"
    RMDir /r "$INSTDIRsasl2"
    Delete "$INSTDIRsoundspurplealert.wav"
    Delete "$INSTDIRsoundspurplelogin.wav"
    Delete "$INSTDIRsoundspurplelogout.wav"
    Delete "$INSTDIRsoundspurplereceive.wav"
    Delete "$INSTDIRsoundspurplesend.wav"
    RMDir "$INSTDIRsoundspurple"
    RMDir "$INSTDIRsounds"
    Delete "$INSTDIRfreebl3.dll"
    Delete "$INSTDIRidletrack.dll"
    Delete "$INSTDIRlibgtkspell.dll"
    Delete "$INSTDIRlibjabber.dll"
    Delete "$INSTDIRlibmeanwhile-1.dll"
    Delete "$INSTDIRliboscar.dll"
    Delete "$INSTDIRlibpurple.dll"
    Delete "$INSTDIRlibsasl.dll"
    Delete "$INSTDIRlibsilc-1-1-2.dll"
    Delete "$INSTDIRlibsilcclient-1-1-2.dll"
    Delete "$INSTDIRlibxml2.dll"
    Delete "$INSTDIRnspr4.dll"
    Delete "$INSTDIRnss3.dll"
    Delete "$INSTDIRnssckbi.dll"
    Delete "$INSTDIRpidgin.dll"
    Delete "$INSTDIRpidgin.exe"
    Delete "$INSTDIRplc4.dll"
    Delete "$INSTDIRplds4.dll"
    Delete "$INSTDIRsmime3.dll"
    Delete "$INSTDIRsoftokn3.dll"
    Delete "$INSTDIRssl3.dll"
    Delete "$INSTDIR${PIDGIN_UNINST_EXE}"
    !ifdef DEBUG
    Delete "$INSTDIRexchndl.dll"
    !endif
    Delete "$INSTDIRinstall.log"
 
    ;Try to remove Pidgin install dir (only if empty)
    RMDir "$INSTDIR"
 
    ; Shortcuts..
    Delete "$DESKTOPPidgin.lnk"
 
    Goto done
 
  cant_uninstall:
    MessageBox MB_OK $(un.PIDGIN_UNINSTALL_ERROR_1) /SD IDOK
    Quit
 
  no_rights:
    MessageBox MB_OK $(un.PIDGIN_UNINSTALL_ERROR_2) /SD IDOK
    Quit
 
  done:
SectionEnd ; end of uninstall section
 
;--------------------------------
;Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecPidgin} 
        $(PIDGIN_SECTION_DESCRIPTION)
!ifdef WITH_GTK
  !insertmacro MUI_DESCRIPTION_TEXT ${SecGtk} 
        $(GTK_SECTION_DESCRIPTION)
!endif
 
  !insertmacro MUI_DESCRIPTION_TEXT ${SecShortcuts} 
        $(PIDGIN_SHORTCUTS_SECTION_DESCRIPTION)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktopShortcut} 
        $(PIDGIN_DESKTOP_SHORTCUT_DESC)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenuShortcut} 
        $(PIDGIN_STARTMENU_SHORTCUT_DESC)
 
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheck} 
        $(PIDGIN_SPELLCHECK_SECTION_DESCRIPTION)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckBreton} 
        "$(PIDGIN_SPELLCHECK_BRETON) (862kb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckCatalan} 
        "$(PIDGIN_SPELLCHECK_CATALAN) (3.9Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckCzech} 
        "$(PIDGIN_SPELLCHECK_CZECH) (17Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckWelsh} 
        "$(PIDGIN_SPELLCHECK_WELSH) (4.2Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckDanish} 
        "$(PIDGIN_SPELLCHECK_DANISH) (6.9Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckGerman} 
        "$(PIDGIN_SPELLCHECK_GERMAN) (5.4Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckGreek} 
        "$(PIDGIN_SPELLCHECK_GREEK) (7.1Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckEnglish} 
        "$(PIDGIN_SPELLCHECK_ENGLISH) (2.3Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckEsperanto} 
        "$(PIDGIN_SPELLCHECK_ESPERANTO) (5.7Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckSpanish} 
        "$(PIDGIN_SPELLCHECK_SPANISH) (7.0Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckFaroese} 
        "$(PIDGIN_SPELLCHECK_FAROESE) (913kb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckFrench} 
        "$(PIDGIN_SPELLCHECK_FRENCH) (9.3Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckItalian} 
        "$(PIDGIN_SPELLCHECK_ITALIAN) (770kb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckDutch} 
        "$(PIDGIN_SPELLCHECK_DUTCH) (3.7Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckNorwegian} 
        "$(PIDGIN_SPELLCHECK_NORWEGIAN) (3.2Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckPolish} 
        "$(PIDGIN_SPELLCHECK_POLISH) (9.3Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckPortuguese} 
        "$(PIDGIN_SPELLCHECK_PORTUGUESE) (5.5Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckRomanian} 
        "$(PIDGIN_SPELLCHECK_ROMANIAN) (906kb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckRussian} 
        "$(PIDGIN_SPELLCHECK_RUSSIAN) (11Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckSlovak} 
        "$(PIDGIN_SPELLCHECK_SLOVAK) (8.0Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckSwedish} 
        "$(PIDGIN_SPELLCHECK_SWEDISH) (2.2Mb)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecSpellCheckUkrainian} 
        "$(PIDGIN_SPELLCHECK_UKRAINIAN) (12Mb)"
!insertmacro MUI_FUNCTION_DESCRIPTION_END
 
;--------------------------------
;Functions
 
; Default the URI handler checkboxes if Pidgin is the current handler or if there is no handler
Function SelectURIHandlerSelections
  Push $R0
  Push $R1
  Push $R2
  Push $R3
 
  ; Start with the first URI handler
  IntOp $R0 ${SecURIHandlers} + 1
 
  start:
  ; If it is the end of the section group, stop
  SectionGetFlags $R0 $R1
  IntOp $R2 $R1 & ${SF_SECGRPEND}
  IntCmp $R2 ${SF_SECGRPEND} done
 
  SectionGetText $R0 $R2
  ;Strip the trailing ':'
  StrLen $R3 $R2
  IntOp $R3 $R3 - 1
  StrCpy $R2 $R2 $R3
 
  ClearErrors
  ReadRegStr $R3 HKCR "$R2" ""
  IfErrors default_on ;there is no current handler
 
  Push $R2
  Call CheckIfPidginIsCurrentURIHandler
  Pop $R3
 
  ; If Pidgin isn't the current handler, we don't steal it automatically
  IntCmp $R3 0 end_loop
 
  ;We default the URI handler checkbox on
  default_on:
  IntOp $R1 $R1 | ${SF_SELECTED} ; Select
  SectionSetFlags $R0 $R1
 
  end_loop:
  IntOp $R0 $R0 + 1 ;Advance to the next section
  Goto start
 
  done:
  Pop $R3
  Pop $R2
  Pop $R1
  Pop $R0
FunctionEnd ;SelectURIHandlerSections
 
; Check if Pidgin is the current handler
; Returns a boolean on the stack
!macro CheckIfPidginIsCurrentURIHandlerMacro UN
Function ${UN}CheckIfPidginIsCurrentURIHandler
  Exch $R0
  ClearErrors
 
  ReadRegStr $R0 HKCR "$R0shellOpencommand" ""
  IfErrors 0 +3
    IntOp $R0 0 + 0
    Goto done
 
  !ifdef __UNINSTALL__
  ${un.WordFind} "$R0" "pidgin.exe" "E+1{" $R0
  !else
  ${WordFind} "$R0" "pidgin.exe" "E+1{" $R0
  !endif
  IntOp $R0 0 + 1
  IfErrors 0 +2
    IntOp $R0 0 + 0
 
  done:
  Exch $R0
FunctionEnd
!macroend
!insertmacro CheckIfPidginIsCurrentURIHandlerMacro ""
!insertmacro CheckIfPidginIsCurrentURIHandlerMacro "un."
 
; If Pidgin is the current URI handler for the specified protocol, remove it.
Function un.UnregisterURIHandler
  Exch $R0
  Push $R1
 
  Push $R0
  Call un.CheckIfPidginIsCurrentURIHandler
  Pop $R1
 
  ; If Pidgin isn't the current handler, leave it as-is
  IntCmp $R1 0 done
 
  ;Unregister the URI handler
  DetailPrint "Unregistering $R0 URI Handler"
  DeleteRegKey HKCR "$R0"
 
  done:
  Pop $R1
  Pop $R0
FunctionEnd
 
Function RegisterURIHandler
  Exch $R0
  DetailPrint "Registering $R0 URI Handler"
  DeleteRegKey HKCR "$R0"
  WriteRegStr HKCR "$R0" "" "URL:$R0"
  WriteRegStr HKCR "$R0" "URL Protocol" ""
  WriteRegStr HKCR "$R0DefaultIcon" "" "$INSTDIRpidgin.exe"
  WriteRegStr HKCR "$R0shell" "" ""
  WriteRegStr HKCR "$R0shellOpen" "" ""
  WriteRegStr HKCR "$R0shellOpencommand" "" "$INSTDIRpidgin.exe --protocolhandler=%1"
  Pop $R0
FunctionEnd
 
 
!macro CheckUserInstallRightsMacro UN
Function ${UN}CheckUserInstallRights
  Push $0
  Push $1
  ClearErrors
  UserInfo::GetName
  IfErrors Win9x
  Pop $0
  UserInfo::GetAccountType
  Pop $1
 
  StrCmp $1 "Admin" 0 +3
    StrCpy $1 "HKLM"
    Goto done
  StrCmp $1 "Power" 0 +3
    StrCpy $1 "HKLM"
    Goto done
  StrCmp $1 "User" 0 +3
    StrCpy $1 "HKCU"
    Goto done
  StrCmp $1 "Guest" 0 +3
    StrCpy $1 "NONE"
    Goto done
  ; Unknown error
  StrCpy $1 "NONE"
  Goto done
 
  Win9x:
    StrCpy $1 "HKLM"
 
  done:
    Exch $1
    Exch
    Pop $0
FunctionEnd
!macroend
!insertmacro CheckUserInstallRightsMacro ""
!insertmacro CheckUserInstallRightsMacro "un."
 
;
; Usage:
;   Push $0 ; Path string
;   Call VerifyDir
;   Pop $0 ; 0 - Bad path  1 - Good path
;
Function VerifyDir
  Exch $0
  Push $1
  Push $2
  Loop:
    IfFileExists $0 dir_exists
    StrCpy $1 $0 ; save last
    ${GetParent} $0 $0
    StrLen $2 $0
    ; IfFileExists "C:" on xp returns true and on win2k returns false
    ; So we're done in such a case..
    IntCmp $2 2 loop_done
    ; GetParent of "C:" returns ""
    IntCmp $2 0 loop_done
    Goto Loop
 
  loop_done:
    StrCpy $1 "$0GaImFooB"
    ; Check if we can create dir on this drive..
    ClearErrors
    CreateDirectory $1
    IfErrors DirBad DirGood
 
  dir_exists:
    ClearErrors
    FileOpen $1 "$0pidginfoo.bar" w
    IfErrors PathBad PathGood
 
    DirGood:
      RMDir $1
      Goto PathGood1
 
    DirBad:
      RMDir $1
      Goto PathBad1
 
    PathBad:
      FileClose $1
      Delete "$0pidginfoo.bar"
      PathBad1:
      StrCpy $0 "0"
      Push $0
      Goto done
 
    PathGood:
      FileClose $1
      Delete "$0pidginfoo.bar"
      PathGood1:
      StrCpy $0 "1"
      Push $0
 
  done:
  Exch 3 ; The top of the stack contains the output variable
  Pop $0
  Pop $2
  Pop $1
FunctionEnd
 
Function .onVerifyInstDir
  Push $0
  Push $INSTDIR
  Call VerifyDir
  Pop $0
  StrCmp $0 "0" 0 dir_good
  Pop $0
  Abort
 
  dir_good:
  Pop $0
FunctionEnd
 
;
; Usage:
; Call DoWeNeedGtk
; First Pop:
;   0 - We have the correct version
;       Second Pop: Key where Version was found
;   1 - We have an old version that should work, prompt user for optional upgrade
;       Second Pop: HKLM or HKCU depending on where GTK was found.
;   2 - We have an old version that needs to be upgraded
;       Second Pop: HKLM or HKCU depending on where GTK was found.
;   3 - We don't have Gtk+ at all
;       Second Pop: "NONE, HKLM or HKCU" depending on our rights..
;
Function DoWeNeedGtk
  ; Logic should be:
  ; - Check what user rights we have (HKLM or HKCU)
  ;   - If HKLM rights..
  ;     - Only check HKLM key for GTK+
  ;       - If installed to HKLM, check it and return.
  ;   - If HKCU rights..
  ;     - First check HKCU key for GTK+
  ;       - if good or bad exists stop and ret.
  ;     - If no hkcu gtk+ install, check HKLM
  ;       - If HKLM ver exists but old, return as if no ver exits.
  ;   - If no rights
  ;     - Check HKLM
  Push $0
  Push $1
  Push $2
  Push $3
 
  Call CheckUserInstallRights
  Pop $1
  StrCmp $1 "HKLM" check_hklm
  StrCmp $1 "HKCU" check_hkcu check_hklm
    check_hkcu:
      ReadRegStr $0 HKCU ${GTK_REG_KEY} "Version"
      StrCpy $2 "HKCU"
      StrCmp $0 "" check_hklm have_gtk
 
    check_hklm:
      ReadRegStr $0 HKLM ${GTK_REG_KEY} "Version"
      StrCpy $2 "HKLM"
      StrCmp $0 "" no_gtk have_gtk
 
  have_gtk:
    ; GTK+ is already installed; check version.
    ; Change this to not even run the GTK installer if this version is already installed.
    ${VersionCompare} ${GTK_INSTALL_VERSION} $0 $3
    IntCmp $3 1 +1 good_version good_version
    ${VersionCompare} ${GTK_MIN_VERSION} $0 $3
 
      ; Bad version. If hklm ver and we have hkcu or no rights.. return no gtk
      StrCmp $1 "NONE" no_gtk ; if no rights.. can't upgrade
      StrCmp $1 "HKCU" 0 +2   ; if HKLM can upgrade..
      StrCmp $2 "HKLM" no_gtk ; have hkcu rights.. if found hklm ver can't upgrade..
      Push $2
      IntCmp $3 1 +3
        Push "1" ; Optional Upgrade
        Goto done
        Push "2" ; Mandatory Upgrade
        Goto done
 
  good_version:
    StrCmp $2 "HKLM" have_hklm_gtk have_hkcu_gtk
      have_hkcu_gtk:
        ; Have HKCU version
        ReadRegStr $0 HKCU ${GTK_REG_KEY} "Path"
        Goto good_version_cont
 
      have_hklm_gtk:
        ReadRegStr $0 HKLM ${GTK_REG_KEY} "Path"
        Goto good_version_cont
 
    good_version_cont:
      Push $0  ; The path to existing GTK+
      Push "0"
      Goto done
 
  no_gtk:
    Push $1 ; our rights
    Push "3"
    Goto done
 
  done:
  ; The top two items on the stack are what we want to return
  Exch 4
  Pop $1
  Exch 4
  Pop $0
  Pop $3
  Pop $2
FunctionEnd
 
 
!macro RunCheckMacro UN
Function ${UN}RunCheck
  Push $R0
  Push $R1
 
  IntOp $R1 0 + 0
  retry_runcheck:
  ; Close the Handle (needed if we're retrying)
  IntCmp $R1 0 +2
    System::Call 'kernel32::CloseHandle(i $R1) i .R1'
  System::Call 'kernel32::CreateMutexA(i 0, i 0, t "pidgin_is_running") i .R1 ?e'
  Pop $R0
  IntCmp $R0 0 +3 ;This could check for ERROR_ALREADY_EXISTS(183), but lets just assume
    MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION $(PIDGIN_IS_RUNNING) /SD IDCANCEL IDRETRY retry_runcheck
    Abort
 
  ; Close the Handle (If we don't do this, the uninstaller called from within will fail)
  ; This is not optimal because there is a (small) window of time when a new process could start
  System::Call 'kernel32::CloseHandle(i $R1) i .R1'
 
  Pop $R1
  Pop $R0
FunctionEnd
!macroend
!insertmacro RunCheckMacro ""
!insertmacro RunCheckMacro "un."
 
Function .onInit
  Push $R0
  Push $R1
  Push $R2
  Push $R3 ; This is only used for the Parameters throughout the function
 
  ${GetParameters} $R3
 
  IntOp $R1 0 + 0
  retry_runcheck:
  ; Close the Handle (needed if we're retrying)
  IntCmp $R1 0 +2
    System::Call 'kernel32::CloseHandle(i $R1) i .R1'
  System::Call 'kernel32::CreateMutexA(i 0, i 0, t "pidgin_installer_running") i .R1 ?e'
  Pop $R0
  IntCmp $R0 0 +3 ;This could check for ERROR_ALREADY_EXISTS(183), but lets just assume
    MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION $(INSTALLER_IS_RUNNING) /SD IDCANCEL IDRETRY retry_runcheck
    Abort
 
  ; Allow installer to run even if pidgin is running via "/NOPIDGINRUNCHECK=1"
  ; This is useful for testing
  ClearErrors
  ${GetOptions} "$R3" "/NOPIDGINRUNCHECK=" $R1
  IfErrors 0 +2
  Call RunCheck
 
  StrCpy $name "Pidgin ${PIDGIN_VERSION}"
  StrCpy $SPELLCHECK_SEL ""
 
  ;Try to copy the old Gaim installer Lang Reg. key
  ;(remove it after we're done to prevent this being done more than once)
  ClearErrors
  ReadRegStr $R0 HKCU "${PIDGIN_REG_KEY}" "Installer Language"
  IfErrors 0 +5
  ClearErrors
  ReadRegStr $R0 HKCU "${OLD_GAIM_REG_KEY}" "Installer Language"
  IfErrors +3
  DeleteRegValue HKCU "${OLD_GAIM_REG_KEY}" "Installer Language"
  WriteRegStr HKCU "${PIDGIN_REG_KEY}" "Installer Language" "$R0"
 
  !insertmacro SetSectionFlag ${SecSpellCheck} ${SF_RO}
  !insertmacro UnselectSection ${SecSpellCheck}
 
  ;Mark the dictionaries that are already installed as readonly
  Call SelectAndDisableInstalledDictionaries
 
  ;Preselect the URI handlers as appropriate
  Call SelectURIHandlerSelections
 
  ;Preselect the "shortcuts" checkboxes according to the previous installation
  ClearErrors
  ;Make sure that there was a previous installation
  ReadRegStr $R0 HKCU "${PIDGIN_REG_KEY}" "Installer Language"
  IfErrors done_preselecting_shortcuts
    ;Does the Desktop shortcut exist?
    GetFileTime "$DESKTOPPidgin.lnk" $R0 $R0
    IfErrors +1 +5
    ClearErrors
    SetShellVarContext "all"
    GetFileTime "$DESKTOPPidgin.lnk" $R0 $R0
    IfErrors preselect_startmenu_shortcut ;Desktop Shortcut if off by default
    !insertmacro SelectSection ${SecDesktopShortcut}
  preselect_startmenu_shortcut:
    ;Reset ShellVarContext because we may have changed it
    SetShellVarContext "current"
    ClearErrors
    ;Does the StartMenu shortcut exist?
    GetFileTime "$SMPROGRAMSPidgin.lnk" $R0 $R0
    IfErrors +1 done_preselecting_shortcuts ;StartMenu Shortcut is on by default
    ClearErrors
    SetShellVarContext "all"
    GetFileTime "$SMPROGRAMSPidgin.lnk" $R0 $R0
    IfErrors +1 done_preselecting_shortcuts ;StartMenu Shortcut is on by default
    !insertmacro UnselectSection ${SecStartMenuShortcut}
  done_preselecting_shortcuts:
  ;Reset ShellVarContext because we may have changed it
  SetShellVarContext "current"
 
  StrCpy $ISSILENT "/S"
  ; GTK installer has two silent states - one with Message boxes, one without
  ; If pidgin installer was run silently, we want to supress gtk installer msg boxes.
  IfSilent 0 +2
    StrCpy $ISSILENT "/NOUI"
 
  ClearErrors
  ${GetOptions} "$R3" "/L=" $R1
  IfErrors +3
  StrCpy $LANGUAGE $R1
  Goto skip_lang
 
  ; Select Language
    ; Display Language selection dialog
    !insertmacro MUI_LANGDLL_DISPLAY
    skip_lang:
 
  ClearErrors
  ${GetOptions} "$R3" "/DS=" $R1
  IfErrors +8
  SectionGetFlags ${SecDesktopShortcut} $R2
  StrCmp "1" $R1 0 +2
  IntOp $R2 $R2 | ${SF_SELECTED}
  StrCmp "0" $R1 0 +3
  IntOp $R1 ${SF_SELECTED} ~
  IntOp $R2 $R2 & $R1
  SectionSetFlags ${SecDesktopShortcut} $R2
 
  ClearErrors
  ${GetOptions} "$R3" "/SMS=" $R1
  IfErrors +8
  SectionGetFlags ${SecStartMenuShortcut} $R2
  StrCmp "1" $R1 0 +2
  IntOp $R2 $R2 | ${SF_SELECTED}
  StrCmp "0" $R1 0 +3
  IntOp $R1 ${SF_SELECTED} ~
  IntOp $R2 $R2 & $R1
  SectionSetFlags ${SecStartMenuShortcut} $R2
 
  ; If install path was set on the command, use it.
  StrCmp $INSTDIR "" 0 instdir_done
 
  ;  If pidgin or gaim is currently installed, we should default to where it is currently installed
  ClearErrors
  ReadRegStr $INSTDIR HKCU "${PIDGIN_REG_KEY}" ""
  IfErrors +2
  StrCmp $INSTDIR "" 0 instdir_done
  ClearErrors
  ReadRegStr $INSTDIR HKLM "${PIDGIN_REG_KEY}" ""
  IfErrors +2
  StrCmp $INSTDIR "" 0 instdir_done
 
  Call CheckUserInstallRights
  Pop $R0
 
  StrCmp $R0 "HKLM" 0 user_dir
    StrCpy $INSTDIR "$PROGRAMFILESPidgin"
    Goto instdir_done
  user_dir:
    Push $SMPROGRAMS
    ${GetParent} $SMPROGRAMS $R2
    ${GetParent} $R2 $R2
    StrCpy $INSTDIR "$R2Pidgin"
 
  instdir_done:
;LogSet on
  Pop $R3
  Pop $R2
  Pop $R1
  Pop $R0
FunctionEnd
 
Function un.onInit
  Call un.RunCheck
  StrCpy $name "Pidgin ${PIDGIN_VERSION}"
;LogSet on
 
  ; Get stored language preference
  !insertmacro MUI_UNGETLANGUAGE
 
FunctionEnd
 
; Page enter and exit functions..
 
Function preWelcomePage
  Push $R0
 
!ifndef WITH_GTK
  ; If this installer dosn't have GTK, check whether we need it.
  ; We do this here and not in .onInit because language change in
  ; .onInit doesn't take effect until it is finished.
  Call DoWeNeedGtk
  Pop $R0
  Pop $GTK_FOLDER
 
  IntCmp $R0 1 done done
  MessageBox MB_OK $(GTK_INSTALLER_NEEDED) /SD IDOK
  Quit
 
  done:
 
!else
  Push $R1
  Push $R2
 
  Call DoWeNeedGtk
  Pop $R0
  Pop $R2
  IntCmp $R0 1 gtk_selection_done gtk_not_mandatory
    ; Make the GTK+ Section RO if it is required.
    !insertmacro SetSectionFlag ${SecGtk} ${SF_RO}
    Goto gtk_selection_done
  gtk_not_mandatory:
    ; Don't select the GTK+ section if we already have this version or newer installed
    !insertmacro UnselectSection ${SecGtk}
  gtk_selection_done:
 
  ; If on Win95/98/ME warn them that the GTK+ version wont work
  ${Unless} ${IsNT}
    !insertmacro UnselectSection ${SecGtk}
    !insertmacro SetSectionFlag ${SecGtk} ${SF_RO}
    MessageBox MB_OK $(GTK_WINDOWS_INCOMPATIBLE) /SD IDOK
    IntCmp $R0 1 done done ; Upgrade isn't optional - abort if we don't have a suitable version
    Quit
  ${EndIf}
 
  done:
  Pop $R2
  Pop $R1
!endif
  Pop $R0
FunctionEnd
 
!ifdef WITH_GTK
Function preGtkDirPage
  Push $R0
  Push $R1
  Call DoWeNeedGtk
  Pop $R0
  Pop $R1
 
  IntCmp $R0 2 +2 +2 no_gtk
  StrCmp $R0 "3" no_gtk no_gtk
 
  ; Don't show dir selector.. Upgrades are done to existing path..
  Pop $R1
  Pop $R0
  Abort
 
  no_gtk:
    StrCmp $R1 "NONE" 0 no_gtk_cont
      ; Got no install rights..
      Pop $R1
      Pop $R0
      Abort
    no_gtk_cont:
      ; Suggest path..
      StrCmp $R1 "HKCU" 0 hklm1
        ${GetParent} $SMPROGRAMS $R0
        ${GetParent} $R0 $R0
        StrCpy $R0 "$R0GTK2.0"
        Goto got_path
      hklm1:
        StrCpy $R0 "${GTK_DEFAULT_INSTALL_PATH}"
 
   got_path:
     StrCpy $name "GTK+ ${GTK_INSTALL_VERSION}"
     StrCpy $GTK_FOLDER $R0
     Pop $R1
     Pop $R0
FunctionEnd
 
Function postGtkDirPage
  Push $R0
  StrCpy $name "Pidgin ${PIDGIN_VERSION}"
  Push $GTK_FOLDER
  Call VerifyDir
  Pop $R0
  StrCmp $R0 "0" 0 done
    MessageBox MB_OK $(GTK_BAD_INSTALL_PATH) /SD IDOK
    Pop $R0
    Abort
  done:
  Pop $R0
FunctionEnd
!endif
 
; SpellChecker Related Functions
;-------------------------------
 
; Convert the a Section index to the language code
; Push the section index onto the stack and pop off the language code after the call
; This will set the error code, if no match is found
Function GetLangCodeForSection
  ClearErrors
  Push $R0
  Exch
  Pop $R0 ;This is the section index
 
  IntCmp $R0 ${SecSpellCheckBreton} 0 +3 +3
  StrCpy $R0 "br"
  Goto done
  IntCmp $R0 ${SecSpellCheckCatalan} 0 +3 +3
  StrCpy $R0 "ca"
  Goto done
  IntCmp $R0 ${SecSpellCheckCzech} 0 +3 +3
  StrCpy $R0 "cs"
  Goto done
  IntCmp $R0 ${SecSpellCheckWelsh} 0 +3 +3
  StrCpy $R0 "cy"
  Goto done
  IntCmp $R0 ${SecSpellCheckDanish} 0 +3 +3
  StrCpy $R0 "da"
  Goto done
  IntCmp $R0 ${SecSpellCheckGerman} 0 +3 +3
  StrCpy $R0 "de"
  Goto done
  IntCmp $R0 ${SecSpellCheckGreek} 0 +3 +3
  StrCpy $R0 "el"
  Goto done
  IntCmp $R0 ${SecSpellCheckEnglish} 0 +3 +3
  StrCpy $R0 "en"
  Goto done
  IntCmp $R0 ${SecSpellCheckEsperanto} 0 +3 +3
  StrCpy $R0 "eo"
  Goto done
  IntCmp $R0 ${SecSpellCheckSpanish} 0 +3 +3
  StrCpy $R0 "es"
  Goto done
  IntCmp $R0 ${SecSpellCheckFaroese} 0 +3 +3
  StrCpy $R0 "fo"
  Goto done
  IntCmp $R0 ${SecSpellCheckFrench} 0 +3 +3
  StrCpy $R0 "fr"
  Goto done
  IntCmp $R0 ${SecSpellCheckItalian} 0 +3 +3
  StrCpy $R0 "it"
  Goto done
  IntCmp $R0 ${SecSpellCheckDutch} 0 +3 +3
  StrCpy $R0 "nl"
  Goto done
  IntCmp $R0 ${SecSpellCheckNorwegian} 0 +3 +3
  StrCpy $R0 "no"
  Goto done
  IntCmp $R0 ${SecSpellCheckPolish} 0 +3 +3
  StrCpy $R0 "pl"
  Goto done
  IntCmp $R0 ${SecSpellCheckPortuguese} 0 +3 +3
  StrCpy $R0 "pt"
  Goto done
  IntCmp $R0 ${SecSpellCheckRomanian} 0 +3 +3
  StrCpy $R0 "ro"
  Goto done
  IntCmp $R0 ${SecSpellCheckRussian} 0 +3 +3
  StrCpy $R0 "ru"
  Goto done
  IntCmp $R0 ${SecSpellCheckSlovak} 0 +3 +3
  StrCpy $R0 "sk"
  Goto done
  IntCmp $R0 ${SecSpellCheckSwedish} 0 +3 +3
  StrCpy $R0 "sv"
  Goto done
  IntCmp $R0 ${SecSpellCheckUkrainian} 0 +3 +3
  StrCpy $R0 "uk"
  Goto done
 
  SetErrors
 
  done:
  Exch $R0
FunctionEnd ;GetLangCodeForSection
 
; Select and Disable any Sections that have currently installed dictionaries
Function SelectAndDisableInstalledDictionaries
  Push $R0
  Push $R1
  Push $R2
 
  ; Start with the first language dictionary
  IntOp $R0 ${SecSpellCheck} + 1
 
  start:
  ; If it is the end of the section group, stop
  SectionGetFlags $R0 $R1
  IntOp $R2 $R1 & ${SF_SECGRPEND}
  IntCmp $R2 ${SF_SECGRPEND} done
 
  Push $R0
  Call GetLangCodeForSection
  Pop $R2
  IfErrors end_loop
  ReadRegStr $R2 HKLM "${ASPELL_REG_KEY}-$R2" "" ; Check that the dictionary is installed
  StrCmp $R2 "" end_loop ; If it isn't installed, skip to the next item
  IntOp $R1 $R1 | ${SF_RO} ; Mark Readonly
  IntOp $R1 $R1 | ${SF_SELECTED} ; Select
  SectionSetFlags $R0 $R1
 
  end_loop:
  IntOp $R0 $R0 + 1 ;Advance to the next section
  Goto start
 
  done:
  Pop $R2
  Pop $R1
  Pop $R0
FunctionEnd
 
Function InstallAspellAndDict
  Push $R0
  Exch
  Call GetLangCodeForSection
  Pop $R0 ;This is the language code
  Push $R1
 
  IfErrors done ; We weren't able to convert the section to lang code
 
  retry:
    Call InstallAspell
    Pop $R1
    StrCmp $R1 "" +3
    StrCmp $R1 "cancel" done
    MessageBox MB_RETRYCANCEL "$(PIDGIN_SPELLCHECK_ERROR) : $R1" /SD IDCANCEL IDRETRY retry IDCANCEL done
 
  retry_dict:
    Push $R0
    Call InstallAspellDictionary
    Pop $R1
    StrCmp $R1 "" +3
    StrCmp $R1 "cancel" done
    MessageBox MB_RETRYCANCEL "$(PIDGIN_SPELLCHECK_DICT_ERROR) : $R1" /SD IDCANCEL IDRETRY retry_dict
 
  done:
 
  Pop $R1
  Pop $R0
FunctionEnd
 
Function InstallAspell
  Push $R0
  Push $R1
  Push $R2
 
  check:
  ClearErrors
  ReadRegDWORD $R0 HKLM ${ASPELL_REG_KEY} "AspellVersion"
  IntCmp $R0 15 installed
 
  ; If this is the check after installation, don't infinite loop on failure
  StrCmp $R1 "$TEMPaspell_installer.exe" 0 +3
    StrCpy $R0 $(ASPELL_INSTALL_FAILED)
    Goto done
 
  ; We need to download and install aspell
  StrCpy $R1 "$TEMPaspell_installer.exe"
  StrCpy $R2 "${DOWNLOADER_URL}?version=${PIDGIN_VERSION}&dl_pkg=aspell_core"
  DetailPrint "Downloading Aspell... ($R2)"
  NSISdl::download /TIMEOUT=10000 $R2 $R1
  Pop $R0
  StrCmp $R0 "success" +2
    Goto done
  ExecWait '"$R1"'
  Delete $R1
  Goto check ; Check that it is now installed correctly
 
  installed: ;Aspell is currently installed, no error message
    DetailPrint "Aspell is installed"
    StrCpy $R0 ''
 
  done:
  Pop $R2
  Pop $R1
  Exch $R0
FunctionEnd
 
Function InstallAspellDictionary
  Push $R0
  Exch
  Pop $R0 ;This is the language code
  Push $R1
  Push $R2
  Push $R3
  Push $R4
 
  check:
  ClearErrors
  ReadRegStr $R2 HKLM "${ASPELL_REG_KEY}-$R0" ""
  StrCmp $R2 "" 0 installed
 
  ; If this is the check after installation, don't infinite loop on failure
  StrCmp $R1 "$TEMPaspell_dict-$R0.exe" 0 +3
    StrCpy $R0 $(ASPELL_INSTALL_FAILED)
    Goto done
 
  ; We need to download and install aspell
  StrCpy $R1 "$TEMPaspell_dict-$R0.exe"
  StrCpy $R3 "${DOWNLOADER_URL}?version=${PIDGIN_VERSION}&dl_pkg=lang_$R0"
  DetailPrint "Downloading the Aspell $R0 Dictionary... ($R3)"
  NSISdl::download /TIMEOUT=10000 $R3 $R1
  Pop $R3
  StrCmp $R3 "success" +3
    StrCpy $R0 $R3
    Goto done
  ; Use a specific temporary $OUTDIR for each dictionary because the installer doesn't clean up after itself
  StrCpy $R4 "$OUTDIR"
  SetOutPath "$TEMPaspell_dict-$R0"
  ExecWait '"$R1"'
  SetOutPath "$R4"
  RMDir /r "$TEMPaspell_dict-$R0"
  Delete $R1
  Goto check ; Check that it is now installed correctly
 
  installed: ;The dictionary is currently installed, no error message
    DetailPrint "Aspell $R0 Dictionary is installed"
    StrCpy $R0 ''
 
  done:
  Pop $R4
  Pop $R3
  Pop $R2
  Pop $R1
  Exch $R0
FunctionEnd
langmacros.nsh:
;;
;; Windows Pidgin NSIS installer language macros
;;
 
!macro PIDGIN_MACRO_DEFAULT_STRING LABEL VALUE
  !ifndef "${LABEL}"
    !define "${LABEL}" "${VALUE}"
    !ifdef INSERT_DEFAULT
      !warning "${LANG} lang file missing ${LABEL}, using default..."
    !endif
  !endif
!macroend
 
!macro PIDGIN_MACRO_LANGSTRING_INSERT LABEL LANG
  LangString "${LABEL}" "${LANG_${LANG}}" "${${LABEL}}"
  !undef "${LABEL}"
!macroend
 
!macro PIDGIN_MACRO_LANGUAGEFILE_BEGIN LANG
  !define CUR_LANG "${LANG}"
!macroend
 
!macro PIDGIN_MACRO_LANGUAGEFILE_END
  !define INSERT_DEFAULT
  !include "${PIDGIN_DEFAULT_LANGFILE}"
  !undef INSERT_DEFAULT
 
  ; Pidgin Language file Version 3
  ; String labels should match those from the default language file.
 
  ; Startup checks
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT INSTALLER_IS_RUNNING		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_IS_RUNNING			${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_INSTALLER_NEEDED		${CUR_LANG}
 
  ; License Page
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_LICENSE_BUTTON			${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_LICENSE_BOTTOM_TEXT		${CUR_LANG}
 
  ; Components Page
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SECTION_TITLE			${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_SECTION_TITLE			${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SHORTCUTS_SECTION_TITLE	${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_DESKTOP_SHORTCUT_SECTION_TITLE ${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_STARTMENU_SHORTCUT_SECTION_TITLE	${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SECTION_DESCRIPTION		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_SECTION_DESCRIPTION		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SHORTCUTS_SECTION_DESCRIPTION	${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_DESKTOP_SHORTCUT_DESC		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_STARTMENU_SHORTCUT_DESC	${CUR_LANG}
 
  ; GTK+ Directory Page
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_UPGRADE_PROMPT			${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_WINDOWS_INCOMPATIBLE		${CUR_LANG}
 
  ; Installer Finish Page
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_FINISH_VISIT_WEB_SITE		${CUR_LANG}
 
  ; Pidgin Section Prompts and Texts
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_PROMPT_CONTINUE_WITHOUT_UNINSTALL	${CUR_LANG}
 
  ; GTK+ Section Prompts
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_INSTALL_ERROR			${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT GTK_BAD_INSTALL_PATH		${CUR_LANG}
 
  ; URI Handler section
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT URI_HANDLERS_SECTION_TITLE		${CUR_LANG}
 
  ; Uninstall Section Prompts
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT un.PIDGIN_UNINSTALL_ERROR_1		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT un.PIDGIN_UNINSTALL_ERROR_2		${CUR_LANG}
 
  ; Spellcheck Section Prompts
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_SECTION_TITLE	${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_ERROR		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_DICT_ERROR		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_SECTION_DESCRIPTION	${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT ASPELL_INSTALL_FAILED		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_BRETON		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_CATALAN		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_CZECH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_WELSH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_DANISH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_GERMAN		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_ENGLISH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_GREEK		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_ESPERANTO		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_SPANISH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_FAROESE		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_FRENCH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_ITALIAN		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_DUTCH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_NORWEGIAN		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_POLISH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_PORTUGUESE		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_ROMANIAN		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_RUSSIAN		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_SLOVAK		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_SWEDISH		${CUR_LANG}
  !insertmacro PIDGIN_MACRO_LANGSTRING_INSERT PIDGIN_SPELLCHECK_UKRAINIAN		${CUR_LANG}
 
  !undef CUR_LANG
!macroend
 
!macro PIDGIN_MACRO_INCLUDE_LANGFILE LANG FILE
  !insertmacro PIDGIN_MACRO_LANGUAGEFILE_BEGIN "${LANG}"
  !include "${FILE}"
  !insertmacro PIDGIN_MACRO_LANGUAGEFILE_END
!macroend

sample translation:


;;  vim:syn=winbatch:fileencoding=cp1252:
;;
;;  french.nsh
;;
;;  French language strings for the Windows Pidgin NSIS installer.
;;  Windows Code page: 1252
;;
;;  Version 3
;;  Author: Eric Boumaour , 2003-2007.
;;
 
; Make sure to update the PIDGIN_MACRO_LANGUAGEFILE_END macro in
; langmacros.nsh when updating this file
 
; Startup Checks
!define INSTALLER_IS_RUNNING			"Le programme d'installation est dï¿½jï¿½ en cours d'exï¿½cution."
!define PIDGIN_IS_RUNNING			"Une instance de Pidgin est en cours d'exï¿½cution. Veuillez quitter Pidgin et rï¿½essayer."
!define GTK_INSTALLER_NEEDED			"Les bibliothï¿½ques de l'environnement GTK+ ne sont pas installï¿½es ou ont besoin d'une mise ï¿½ jour.$rVeuillez installer la version ${GTK_MIN_VERSION} ou plus rï¿½cente des bibliothï¿½ques GTK+."
 
; License Page
!define PIDGIN_LICENSE_BUTTON			"Suivant >"
!define PIDGIN_LICENSE_BOTTOM_TEXT		"$(^Name) est disponible sous licence GNU General Public License (GPL). Le texte de licence suivant est fourni uniquement ï¿½ titre informatif. $_CLICK"
 
; Components Page
!define PIDGIN_SECTION_TITLE			"Pidgin client de messagerie instantanï¿½e (obligatoire)"
!define GTK_SECTION_TITLE			"Bibliothï¿½ques GTK+ (obligatoire)"
!define PIDGIN_SHORTCUTS_SECTION_TITLE		"Raccourcis"
!define PIDGIN_DESKTOP_SHORTCUT_SECTION_TITLE	"Bureau"
!define PIDGIN_STARTMENU_SHORTCUT_SECTION_TITLE	"Menu Dï¿½marrer"
!define PIDGIN_SECTION_DESCRIPTION		"Fichiers et DLLs de base de Pidgin"
!define GTK_SECTION_DESCRIPTION			"Un ensemble d'outils pour interfaces graphiques multi-plateforme, utilisï¿½ par Pidgin"
 
!define PIDGIN_SHORTCUTS_SECTION_DESCRIPTION	"Raccourcis pour lancer Pidgin"
!define PIDGIN_DESKTOP_SHORTCUT_DESC		"Crï¿½er un raccourci pour Pidgin sur le bureau"
!define PIDGIN_STARTMENU_SHORTCUT_DESC		"Crï¿½er un raccourci pour Pidgin dans le menu Dï¿½marrer"
 
; GTK+ Directory Page
!define GTK_UPGRADE_PROMPT			"Une ancienne version des bibliothï¿½ques GTK+ a ï¿½tï¿½ trouvï¿½e. Voulez-vous la mettre ï¿½ jour ?$rNote : $(^Name) peut ne pas fonctionner si vous ne le faites pas."
!define GTK_WINDOWS_INCOMPATIBLE		"Windows 95/98/Me est incompatible avec GTK+ version 2.8.0 ou plus rï¿½centes.  GTK+ ${GTK_INSTALL_VERSION} ne sera pas installï¿½.$rSi vous n'avez pas installï¿½ GTK+ version ${GTK_MIN_VERSION} ou pkus rï¿½cente, l'installation s'arrï¿½tera."
 
; Installer Finish Page
!define PIDGIN_FINISH_VISIT_WEB_SITE		"Visitez la page web de Pidgin Windows"
 
; Pidgin Section Prompts and Texts
!define PIDGIN_PROMPT_CONTINUE_WITHOUT_UNINSTALL	"Impossible de dï¿½sinstaller la version de Pidgin en place. La nouvelle version sera installï¿½e sans supprimer la version en place."
 
; GTK+ Section Prompts
!define GTK_INSTALL_ERROR			"Erreur lors de l'installation des bibliothï¿½ques GTK+"
!define GTK_BAD_INSTALL_PATH			"Le dossier d'installation ne peut pas ï¿½tre crï¿½ï¿½ ou n'est pas accessible."
 
; URL Handler section
!define URI_HANDLERS_SECTION_TITLE		"Gestion des liens (URI)"
 
; Uninstall Section Prompts
!define un.PIDGIN_UNINSTALL_ERROR_1		"Le programme de dï¿½sinstallation n'a pas retrouvï¿½ les entrï¿½es de Pidgin dans la base de registres.$rL'application a peut-ï¿½tre ï¿½tï¿½ installï¿½e par un utilisateur diffï¿½rent."
!define un.PIDGIN_UNINSTALL_ERROR_2		"Vous n'avez pas les permissions pour supprimer cette application."
 
; Spellcheck Section Prompts
!define PIDGIN_SPELLCHECK_SECTION_TITLE		"Correction orthographique"
!define PIDGIN_SPELLCHECK_ERROR			"Erreur ï¿½ l'installation du correcteur orthographique"
!define PIDGIN_SPELLCHECK_DICT_ERROR		"Erreur ï¿½ l'installation du dictionnaire pour le correcteur orthographique"
!define PIDGIN_SPELLCHECK_SECTION_DESCRIPTION	"Correction orthogaphique. (Une connexion internet est nï¿½cessaire pour son installation)"
!define ASPELL_INSTALL_FAILED			"ï¿½chec de l'installation"
!define PIDGIN_SPELLCHECK_BRETON		"Breton"
!define PIDGIN_SPELLCHECK_CATALAN		"Catalan"
!define PIDGIN_SPELLCHECK_CZECH			"Tchï¿½que"
!define PIDGIN_SPELLCHECK_WELSH			"Gallois"
!define PIDGIN_SPELLCHECK_DANISH		"Danois"
!define PIDGIN_SPELLCHECK_GERMAN		"Allemand"
!define PIDGIN_SPELLCHECK_GREEK			"Grec"
!define PIDGIN_SPELLCHECK_ENGLISH		"Anglais"
!define PIDGIN_SPELLCHECK_ESPERANTO		"Espï¿½ranto"
!define PIDGIN_SPELLCHECK_SPANISH		"Espagnol"
!define PIDGIN_SPELLCHECK_FAROESE		"Fï¿½ringien"
!define PIDGIN_SPELLCHECK_FRENCH		"Franï¿½ais"
!define PIDGIN_SPELLCHECK_ITALIAN		"Italien"
!define PIDGIN_SPELLCHECK_DUTCH			"Hollandais"
!define PIDGIN_SPELLCHECK_NORWEGIAN		"Norvï¿½gien"
!define PIDGIN_SPELLCHECK_POLISH		"Polonais"
!define PIDGIN_SPELLCHECK_PORTUGUESE		"Portugais"
!define PIDGIN_SPELLCHECK_ROMANIAN		"Roumain"
!define PIDGIN_SPELLCHECK_RUSSIAN		"Russe"
!define PIDGIN_SPELLCHECK_SLOVAK		"Slovaque"
!define PIDGIN_SPELLCHECK_SWEDISH		"Suï¿½dois"
!define PIDGIN_SPELLCHECK_UKRAINIAN		"Ukrainien"
```


