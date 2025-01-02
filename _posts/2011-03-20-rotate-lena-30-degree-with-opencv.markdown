---
comments: true
date: 2011-03-20 00:52:53
layout: post
slug: rotate-lena-30-degree-with-opencv
title: How To Rotate An Image
wordpress_id: 500
categories: articles
tags:
- Graphics
tags:
- Lena
- OpenCV
- Rotate
---

With OpenCV, it's easy to rotate an image by code.

<!-- more -->

This is Lena:

[![](/uploads/2011-03-lena.png)](/uploads/2011-03-lena.png)


Now, I want to rotate this picture 30 degree like this:
[![](/uploads/2011-03-Screenshot.png)](/uploads/2011-03-Screenshot.png)


Here is the code:


``` cpp Rotate Lena 30 Degrees 
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <cv.h>
#include <highgui.h>

//Created by Leon
//http://leons.im
//20, Mar, 2011

#define PI acos(-1)
int main() {
  IplImage* img = 0; 
  int height,width,step,channels;
  uchar *data, *result;
  int i,j,k,t,x,y;
  double angle = PI / 6;
  double cosa, sina;
  cosa = cos(angle);
  sina = sin(angle);

  // load an image  
  img=cvLoadImage("lena.bmp");
  if(!img){
    printf("Could not load image filen");
    exit(0);
  }

  // get the image data
  height    = img->height;
  width     = img->width;
  step      = img->widthStep;
  channels  = img->nChannels;
  data      = (uchar *)img->imageData;
  result	= (uchar *)malloc(height * step);
  printf("Processing a %dx%d image with %d channelsn",height,width,channels); 


  // create a window
  cvNamedWindow("mainWin", CV_WINDOW_AUTOSIZE); 
  cvMoveWindow("mainWin", 100, 100);

  // invert the image
	for(i=0;i<height;i++) {
		for(j=0;j<width;j++) {
			x = (j - width / 2) * cosa - (i - height / 2) * sina + width / 2;
			y = (j - width / 2) * sina + (i - height / 2) * cosa + height / 2;
			for(k=0;k<channels;k++) {
				t = y * step + x * channels + k;
				if (t >= 0 && t < height * step){
					result[i * step + j * channels + k] = data[t];
				}
			}
		}
	}

	for (i = 0; i < height * step; ++i) {
		data[i] = result[i];
	}
  // show the image
  cvShowImage("mainWin", img );

  // wait for a key
  cvWaitKey(0);

  // release the image
  cvReleaseImage(&img );
  return 0;
}
```
    

Here is my Makefile on Linux:

    
{% highlight make linenos %}
CC = g++
CFLAGS = `pkg-config --cflags opencv` `pkg-config --libs opencv`

hello : hello-world.cpp
	PKG_CONFIG_PATH=/usr/local/lib/pkgconfig && 
	export PKG_CONFIG_PATH && 
	$(CC) $(CFLAGS) hello-world.cpp -o hello
{% endhighlight %}


You may change the angle to rotate to any degree you like.
As you can see, the picture rotated is aliasing, so if anyone knows how to anti-aliasing, please tell me.
