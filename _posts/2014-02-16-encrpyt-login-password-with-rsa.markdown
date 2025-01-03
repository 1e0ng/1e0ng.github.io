---
layout: post
title: "Encrpyt Login Password With RSA"
date: 2014-02-16 13:30:09 +0800
comments: true
categories:
- Security
- Python
- Javascript
- Web

---

Today I'm thinking about questions of those website using http protocol.
When user logins in a http website, how to protect the password's security.
The conclusion is it is not easy to do so, because I haven't figured out a method to prevent the possibility of man-in-the-middle attack without a PKI infrastructure.
Maybe in the future, with the use of quantum cryptography, we can do that easily, but currently it's hard.


Nevertheless, we still can make the process of login more securier.
One approach is to hash password, and only transmit the digest instead of the plain password.
To use this method, don't forget to change salt frequently enough.
But now I want to use another approach, just for fun.

<!--more-->

To implement this, we need two parts. One for the back-end, and the other for the front-end.
I'm gonna to use a Python server as the back-end and a js script to implement the front-end.


## Python Server

Install the pure python rsa package:

```
pip install rsa
```

Then we can use it to generate a (public key, private key) tuple.


```python
import rsa
(pubkey, privkey) = rsa.newkeys(512)
n = '%x' % pubkey.n
e = '%x' % pubkey.e
```

Pass the `e` and `n` variable to front-end.

## Javascript

Download js rsa from <http://www-cs-students.stanford.edu/~tjw/jsbn/>

For now I just use the demo website <http://www-cs-students.stanford.edu/~tjw/jsbn/rsa.html>.

Copy the `n` variable to the `Modulus (hex)` input box and copy the `e` variable to the `Public exponent (hex, F4=0x10001)` input box.

Enter a message in `Plaintext (string)` and click `encrypt`.

Now we get the encrypted message in `Ciphertext (hex)`.

Pass the ciphertext to Pytho server.


## Python Sever Again

We get the ciphertext, but now we need translate it from hex to str first.

```python
import re
ciphertext = ''.join([chr(int(x, 16)) for x in re.findall(r'\w\w', ciphertext)])
```

Now get the plaintext.

```python
import rsa
plaintext = rsa.decrypt(ciphertext, privkey)
```

## Security Notes

This method does not prevent the man-in-the-middle attack, and also if a router between the server and client has been hacked and hackers can it to modify the js file used in the login page.


