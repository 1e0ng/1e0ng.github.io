---
layout: post
title: "Upload File With HTML5"
date: 2013-10-28 21:03
comments: true
categories: articles
tags:
- Web
- Python


---


Since HTML5 is currently widely supported, and it's a standard, it's time to use it. Users who don't have a modern browser should have one now. And browsers are free, why not use a faster and more standard one?

Uploading files was not supported by HTML for a long time. For example, you can not post a new file to server via Ajax. Actually you can do this, but in a hack way or with Flash. There is not even an elegent way to do this. But this will not happen any more. Things move forward. We have HTML5 now.

With HTML5, we can implement an uploading file server easily. Let me show you.

<!--more-->

First, add this code to your html file.


{% highlight html linenos %}
<form id="upload">
    <fieldset>
        <div>
            <div id="filedrag">To append a new image, drop file here!</div>
        </div>
    </fieldset>
</form>
<div class="upload_progress progress progress-striped active" style="display:none">
    <div class="upload_progress_bar progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
        <span class="sr-only">0% Complete</span>
    </div>
</div>
<script type="text/javascript" src="/static/js/filedrag.js"></script>
{% endhighlight %}

Second, add the js file `filedrag.js` you includes in the html file.

{% highlight js linenos %}
/*
filedrag.js - HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
Modified by Leon(i@leons.im)
*/
(function() {

    // getElementById
    function $id(id) {
        return document.getElementById(id);
    }

    // file drag hover
    function FileDragHover(e) {
        e.stopPropagation();
        e.preventDefault();
        e.target.className = (e.type == "dragover" ? "hover" : "");
    }

    // update the progress bar
     function uploadProgress(evt) {
        if (evt.lengthComputable) {
            var uploaded = Math.round(evt.loaded * 100 / evt.total);
            $(".upload_progress").show();
            $(".upload_progress_bar").attr("style","width:" + uploaded + "%;");
            $(".upload_progress_bar").attr("aria-valuenow", uploaded);
            $(".upload_progress_bar>.sr-only").text(uploaded + '% Completed.');

            //document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
        }
        else {
            //document.getElementById('progressNumber').innerHTML = 'unable to compute';
        }
    }

    // file selection
    function FileSelectHandler(e) {

        // cancel event and hover styling
        FileDragHover(e);

        // fetch FileList object
        var files = e.target.files || e.dataTransfer.files;

        // init the ajax request
        var xhr = new XMLHttpRequest();
        var url = window.location.href.toString();
        var filepath = '/upload';

        xhr.open('post', filepath, true);
        xhr.upload.addEventListener("load", uploadProgress, false);
        xhr.upload.addEventListener("progress", uploadProgress, false);
        xhr.onload = function(e) {

            if (this.status == 200) {
                var url = this.response;
                $('<img src="' + url + '" class="img-responsive new-img">').insertBefore('#filedrag');
                //alert(this.response);
                $('.upload_progress').hide();
            }
            else {
                alert('Failed.');
            }
        }

        var formData = new FormData();

        // process all File objects
        for (var i = 0, f; f = files[i]; i++) {
            formData.append('file', f);
        }
        xhr.send(formData);
    }

    // initialize
    function Init() {

        var filedrag = $id("filedrag");

        // is XHR2 available?
        var xhr = new XMLHttpRequest();
        if (xhr.upload) {

            // file drop
            filedrag.addEventListener("dragover", FileDragHover, false);
            filedrag.addEventListener("dragleave", FileDragHover, false);
            filedrag.addEventListener("drop", FileSelectHandler, false);
            filedrag.style.display = "block";
        }
    }

    // call initialization file
    if (window.File && window.FileList && window.FileReader) {
        Init();
    }
})();

{% endhighlight %}

At last, implement the server side. For instance, this is a Python code in Tornado Framework.

{% highlight python linenos %}
import logging
from tornado.web import RequestHandler

class MainHandler(RequestHandler):
    def post(self):
        if 'file' in self.request.files:
            f = self.request.files['file'][0]
            f_data = f['body']
            f_type = f['filename'].split('.')[-1]
            f_url = self.img_root + data_file.save(self.root, f_data, f_type)

            logging.info('f_url = %s' % f_url)
            self.write(f_url);
{% endhighlight %}

Here, you need to implement `data_file.save()` method by yourself.

Done.
