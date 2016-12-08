---
layout: page
title:  "Distributed Programming Languages"
by: "A Systems Person"
---

## Problems of Distributed Programming

There are problems that exist in distributed system environments that do not exist in single-machine environments.
Partial failure, concurrency, and latency are three problems that make distributed computing fundamentally different from local computing.
In order to understand the design decisions behind programming languages and systems for distributed computing, it is necessary to discuss these three problems that make distributed computing unique.
In this section, we present an overview of these three problems and their impact on distributed programming models.

### Partial Failure

In the case of a crash on a local environment, either the machine has failed (total failure), or the source of the crash can be learned from a central resource manager such as the operating system. (// TODO cite "a note on dist. comp.)
If an application consists of multiple communicating processes partial failure is possible, however because the cause of the partial failure can be determined, this kind of partial failure can be repaired given the operating system's knowledge about the failure.
For example, a process can be restored based on a checkpoint, another process in the application can query the operating system about another's state, etc.

* Failure in a distributed setting
  * 2 sources, network and host
  * no central manager (no knowledge)
  * non-determinism
  * consistency (leave until next section)
  * control is not returned to the caller, message or response may "vanish"
  
* Impact, methods of dealing with partial failure
  * recompute, duplicate computation (MR, RDD, Hadoop)
  * 2-phase commit (Argus)
  * redundancy (MR (spark's duplicate master), Orleans, Argus)
  * checkpoint-restore (Naiad, Hadoop)

### Consistency (Concurrency)

* Local
  * enforce consistency with locks
  * state located under one resource manager (partial local crash)

* Distributed
  * preserve state in instance of failure
  * concurrent method invocations / messages
  * operations on replicated objects (for scalability)
 
* Methods
  * sequencer
  * message queues
  * read only vs. write ops

### Latency

* Local
  * operations are relatively fast
  * topology doesn't change

* Distributed
  * Network failures and recovery
  * changing topology
  * efficiency

* Methods
  * process locality (static, dynamic analysis)
  * minimize communication
  * data replication (Orca)
  * pipelining (HTTP)
  * asynchronous callbacks
  
### The CAP Theorem

Indeed, these three issues of distributed computing are not disjoint.
A solution designed to solve one problem may exacerbate another.

* Consistency
* Availability
* Partitioning

## Three major approaches to distributed languages:

### Shared Memory

* Definition

* Mirage
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
