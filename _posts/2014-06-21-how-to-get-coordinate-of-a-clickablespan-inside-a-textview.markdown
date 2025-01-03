---
layout: post
title: "How to get coordinate of a ClickableSpan inside a TextView"
date: 2014-06-21 16:14:06 +0800
comments: true
categories:
- Android
- Java

---

I have a `TextView` with many `ClickableSpan`.

On click on a `ClickableSpan`, I have to get the coordinate on screen of it (to show a custom `View` at his position).

The problem is that the onClick() method of the ClickableSpan gives me in parameter a View, the TextView which contains the ClickableSpan.

Thanks to Google, I find this solution. This helps me to win a Leopard Buffet. :D

<!--more-->

{% highlight java linenos %}
@Override
public void onClick(View widget) {

    TextView parentTextView = (TextView) widget;

    Rect parentTextViewRect = new Rect();

    // Initialize values for the computing of clickedText position
    SpannableString completeText = (SpannableString)(parentTextView).getText();
    Layout textViewLayout = parentTextView.getLayout();

    double startOffsetOfClickedText = completeText.getSpanStart(this);
    double endOffsetOfClickedText = completeText.getSpanEnd(this);
    double startXCoordinatesOfClickedText = textViewLayout.getPrimaryHorizontal((int)startOffsetOfClickedText);
    double endXCoordinatesOfClickedText = textViewLayout.getPrimaryHorizontal((int)endOffsetOfClickedText);


    // Get the rectangle of the clicked text
    int currentLineStartOffset = textViewLayout.getLineForOffset((int)startOffsetOfClickedText);
    int currentLineEndOffset = textViewLayout.getLineForOffset((int)endOffsetOfClickedText);
    boolean keywordIsInMultiLine = currentLineStartOffset != currentLineEndOffset;
    textViewLayout.getLineBounds(currentLineStartOffset, parentTextViewRect);


    // Update the rectangle position to his real position on screen
    int[] parentTextViewLocation = {0,0};
    parentTextView.getLocationOnScreen(parentTextViewLocation);

    double parentTextViewTopAndBottomOffset = (
        parentTextViewLocation[1] -
        parentTextView.getScrollY() +
        parentTextView.getCompoundPaddingTop()
    );
    parentTextViewRect.top += parentTextViewTopAndBottomOffset;
    parentTextViewRect.bottom += parentTextViewTopAndBottomOffset;

    parentTextViewRect.left += (
        parentTextViewLocation[0] +
        startXCoordinatesOfClickedText +
        parentTextView.getCompoundPaddingLeft() -
        parentTextView.getScrollX()
    );
    parentTextViewRect.right = (int) (
        parentTextViewRect.left +
        endXCoordinatesOfClickedText -
        startXCoordinatesOfClickedText
    );

    int x = (parentTextViewRect.left + parentTextViewRect.right) / 2;
    int y = parentTextViewRect.bottom;
    if (keywordIsInMultiLine) {
        x = parentTextViewRect.left;
    }

    Log.d("location2:" + x + "," + y);
}

{% endhighlight %}
