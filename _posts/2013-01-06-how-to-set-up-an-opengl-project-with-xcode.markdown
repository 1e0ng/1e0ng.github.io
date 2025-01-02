---
layout: post
title: "How to set up an OpenGL project with XCode"
date: 2013-01-06 21:22
comments: true
categories: articles
tags: 
- Mac OS
- Graphics
---

If you search this topic, you find few people are talking about this. Why? because it's too easy to set up an OpenGL project for Mac. But I still write this article, because maybe someone are finding something like a quick start. 

Unlike other platforms, in Mac, you don't need to install OpenGL independently. To use OpenGL in Mac, you need to install XCode first.

<!--more-->
## Download & Install XCode

Download XCode freely from apple's offical website: [http://developer.apple.com/xcode/](http://developer.apple.com/xcode/).This may cost you some time, because XCode is huge.

## Create a Project

Create a new OS X Application. Choose `Command Line Tool`.

![OpenGL with XCode step 1](/uploads/2013-01-06-step1.png)

Input a product name.

![OpenGL with XCode step 2](/uploads/2013-01-06-step2.png)

Then choose a location for you project and click `Next`.

<!-- more -->

## Add OpenGL Support

Select project Name -> Target Name -> Build Phases -> Link Binary With Libraries.

![OpenGL with XCode step 3](/uploads/2013-01-06-step3.png)

Click the plus button to add OpenGL and GLUT frameworks.

![OpenGL with XCode step 4](/uploads/2013-01-06-step4.png)

## Write Code

Now, write code in file `main.cpp`.

![OpenGL with XCode step 5](/uploads/2013-01-06-step5.png)

Here is an example file. Just copy and paste it into your `main.cpp` file and don't ask me about what each line of code means.

{% highlight cpp linenos %}
//
//  main.cpp
//  Three-Dimentional Gasket
//
//  Created by Leon on 1/6/13.
//  Copyright (c) 2013 Leon. All rights reserved.
//

#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <GLUT/glut.h>

const GLfloat EDGE = 50.0;
const GLfloat SQR3 = sqrt(3);
const GLfloat SQR6 = sqrt(6);

bool is_equal(GLfloat a[3], GLfloat b[3]) {
    for (int i = 0; i < 3; ++i) {
        if (abs(a[i] - b[i]) >= 5) {
            return false;
        }
    }
    return true;
}

bool is_equal(GLfloat vertices[4][3]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = i + 1; j < 4; ++j) {
            if (!is_equal(vertices[i], vertices[j])) {
                return false;
            }
        }
    }
    return true;
}

void triangle(GLfloat vertices[3][3], GLfloat color[3]) {
    glColor3fv(color);
    for (int i = 0; i < 3; ++i) {
        glVertex3fv(vertices[i]);
    }
}

bool cmp(GLfloat v1[3], GLfloat v2[3]) {
    for (int i = 2; i >= 0; --i) {
        if (v1[i] != v2[i]) {
            return v1[i] < v2[i];
        }
    }
    return false;
}

void swap(GLfloat v1[3], GLfloat v2[3]) {
    for (int i = 0; i < 3; ++i) {
        GLfloat tmp = v1[i];
        v1[i] = v2[i];
        v2[i] = tmp;
    }
}

void sort(GLfloat vertices[4][3]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = i + 1; j < 4; ++j) {
            if (!cmp(vertices[i], vertices[j])) {
                swap(vertices[i], vertices[j]);
            }
        }
    }
}

void tetra(GLfloat vertices[4][3], GLfloat colors[4][3]) {
    sort(vertices);
    for (int i = 0; i < 4; ++i) {
        GLfloat tri[3][3];
        for (int j = 0; j < 3; ++j) {
            for (int k = 0; k < 3; ++k) {
                tri[j][k] = vertices[(i+j)%4][k];
            }
        }
        triangle(tri, colors[i]);
    }
}

void divide_triangle(GLfloat vertices[4][3], GLfloat colors[4][3]) {
    if (is_equal(vertices)) {
        tetra(vertices, colors);
    }
    else {
        for (int i = 0; i < 4; ++i) {
            GLfloat child[4][3];
            for (int j = 0; j < 4; ++j) {
                for (int k = 0; k < 3; ++k) {
                    child[j][k] = (vertices[i][k] + vertices[(i+j)%4][k]) / 2;
                }
            }
            divide_triangle(child, colors);
        }
    }
}

void display()
{
    GLfloat vertices[4][3] = { {0.0, 0.0, 0.0}, {EDGE, 0.0, 0.0}, {EDGE/2, EDGE*SQR3/2, 0.0}, {EDGE/2, EDGE*SQR3/6, EDGE*SQR6/3} };
    GLfloat colors[4][3] = { {1.0, 1.0, 0.5}, {0.5, 1.0, 0.5}, {0.5, 0.8, 0.5}, {0.5, 0.5, 1.0} };
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    glBegin(GL_TRIANGLES);
    divide_triangle(vertices, colors);
    glEnd();
    glFlush();
    
}

void myinit() {
    glEnable(GL_DEPTH_TEST);
    glClearColor(1.0, 1.0, 1.0, 1.0);
    glColor3f(0.0, 1.0, 0.0);
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, EDGE, 0, EDGE*SQR3/2, -EDGE, 0);
    
    glMatrixMode(GL_MODELVIEW);
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH);
    
    glutInitWindowSize(500, 500*SQR3/2);
    glutInitWindowPosition(0, 0);
    glutCreateWindow("GLUT Program");
    
    glutDisplayFunc(display);
    
    myinit();
    glutMainLoop();
    return 0;
}
{% endhighlight %}

The above example is a three-dimentional Gasket. It's an example from the book `Interactive Computer Graphics: A Top-Down Approach (Fourth Edition)`. I rewrite it to make it cooler.

## Run

OK, `Command + R` to run your application.

![OpenGL with XCode step 6](/uploads/2013-01-06-step6.png)

## Next

To learn more about OpenGL programming for Mac, take this: [https://developer.apple.com/library/mac/#documentation/graphicsimaging/conceptual/OpenGL-MacProgGuide/opengl_drawing/opengl_drawing.html](https://developer.apple.com/library/mac/#documentation/graphicsimaging/conceptual/OpenGL-MacProgGuide/opengl_drawing/opengl_drawing.html).
