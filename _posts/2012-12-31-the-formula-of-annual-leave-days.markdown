---
layout: post
title: "The Formula of Annual Leave Days"
date: 2012-12-31 00:00
comments: true
categories:
- Math
---

Company D recently changed the policy of annual leave days, which confused many people. So I make up these mathematical formulas to make it more clear.

Assume Amy's entry date is year $$ x_0 $$, month $$ y_0 $$, day $$ z_0 $$, then $$ F(x) $$, the annual leave days for year $$ x $$ is
$$
F(x) = \dfrac{\left\lfloor{2\left(f(x)+\dfrac{1}{4}\right)}\right\rfloor}{2}
f(x) = \begin{cases}
\dfrac{(x - x_0 + 9)(y_0 - 1) + (x - x_0 + 10)(12 - y_0 + 1)}{12},  &\text{if $x > x_0$;}\\
\dfrac{10(13 - y_0)}{12},                                           &\text{if $x = x_0 , z_0 <= 15$;}\\
\dfrac{10(12 - y_0)}{12},                                           &\text{if $x = x_0, z_0 > 15$;}\\
\end{cases}
$$
<!--more-->

The current available annual leave days $$ G(x, y, z) $$, for year $$ x $$, month $$ y $$, day $$ z $$, is
$$
G(x, y, z) = \dfrac{\left\lfloor2\left(g(x, y, z) + \dfrac{1}{4}\right)\right\rfloor}{2} + M(x, y, z) - N
g(x, y, z) =
\begin{cases}
\dfrac{f(x)(y - 1)}{12},               &\text{if $x > x_0$, $z$ is not the last day of month $y$;}\\
\dfrac{f(x)y}{12},                     &\text{if $x > x_0$, $z$ is the last day of month $y$;}\\
\max(0, \dfrac{10(y - y_0 - 1)}{12}),  &\text{if $x = x_0$, $z_0 > 15$, $z$ is not the last day of month $y$;}\\
\dfrac{10(y - y_0)}{12},               &\text{if $x = x_0$, $z_0 <= 15$, $z$ is not the last day of month $y$;}\\
\dfrac{10(y - y_0)}{12},               &\text{if $x = x_0$, $z_0 > 15$, $z$ is the last day of month $y$;}\\
\dfrac{10(y - y_0 + 1)}{12},           &\text{if $x = x_0$, $z_0 <= 15$, $z$ is the last day of month $y$;}\\
\end{cases}
M(x, y, z) =
\begin{cases}
G(x - 1, 12, 31),   &\text{if $(y, z) <= (6, 30)$;}\\
0,                  &\text{if $(y, z) > (6, 30)$;}\\
\end{cases}
N = \text{Annual leave days have been used for this year}
$$
