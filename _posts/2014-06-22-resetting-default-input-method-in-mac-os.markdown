---
layout: post
title: "Resetting default input method in Mac OS"
date: 2014-06-22 20:42:17 +0800
comments: true
categories: articles
tags:
- Mac OS

---

I became a Dvorak guy. Before that, I had initialized my Mac to a U.S. keyboard layout. After I changed my Mac to Dvorak keyboard layout, everything worked like a charm except the login window was still the U.S. layout. This frustrates me a lot. So today I spend a little time to reslove this issue.

<!--more-->

The easiest way is to re-initialize the system by this command:

{% highlight bash linenos %}
sudo "/System/Library/CoreServices/Setup Assistant.app/Contents/MacOS/Setup Assistant"
{% endhighlight %}

But in this way, I have to creat a new user, which means I have to do some migration work. I think there must be a elegent way to resolve this. After Googleing a while, I find the solution.

{% highlight bash linenos %}
sudo cp /Library/Preferences/com.apple.HIToolbox.plist /tmp/
sudo chmod 777 /tmp/com.apple.HIToolbox.plist
plutil -convert xml1 /tmp/com.apple.HIToolbox.plist
{% endhighlight %}

Now open `/tmp/com.apple.HIToolbox.plist` in a text editor (e.g. vim or Emacs).

Throughout the file you will find several mentions of a `KeyboardLayout ID` key followed by an integer and `KeyboardLayout Name` followed by a string. Change these strings to the name of your custom keyboard layout and the id integers to the ID of your layout (the easiest way to find the right values is to compare with your user settings found in the file `~/Library/Preferences/com.apple.HIToolbox.plist`

{% highlight bash linenos %}
sudo cp ~/Library/Preferences/com.apple.HIToolbox.plist /tmp/my.plist
plutil -convert xml1 /tmp/my.plist
cat /tmp/my.plist
{% endhighlight %}

Also the value of the key `AppleCurrentKeyboardLayoutInputSourceID` must be changed accordingly (for this circumstance it's `com.apple.keylayout.Dvorak`). Again you can find this value in your local preference file.

Once these changes are done, save the file and go back to the terminal. To play it safe, you can create a copy of the original `com.apple.HIToolbox.plist` file, just in case you made an error and need to roll back. Then do the following:

```
sudo cp /tmp/com.apple.HIToolbox.plist /Library/Preferences/
sudo chmod 644 /Library/Preferences/com.apple.HIToolbox.plist
```


Exit the terminal, and restart the computer (logout is not sufficient: the file will not be reread). After restart, you should have your keyboard layout in the login screen. You may need to restart twice.

