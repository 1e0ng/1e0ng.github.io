---
layout: post
title: "Atlassian License Analytics"
date: 2016-01-01 00:17:38 +0800
comments: true
categories:
- Python
- Security
---

Bitbucket Server, Jira, Confluence, Crowd etc, so many excellent software come from a same company --- Atlassian. Some of them are technically designed well (even though not best), so they are good study cases. These days I'm interested in the license generating algorithm, so I dig into them for studying. Its license algorithm is DSA. Theoritically, it's impossible to know the private key, so the private key can be think as unknown and safe. Without private key, it's impossible to generate the corresponding signature for raw text. In this way, it makes sure that every issued license is from the owner.

To better understand the relationship between orignal text and the license text, I write a Python code to uncover the original text from a license text.
<!--more-->

{% highlight python linenos %}
import zlib
import base64

def get_original_text(license):
    license = ''.join(license.split())
    i = license.rfind('X')
    l = int(license[i + 3:], 31)
    license = license[:l]
    s = base64.b64decode(license)
    l = ord(s[:4].decode('UTF-32BE'))
    text, signature = s[4:4 + l], s[4 + l:]
    ans = zlib.decompress(text[5:])
    return ans.decode('utf-8')

license = '''
AAABJA.......
'''
print(get_original_text(license))
{% endhighlight %}
