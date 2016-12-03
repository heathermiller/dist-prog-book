---
layout: page
title:  "Message Passing and the Actor Model"
by: "Nathaniel Dempkowski"
---

# Introduction

In the field of message passing programming models, it is not only important to consider recent state of the art research, but additionally the historic initial papers on message passing and the actor model that are the roots of the programming models described in newer papers. Message passing programming models have strong roots in computer science, and have essentially been discussed since the advent of object-oriented programming with Smalltalk in the 1980's. It is enlightening to see which aspects of the models have stuck around, and many of the newer papers reference and address deficiencies present in older papers. There have been plenty of programing languages designed around message passing, including those focused on the actor model of programming and organizing units of computation.

Message passing programming models are continuing to develop and become more robust, as some of the recently published papers and systems in the field show. Orleans gives an example of this, detailing not just a programming model, but a runtime system that is a quite advanced implementation of a message passing and actor model to solve real world problems.
The important question to ask about these sources is “Why message passing?” There are a number of distributed programming models, so why was this one so important when it was initially proposed. What are the advantages of it for the programmer? Why has it facilitated advanced languages, systems, and libraries that are widely used today?

# Original Proposal of the Actor Model

# Classic Actor Model

The classic actor model came about with the formalization of an actor as a unit of computation that implements the following primitives:
* `create`: create an actor from a behavior description and a set of parameters, including other existing actors
* `send`: send a message to another actor
* `become`: have an actor replace their behavior with a new one

"The sequential subset of actor systems that implement this model is typically functional. Changes to the state of an actor are aggregated in a single become statement. Actors have a flexible interface that can similarly be changed by switching the behaviour of that actor." (43 Years of Actors)

If you squint a little, this actor definition sounds similar to Alan Kay’s original definition of Object Oriented programming. This definition describes a system where objects have a behavior, their own memory, and communicate by sending and receiving messages that may contain other objects or simply trigger actions.

This

## Concurrent Object-Oriented Programming (1990)

This is a seminal paper for the classic actor model, as it offers classic actors as a natural solution to solving problems at the intersection of two trends of computing: increased distributed computing resources and the rising popularity of object-oriented programming. The paper defines common patterns of parallelism: pipeline concurrency, divide and conquer, and cooperative problem solving. It then focuses on how the actor model can be used to solve these problems in an object-oriented style, and some of the challenges that arise with distributed actors and objects, as well as strategies and tradeoffs for communication and reasoning about behaviors.

This paper looks at a lot of systems and languages that are implementing solutions in this space, and starts to actually identify some of the programmer-centric advantages of actors. The author claims the benefits of using objects stem from a separation of concerns. "By separating the specification of what is done (the abstraction) from how it is done (the implementation), the concept of objects provides modularity necessary for programming in the large. It turns out that concurrency is a natural consequence of the concept of objects." (Agha, September, 1990) Splitting concerns into multiple pieces allows for the programmer to have an easier time reasoning about the behavior of the program. It also allows the programmer to use more flexible abstractions in their programs, as Agha states. “It is important to note that the actor languages give special emphasis to developing flexible program structures which simplify reasoning about programs.” (Agha, September, 1990) This flexibility turns out to be a highly discussed concern that many of the later papers make a point to mention.

## Rosette

## Akka

Akka is an actively developed project built out of the work on [Scala Actors](#scala-actors) in Scala to provide the actor model of programming as a framework to Java and Scala. It makes an effort to bring an industrial-strength actor model to the JVM runtime, which was not explicitly designed to support actors.

# Process-based Actor

The process-based actor model is essentially an actor modelled as a process that runs from start to completion. These actors use a `receive` primitive to specify messages that an actor can receive during a given state. If a message is matched, corresponding code is evaluated, but otherwise the actor simply blocks until it gets a message that it knows how to handle. Depending on the language implementation `receive` might specify an explicit message type or perform some pattern matching on message values. Erlang's implementation of process-based actors gets to the core of what it means to be a process-based actor.

## Erlang

Erlang was the primary driver of the process-based actor model, originally developing it to program large highly-reliable fault-tolerant telecommunications switching systems. This model was essentially developed independently from other actor systems and research. (It would be nice to have more details here, to emphasize how this actor model independently organically arose from some of the core needs of distributed systems)

Erlang actors run as lightweight isolated processes. They do not have visibility into one another, and pass around pure messages, which are immutable. These have no dangling points or data references between objects, and really enforce the idea of immutable separated data between actors unlike many of the classic actor implementations in which references to actors and data can be passed around freely.

TODO: mention disadvantages of Erlang's `receive`

Erlang also seeks to build failure into the programming model, as one of the core assumptions of a distributed system is that things are going to fail. Erlang provides the ability for processes to monitor one another through two primitives:

* `monitor`: one-way unobtrusive notification of process failure/shutdown
* `link`: two-way notification of process failure/shutdown allowing for coordinated termination

These primitives can be used to construct complex hierarchies of supervision that can be used to handle failure in isolation, rather than failures impacting your entire system. Supervision hierarchies are notably almost the only scheme for fault-tolerance that exists in the world of actors. Almost every actor system that is used to build distributed systems takes a similar approach, and it seems to work. (Example of Erlang reliability or something would be good here)

## Scala Actors

Scala Actors brings lightweight Erlang-style message-passing concurrency to the JVM and integrates it with the heavyweight thread/process concurrency models. This is stated well in the original paper about Scala Actors as "an impedance mismatch between message-passing concurrency and virtual machines such as the JVM." The authors say that VMs usually map threads to heavyweight processes, but that a lightweight process abstraction reduces programmer burden and leads to more natural abstractions. The authors say that “The user experience gained so far indicates that the library makes concurrent programming in a JVM-based system much more accessible than previous techniques.”

The realization of this model depends on efficiently multiplexing actors to threads. This technique was originally developed in Scala actors, and later was adopted by Akka. This integration allows for Actors to invoke methods that block the underlying thread in a way that doesn't prevent actors from making process. This is important to consider in an event-driven system where handlers are executed on a thread pool, because the underlying event-handlers can't block threads without risking thread pool starvation. (I feel like there needs to be a better concluding point to this)

In addition to the more natural abstraction, the Erlang model is further enhanced with Scala's type system and advanced pattern-matching capabilities.

# Communicating event-loops

The communicating event-loop model was introduced in the E language, and is similar to process actors, but doesn't make a distinction between passive and active objects.

## E Language

The E language implements a model that is closer to imperative object-oriented programming. Within a single actor-like node of computation called a "vat" many objects are contained.

## AmbientTalk

# Active Objects

Active object actors draw a distinction between two different types of objects: active and passive objects. Every active object has a single entry point defining a fixed set of messages that are understood. Passive objects are the objects that are actually sent between actors, and are copied around to guarantee isolation.

## ABCL/1 Language

## Orleans

# Why the actor model?

The actor programming model offers benefits to programmers of distributed systems by allowing for easier programmer reasoning about behavior, providing a lightweight concurrency primitive that naturally scales across many machines, and enabling looser coupling among components of a system allowing for change without service disruption. Actors enable a programmer to easier reason about their behavior because they are at a fundamental level isolated from other actors.  When programming an actor, the programmer only has to worry about the behavior of that actor and the messages it can send and receive. This alleviates the need for the programmer to reason about an entire system. Instead the programmer has a fixed set of concerns, meaning they can ensure behavioral correctness in isolation, rather than having to worry about an interaction they hadn’t anticipated occurring. Actors provide a single means of communication (message-passing), meaning that a lot of concerns a programmer has around concurrent modification of data are alleviated. Data is restricted to the data within a single actor and the messages it has been passed, rather than all of the accessible data in the whole system.

Actors are lightweight, meaning that the programmer usually does not have to worry about how many actors they are creating. This is a contrast to other fundamental units of concurrency like threads or processes, which a programmer has to be acutely aware of, as they incur high costs of creation, and quickly run into machine resource and performance limitations. Haller (2009) says that without a lightweight process abstraction, burden is increased on the programmer to write their code in an obscured style (Philipp Haller, 2009). Unlike threads and processes, actors can also easily be told to run on other machines as they are functionally isolated. This cannot traditionally be done with threads or processes, as they are unable to be passed over the network to run elsewhere. Messages can be passed over the network, so an actor does not have to care where it is running as long as it can send and receive messages. They are more scalable because of this property, and it means that actors can naturally be distributed across a number of machines to meet the load or availability demands of the system.

Finally, because actors are loosely coupled, only depending on a set of input and output messages to and from other actors, their behavior can be modified and upgraded without changing the entire system. For example, a single actor could be upgraded to use a more performant algorithm to do its work, and as long as it can process the same input and output messages, nothing else in the system has to change. This isolation is a contrast to methods of concurrent programming like remote procedure calls, futures, and promises. These models emphasize a tighter coupling between units of computation, where a process may call a method directly on another process and expect a specific result. This means that both the caller and callee (receiver of the call) need to have knowledge of the code being run, so you lose the ability to upgrade one without impacting the other. This becomes a problem in practice, as it means that as the complexity of your distributed system grows, more and more pieces become linked together. Agha (1990) states, “It is important to note that the actor languages give special emphasis to developing flexible program structures which simplify reasoning about programs.” This is not desirable, as a key characteristic of distributed systems is availability, and the more things are linked together, the more of your system you have to take down or halt to make changes/upgrades. Actors compare favorably to other concurrent programming primitives like threads or remote procedure calls due to their low cost and loosely coupled nature. They are also programmer friendly, and ease the programmer burden of reasoning about a distributed system.

# Modern usage in production

It is important when reviewing models of programming distributed systems not to look just to academia, but to see which of these systems are actually used in industry to build things. This can give us insight into which features of actor systems are actually useful, and the trends that exist throughout these systems.

_On the Integration of the Actor Model into Mainstream Technologies_ by Philipp Haller provides some insight into the requirements of an industrial-strength actor implementation on a mainstream platform. These requirements were drawn out of an initial effort with [Scala Actors](#scala-actors) to bring the actor model to mainstream software engineering, as well as lessons learned from the deployment and advancement of production actors in [Akka](#akka).

* _Library-based implementation_: It is not obvious which concurrency abstraction wins in real world cases, and different concurrency models might be used to solve different problems, so implementing a concurrency model as a library enables flexibility in usage.
* _High-level domain-specific language_: A domain-specific language or something comparable is a requirement to compete with languages that specialize in concurrency, otherwise your abstractions are lacking in idioms and expressiveness.
* _Event-driven implementation_: Actors need to be lightweight, meaning they cannot be mapped to an entire VM thread or process. For most platforms this means an event-driven model.
* _High performance_: Most industrial applications that use actors are highly performance sensitive, and high performance enables more graceful scalability.
* _Flexible remote actors_: Many applications can benefit from remote actors, which can communicate transparently over the network. Flexibility in deployment mechanisms is also very important.

These attributes give us a good basis for analyzing whether an actor system can be successful in production. These are attributes that are necessary, but not sufficient for an actor system to be useful in production.

## Actors as a framework

One trend that seems common among the actor systems we see in production is extensive environments and tooling. I would argue that Akka, Erlang, and Orleans are the primary actor systems that see real production use, and I think the reason for this is that they essentially act as frameworks where many of the common problems of actors are taken care of for you. This allows the programmer to focus on the problems within their domain, rather than the common problems of monitoring, deployment, and composition.

Akka and Erlang provide modules that you can piece together to build various pieces of functionality into your system. Akka provides a huge number of modules and extensions to configure and monitor a distributed system built using actors. They provide a number of utilities to meet common use-case and deployment scenarios, and these are thoroughly listed and documented. Additionally they provide support for Akka Extensions, which are a mechanism for adding your own features to Akka. These are powerful enough that some core features of Akka like Typed Actors or Serialization are implemented as Akka Extensions. Erlang provides the Open Telecom Platform (OTP), which is a framework comprised of a set of modules and standards designed to help build applications. OTP takes the generic patterns and components of Erlang, and provides them as libraries that enable code reuse and best practices when developing new systems.

### Module vs. Runtime approaches to tooling

Both Akka and Erlang take a module-based approach to tooling around their actor systems. The Orleans framework goes in another direction, instead providing an TODO: finish this thought


# References

{% bibliography --file message-passing %}
