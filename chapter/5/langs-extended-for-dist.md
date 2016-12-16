---
layout: page
title:  "General Purpose Languages Extended for Distribution"
by: "Sam Caldwell"
---

## Introduction

In very general terms, a distributed system is comprised of nodes
that internally perform computation and communicate with each other.
Therefore programming a distributed system requires two distinct
models: one for the computation on each node and one to model the
network of communications between nodes.

A slightly-secondary concern is fault-tolerance. Failure of nodes and communication is one of the defining aspects of distributed computing {% cite note-on-dc --file langs-extended-for-dist %}. A programming model for distributed systems then must either implement a strategy for handling failures or equip programmers to design their own.

Nodes can perform computation in any of the various paradigms
(imperative, functional, object-oriented, relational, and so on). The
models are not completely orthogonal. Some matters necessarily
concern both. Serialization is a communication concern that is greatly
influenced by the design of the computation language. Similar concerns
affect the means of deployment and updating systems.

Early designs of distributed programming models in the late 1970s focused on *building novel programming languages* (Eden, Argus, Emerald). As time has gone on researchers shifted towards *extending existing languages* with facilities for programming distributed system. This article explores the history of these designs and the tradeoffs to be made between the two approaches.

## Languages and Libraries

The different approaches to implementing a distributed programming model differ on the tradeoffs they offer to both language designers and users.

### Clean-slate language implementations
A straightforward approach to implementing a new language is to start from scratch. Beginning with a clean slate offers several advantages. First, the implementor has complete control (up to what they are willing and able to implement) over every aspect of the design. Second, some elements of language design are difficult to integrate with other languages. Type systems are a good example of the problem. How to combine the designs of two type systems into one that has the properties of both is an open problem. If types play a prominent role in the language than starting anew may be the only option. However, as explained below, this strategy has apparent drawbacks not only in term of implementation effort for the creator(s) but also for users.

### Extension to an existing language
Another option is to use another language as a starting point and modify that language’s implementation for your own purposes. Think of it as forking a compiler and/or runtime and then making your own modifications. An advantage of this approach is the savings in implementation effort. If the computation models coincide then the language designer only has to implement the communication model and fault-tolerance strategy. Another plus is that users of the existing language may be more likely to consider trying or adopting the new language since it is only a step away from what they already know. A downside for maintaining any fork is keeping up to date with upstream changes.

### Library
The final approach to consider is similar to extending a language, but this time doing so only by writing code in that language to create new abstractions implementing a language model. This strategy offers similar savings in implementation effort to extending a language (perhaps moreso). But a major benefit is that is significantly easier for users to use and adopt; the only new concepts they must learn are the specifics of the programming model, as opposed to other concerns such as syntax.

## Roadmap
Language designers have explored a broad spectrum of designs for distributed programming models.

### Actors
One common sense and popular approach to extending a language for
distribution is to implement the constructs of the Actor model (discussed in chapter 3). This
is the approach taken by Termite Scheme, CloudHaskell, and Scala
Actors to name a few. Doing so requires two steps: first, implementing facilities
for spawning and linking actors and sending and receiving messages; and second, fitting actor-style concurrency on top of the language’s concurrency model.


Erlang/OTP {% cite Erlang --file langs-extended-for-dist %} is a language designed with the intention of
building resilient distributed applications for operating telephony
switches. Erlang provides a simple base language and an extensive
library of facilities for distribution. Erlang/OTP fits into the
Actor model of distribution: the basic agents in a system are
processes which communicate by sending messages to each other.
Erlang/OTP stands out for the extent to which fault tolerance is
considered. Erlang programmers are encouraged to think about failure
as a routine occurrence and provides libraries for describing policies
on how to handle such failures. Chapter 3 includes a more detailed overview of Erlang.

TermiteScheme {% cite TermiteScheme --file langs-extended-for-dist %} is an extension to a Scheme
language with constructs for Erlang-style distribution. The primary
innovations of Termite are found by leveraging features of the host
language. In particular, the features of interest are macros and
continuations.

Macros allow users or library developers to design higher-level abstractions than
the actor model and treat them as first-class in the language. Macros are a very powerful tool for abstraction. They allow library authors to elevate many patterns, such as patterns of communication, to first-class constructs. A simple example is a construct for RPC implemented by TermiteScheme as a macro expanding to a send followed by a receive.

A continuation is a concrete representation of how to finish computation of a program. A helpful analogy is to the call-stack in a procedural language. The call-stack tells you, once you’ve finished the current procedure, what to do next. Likewise, a continuation tells you, once you’ve finished evaluating the current expression, what to do next. Languages with first-class continuations have a way of reifying this concept, historically named `call/cc`, an abbreviation for `call-with-current-continuation`. First-class continuations allow for simple process migration; a process can capture its continuation and use that as the behavior of a spawned
actor on another node.

In addition to supporting the classic actor style which places few if
any constraints on what messages may be sent, Haskell and Scala based
implementations leverage the host language's powerful type system to
create more structured communication patterns. Both CloudHaskell and
Akka, the successor to Scala Actors, provide *typed
  channels* between actors. For example, the type
checker will reject a program where an actor expecting to receive
numbers is instead sent a string. Anecodatally, typed actors in Akka are not commonly used. This might suggest that errors due to incorrect message types are not that serious of a concern for users.

One disadvantage of this approach of implementing the simple actor model of Erlang is that Erlang also provides an extensive support platform for creating and deploying distributed systems. Even after the Erlang model has been implemented in Scheme, it is a long road to feature-parity.

### Types

Several efforts have explored the interplay between statically typed
languages and distributed computing. Research is focused on extending functional languages like SML, Haskell, and Scala which feature relatively advanced type systems. Areas of investigation include how to integrate an existing model of distribution with a type system and how to take advantage of types to help programmers.

CloudHaskell {% cite CloudHaskell --file langs-extended-for-dist %} is an extension to Haskell.
CloudHaskell is largely designed in the mold of Erlang
style process-based actors. It offers a novel typeclass based approach for
ensuring safe serialization (as in only serializing things known to be
serializable). Typeclasses {% cite typeclasses --file langs-extended-for-dist %}  are a novel feature of Haskell’s language system that enable flexible overloading. Typeclass *instances* can be *derived automatically* {% cite deriving-typeclasses --file langs-extended-for-dist %} to reduce boilerplate. For example, the code to perform serialization and deserialization can be automatically generated for each kind of message using its definition. CloudHaskell takes the stance that the cost of communication operations should be readily apparent to the programmer. A consequence of this is that calls to the (automatically generated) serialization functions for messages must be explicitly inserted into the code. For example, in Erlang where we might write `send msg` in CloudHaskell we write `send (serialize msg)`. CloudHaskell is implemented as an extension to GHC Haskell (actually it was first implemented as a library then later on the features they needed were added as extensions to GHC).

The fact that CloudHaskell allows concurrency within an actor demonstrates the separation between computation and communication models. That is, in CloudHaskell a single process might internally be implemented by a group of threads. To the rest of the system this fact is completely opaque (a good thing).

CloudHaskell also takes a stance against “everything is serializable”, for example mutable reference cells should not be. This makes serializing functions (closures) tricky because it is not apparent how to tell if a closure’s environment is serializable. To solve this, CloudHaskell uses *static pointers* and forces closures to use pre-serialized environments. Pre-serialization means that a closure is a pair of a closed expression and a byte string representing the environment; presumably the first code the closure will execute when invoked is to deserialize the environment to retrieve the proper information.

ML5 {% cite ML5 --file langs-extended-for-dist %} is an extension to
the SML {% cite sml --file langs-extended-for-dist %} programming language. ML5 uses the notion of
*location* and *movability*. The type system keeps track
of the locations (nodes) in the system, which location each piece of
the program is, and what can and cannot be moved between locations. As
a result, the system is able to detect unpermitted attempts to access a resource. The ML5 type system cleanly integrates with the ML type system. ML5 supports type inference, a tricky but fundamental feature of SML.

Though applicable to distributed systems in general, the presentation of ML5 focuses in particular on client-server interactions, and more specifically on those between a web front-end and back-end. The ML5 compiler is able to generate Javascript code that executes in-browser.

An example of some ML5 code (from {% cite ML5 --file langs-extended-for-dist %}) follows:

```
extern javascript world home
extern val alert : string -> unit @ home
do alert [Hello, home!]
```

This snippet declares a location in the system called `home` that can execute Javascript code. Additionally, there is a function named `alert` that can be used from the location `home` (defined through an interface to plain Javascript). The last line is an example of calling the `alert` function with the string `”Hello, home!”` (yes, strings are in brackets).

A slightly more complex example (again from {% cite ML5 --file langs-extended-for-dist %}) demonstrates movement between locations:
```
extern bytecode world server
extern val server : server addr @ home
extern val version : unit -> string @ server
extern val alert : string -> unit @ home
do alert (from server get version ())
```
This example features two locations (worlds), the default `home` location and one named `server`. As before, we can call `alert` from `home`, but now we can also call `version` on `server`. Locations access one another using addresses; the declaration of `server` as a `server addr @ home` says that the home location knows the address of the `server` location and can therefore access `version`.

ML5 does not consider fault-tolerance. For the web front/back-end examples this is perhaps not too big of an issue. Still, the absence of a compelling strategy for handling failures is a shortcoming of the design. Since `home` is the default location, the same way that `main` is the default entry point for C programs, this program typechecks. An error would be raised if the `alert` function was called from a different location.

AliceML {% cite Alice --file langs-extended-for-dist %} is an
example of another extension to SML. AliceML leverages SML's advanced module
system to explore building *open* distributed systems. Open
systems are those where each node is only loosely coupled to its
peers, meaning it allows for dynamic update and replacements. AliceML
enables this by forcing components to program to interfaces and
dynamically type-checking components as they enter the system.

### Objects
Object-Oriented languages have been extended for distribution in
various fashions. Objects are an appealing model for agents in a
distributed system. Indeed, Alan Kay's metaphor of objects as
miniature computers and method invocation as message passing
{% cite smalltalkHistory --file langs-extended-for-dist %} seems directly evocative of distributed
systems.

Eden {% cite Eden --file langs-extended-for-dist %} was an early pioneer (the project began in 1979) in
both distributed and object-oriented programming languages. In fact,
Eden can be classified as a language extended for distribution: Eden
applications “were written in the Eden Programming Language (EPL) — a
version of Concurrent Euclid to which the Eden team had added
support for remote object invocation” {% cite bhjl07 --file langs-extended-for-dist %}. However, Eden
did not take full advantage of the overlap (namely, objects) between
the computation and distribution models.

See Chapter 4 for a more extensive overview of the languages using an object-based model for distribution, such as Emerald, Argus, and E.

### Batch Processing
Another common extension is in the domain of batch processing
large-scale data. MapReduce (and correspondingly Hadoop) is the landmark example of a programming model for distributed batch processing. Essentially, batch processing systems present a restricted programming model. For example, MapReduce programs must fit into the rigid model of two-step produce then aggregrate. A restricted model alllows the system to make more guarantees, such as for fault tolerance. Subsequently language designers have sought to increase the expressiveness of the programming models and to boost performance. Chapter 8 covers batch processing languages in more detail.

MBrace {% cite MBrace --file langs-extended-for-dist %} is an extension to the F# programming language for writing compuations for clusters. MBrace provides a *monadic* interface (point to something about monads here) which allows for building cluster jobs out of smaller jobs while still exploiting available parallelism. MBrace is a framework that features its own runtime for provisioning, scheduling, and monitoring nodes in a cluster.

Batch processing systems offer an interesting take on how to handle
fault tolerance. The common approach taken is to use a central
coordinator (for example, on the machine that initiated the job) to
detect the failure of nodes. By tracking what each other node in the
system is doing, the coordinator can restart a task on failure.

### Consistency

Several languages explore designs for ensuring the *consistency* of distributed applications, or the requirement that each node agree on some state. CRDTs are a family of distributed data structures that maintain consistency. Chapter 6 explains consistency and CRDTS in further detail while chapter 7 takes a closer look at the following languages.

Dedalus {% cite Dedalus --file langs-extended-for-dist %} and Bloom {% cite Bloom --file langs-extended-for-dist %} both represent uses of a logic-programming based attempt to design languages providing consistency guarantees. Dedalus is meant to provide the underlying model of distribution while Bloom provides a high-level language intended to be usable for creating applications. Logic-programming is an attractive model because execution is order-independent. Using Datalog, a logic-programming language, as the computation model encourages programmers to develop applications that are agnostic to message-reorderings. Bloom is implemented as a Ruby library BUD.

Lasp {% cite Lasp --file langs-extended-for-dist %} is a language model where CRDTs are the only distributed data. CRDT sets are the primary data structure and Lasp programs are built by composing set transformations such as maps, filters, and folds.

Lasp is implemented as an Erlang library. In practice, applications using Lasp are free to use other forms of distributed data, but consistency is only promised for the library-provided tools. Lasp nodes then share the same fault-tolerance platform as Erlang applications.

Lasp’s programming model is very restrictive; sets are the primary data structure and folding operations. Future work may show how to enrich the programming model while still making the same strong consistency guarantees.

### Tuplespaces
Linda {% cite Linda --file langs-extended-for-dist %} is a distributed programming model more in the vein of shared memory than message passing. Linda programs are a collection of processes and a shared *tuplespace*. The tuplespace holds an unordered collection of tuples. A process adds data to the tuplespace using the `out` form. The `in` form takes a *pattern* and removes and returns a tuple matching the pattern from the tuplespace, blocking until one such appears.

A simple example demonstrating communication in Linda:

```
;; INITIALLY the tuplespace is empty
;; Process A
out (“Hello”, “from process A”);

;; after Process A executes the tuplespace contains one record, (“Hello”, “from process A”)

;; Process B
in(“Hello”, x);
;; x = “from process A”
;; the tuplespace is empty again
```

If the tuplespace was not empty but instead contained tuples of some for *besides* 2-entry tuples where the first element was the string `”Hello”` the above interaction would remain unchanged. However, if some process C had entered the tuple `(“Hello”, “I am process C”)` then
B would receive either A’s or B’s tuple with one of the tuples remaining in the tuplespace.

The Linda model of distribution has several advantages. Linda processes are not only spatially decoupled (able to execute on different machines, as in actor implementations) but *temporally* decoupled as well. That is, a Linda process can communicate with other processes even after it exits! Tuples remain in the shared space even after the process that created them exits. Therefore a different process can receive those tuples at any point in the future. Another point is that Linda processes don’t need to know the identities of the other process it communicates with. Unlike actors, which in order to send a message need to know the address of the other actor’s mailbox, Linda processes operate entirely through their connection to the tuplespace. Processes need to “know exactly as much about one another as is appropriate for the programming situation at hand” {% cite Linda --file langs-extended-for-dist %}.

Linda is agnostic to the internal computation language of each node. Implementations of tuplespaces have been built on top of C and Fortran as well as a little-used Java one named JavaSpaces. (There is reportedly at least one financial institution in the UK that has some JavaSpaces-based systems). The choices of C and Fortran may be why Linda did not gain more popularity. Both languages are low-level and not well-suited for creating new abstractions (`void*` is just about the only abstraction mechanism in C).

Maintaining the consistency of the tuplespace is of paramount importance for Linda implementations. Another concern is the detection of process crashes. Unfortunately, presentations of Linda have not clearly addressed these concerns.

## Discussion

The line between a language and a library can be extremely blurry
{% cite LanguagesAsLibraries --file langs-extended-for-dist %}. A language provides some building blocks
and forms for combining and composing {% cite 700pl --file langs-extended-for-dist %}. For example, numbers, strings, and Booleans are common primitive building blocks. Operations like addition, concatenation, and negation offer ways of combining such blocks. More interesting operations allow *abstraction* over parts of the language: function (or λ) abstraction allows for creating operations over all numbers. Objects provide a way of combining data and functions in a way that abstracts over particular implementation details. Most importantly, a language
defines the *semantics*, or meaning, of such operations.

Many libraries can
be described in the same way. The first-order values provided by a
library are the primitives while the provided functions, classes, or objects perform
combination and composition. A library can implement the primitives
and operations such that they are in correspondence with the forms and semantics defined by a language.

A theme in the literature is presenting an idea as a language and
implementing it as a library or extension to an existing language.
Doing so allows the authors to analyze a minimal presentation of their
idea, but enjoy the benefits of the library/extension appraoch. Both Linda and Lasp take this approach, for example.

Language models benefit from implementations {% cite Redex --file langs-extended-for-dist %}. The
reasons to implement a new distributed language model on top of
existing work are abundant:

* As mentioned above, a distributed language includes both a model
  for single-node computation as well as inter-node communication.
  Building a distributed language from scratch also means
  re-implementing one of the paradigms of computing, and we would rather re-use existing language implementations

* Implementing real-world applications calls for models of many
  domains besides computation and communication, such as persistence
  and parsing. The availability of a rich repository of libraries is
  an important concern for many users in adopting a new technology
  {% cite socioPLT --file langs-extended-for-dist %}.

* Many applications of distributed systems are extremely
  performance sensitive. Performance engineering and fine-tuning are
  time and labor intensive endeavors. It makes sense to re-use as much
  of the work in existing language ecosystems as possible.

These reasons form the foundation of an argument in favor of general-purpose programming languages that allow for the creation of rich abstractions. Such a language can be adapted for different models of computation. (Although, most general-purpose languages have a fixed computation model such as functional or object-oriented). When models are implemented as libraries in a common language, users can mix-and-match different models to get exactly the right behavior where it is needed by the application.

One can argue that one reason the Linda model failed to catch on in iis that the primary implementations were extensions to C and Fortran. While general-purpose, C and Fortran suffer a paucity of options for creating abstractions.

That being said, there are advantages to clean slate languages. A fresh start grants the designer full control over every part of the language. For some areas, such as novel type systems, this is almost a necessity. However, we have seen designs like ML5 that elegantly integrate with a base language's type system. Finally, a language designer can put their new ideas center stage, easily allowing people to see what is new and cool; in time those ideas may spread to other languages.

Erik Meijer points out in {% cite salesman --file langs-extended-for-dist %} that programmers don't jump to new techonologies to access new features. Rather, in time those features make their way to old technologies. Examples abound, such as the arrival of λ in Java and of course all of Meijer's work in C# and Visual Basic.

Ideas from distributed programming models have influenced more than just the languages used in practice. Microservices {% cite microservices --file langs-extended-for-dist %} are a popular technique for architecting large systems as a collection of manageable components. Microservices apply the lessons learned from organizing programs
around actors to organizing the entire system. Actor programming uses
shared-nothing concurrent agents and emphasizes fault-tolerance.
Building a system using microservices means treating an entire block
of functionality as an actor: it can exchange messages with the other
components, but it can also go on and offline (or crash) independent
from the rest of the system. The result is more resilient and modular.

## Conclusion

All design lies on a spectrum of tradeoffs; to gain convenience in one
area means to sacrifice in another. Distributed systems come with a
famous trade off: the CAP theorem. Building new language models on top
of an existing, flexible general-purpose language is an attractive
option for both implementors and users.

## References

{% bibliography --file langs-extended-for-dist %}