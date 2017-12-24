---
layout: page
title:  "Distributed Programming Languages"
by: "Connor Zanin"
---

# Why is Distributed Computing so hard?

There are problems that exist in distributed system environments that do not exist in single-machine environments.

## Node Failures

## Packet Drops / Delays / Corruption

## Network Partitions

## Latency

## The CAP Theorem
This needs to be mentioned *somewhere*.

# How can we make it easier? : Distribution as a Domain
RPC failed as a holistic solution because it didn't address these problems. Can we develop tools to help programs deal with these problems? Or should we just leave it up to the programmer?

Avoid the definition of a language. A domain-specific language is a programming tool that is tailored to a specific domain.

Given the examples of models and systems, I think it is reasonable to qualify distribution as a domain.
Distributed computing has a unique set of problems, such as fault-tolerance, nondeterminism, network partitioning, and consistency that make it unique from parallel computing on a single machine.
The languages, systems, and models presented here all are built to assist the developer in dealing with these problems.

### Drilling down further
It's possible for something to drill further into a domain. Distribution may be a broad domain, but there may be more specific domains within distribution to take into account: for example, Spark is a distributed computation DSL, but more specifically is concerned with the processing of data as opposed to, say, running a highly fault-tolerant webserver.

What other sub-taxonomies can we present?

## Four Major Approaches to Distributed Languages / DSLs

### Distributed Shared Memory

#### Mirage (1989)

#### Orca (1992)

#### Linda (1993)

### Virtualization Models 
[What I mean: Argus virtualizes computation at the level of a node. Guardians are essentially collections of objects performing operations, ie virtualized nodes. These virtual nodes can be moved at will. Emerald virtualized at the level of objects: objects become distributed, abstract entities (they are already, to some degree, but cannot yet be distributed) which are now capabale of moving throughout the system. Perhaps rather than `virtualized`, I mean `distributed`. The actor model virtualizes at the level of the *process*. These are the building blocks at which the system reasons about distribution. I think this is a cleaner way to present this information.]

#### Argus (1988)

#### Emerald (1987)

#### Erlang (2000)

#### Orleans (2011)

#### Cloud Haskell

#### ML5

#### Eden

#### Akka

### Dataflow model

#### MapReduce (2004)

#### Discretized Streams (2012)

#### GraphX (2013)

## Comparing Design

Here, we present a further taxonomy which can be used to classify each of the examples.

### Concern with Fault Tolerance
Some languages care, some don't. Some give you guarantees, some don't.

### Generalizability
Some are frameworks for creating all kinds of distributed applications. Some are specific tools aimed at solving specific problems.

### Abstraction & Distributed Control
Are you aware you are running a distributed system? How much control do you have over locality and process management?

### New Language or DSL?

**Is this actually relevant?**

At first, systems designed to tackle the distribution domain were implemented as stand-alone languages.
Later, these systems appear as libraries built on top of existing general-purpose languages.
 
[ripped from 5]
### Clean-slate language implementations

 A straightforward approach to implementing a new language is to start from scratch. Beginning with a clean slate offers several advantages. First, the implementor has complete control (up to what they are willing and able to implement) over every aspect of the design. Second, some elements of language design are difficult to integrate with other languages. Type systems are a good example of the problem. How to combine the designs of two type systems into one that has the properties of both is an open problem. If types play a prominent role in the language then starting anew may be the only option. However, this strategy has apparent drawbacks not only in term of implementation effort for the creator(s) but also for users.

### Extension to an existing language

 Another option is to use another language as a starting point and modify that language’s implementation for your own purposes. Think of it as forking a compiler and/or runtime and then making your own modifications. An advantage of this approach is the savings in implementation effort. If the computation models coincide then the language designer only has to implement the communication model and fault-tolerance strategy. Another plus is that users of the existing language may be more likely to consider trying or adopting the new language since it is only a step away from what they already know. A downside for maintaining any fork is keeping up to date with upstream changes.

### Library

 The final approach to consider is similar to extending a language, but this time doing so only by writing code in that language to create new abstractions implementing a language model. This strategy offers similar savings in implementation effort to extending a language (perhaps more so). But a major benefit is that is significantly easier for users to use and adopt; the only new concepts they must learn are the specifics of the programming model, as opposed to other concerns such as syntax.

PROS AND CONS:

#### Domain Composition

#### Ecosystem

## References

{% bibliography --file dist-langs %}
