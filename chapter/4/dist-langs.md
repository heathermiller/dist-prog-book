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

## Three Major Approaches to Distributed Languages

Clearly, there are problems present in distributed programming that prevent traditional local programming models from applying directly to distributed environments.
Languages and systems built for writing distributed applications can be classified into three categories: distributed shared memory, actors, and dataflow.
Each model has strengths and weaknesses.
Here, we describe each model and provide examples of languages and systems that implement them.

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

Mirage is an OS-level implementation of DSM.
In Mirage, regions of memory known as *segments* are created and indicated as shared.
A segment consists of one or more fixed-size pages.
Other local or remote processes can *attach* segments to arbitrary regions of their own virtual address space.
When a process is finished with a segment, the region can be *detached*.
Requests to shared memory are transparent to user processes.
Faults occur on the page level.

Operations on shared pages are gauranteed to be coherent; after a process writes to a page, all subsequent reads will observe the results of the write.
To accomplish this, Mirage uses a protocol for requesting read or write access to a page.
Depending on the permissions of the current "owner" of a page, the page may be invalidated on other nodes.
The behavior of the protocol is outlined by the table below.

| State of Owner | State of Requester | Clock Check? | Invalidation?                                               |
|----------------|--------------------|--------------|-------------------------------------------------------------|
| Reader         | Reader             | No           | No                                                          |
| Reader         | Writer             | Yes          | Yes, Requester is possibly sent current version of the page |
| Writer         | Reader             | Yes          | No, Owner is demoted to Reader                              |
| Writer         | Writer             | Yes          | Yes                                                         |

Crucially, the semantics of this protocol are that at any time there may only be either (1) a single writer or (2) one or more readers of a page.
When a single writer exists, no other copies of the page are present.
When a read request arrives for a page that is being written to, the writer is demoted to a reader.
These two properties ensure coherence.
Many read copies of a page may be present, both to minimize network traffic and provide locality.
When a write request arrives for a page, all read instances of the page are invalidated.

To ensure fairness, the system associates each page with a timer.
When a request is honored for a page, the timer is reset.
The timer gaurantees that the page will not be invalidated for a minimum period of time.
Future request that result in invalidation or demotion (writer to reader) are only honored if the timer is satisfied.

#### Linda

#### Orca

Orca is a programming language built for distribution and is based on the DSM model.
Orca expresses parallelism explicitly through processes.
Processes in Orca are similar to procedures, but are concurrent instead of serial.
When a process is forked, it can take parameters that are either passed as a copy of the original data, or passed as a *shared data-object*.
Processes communicate through these shared objects.

Shared data objects in Orca are similar to objects in OOP.
An object is defined abstractly by a name and a set of interfaces.
An implementation of the object defines any private data fields as well as the interfaces (methods).
Importantly, these interfaces are gauranteed to be indivisible, meaning that simultaneous calls to the same interface are serializable.
Although serializability alone does not eliminate indeterminism from Orca programs, it keeps the model simple while it allows programmers to construct richer, multi-operation locks for arbitrary semantics and logic.

Another key feature of Orca is the ability to express symbolic data structures as shared data objects.
In Orca, a generic graph type is offered as a first-class data-object.
Because operations are serializable at the method level, the graph data-object can offer methods that span multiple nodes while still retaining serializability.

### Actor / Object model

Unlike DSM, communication in the actor model is explicit and exposed through message passing.
Messages can be synchronous or asynchronous, point-to-point or broadcast style.
In the actor model, concurrent entities do not share state as they do in DSM.
Each process, object, actor, etc., has its own address space.
The model maps well to single multicore machines as well as to clusters of machines.
Although an underlying system is required to differentiate between local and remote messages, the location of processes, objects, or actors can be transparent to the application programmer.
Erlang, Emerald, Argus, and Orleans are just a few of many implementations of the actor model.

#### Erlang

Erlang is a distributed language which combines functional programming with message passing.
Units of distribution in Erlang are processes.
These processes may be colocated on the same node or distributed amongst a cluster.

Processes in Erlang communicate by message passing.
Specifically, a process can send an asynchronous message to another process' *mailbox*.
At some future time, the receiving process may enter a *receive* clause, which searches the mailbox for the first message that matches one of a set of patterns.
The branch of code that is executed in response to a message is dependent on the pattern that is matched.

In general, an application written in Erlang is separated into two broad components: *workers* and *monitors*.
Workers are responsible for application logic.
Erlang offers a special function `link(Pid)` which allows one process to monitor another.
If the process indicated by `Pid` fails, the monitor process will be notified and is expected to handle the error.
Worker processes are "linked" by monitor processes which implement the fault-tolerance logic of the application.

Erlang, first implemented in Prolog, has the features and styles of a functional programming language.
Variables in Erlang are immutable; once assigned a value, they cannot be changed.
Because of this, loops in Erlang are written as tail recursive function calls.
Although this at first seems like a flawed practice (to traditional procedural programmers), tail recursive calls do not grow the current stack frame, but instead replace it.
It is worth noting that stack frame growth is still possible, but if the recursive call is "alone" (the result of the inner function is the result of the outer function), the stack will not grow.

#### Cloud Haskell

#### Emerald

#### Argus

#### Orleans

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
