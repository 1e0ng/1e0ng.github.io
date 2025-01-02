---
comments: true
date: 2011-03-28 07:25:58
layout: post
slug: get-the-title-of-a-website-in-c
title: Obtain The Title Of A Website
wordpress_id: 519
categories:
- Web
tags:
- C++
- HTML
- libcurl
- Parse
- regex
- Regular Expression
- Web
---

The idea is to retrieve the html file of the website and parse it to find the content between &lt;title&gt; and &lt;/title&gt;.

To get the html file, we need a library in C++, as the standard library has no such functions. I choose the `libcurl` library, and you can download it here: [http://curl.haxx.se/libcurl/](http://curl.haxx.se/libcurl/).

<!--more-->
To parse the html file, I use the regular expression library, which is based on GNU systems.

Here is my code:

``` c Get The Title Of A Website
#include <stdlib.h>
#include <stdio.h>
#include <curl/curl.h>
#include <regex.h>
#include <string.h>

//Created by Leon
//http://leons.im
//Mar, 21, 2011

FILE *fin;
FILE *ftmp;
FILE *fout;

size_t write_data (void *buffer, size_t size, size_t nmemb, void *userp) {
    return size * nmemb;
}

int main (void) {
    CURL *curl;
    CURLcode res;
    
    fin = fopen ("in.txt", "r");
    ftmp = fopen("tmp.txt", "w");
    fout = fopen("out.txt", "w");
    curl = curl_easy_init();
    
    if(curl) {
        printf("Got easy handle...n");
        curl_easy_setopt(curl, CURLOPT_URL, "http://leons.im");
        //curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, ftmp);
        //curl_easy_setopt(curl, CURLOPT_PROXY, "proxy.com:8080");
        //curl_easy_setopt(curl, CURLOPT_PROXYUSERPWD, "user:pwd");
        printf("Options is set.n");
        res = curl_easy_perform(curl);
        printf("Performed.n");
        fclose(ftmp);
        
        ftmp = fopen ("tmp.txt", "rb");
        if (NULL == ftmp) {
            fputs ("File error", stderr);
            exit (1);
        }
        // Obtain file size:
        fseek (ftmp, 0, SEEK_END);
        long lSize = ftell (ftmp);
        rewind (ftmp);
        
        // Allocate memory to contain the whole file:
        char *buffer;
        buffer = (char *) malloc (sizeof(char) * lSize);
        if (NULL == buffer) {
            fputs ("Memory error", stderr);
            exit (2);
        }
        
        // Copy the file into the buffer:
        size_t result;
        result = fread (buffer, 1, lSize, ftmp);
        if (result != lSize) {
            fputs ("Reading error", stderr);
            exit (3);
        }
        
        // Regular expression compilation
        regex_t compiled;
        int res = regcomp (&compiled, "<title>\([^<]*\)</title>", REG_ICASE);
        if (0 != res) {
            fputs ("Regular expression compilation error.", stderr);
            exit (4);
        }
        
        // Regular expression match
        regmatch_t matchptr[2];
        char err_msg[80];
        res = regexec (&compiled, buffer, 2, matchptr, 0);
        if (0 != res) {
            regerror(res, &compiled, err_msg, 80);
            printf("%sn", err_msg);
            exit (5);
        }
        char *title = (char *)malloc(sizeof(char) * (matchptr[1].rm_eo - matchptr[1].rm_so) + 1);
        strncpy (title, buffer + matchptr[1].rm_so, matchptr[1].rm_eo - matchptr[1].rm_so);
        printf("%sn", title);
        fprintf(fout, "%sn", title);
        
        regfree (&compiled);
        free (buffer);
        /* always cleanup */
        curl_easy_cleanup(curl);
    }
    fclose(fin);
    fclose(ftmp);
    fclose(fout);
    return 0;
}
```
