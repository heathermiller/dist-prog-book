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

### Distributed Shared Memory

Virtual memory provides a powerful abstraction for processes.
It allows each process running on a machine to believe it is the sole user of the machine, as well as provide each process with more (or less) memory addresses than may be physically present.
The operating system is responsible for mapping virtual memory addresses to physical ones and swapping addresses to and from disk.

Distributed shared memory (DSM) takes the virtual memory abstraction one step further by allowing virtual addresses to be mapped to physical memory regions on  remote machines.
Given such an abstraction, programs can communicate simply by reading from and writing to shared memory addresses.
DSM is appealing because the programming model is the same for local and distributed systems.
However, it requires an underlying system to function properly.
Mirage, Linda, and Orca are three systems that use distributed shared memory to provide a distributed programming model.

#### Mirage

#### Linda

#### Orca

Orca is a programming language built for distribution and is based on the DSM model.
Orca expresses parallelism explicitly through processes.
Processes in Orca are similar to procedures, but are concurrent instead of serial.
When a process is forked, it can take parameters that are either passed as a copy of the original data, or passed as a *shared data-object*.
Processes can then communicate through these shared objects.

Shared data objects in Orca are similar to objects in OOP.
An object is defined abstractly by a name and a set of interfaces.
An implementation of the object defines any private data fields as well as the interfaces (methods).
Importantly, these interfaces are gauranteed to be indivisible, meaning that simultaneous calls to the same interface are serializable.
Although serializability alone does not eliminate indeterminism from Orca programs, it keeps the model simple while it allows programmers to construct richer, multi-operation locks for arbitrary semantics and logic.

Another key feature of Orca is the ability to express symbolic data structures as shared data objects.
Because shared data is expressed through data-objects, it is easy to serialize, for instance, operations on a binary tree.

* processes - for distribution, sharing data
    * concurrency is explicit
    * control over where processes are located
    * invocation ( fork( parameters ) [ on CPU # ]; )
* abstract data types - shared data objects
    * similar to objects in OOP
    * interfaces
    * operations on objects (methods) are indivisible (serializable)
    * talk about their implementation

#### RPC ( and why RPC is shared-memory )

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
