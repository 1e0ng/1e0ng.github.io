---
layout: post
title: "Integrate everything into Slack"
date: 2016-06-16 10:38:47 +0800
comments: true
categories:
- tool
- scrum
---


Slack is gradually becoming the standard for modern office communication. While you may argue that technically Slack is no different than, say, IRC – the polished experience is what makes it stand out in the crowd of messaging services. Using less gentler words, Slack is killing email for office communications. And has built in support for code snippets with syntax highlighting. Boom.

Actually, Slack is more than just a communication tool. What makes it extraordinary is it provides the possibility to integrate everything and make your workflow complete. In this post we're highlighting some of the most useful new workflows that Slack is enabling. All these are currently heavily in use in our team, and we find they are exceptionally helpful.

<!-- more -->


### Jira

The Jira integration posts messages once a task or bug changes its status, for instance, task created, task changed to Confirmed, In progress, Resolved, Verified etc.

To integrate Jira, you need to add JIRA to your slack with multiple configurations, one configuration for one channel. Configure the `Status Changes` to `* -> *`. Copy the `Webhook URL`. On Jira, click `Admin > System > WebHooks` and create multiple webhooks, one webhook for one channel. For each webhook, you can specify a JQL query to send only events triggered by matching issues. Paste the `Webhook URL` to `URL` field. Check all checkboxes under `Issue`.

You may configure another channel just for QA. For this configuration, constrain the `Status Changes` to `* -> Resolved`. That's because in our projects, we use a Bugzilla Workflow. Tasks moved to resolved are ready for QA to test. Of course it's better to create a channel on Slack just for QA.

### Hubot

The above Slack app just track down the task status changes. If someone comment on a task, Slack will not receive the notification. That's because the current Jira app for Slack doesn't support comments feature. I believe it still need some time before we can use this feature. To work around this, we need Hubot.

Follow this link to install Hubot jira comment <https://github.com/mnpk/hubot-jira-comment>.

Hubot can do much more than that. Don't forget, it's a robot.

### Bitbucket

The Bitbucket integration posts messages about all commits, pull requests, comments and issues. The messages include links to events on Bitbucket's.

### Jenkins CI

Once configured, Jenkins sends messages on failed and successful builds to your Slack channel. All your team can easily get notified and stay informed of any change in your build.

### Sentry

Tools like Sentry report on exceptions and log errors that are happening in your application. After adding the appropriate code and build changes, these tools are able to get access to your errors, arggregate them, and report high level stats.

Get notified when errors happen.

### Lunchbox

One of the most often asked question in my team is where are we going for lunch today. With Lunchbox, we can easily propose some places for lunch and vote.

### Giphy

It can turn each sentence to a gif.
