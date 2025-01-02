---
comments: true
date: 2011-03-06 18:37:44
layout: post
slug: my-emacs-configure-file
title: My Emacs Configure File
wordpress_id: 438
categories:
- Linux
tags:
- Configure
- Emacs
- Linux
---

Open the file named ".emacs" in your home folder. (if it doesn't exist, create one.)  Copy the following code and paste it into the opening file. Save the file and restart Emacs.

<!-- more -->

``` plain My Emacs Configure File
(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
)
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )
(setq default-tab-width 4)
(setq c-basic-offset 4)
(setq frame-title-format "%b@Leon's Emacs")
(setq default-major-mode 'text-mode)
(show-paren-mode t)
(setq show-paren-style 'parentheses)
(setq inhibit-startup-message t)
(require 'color-theme)
(eval-after-load "color-theme"
  '(progn
     (color-theme-initialize)))
(color-theme-dark-laptop)

(require 'cc-mode)
(c-set-offset 'inline-open 0)
(c-set-offset 'friend '-)
(c-set-offset 'substatement-open 0)

(defun my-c-mode-common-hook()
  (setq tab-width 4 indent-tabs-mode nil)
  ;;; hungry-delete and auto-newline
  ;;;  (c-toggle-auto-hungry-state 1)
  ;;Shortcut key defination
  (define-key c-mode-base-map [(control `)] 'hs-toggle-hiding)
  (define-key c-mode-base-map [(return)] 'newline-and-indent)
  (define-key c-mode-base-map [(f7)] 'compile)
  (define-key c-mode-base-map [(meta `)] 'c-indent-command)
;;  (define-key c-mode-base-map [(tab)] 'hippie-expand)
  (define-key c-mode-base-map [(tab)] 'my-indent-or-complete)
  (define-key c-mode-base-map [(meta ?/)] 'semantic-ia-complete-symbol-menu)

  ;;Pre-compilation
  (setq c-macro-shrink-window-flag t)
  (setq c-macro-preprocessor "cpp")
  (setq c-macro-cppflags " ")
  (setq c-macro-prompt-flag t)
  (setq hs-minor-mode t)
  (setq abbrev-mode t)
)
(add-hook 'c-mode-common-hook 'my-c-mode-common-hook)

;;;;C++ strategy
(defun my-c++-mode-hook()
  (setq tab-width 4 indent-tabs-mode nil)
  (c-set-style "java")
;;  (define-key c++-mode-map [f3] 'replace-regexp)
)

(load-file "/usr/share/emacs/23.2/lisp/cedet/cedet.el")

(setq semanticdb-project-roots
      (list
        (expand-file-name "/")))

(defun my-indent-or-complete ()
   (interactive)
   (if (looking-at "\>")
      (hippie-expand nil)
      (indent-for-tab-command))
 )

(global-set-key [(control tab)] 'my-indent-or-complete)

(autoload 'senator-try-expand-semantic "senator")

(setq hippie-expand-try-functions-list
      '(
        senator-try-expand-semantic
        try-expand-dabbrev
        try-expand-dabbrev-visible
        try-expand-dabbrev-all-buffers
        try-expand-dabbrev-from-kill
        try-expand-list
        try-expand-list-all-buffers
        try-expand-line
        try-expand-line-all-buffers
        try-complete-file-name-partially
        try-complete-file-name
        try-expand-whole-kill
        )
)
```
