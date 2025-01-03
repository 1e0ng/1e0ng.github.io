---
comments: true
date: 2011-12-13 23:54:00
layout: post
slug: my-first-keygen
title: My First Keygen
wordpress_id: 880
categories:
- Security
---

Recently, I'm reading [pediy](http://www.pediy.com)'s book: `Encryption and Decryption`. This is a really good book with many practical technologies and skills, and it's also very interesting. In Chapter 2, I met a problem, so I cracked the demo crack-me program with ollydbg, but I'm not satisfied with that, so I studied the encrytion algorithm and wrote a keygen program.

The main algorithm is very simple, but it took me a lot of time to deal with the multi-byte characters problems, and I found there is another defination of unicode on Microsoft's platform! I can't figure out why Micro$oft didn't use UTF-8 to build his system just like Macintosh, because with UTF-8, we programmers don't have to deal with these troubles at all. Anyway, Windows is such a snorty that most people still have to use it.

<!-- more -->
Here is the main code:

``` cpp My First Keygen
void CCrackMeKeygenDlg::OnOK()
{
    USES_CONVERSION;
    UpdateData(TRUE);
    WCHAR *user_name;
    user_name = T2W((LPCTSTR)m_username);
    int m[8] = {0x0C, 0x0A, 0x13, 0x09,
                0x0C, 0x0B, 0x0A, 0x08};
    unsigned i = 3, j = 0;
    int ans = 0;
    if (wcslen(user_name) < 5) {
        MessageBox(_T("Username should be at least 5 characters."));
        return;
    }
    for (; i < wcslen(user_name); ++i, ++j) {
        if (j > 7) {
            j = 0;
        }
        ans += m[j] * ((BYTE)user_name[i]);
    }
    TCHAR res[1000];
    wsprintf(res, _T("%ld"), ans);
    m_serialnumber = res;
    m_author = _T("Created by Leon.\nhttp://leons.im");
    UpdateData(FALSE);
    //CDialog::OnOK();
}
```
