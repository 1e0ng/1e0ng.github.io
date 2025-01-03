---
layout: post
title: "Calculate distance between Latitude/Longitude points"
date: 2015-08-20 09:44:20 +0800
comments: true
categories:
- Math
---


This page presents a variety of calculations for latitude/longitude points, with the formula and code fragments for implementing them.

All these formula are for calculations on the basis of a spherical earth (ignoring ellipsoidal effects) – which is accurate enough for most purposes [In fact, the earth is very slightly ellipsoidal; using a spherical model gives errors typically up to 0.3%].

### Distance

This uses the [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) to calculate the great-circle distance between two points – that is, the shortest distance over the earth's surface – giving an "as-the-crow-flies" distance between the points (ignoring any hills they fly over, of course!).

Haversine formula: $$ haversin{\left(\dfrac{d}{r}\right)} = haversin{\left(\phi_2-\phi_1\right)} + \cos{\phi_1}\cos{\phi_2}\,haversin{\left(\lambda_2-\lambda_1\right)} $$

where

$$ haversin(\theta) = \sin^2\left(\dfrac{\theta}{2}\right) = \dfrac{1-\cos(\theta)}{2} $$

$$ d $$ is the distance between the two points (along a great circle of the sphere)

$$ r $$ is the radius of the sphere

$$ \phi_1 $$, $$ \phi_2 $$: latitude of point 1 and latitude of point 2

$$ \lambda_1 $$, $$ \lambda_2 $$: longitude of point 1 and longitude of point 2




