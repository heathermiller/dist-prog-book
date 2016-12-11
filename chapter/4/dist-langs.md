---
layout: page
title:  "Distributed Programming Languages"
by: "A Systems Person"
---

### Two major major, orthogonal approaches to distributed languages:

#### Actor / Object model

The actor model has its roots in procedural programming.
This model maps in a straighforward way to a distributed environment.

* Erlang
* Cloud Haskell (I know, right? Why?)

#### Dataflow model (static and stream)

The dataflow model has its roots in functional programming.
Some languages that use this model are:

* Multilisp
* MapReduce (Spark, Hadoop, etc.)

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

## References

{% bibliography --file dist-langs %}
