---
layout: page
title:  "RPC is Not Dead: Rise, Fall and Rise of RPC"
by: "Muzammil Abdul Rehman and Paul Grosu"
---

## Introduction

*Remote Procedure Call* (RPC) is a design *paradigm* that allow two entities to communicate over a communication channel in a general request-response mechanism. It was initially built as a tool for outsourcing computation to a server in a distributed system, however, it has evolved over the years to build 

* Define what RPC is.
* The main idea of our paper: 
* RPC was initially built as a tool for outsourcing computing. 
* RPC is relevant to this day as a language for building and connecting scalable modularized, language-agnostic systems.
* It is the design and idea of remote computation, the driving force behind RPC, gave rise to truly distributed systems and different communication schemes between different entities.
* Why is RPC relevant?
* Microservices
* Asynchronous Bidirectional communication for connecting services and devices
* GRPC, Finagle, Thrift, SOAP, CORBA, RMI
* It has influenced other programming designs. 
* Evolved with Time
* REST, HTTP


* The main idea of our paper: 

    * RPC was initially built as a tool for outsourcing computing. 

    * RPC is relevant to this day as a language for building and connecting scalable modularized, language-agnostic systems.

    * It is the design and idea of remote computation, the driving force behind RPC, gave rise to truly distributed systems and different communication schemes between different entities.

* Why is RPC relevant?

    * Microservices

    * Asynchronous Bidirectional communication for connecting services and devices

    * GRPC, Finagle, Thrift, SOAP, CORBA, RMI

    * It has influenced other programming designs. 

        * Evolved with Time

        * REST, HTTP

## Remote Procedure Calls:

* Local and remote endpoints, communication protocol.

    * Diagram.

* Initially: there was a registry involved(now they’ve moved), kept an open connection,.

* Now:

	* Security(Authentication and authorization)

    * Fault tolerance.

    * Asynchronously

    * Load Balancing

* Examples:

    * One could view the internet as example of RPC.e.g  TCP handshake(both act as server and client).

    * First: Google Maps API(REST)

    * SSL Handshake.

Suggestions from Heather:

* Be aware of Chris's thing: https://christophermeiklejohn.com/pl/2016/04/12/rpc.html

* Thrift vs gRPC.

## Evolution of RPC:

* RPC has evolved from what it was originally proposed.

* Chris’s thing: https://christophermeiklejohn.com/pl/2016/04/12/rpc.html

* 1980’s

    * RPC origin.

        * Implementing RPC: [https://dl.acm.org/citation.cfm?id=357392](https://dl.acm.org/citation.cfm?id=357392)

        * The RPC thesis(Nelson)

        * More examples

* 1990’s

    * The fall of RPC/Criticism of RPC

        * Limitations

        * [http://www.cs.vu.nl//~ast/afscheid/publications/euteco-1988.pdf](http://www.cs.vu.nl//~ast/afscheid/publications/euteco-1988.pdf)

        * Systems that use message passing.

* 2000-*

## Remote Method Invocation:

* Pros and Cons

## CORBA:

* Pros and Cons

## XML-RPC and SOAP:

* Pros and Cons

## Thrift:

* Pros and Cons

## Finagle:

* Pros and Cons

## gRPC:

## Discussion 1(change heading): 

* gRPC vs Thrift (maybe also Finagle)

## Applications:

* RPC and shared state (Persistence Layer):

    * [http://ieeexplore.ieee.org/document/1302942/?arnumber=1302942&tag=1](http://ieeexplore.ieee.org/document/1302942/?arnumber=1302942&tag=1)

    * http://ieeexplore.ieee.org/document/918991/?arnumber=918991

* Grid computing: 

    * https://link.springer.com/article/10.1023/A:1024083511032

* Mobile Systems(offloading and battery requirements): [https://link.springer.com/article/10.1007/s11036-012-0368-0](https://link.springer.com/article/10.1007/s11036-012-0368-0)

* Embedded RPC:

    * https://dl.acm.org/citation.cfm?id=1127840

* Micro services architecture(ecosystem)

* Streaming

* RPC can be async

* Shared State

* microservices

## RPC in Streaming Protocols:

* Streaming requests and buffered responses

## RPC in microservices ecosystem:

* Creating new services.

* Bootstrapping

* Load balancing

    * Creating new services in Actor-Like model

    * Fault tolerance

    * Self-recovery

* Business and Persistence Layer were combined and the Persistence layer is not shared anymore, where each endpoints has its own persistent state:

    * [https://help.sap.com/saphelp_nwmobile711/helpdata/de/7e/d1a40b5bc84868b1606ce0dc72d88b/content.htm](https://help.sap.com/saphelp_nwmobile711/helpdata/de/7e/d1a40b5bc84868b1606ce0dc72d88b/content.htm)

## Security in RPC:

* Initially it was separate.

    * Authentication, authorization issues have been resolved

* Now embedded in the protocol

* Security and Privacy in RPC

    * Bugs in the libraries.

    * Trust Issues between client and the server.

    * [http://static.usenix.org/publications/library/proceedings/sec02/full_papers/giffin/giffin_html/](http://static.usenix.org/publications/library/proceedings/sec02/full_papers/giffin/giffin_html/)

    * Brewer’s view: https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf

    * E programming language: distributed object model/VAT

## Discussion:

* RPC vs REST and other services. RPC influence.

* The future of RPC

    * Where it shines. Not in message passing.

## Conclusions:

	Some conclusion.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Class: Functional Programming for Distributed Computing

Theme: The idea of communicating and invoking remote functions for distributed computation.

Target Audience: Networks background, and wants to learn RPC.

-> RPC is not XYZ (HTTP, REST, …) though it has influenced.  The 

RPC influence in XYZ design, though 

* RPC started in 1980’s and still continues as a relevant model of performing distributed computation, which initially was developed for a LAN and now can be globally implemented.

* RPC started as a separate implements of REST, Streaming RPC, and now made possible of integration of all these implementations as a single abstraction for a user endpoint service.

    * (subsection) How RPC influenced other models of communication.

* RPC Models: 

    * One Server Model

* Methods of invoking remote function.

* Discuss the evolution and pitfalls as they developed to an optimized 

* Software-As-A-Service: End-User focused.



Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. {% cite Uniqueness --file rpc %}

## References

{% bibliography --file rpc %}