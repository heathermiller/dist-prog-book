---
layout: page
title:  "Distributed Programming Languages"
by: "A Systems Person"
---

### Problems of Distributed Programming

* Partial failure
* Consistency
* Efficiency
* Scallability

Languages and systems designed for distribution aim to abstract these problems from the application developer.


### Three major approaches to distributed languages:

#### Shared Memory

What is it?

Some examples:

* Linda
* Orca

Tries to make many machines look like a single machine.
This is hard because of consistency and partitioning.
The logic of the program is simple, but requiring that the system handle shared memory opens up many opportunities for performance bugs.

#### Actor / Object model

The actor model has its roots in procedural and object oriented programming.
Communication through RPC or message-passing.
Actors/Objects are location agnostic, because state is not shared.
The system can decide how to most efficiently place actors.

* Erlang
* Cloud Haskell (I know, right? Why?)
* Emerald
* Argus

#### Dataflow model (static and stream)

The dataflow model has its roots in functional programming.
Some languages that use this model are:

* Multilisp
* MapReduce (Spark, Hadoop, etc.)
* Orleans (Wait, what??)

#### Which is best? Why?

Why is MR all-the-rage?

* MR is DSL for distribution? (wouldn't use it to develop single-machine app (probably))

* Dataflow / MapReduce fundamentally changed the programming style for distributed systems
* Other models (Actor, DSM) tried to mask distribution
* By changing the style, programs need necessarily consider communication patterns (disk, network)
* Although, system may still handle fault tolerance

## Maybe use below topics

### Why GPL's not DSL's?

* problem of domain-composition
* problem of abstraction
* problem of ecosystem
* problem of tumultuous architecture
* "any gpl + library can act as a dsl" - mernik"

#### Erlang vs C: A Tar and Feathering

{% cite Armstrong2010 --file dist-langs %}

Erlang offers nothing that is unavailable in C.

For example, dynamic code swapping is one of Erlang's major selling points.
However, code swapping can easily be achieved in C with dynamic linking.
This approach is analogous to the example offered in the Erlang paper.

Other selling points, such as isolation, concurrency, and message passing can all be accomplished with unix-style system calls.
Why is this language not considered redundant?

#### MapReduce: A New Hope

Unlike Erlang, MapReduce and DSL's that implement the paradigm are "all the rage."
Unlike Erlang, MapReduce has experienced adoption because it offers true abstraction of the problems of distributed computing.
Erlang only provided a way of detecting a process failure; it did not consider machine or network failures.

* MapReduce is a GPL for the domain of distribution

## References

{% bibliography --file dist-langs %}
