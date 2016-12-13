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
If an application consists of multiple communicating processes partial failure is possible, however because the cause of the partial failure can be determined, this kind of partial failure can be repaired given the operating system's knowledge.
For example, a process can be restored based on a checkpoint, another process in the application can query the operating system about the failed process' state, etc.

Because failure in a distributed setting involves another player, the network, it is impossible in most cases to determine the cause of failure.
In a distributed environment, there is no (reliable) central manager that can report on the state of all components.
Further, due to the inherent concurrency in a distributed system, nondeterminism is a problem that must be considered when designing distributed models, languages, and systems.
Communication is perhaps the most obvious example of this; messages may be lost or arrive out-of-order.
Finally, unlike in a local environment where failure returns control to the caller, failure may not be reported or the response may simply vanish.
Because of this, distributed communication must be designed expecting partial failure, and be able to "fail gracefully."

Several methods have been developed to deal with the problem of partial failure.
One method, made popular with batch processing and MapReduce style frameworks, is to remember the series of computations needed to obtain a result and recompute the result in the case of failure.
Systems such as MapReduce, Spark, GraphX, and Spark Streaming use this model, as well as implement optimizations to make it fast.
Another method of dealing with partial failure is the two phase commit.
To perform a change of state across many components, first a logically central "leader" checks to see if all components are ready to perform and action.
If all reply "yes," the action is *committed*.
Otherwise, as in the case of partial failure, no changes are committed.
Two phase commit ensures that state is not changed in a partial manner.
Another solution to partial failure is redundancy, or replication.
If one replica of a computation failes, the others may survive and continue.
Replication can also be used to improve performance, as in MapReduce and Spark Streaming.
Checkpoint and restore has also been implemented as a way to recover from partial failure.
By serializing a recent "snapshot" of state to stable storage, recomputing current state is made cheap.
This is the primary method of partial failure in RDD-based systems.
In other systems, like Argus, objects are reconstructed from state that is automatically or manually serialized to disk.

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
  * pipe-lining (HTTP)
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
Mirage, Orca, and Linda are three systems that use distributed shared memory to provide a distributed programming model.

#### Mirage (1989)

Mirage is an OS-level implementation of DSM.
In Mirage, regions of memory known as *segments* are created and indicated as shared.
A segment consists of one or more fixed-size pages.
Other local or remote processes can *attach* segments to arbitrary regions of their own virtual address space.
When a process is finished with a segment, the region can be *detached*.
Requests to shared memory are transparent to user processes.
Faults occur on the page level.

Operations on shared pages are guaranteed to be coherent; after a process writes to a page, all subsequent reads will observe the results of the write.
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
The timer guarantees that the page will not be invalidated for a minimum period of time.
Future request that result in invalidation or demotion (writer to reader) are only honored if the timer is satisfied.

#### Orca (1992)

Orca is a programming language built for distribution and is based on the DSM model.
Orca expresses parallelism explicitly through processes.
Processes in Orca are similar to procedures, but are concurrent instead of serial.
When a process is forked, it can take parameters that are either passed as a copy of the original data, or passed as a *shared data-object*.
Processes communicate through these shared objects.

Shared data objects in Orca are similar to objects in OOP.
An object is defined abstractly by a name and a set of interfaces.
An implementation of the object defines any private data fields as well as the interfaces (methods).
Importantly, these interfaces are guaranteed to be indivisible, meaning that simultaneous calls to the same interface are serializable.
Although serializability alone does not eliminate indeterminism from Orca programs, it keeps the model simple while it allows programmers to construct richer, multi-operation locks for arbitrary semantics and logic.

Another key feature of Orca is the ability to express symbolic data structures as shared data objects.
In Orca, a generic graph type is offered as a first-class data-object.
Because operations are serializable at the method level, the graph data-object can offer methods that span multiple nodes while still retaining serializability.

#### Linda (1993)

Linda is a programming model based on DSM.
In Linda, shared memory is known as the *tuple space*; the basic unit of shared data is the tuple.
Instead of processes reading and writing to shared memory addresses, processes can insert, extract, or copy entries from the tuple space.
Under the Linda model, processes communicate and distribute work through tuples.

A Linda tuple is not a fixed size; it can contain any combination of primitive data types and values.
To insert a tuple into the space, the fields of the tuple are fully evaluated before insertion.
A process can decide to evaluate a tuple serially, or spin up a background task to first evaluate the fields, then insert the tuple.
To retrieve a tuple from the space, a *template* tuple is provided that contains a number of fixed fields to match against, as well as *formals* that are "filled in" by the tuple that matches the search.
If many tuples match the template, one is selected arbitrarily.
When retrieving a tuple, the tuple may be left in the tuple space or removed.

In practice, the tuple space is disjointly distributed among the nodes in the cluster.
The number and type of elements in a tuple defines the tuple's *class*.
All requests made for a particular class of tuple are sent through a *rendezvous point*, which provides a logically central way of performing book keeping about tuples.
The rendezvous services requests for insertion and deletions of all tuples of a class.
In the most basic implementation of Linda, each rendezvous point is located on a single participating node in the cluster.

### Actor / Object model

Unlike DSM, communication in the actor model is explicit and exposed through message passing.
Messages can be synchronous or asynchronous, point-to-point or broadcast style.
In the actor model, concurrent entities do not share state as they do in DSM.
Each process, object, actor, etc., has its own address space.
The model maps well to single multicore machines as well as to clusters of machines.
Although an underlying system is required to differentiate between local and remote messages, the location of processes, objects, or actors can be transparent to the application programmer.
Erlang, Emerald, Argus, and Orleans are just a few of many implementations of the actor model.

#### Emerald (1987)

Emerald is a distributed programming language based around a unified object model.
Programs in Emerald consist of collections of Objects.
Critically, Emerald provides the programmer with a unified object model so as to abstract object location from the invocation of methods.
With that in mind, Emerald also provides the developer with the tools to designate explicitly the location of objects.

Objects in Emerald resemble objects in other OOP languages such as Java.
Emerald objects expose methods to implement logic and provide functionality, and may contain internal state.
However, their are a few key differences between Emerald and Java Objects.
First, objects in Emerald may have an associated process which starts after initialization.
In Emerald, object processes are the basic unit of concurrency.
Additionally, an object may *not* have an associated process.
Objects that do not have a process are known as *passive* and more closely resemble traditional Java objects; their code is executed when called by processes belonging to other objects.
Second, processes may not touch internal state (members) of other objects.
Unlike Java, all internal state of Emerald objects must be accessed through method calls.
Third, objects in Emerald may contain a special *monitor* section which can contain methods and variables that are accessed atomically.
If multiple processes make simultaneous calls to a "monitored" method, the calls are effectively serialized.

Emerald also takes an OOP approach to system upgrades.
With a large system, it may not be desirable to disable the system, recompile, and re-launch.
Emerald uses abstract types to define sets of interfaces.
Objects that implement such interfaces can be "plugged in" where needed.
Therefore, code may be dynamically upgraded, and different implementations may be provided for semantically similar operations.

#### Argus (1988)

Argus is a distributed programming language and system.
It uses a special kind of object, called a *guardian*, to create units of distribution and group highly coupled data and logic.
Argus procedures are encapsulated in atomic transactions, or *actions*, which allow operations that encompass multiple guardians to exhibit serializability.
The presence of guardians and actions was motivated by Argus' use as a platform for building distributed, consistent applications.

An object in Argus is known as a guardian.
Like traditional objects, guardians contain internal data members for maintaining state.
Unique to Argus is the distinction between volatile and stable data members.
To cope with crashes, data members that are stable are periodically serialized to disk.
When a guardian crashes and is restored, this serialized state is used to reconstruct guardians.
Like in Emerald, internal data members may not be accessed directly, but rather through handlers.
Guardians are interacted with through methods known as *handlers*.
When a handler is called, a new process is created to handle the operation.
Additionally, guardians may contain a background process for performing continual work.

Argus encapsulates handler calls in what it calls *actions*.
Actions are designed to solve the problems of consistency, synchronization, and fault tolerance.
To accomplish this, actions are serializable as well as total.
Being serializable means that no actions interfere with one another.
For example, a read operation that spans multiple guardians either "sees" the complete effect of a simultaneous write operation, or it sees nothing.
Being total means that write operations that span multiple guardians either fully complete or fully fail.
This is accomplished by a two-phase commit protocol that serializes the state of *all* guardians involved in an action, or discards partial state changes.

#### Erlang (2000)

Erlang is a distributed language which combines functional programming with message passing.
Units of distribution in Erlang are processes.
These processes may be co-located on the same node or distributed amongst a cluster.

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

#### Orleans (2011)

Orleans is a programming model for distributed computing based on actors.
An Orleans program can be conceptualized as a collection of actors.
Because Orleans is intended as a model for building cloud applications, actors do not spawn independent processes as they do in Emerald or Argus.
Rather, Orleans actors are designed to execute only when responding to requests.

As in Argus, Orleans encapsulates requests (root function calls) within *transactions*.
When processing a transaction, function calls may span many actors.
To ensure consistency in the end result of a transaction, Orleans offers another abstraction, *activations*, to allow each transaction to operate on a consistent state of actors.
An activation is an instance of an actor.
Activations allow (1) consistent access to actors during concurrent transactions, and (2) high throughput when an actor becomes "hot."
Consistency is achieved by only allowing transactions to "touch" activations of actors that are not being used by another transaction.
High throughput is achieved by spawning many activations of an actor for handling concurrent requests.

For example, suppose there is an actor that represents a specific YouTube video.
This actor will have data fields like `title`, `content`, `num_views`, etc.
Suppose their are concurrent requests (in turn, transactions) for viewing the video.
In the relevant transaction, the `num_views` field is incremented.
Therefore, in order to run the view requests concurrently, two activations (or copies) of the actor are created.

Because there is concurrency within individual actors, Orleans also supports means of state reconciliation.
When concurrent transactions modify different activations of an actor, state must eventually be reconciled.
In the case of the above example, it may not be necessary to know immediately the exact view count of a video, but we would like to be able to know this value eventually.
To accomplish reconciliation, Orleans provides data structures that can be automatically merged.
As well, the developer can implement arbitrary logic for merging state.
In the case of the YouTube video, we would want logic to determine the delta of views since the start of the activation, and add that to the actors' sum.

### Dataflow model

In the dataflow model, programs are expressed as transformations on data.
Given a set of input data, programs are constructed as a series of transformations and reductions.
Computation is data-centric, and expressed easily as a directed acyclic graph (DAG).
Unlike the DSM and actor models, processes are not exposed to the programmer.
Rather, the programmer designs the data transformations, and a system is responsible for initializing processes and distributing work across a system.

#### MapReduce (2004)

MapReduce is a model and system for writing distributed programs that is data-centric.
Distributed programs are structured as series of *Map* and *Reduce* data transformations.
These two primitives are borrowed from traditional functional languages, and can be used to express a wide range of logic.
The key strength of this approach is that computations can be reasoned about and expressed easily while an underlying system takes care of the "dirty" aspects of distributed computing such as communication, fault-tolerance, and efficiency.

A MapReduce program consists of a few key stages.
First, the data is read from a filesystem or other data source as a list of key-value pairs.
These pairs are distributed amongst a set of workers called *Mappers*.
Each mapper processes each element in its partition, and may output zero, one, or many *intermediate* key-value pairs.
Then, intermediate key-value pairs are grouped by key.
Finally, *Reducers* take all values pertaining to an intermediate key and output zero, one, or many output key-value pairs.
A MapReduce job may consist of one or many iterations of map and reduce.

Crucially, for each stage the programmer is only responsible for programming the Map and Reduce logic.
The underlying system (in the case of Google, a C++ library), handles distributing input data and *shuffling* intermediate entries.
Optionally, the user can implement custom logic for formatting input and output data.

An example program in MapReduce is illustrated below.
First, the input file is partitioned and distributed to a set of worker nodes.
Then, the map function transforms lines of the text file into key-value pairs in the format (\< word \>, 1).
These intermediate pairs are aggregated by key: the word.
In the reduce phase, the list of 1's is summed to compute a wordcount for each word.

![Alt text] (./MR.png "MapReduce Workflow")
(http://www.milanor.net/blog/an-example-of-mapreduce-with-rmr2/)

#### Discretized Streams (2012)

Discretized Streams is a model for processing streams data in real-time based on the traditional dataflow paradigm.
Streams of data are "chunked" discretely based on a time interval.
These chunks are then operated on as normal inputs to DAG-style computations.
Because this model is implemented on top of the MapReduce framework Spark, streaming computations can be flexibly combined with static MapReduce computations as well as live queries.

Discretized Streams (D-Streams) are represented as a series of RDD's, each spanning a certain time interval.
Like traditional RDD's, D-Streams offer stateless operations such as *map*, *reduce*, *groupByKey*, etc., which can be performed regardless of previous inputs and outputs.
Unlike traditional RDD's, D-Streams offer *stateful* operations.
These stateful operations, such as *runningReduce*, are necessary for producing aggregate results for a *possibly never-ending* stream of input data.

Because the inputs are not known *a priori*, fault tolerance in streaming systems must behave slightly differently.
For efficiency, the system periodically creates a checkpoint of intermediate data.
When a node fails, the computations performed since the last checkpoint are remembered, and a new node is assigned to recompute the lost partitions from the previous checkpoint.
Two other approaches to fault tolerance in streaming systems are replication and upstream backup.
Replication is not cost effective as every process must be duplicated, and does not cover the case of all replicas failing.
Upstream backup is slow as the system must wait for a backup node to recompute everything in order to recover state.

#### GraphX (2013)

Many real world problems are expressed using graphs.
GraphX is a system built on top of the Spark MapReduce framework { // TODO cite RDD } that exposes traditional graph operations while internally representing a graph as a collection of RDD's.
GraphX exposes these operations through what it calls a Resilient Distributed Graph (RDG).
Internally, an RDG is a collection of RDD's that define a vertex split of a graph { // TODO CITE powergraph }.
Because they are built on top of RDD's, RDG's inherit immutability.
When a transformation is performed, a new graph is created.
In this way, fault tolerance in GraphX can be executed the same way as it is in vanilla Spark; when a fault happens, the series of computations is remembered and re-executed.

A key feature of GraphX is that it is a DSL library built on top of a GPL library.
Because it uses the general purpose computing framework of Spark, arbitrary MapReduce jobs may be performed in the same program as more specific graph operations.
In other graph-processing frameworks, results from a graph query would have to be written to disk to be used as input to a general purpose MapReduce job.

With GraphX, if you can structure your application logic as a series of graph operations, an implementation may be created on top of RDD's.
Because many real-world applications, like social media "connections," are naturally expressed as graphs, GraphX can be used to create a highly scalable, fault-tolerant implementation.

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
