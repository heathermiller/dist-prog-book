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

[citation erlang paper]

Erlang has only one clear benefit over C, which is dynamic code upgrading.
However, there are ways of making C behave in a similar fashion with minimal downtime.
Shuffler [citation] is a system for continuous randomization of code.
Using techniques discussed in the paper, one could dynamically replace sections of a binary.
Another, slightly hack-ish workaround would be to receive the upgrade, serialize the current state, and finally run the new binary based on the serialized state.
A third way of circumventing this problem would be to encapsulate any code in a shared library, and have logic in the program to unmap the old code, replace the library, and remap.
This approach is analogous to Erlang's approach.

Other than dynamic code swapping and poor error detection, Erlang does not offer anything that is not offered by a traditional OS.
Isolation, concurrency, and message passing can all be accomplished with unix-style system calls.
Why is this language not considered redundant?

## References

{% bibliography --file dist-langs %}
