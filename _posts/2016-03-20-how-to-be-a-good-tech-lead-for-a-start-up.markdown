---
layout: post
title: "How to be a good tech lead for a start up"
date: 2016-03-20 16:18:44 +0800
comments: true
categories:
- management
---

To be a good tech lead in a start up is totally different from being CTO at a mature big company. There are numerous theories and technologies about managment in big companies. Unfortunately, there are not so much knowledges about how to lead a technical start up. Today, I'm gonna to give my advices. Hope they will inspire you.

I'm gonna talk this in 9 respects. They are not all ordered by importances, even though some are.

<!-- more -->
### Big Picture

The most important thing is being aware of the big picture, ie the goal of this company, the current process, how many steps it's gona be. Always focus to the most important things. Resources are limited, you're gonna make a big differences and all these depends on how to use the limited resources to reslove the most critical problems in a limited time.

### Staff Composition & Recruitment

For an internet technology start up, you need to know how many software engineers, how many designers and how many products managers to hire for the first stage and the right sequences. Recruitment is hard for start ups. Work is heavier while salary is the same. Options can provide but if company dies you got nothing. Everyone knows that. For a start up, trust is essential for the first several members. So the initial guys are best to be friends for several years and know each other well enough and even though there are some diagreements you can work them out.

It's best if you can contact some old friends and pull them in. Friends of friends are good as well. Just remeber don't bring in office politics. Keep the work enviroment pure and simple.

For the technical recruitment, you need to draw a craft about the standard of hiring. For example, in my company, I set up 3 steps for the interviews. One need to pass all 3 steps to join in. First is a problem solving interview. There are 4 problems, and candidates can choose any one to solve in any language. This is for basic code knowledges and algorithm skills. In second, screen resume and HR related questions. In third, I'm gonna to ask questions face to face about work experiences and other stuff for capability assessment.

### IT Work & Office Equipment Selection

There is no IT department for a start up, at least when it starts. So you need to set up the office network, choose routers, switches, AP etc. You have to consider a lot of aspects. For example, I expect there will be about 20 staff for the first year, so I choose to use 2 Netgear WNDR4300, one for the main router and the other for wireless AP instead of using Cisco which is more expensive. After flushing the openwrt system to the routers, their performences are way good as now.

What people use what kind of computers? That's not so important? Actually it's not so unimpartant as it seems. People with good equipment can enormously increase productivity. In my company, I choose 27-inch iMac with Retina 5K display for designers, 2.6GHz Mac mini and two seperate displays for engineers. The 2.6GHz without SSD? Well I change the hard disk to SSD by myself for saving money and cool! Of course I have to buy 2 screwdriver (T6 and T9) and the warranty breaks, but it's really cool. Right on.

### Technology Selection & System Infrastructure

It's always good to use a dynamic language like Python or Ruby as the main server language for a start up. Advantages are obvious, just think about how much time you save, and time, is one of those critical parameters control whether a start up grows up or not. Well, it's hard to recruitment? Nevermind, qualified engineers can learn. From my experience, it worth to do that kind of thing. That's why you need a standard for recruitment because the HR only know to hire a PHP guy, an Android guy or a Java guy, or maybe 2-year experiences, 5-year experiences. They will never know this job should not do in this way. Seperating engineers by languages is stupid. That's why I propose several algorithm quiz, and tell them whether she is graduated or not, whether she knows Node or Javascript, only need to work out one of the 4 algothim problems will we procee to the onsite interview.

I use some kinds of languages since primary school, from QBasic, C, VBasic, Pascal, ASM, C++ and then Java, PHP, Obj C, Python, Node. For most engineers I believe I learned more languages, but wait there are hundreds of languages, there! I'm not gonna show up. It's just that I have a reason to choos Python for the current start up by comparing all these languages I know about.

For a start up, it's common to ask questions like do we need to develop native app? do wee need to use cloud server? It's easier to answer the second question. For most cases, if you are not dealing with sensitive data you should use cloud server because it saves time. Which cloud server should I have? The best. For now, it's Amazon's AWS. It's a little bit trick to answer the first question. Well there are cross platform solutions for developing Android and iOS app at the same time, but if the budget is not so tight and time is allowed, I would advise to do develop the native app.

### Workflow & Task Assignment

SCRUM is awesome, especially for a start up. Many big companies are striving to turing into SCRUM. However, for a start up, it's a new company, why not use SCRUM at the first time? I would not figure out a reason for not using SCRUM.

To build a SCRUM, we need a series of tools. Jira for task management, Jenkins for continous integrement, and Github for code management. I also set up a wiki for knowledge store and product summary. All these systems linked up together. Besides that, we need to set up rules and get people obey the rules to run SCRUM smoothly.

As to taks assignment, it's best to do this before a sprint starts, get the story points by discussing with product managers and get the estimate times by discussing with engineers, and reorder tasks by priority and assignment the right person. Normally once a sprint starts, the scope should not changes.

You need to balance different engineers' interests, pressure and expertises. Track down the burning graph during the whole sprint, and reslove any obstcules you find. One thing is not gonna change forever, quality is the most important while scope or schedule is not, even though the remaining two are also very important.

### Product Perspective

You need to know product from a product perspective even though you are not a product manager. It helps when you argue with them when they think the cost is not correct for one feature. Just joking. Actually it's more than that. You are in a team, everyone should think exchangebly. Only in this way can you help to make the priority list right.

### Aesthetic Taste

You should always trust professional people do professinal stuff and you should always trust your coworkers. However you must have a good aesthetic taste otherwise you may disagree with designeers work. Try to be humble and learn to designers.

### Team Building & Talent Development

For one or two months, there should be a team building. Just go climbing or go swimming or do anything cool in a team. You will find many things about your colleagues you didn't know before, and get some unexpected discoveries.

For new joined enginerrs, you have the responsibility to guid them, and point out a clear way to grow up if they need.

Tech sharing metting is a good way to learn technologies fast and know engineers at the same time. You should open it periodically.

### Development & System Admin

At last, as a tech lead, you also should bear some development tasks and operation tasks. Your code should be canonical to other engineers. Talk is cheap, show me your code. So show your code to others.
