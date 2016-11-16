---
layout: page
title:  "Distributed Programming Languages"
by: "A Systems Person"
---

Distributed programming is hard because of:

* Network partitions
* Node failures
* Efficiency / Communication
* Data distribution / locality

### Two major major, orthogonal approaches to distributed languages:

#### Actor / Object model

* Erlang
* Cloud Haskell

#### Dataflow model

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

## References

{% bibliography --file dist-langs %}
