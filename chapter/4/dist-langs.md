---
layout: page
title:  "Distributed Programming Languages"
by: "A Systems Person"
---

## Problems of Distributed Programming

There are problems that exist in distributed system environments that do not exist in single-machine environments.
For example, programs running on distributed systems must be resilient to partial failure.
In a single-machine environment, a program is either running or crashed.
When instructions are distributed accross multiple machines, the program can be running, crashed, or partially crashed.
Programs, systems, and languages designed for distribution must be able to tolerate problems such as partial failure.
Furthermore, they must abstract some or all of these problems from the application developer and application logic.

### Partial Failure

On a single-machine environment, a crash means that either the machine has failed (total failure), or the source of the crash can be learned from a central resource manager such as the operating system. (// TODO cite "a note on dist. comp.)
If an application consists of multiple communicating processes, it is possible for some components to remain running when others have crashed.

### Consistency (Concurrency)



### Efficiency (Latency)



### Scallability

For the above points cite "A Note on Distributed Computing," "Fallacies of Distributed Computing Explained"

Languages and systems designed for distribution aim to abstract these problems from the application developer.


## Three major approaches to distributed languages:

### Shared Memory

What is it?

Some examples:

* Linda
* Orca
* RPC ( and why RPC is shared-memory )

Tries to make many machines look like a single machine.
This is hard because of consistency and partitioning.
The logic of the program is simple, but requiring that the system handle shared memory opens up many opportunities for performance bugs.

### Actor / Object model

The actor model has its roots in procedural and object oriented programming.
Communication through RPC or message-passing.
Actors/Objects are location agnostic, because state is not shared.
The system can decide how to most efficiently place actors.

* Erlang
* Cloud Haskell
* Emerald
* Argus
* Orleans

### Dataflow model (static and stream)

The dataflow model has its roots in functional programming.
Some languages that use this model are:

* Multilisp
* MapReduce (Spark, Hadoop, etc.)
* RDD
* Dryad, DryadLinq

### Which is best? Why?

MR vs Actors: depends on problem, solution

How fine grain is your data and logic? (MR job can be built from actor model)
Does your algorithm map to a batch processing job?

MR:

* MR is DSL for distribution? (wouldn't use it to develop single-machine app (probably))
* Dataflow / MapReduce fundamentally changed the programming style for distributed systems
* Other models (Actor, DSM) tried to mask distribution
* By changing the style, programs need necessarily consider communication patterns (disk, network)
* Although, system may still handle fault tolerance

Actors:

* Message-passing chapter

## Support for Distribution

### Intro

* What is a DSL?

> Domain-specific languages are languages tailored to a specific application domain.

Another definition:

> A domain-specific language is a programming language or executable specification language that offers, through appropriate notations and abstractions, expressive power focused on, and usually restricted to, a particular problem domain.

### Where is it in the stack?

* Libraries:
* Compiler Extension
* Compiler / Runtime:
* Hardware

### Why DSL's as Libraries?

Reasons for moving to GPL's as base for DSL's

* problem of domain-composition
* problem of abstraction
* problem of ecosystem
* problem of tumultuous architecture
* "any gpl + library can act as a dsl" - mernik"

## References

{% bibliography --file dist-langs %}
