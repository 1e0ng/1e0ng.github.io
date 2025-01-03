---
layout: post
title: "Why EMV QR Code was NOT designed well"
date: 2022-06-28 00:17:12 +0800
comments: true
categories:
- payments
---

[EMV](https://en.wikipedia.org/wiki/EMV) QA code is being widely used in payment areas, actually it's kind of a defacto standard for a lot of payment flows. Everyone can download the standard on [emvco.com official website](https://www.emvco.com/emv-technologies/qrcodes/#:~:text=A%20QR%20Code%20is%20an,and%20Merchant%2Dpresented%20QR%20Codes.).

A lot of governments' authorities created their QR code standards based on EMV QR code. For instance, [SGQR](https://www.mas.gov.sg/development/e-payments/sgqr#:~:text=SGQR%20is%20the%20world's%20first,for%20both%20consumers%20and%20merchants.) from Singapore, [BR Code](https://www.bcb.gov.br/content/config/Documents/BR_Code_MANUAL_Version_2_May_2020.pdf) from Brazil etc.

Even though EMV QR code is ubiqus, yet I don't think it's designed well from the beginning. Actually, to me, the EMV QR code looks very likely to be designed by someone with very little engineering excellence knowledge.

<!-- more -->

## Effeciency

As a QR code, it denotes a string and it is encoded by a string value. The length of the string value usually decides how complex the QR code is. Most of the times, the longer the string value, the bigger QR will be. What does it imply for a bigger QR code? It means users need a better smart phone with a better camera to read the QR code, also the decoding process will be slightly longer. Well, it may mean nothing for you, there are actually so many users are using low-end or middle-range smart phones with less powerful cameras. What I mean here is making a QR code shorter and smaller does matter.

Let's look at how EMV code standard does. Basically it follows a TLV ([Type–length–value](https://en.wikipedia.org/wiki/Type%E2%80%93length%E2%80%93value#:~:text=Within%20communication%20protocols%2C%20TLV%20(type,and%20finally%20the%20value%20itself.) format. TLV provides an excellent extensibility. Users can define a new Type and declare the length for the value then append a value, bingo. But is that the best you can do? Can you do better to make the value shorter while maintaining the extensibility. For example, can we combine the Type and Length, or even for certain type, we pre-defined the length? Of course, this will the standard more complex, but for the effeciency, it is well worth we invest more on the standard. The end-users, the consumers and the merchants won't be bothered by the complexisity of the encoding or decoding of the QR code, as they never do it today. It's the developers with sophisticated engineering knowledge who will do the encoding and decoding, so a little bit complexisity will for sure bring a much more effeciency QR code.

The Type part of the TLV simply use a 2 digit string value, from "00" to "99". Sigh, even one byte can denote 2^8 = 256 values, you use 2 bytes?!!

Ok, let talk about the Value part of TLV. Even the Value part itself, EMV does a terrable job on efficiency. Look at how it denotes transaction currency: A 3-digit numeric value, as defined by [ISO 4217]. It simply uses 3 bytes for that where even two byte is a waste for a number less than 1000. One byte can denote 2^8 = 256, while 10 bits can denote 2^10 = 1024. So 10 bits is more than enough. To design a effecient QR stard, we'd better to count in bit instead of bytes! Someone may argue about readability. Please note, a value of the QR code is not designed for human to read it directly. Even with the existing EMV QR standard, one still need a decoder to view the vaules of each fields, so readability is non-sense.

How about transaction amount? From the standard, The transaction amount (excluding tips and convenience fees), if known. For instance, "99.34". Let's use the example from the standard, 99.34. It's 5 bytes! Come one, one simple solution is to use the minor unit standard from [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217), we can simply put 9934 without a dot. Minor unit standard is widely used and it can denote amount in integer without any concerns about float values (float can not be described precisely in computer). Check the APIs from Stripe, or other well designed APIs, all use the minor unit to denote the amount of money. Only non-professionals like PayPal will use a string of decimal to denote money. Ok, let's say we use an int32 to denote money, only 4 bytes, we can denote from -2,147,483,648 to +2,147,483,647. But what if we want to add an amount of 21474836.47 by EMV QR standard? It's 11 bytes.

In summary, TLV: not effecient. T: not effecient. L: not effecient. V: not effecient. I don't think EMV code is designed with data effeciency in mind.

## Not Following Standards

As mentioned earlier, the amount of money is not following the minor unit standard from ISO 4217. Even the CRC check is not following the [standard](https://en.wikipedia.org/wiki/Cyclic_redundancy_check). If you follow the wikipedia algorithm to implement the CRC, you will find the result doesn't match... Ok, later, they revised the standard to mention they are using the polynomial '1021' (hex) and initial value 'FFFF' (hex). The first version, they even not mention those 2 parameters, let the developers to try and guess. Can you imagine that? LOL.

In the EMV QR code standard, it mentions a field called Globally Unique Identifier, but there is not a strict format for it. According to the comment, An identifier that sets the context of the data that follows.
The value is one of the following:

- an Application Identifier (AID);
- a [UUID] without the hyphen (-) separators;
- a reverse domain name.

Well, if the format can be any one of the above format, and it's possible to be in other format as well, then how do we make sure it's globally unique? To design a standard, it's better to think thorougly. Is it going to be used in a centralised way or decentralised way? Is the global uniqueness guaranteed by each country's authorities, the QR generator (merchants for instance), the merchant acquirers, the payment gateway? Is it possible to define it in a more strict way and also make it as short as possible while gurantee the uniqueness? I don't see a responsibility here when designing a standard.

## Who Cares?

If a standard was designed so bad, why a lot of countries' authorities chose to use it? I don't have an answer yet. These days, less and less people would like to think by themselves rather than following others. Please do think, and it's a privilge as a human being.
