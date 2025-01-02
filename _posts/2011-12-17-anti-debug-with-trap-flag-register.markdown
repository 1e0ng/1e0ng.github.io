---
comments: true
date: 2011-12-17 23:41:00
layout: post
slug: anti-debug-with-trap-flag-register
title: Anti-Debug with Trap Flag Register
wordpress_id: 902
categories:
- Security
tags:
- Anti-Debug
- TF
---

Let’s play an interesting [Crack-me](http://en.wikipedia.org/wiki/Crackme) — [muckis’s crackme #2](/uploads/2011-12-crackme2.zip).

When you run the crack-me with a debugger, say OllyDbg, the program pops up a message box saying “What the hell are you doing in my app with a debugger?” and then exists, but when you run the crack-me without a debugger, just double-click on it, it runs normally.

<!-- more -->
How does the crack-me do this? Let’s look the disassembling code:

```
Address   Hex dump                     Command                                Comments
00401000  /.  E8 24000000              CALL 00401029
00401005  |.  8B4C24 0C                MOV ECX,DWORD PTR SS:[ARG.3]
00401009  |.  C701 17000100            MOV DWORD PTR DS:[ECX],10017
0040100F  |.  C781 B8000000 00000000   MOV DWORD PTR DS:[ECX+0B8],0
00401019  |.  31C0                     XOR EAX,EAX
0040101B  |.  8941 14                  MOV DWORD PTR DS:[ECX+14],EAX
0040101E  |.  8941 18                  MOV DWORD PTR DS:[ECX+18],EAX
00401021  |.  806A 00 E8               SUB BYTE PTR DS:[EDX],0E8
00401025  |.  33C0                     XOR EAX,EAX
00401027  |.  33DB                     XOR EBX,EBX
00401029  |$  68 60104000              PUSH 00401060
0040102E  |.  64:FF35 00000000         PUSH DWORD PTR FS:[0]
00401035  |.  64:8925 00000000         MOV DWORD PTR FS:[0],ESP               ; Installs SE handler 401060
0040103C  |.  9C                       PUSHFD
0040103D  |.  813424 54010000          XOR DWORD PTR SS:[ESP],00000154
00401044  |.  9D                       POPFD
00401045  |.  6A 30                    PUSH 30                                ; /Type = MB_OK|MB_ICONEXCLAMATION|MB_DEFBUTTON1|MB_APPLMODAL
00401047  |.  68 00604000              PUSH OFFSET 00406000                   ; |Caption = "crackme2"
0040104C  |.  68 7A604000              PUSH OFFSET 0040607A                   ; |Text = "What the hell are you doing in my app with a debugger?"
00401051  |.  6A 00                    PUSH 0                                 ; |hOwner = NULL
00401053  |.  E8 9C030000              CALL          ; \USER32.MessageBoxA
00401058  |.  6A 00                    PUSH 0                                 ; /ExitCode = 0
0040105A  |.  E8 A7030000              CALL        ; \KERNEL32.ExitProcess
0040105F  \.  C3                       RETN
00401060  /$  64:8F05 00000000         POP DWORD PTR FS:[0]                   ; SE handling routine
00401067  |.  83C4 04                  ADD ESP,4
0040106A  |.  6A 00                    PUSH 0                                 ; /ModuleName = NULL
0040106C  |.  E8 A1030000              CALL   ; \KERNEL32.GetModuleHandleA
00401071  |.  A3 35604000              MOV DWORD PTR DS:[406035],EAX
```

Note this line:

```
00401035  |.  64:8925 00000000         MOV DWORD PTR FS:[0],ESP               ; Installs SE handler 401060
```

It installs a structured exception handler. The definition of structured exception can be found here: [http://msdn.microsoft.com/en-us/library/windows/desktop/ms680657(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms680657\(v=vs.85\).aspx).

{% quote %}
An exception is an event that occurs during the execution of a program, and requires the execution of code outside the normal flow of control. There are two kinds of exceptions: hardware exceptions and software exceptions. Hardware exceptions are initiated by the CPU. They can result from the execution of certain instruction sequences, such as division by zero or an attempt to access an invalid memory address. Software exceptions are initiated explicitly by applications or the operating system. For example, the system can detect when an invalid parameter value is specified. Structured exception handling is a mechanism for handling both hardware and software exceptions. Therefore, your code will handle hardware and software exceptions identically. Structured exception handling enables you to have complete control over the handling of exceptions, provides support for debuggers, and is usable across all programming languages and machines. Vectored exception handling is an extension to structured exception handling. The system also supports termination handling, which enables you to ensure that whenever a guarded body of code is executed, a specified block of termination code is also executed. The termination code is executed regardless of how the flow of control leaves the guarded body. For example, a termination handler can guarantee that clean-up tasks are performed even if an exception or some other error occurs while the guarded body of code is being executed.
{% endquote %}

Then,

```
0040103C  |.  9C                       PUSHFD
0040103D  |.  813424 54010000          XOR DWORD PTR SS:[ESP],00000154
00401044  |.  9D                       POPFD
```

The TF (Trap Flag) is set to 1, according to the [Intel x86 FLAGS registers form](http://en.wikipedia.org/wiki/FLAGS_register_\(computing\)):

```
Intel x86 FLAGS register
Bit #	Abbreviation	Description	Category[1]
FLAGS
0	CF	Carry flag	S
1	1	Reserved	 
2	PF	Parity flag	S
3	0	Reserved	 
4	AF	Adjust flag	S
5	0	Reserved	 
6	ZF	Zero flag	S
7	SF	Sign flag	S
8	TF	Trap flag (single step)	X
9	IF	Interrupt enable flag	C
10	DF	Direction flag	C
11	OF	Overflow flag	S
12, 13	1,1 / IOPL	I/O privilege level (286+ only) always 1 on 8086 and 186	X
14	1 / NT	Nested task flag (286+ only) always 1 on 8086 and 186	X
15	1 on 8086 and 186, should be 0 above	Reserved	 
EFLAGS
16	RF	Resume flag (386+ only)	X
17	VM	Virtual 8086 mode flag (386+ only)	X
18	AC	Alignment check (486SX+ only)	X
19	VIF	Virtual interrupt flag (Pentium+)	X
20	VIP	Virtual interrupt pending (Pentium+)	X
21	ID	Able to use CPUID instruction (Pentium+)	X
22	0	Reserved	 
23	0	Reserved	 
24	0	Reserved	 
25	0	Reserved	 
26	0	Reserved	 
27	0	Reserved	 
28	0	Reserved	 
29	0	Reserved	 
30	0	Reserved	 
31	0	Reserved	 
RFLAGS
32-63	0	Reserved	 
```

That means when the program is running in normal mode, it runs one step (0×00401045) and then due to the Trap Flag it handles the exception by the Structured Exception Handler and runs into address 0×00401060, which is the right entrance of the program. But if the program is running in debug mode, it runs one step (0×00401045) and it continues to execute the following instructions, because in debug mode, the Trap Flag is ignored. So the program enters the wrong way and exists.

Even though this method to anti-debug is very weak, it’s practical, simple and classical. Besides it can be used with other methods together to make the debugging of your program more difficult.
