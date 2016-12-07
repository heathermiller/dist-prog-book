---
layout: page
title:  "Message Passing and the Actor Model"
by: "Nathaniel Dempkowski"
---

# Introduction

In the field of message passing programming models, it is not only important to consider recent state of the art research, but additionally the historic initial papers on message passing and the actor model that are the roots of the programming models described in newer papers. Message passing programming models have strong roots in computer science, and have essentially been discussed since the advent of object-oriented programming with Smalltalk in the 1980's. It is enlightening to see which aspects of the models have stuck around, and many of the newer papers reference and address deficiencies present in older papers. There have been plenty of programing languages designed around message passing, including those focused on the actor model of programming and organizing units of computation.

Message passing programming models are continuing to develop and become more robust, as some of the recently published papers and systems in the field show. Orleans gives an example of this, detailing not just a programming model, but a runtime system that is a quite advanced implementation of a message passing and actor model to solve real world problems.

The important question to ask about these sources is “Why message passing?” There are a number of distributed programming models, so why was this one so important when it was initially proposed. What are the advantages of it for the programmer? Why has it facilitated advanced languages, systems, and libraries that are widely used today?

# Original proposal of the actor model

The actor model was originally proposed in _A Universal Modular ACTOR Formalism for Artificial Intelligence_ in 1973 as a method of computation for artificial intelligence research. The original goal of the model was to model parallel communication while safely exploiting distributed concurrency across workstations. The paper makes few presumptions about implementation details, instead defining the high-level message passing communication model.

They define actors as units of computation. These units can send messages to one another, and have a mailbox which contains messages they have received. These messages are of the form `(request: <message-to-target>; reply-to: <reference-to-messenger>)`.

Actors attempt to process messages from their mailboxes by matching their `request` field sequentially against patterns or rules which can be specific values or logical statements. When a pattern is matched, computation occurs and the result of that computation is implicitly returned to the reference in the message's `reply-to` field. This is a continuation, where the continuation is another message to an actor. These messages are one-way and make no claims about whether a message will ever be received in response. This model is limited, but the early ideas of taking advantage of distribution of processing power to enable greater parallel computation are there.

One interesting thing to note is that this original paper talks about actors in the context of hardware. They mention actors as almost another machine architecture. This paper describes the concepts of an "actor machine" and a "hardware actor" as the context for the actor model, which is totally different from the way we think about modern actors as abstracting away a lot of the hardware details we don't want to deal with. This concept reminds me of something like a Lisp machine, but built to specially utilize the actor model of computation for artificial intelligence.

# Classic actor model

The classic actor model came about with the formalization of an actor as a unit of computation in Agha's _Concurrent Object-Oriented Programming_. The classic actor is formalized as the following primitive actions:

* `create`: create an actor from a behavior description and a set of parameters, including other existing actors
* `send`: send a message to another actor
* `become`: have an actor replace their behavior with a new one

As originally described, classic actors communicate by asynchronous message passing. They are a primitive independent unit of computation which can be used to build higher-level abstractions for concurrent programming. Actors are unique addressable, and have their own independent message queues. State changes using the classic actor model are specified using the `become` operation. Each time an actor processes a communication it computes a behavior in response to the next type of communication it expects to process. A `become` operation's argument is another named behavior with some state to pass to that named behavior.

For purely functional actors the new behavior would be identical to the original. For more complex actors however, this enables the aggregation of state changes at a higher level of granularity than something like a variable assignment. This isolation changes the level at which one analyzes a system, freeing the programmer from worrying about interference during state changes.

TODO: Not sure where this quote fits in? Maybe worth just pull-quoting it or taking it out as most of the points this hits on are better explained above.

"The sequential subset of actor systems that implement this model is typically functional. Changes to the state of an actor are aggregated in a single become statement. Actors have a flexible interface that can similarly be changed by switching the behaviour of that actor." (43 Years of Actors)

If you squint a little, this actor definition sounds similar to Alan Kay’s original definition of Object Oriented programming. This definition describes a system where objects have a behavior, their own memory, and communicate by sending and receiving messages that may contain other objects or simply trigger actions. The focus is on the messaging and designing the interactions and communications between the objects.

TODO: write more here

## Concurrent Object-Oriented Programming (1990)

This is a seminal paper for the classic actor model, as it offers classic actors as a natural solution to solving problems at the intersection of two trends of computing: increased distributed computing resources and the rising popularity of object-oriented programming. The paper defines common patterns of parallelism: pipeline concurrency, divide and conquer, and cooperative problem solving. It then focuses on how the actor model can be used to solve these problems in an object-oriented style, and some of the challenges that arise with distributed actors and objects, as well as strategies and tradeoffs for communication and reasoning about behaviors.

This paper looks at a lot of systems and languages that are implementing solutions in this space, and starts to actually identify some of the programmer-centric advantages of actors. The author claims the benefits of using objects stem from a separation of concerns. "By separating the specification of what is done (the abstraction) from how it is done (the implementation), the concept of objects provides modularity necessary for programming in the large. It turns out that concurrency is a natural consequence of the concept of objects." (Agha, September, 1990) Splitting concerns into multiple pieces allows for the programmer to have an easier time reasoning about the behavior of the program. It also allows the programmer to use more flexible abstractions in their programs, as Agha states. “It is important to note that the actor languages give special emphasis to developing flexible program structures which simplify reasoning about programs.” (Agha, September, 1990) This flexibility turns out to be a highly discussed concern that many of the later papers make a point to mention.

## Rosette

Rosette was both a language for concurrent object-oriented programming of actors, as well as a runtime system for managing the usage of and access to resources by those actors. Rosette is mentioned throughout Agha's _Concurrent Object-Oriented Programming_, and the code examples given in the paper are written in Rosette. It is important to mention as it seems to be a language which almost defines what the classic actor model looks like in the context of concurrent object-oriented programming.

The motivation behind Rosette was to provide strategies for dealing with problems like search, where the programmer needs a means of control over how resources are allocated to sub-computations to optimize performance in the face of combinatorial explosion. This supports the use of concurrency in solving computationally intensive problems whose structure is not statically defined. Rosette has an architecture which uses actors in two distinct ways. They describe two different layers with different responsibilities:

* _Interface layer_: This implements mechanisms for monitoring and control of resources. The system resources and hardware are viewed as actors.
* _System environment_: This is comprised of actors who actually describe the behavior of concurrent applications and implement resource management policies based on the interface layer.

The Rosette language features, many of which we take for granted in object-oriented programming languages. It implements dynamic creation and modification of objects for extensible and reconfigurable systems, supports inheritance, and has objects which can be organized into classes. I think the more interesting characteristic is that the concurrency in Rosette is inherent and declarative rather than explicit as with many modern object-oriented languages. The motivation behind this declarative concurrency comes from the heterogeneous nature of distributed concurrent computers. Different computers have varying concurrency characteristics, and the authors argue that forcing the programmer to tailor their concurrency to the machine makes it difficult to re-map a program to another one. I think this idea of using actors as a more flexible and natural abstraction is an important one which is seen in some form within many of the actor systems described here.

Actors in Rosette are organized into three types of classes which describe different aspects of the actors within the system:

* _Abstract classes_ specify requests, responses, and actions within the system which can be observed. The idea behind these is to expose the higher-level behaviors of the system, but tailor the actual actor implementations to the resource constraints of the system.
* _Representation classes_ specify the resource management characteristics of implementations of abstract classes.
* _Behavior classes_ specify the actual implementations of actors in given abstract and representation classes.

These classes represent a concrete object-oriented abstraction to organize actors which handles the practical constraints of a distributed system. It represents a step in the direction of handling not just the information flow and behavior of the system, but the underlying hardware and resources. Rosette's model feels like a direct expression of those concerns which are something every actor system in production inevitably ends up addressing.

## Akka

Akka is an actively developed project built out of the work on [Scala Actors](#scala-actors) in Scala to provide the actor model of programming as a framework to Java and Scala. It makes an effort to bring an industrial-strength actor model to the JVM runtime, which was not explicitly designed to support actors. There are a few notable changes from Scala Actors that make Akka worth mentioning, especially as it is being actively developed while Scala Actors is not.

Akka provides a programming interface with both Java and Scala bindings for actors which looks similar to Scala Actors, but has different semantics in how it processes messages. Akka's `receive` operation defines a global message handler which doesn't block on the receipt of no matching messages, and is instead only triggered when a matching message can be processed. It also will not leave a message in an actor's mailbox if there is no matching patter to handle the message. The message will simply be discarded an an event will be published to the system. Akka's interface also provides stronger encapsulation to avoid exposing direct references to actors. To some degree this fixes problems in Scala Actors where public methods could be called on actors, breaking many of the guarantees programmers expect from message-passing. This system is not perfect, but in most cases it limits the programmer to simply sending messages to an actor using a limited interface.

The Akka runtime also provides advantages over Scala Actors. The runtime uses a single continuation closure for many or all messages an actor processes, and provides methods to change this global continuation. This can be implemented more efficiently on the JVM, as opposed to Scala Actors' continuation model which uses control-flow exceptions which cause additional overhead. Additionally, nonblocking message insert and task schedule operations are used for extra performance.

Akka is the production-ready result of the classic actor model lineage. It is actively developed and actually used to build scalable systems.

# Process-based actors

TODO: better opening sentence

The process-based actor model is essentially an actor modeled as a process that runs from start to completion.

The first language to explicitly implement this model is Erlang, and they even say in a retrospective that their view of computation is broadly similar to the Agha's classic actor model. However, with process-based actors different mechanics are used.

Process-based actors are defined by a computation which runs from start to completion, rather than the classic actor model, which defines an actor almost as a state machine of behaviors and the logic to transition between those. Similar state-machine like expressions are possible through recursion, but programming those feels fundamentally different than using the previously described `become` statement.

These actors use a `receive` primitive to specify messages that an actor can receive during a given state/point in time. If a message is matched, corresponding code is evaluated, but otherwise the actor simply blocks until it gets a message that it knows how to handle. Depending on the language implementation `receive` might specify an explicit message type or perform some pattern matching on message values.

Erlang's implementation of process-based actors gets to the core of what it means to be a process-based actor.

## Erlang

Erlang was the primary driver of the process-based actor model. This model was originally developed to program large highly-reliable fault-tolerant telecommunications switching systems. Erlang's development started in 1985, but its model of programming is still used today. The motivations of the Erlang model were around four key properties that were needed to program fault-tolerant operations:

* Isolated processes
* Pure message passing between processes
* Detection of errors in remote processes
* The ability to determine what type of error caused a process crash

The Erlang researchers initially believed that shared-memory was preventing fault-tolerance and they saw message-passing of immutable data between processes as the solution to avoiding shared-memory. This model was essentially developed independently from other actor systems and research, especially as its development was started before Agha's classic actor model formalization was even published, but it ends up with a broadly similar view of computation to Agha's classic actor model.

Erlang actors run as lightweight isolated processes. They do not have visibility into one another, and pass around pure messages, which are immutable. These have no dangling pointers or data references between objects, and really enforce the idea of immutable separated data between actors unlike many of the early classic actor implementations in which references to actors and data can be passed around freely.


TODO: is it really worth mentioning `receive` again here? I think its assumed that the `receive` semantics above apply here?

Erlang implements a blocking `receive` operation as a means of processing messages from a processes' mailbox.

Erlang also seeks to build failure into the programming model, as one of the core assumptions of a distributed system is that things are going to fail. Erlang provides the ability for processes to monitor one another through two primitives:

* `monitor`: one-way unobtrusive notification of process failure/shutdown
* `link`: two-way notification of process failure/shutdown allowing for coordinated termination

These primitives can be used to construct complex hierarchies of supervision that can be used to handle failure in isolation, rather than failures impacting your entire system. Supervision hierarchies are notably almost the only scheme for fault-tolerance that exists in the world of actors. Almost every actor system that is used to build distributed systems takes a similar approach, and it seems to work. (Example of Erlang reliability or something would be good here)

## Cloud Haskell

Cloud Haskell is an extension/DSL of Haskell which essentially implements an enhanced version of the computational message-passing model of Erlang in Haskell. It enhances Erlang's model with advantages from Haskell's model of functional programming in the form of purity, types, and monads. Cloud Haskell enables the use of pure functions for remote computation, which means that these functions are idempotent and can be restarted or run elsewhere in the case of failure without worrying about side-effects or undo mechanisms. One of the largest improvements over Erlang is the introduction of typed channels for sending messages. These provide guarantees to the programmer about the types of messages their actors can handle, which is something Erlang lacks. Cloud Haskell processes can use multiple typed channels to pass messages between actors, rather than Erlang's single untyped channel. Monadic types make it possible for programmers to use an effective style, where they can ensure that pure and effective code are not mixed. Additionally, Cloud Haskell has shared memory within an actor process, which is useful for certain applications, but forbidden by the type system from being shared across actors. Finally, Cloud Haskell allows for the serialization of function closures, which means that higher-order functions can be distributed across actors. These improvements over Erlang make Cloud Haskell a notable project in the space of process-based actors.

## Scala Actors

Scala Actors brings lightweight Erlang-style message-passing concurrency to the JVM and integrates it with the heavyweight thread/process concurrency models. This is stated well in the original paper about Scala Actors as "an impedance mismatch between message-passing concurrency and virtual machines such as the JVM." The authors say that VMs usually map threads to heavyweight processes, but that a lightweight process abstraction reduces programmer burden and leads to more natural abstractions. The authors say that “The user experience gained so far indicates that the library makes concurrent programming in a JVM-based system much more accessible than previous techniques.”

The realization of this model depends on efficiently multiplexing actors to threads. This technique was originally developed in Scala actors, and later was adopted by Akka. This integration allows for Actors to invoke methods that block the underlying thread in a way that doesn't prevent actors from making process. This is important to consider in an event-driven system where handlers are executed on a thread pool, because the underlying event-handlers can't block threads without risking thread pool starvation. (I feel like there needs to be a better concluding point to this)

In addition to the more natural abstraction, the Erlang model is further enhanced with Scala's type system and advanced pattern-matching capabilities.

# Communicating event-loops

The communicating event-loop model was introduced in the E language, and is similar to process actors, but doesn't make a distinction between passive and active objects.

TODO: what does that sentence really mean? need a better introduction to this model. Could add more about AmbientTalk in the intro? If this is too expanded its going to be repeating the same idea of accessing objects within actors 3 times though.

## E Language

The E language implements a model that is closer to imperative object-oriented programming. Within a single actor-like node of computation called a "vat" many objects are contained. This vat contains not just objects, but a mailbox for all of the objects inside, as well as a call stack. There is a shared message queue and event-loop that acts as one abstraction barrier for computation. The actual references to objects within a vat which are used for communication and computation across actors operate at a different level of abstraction.

When handing out references at a different level of granularity than actor-global, how do you ensure the benefits of isolation that the actor model provides? After all, by handing out references inside of an actor it sounds like we're just reinventing shared-memory problems. The answer is that E's reference-states define many of the isolation guarantees around computation that we expect from actors. Two different reference-states are defined:

* _Near reference_: This is a reference between two objects in the same vat. These expose both immediate-calls and eventual-sends.
* _Eventual reference_: This is a reference which crosses vat boundaries, and only exposes eventual-sends, not immediate-calls.

The difference in semantics between the two types of references means that only objects within the same vat are granted synchronous access to one another. The most an eventual reference can do is send and queue a message for processing at some unspecified point in the future. This means that within the execution of a vat, a degree of temporal isolation can be defined between the objects and communications within the vat, and the communications to and from other vats.

TODO: better transition sentence from reference types -> why we care about references at a less abstract level than the actor.

Additionally, it some of motivation here comes from wanting to work at a finer-grained level of references than a traditional actor exposes.

The simplest example is that you want to ensure that another actor in your system can read a value, but can't write to it. How do you do that within another actor model? You might imagine creating a read-only variant of an actor which doesn't expose a write message type, or proxies only `read` messages to another actor which supports both `read` and `write` operations. In E because you are handing out object references, you would simply only pass around references to a `read` method, and you don't have to worry about other actors in your system being able to write values. These finer-grained references make reasoning about state guarantees easier because you are no longer exposing references to an entire actor, but instead the granular capabilities of the actor.

TODO: write more here, maybe something around promise pipelining and partial failure? implications of different types of communication?

## AmbientTalk/2

AmbientTalk/2 is a modern revival of the communicating event-loops actor model as a distributed programming language with an emphasis on developing mobile peer-to-peer applications. This idea was originally realized in AmbientTalk/1 where actors were modelled as ABCL/1-like active objects, but AmbientTalk/2 models actors similarly to E's vats. The authors of AmbientTalk/2 felt limited by not allowing passive objects within an actor to be referenced by other actors, so they chose to go with the more fine-grained approach which allows for remote interactions between passive objects.

Actors in AmbientTalk/2 are representations of an event loops. The message queue is the event queue, messages are events, asynchronous message sends are event notifications, and object methods are the event handlers. The event loop serially processes messages from the queue to avoid race conditions. Local objects within an actor are owned by that actor, which is the only entity allowed to directly execute methods on them. Like E, objects within an actor can communicate using synchronous or asynchronous methods of communication. Again similar to E, objects that are referenced outside of an actor can only be communicated to asynchronously by sending messages. Objects can additionally declare themselves serializable, which means they can be copied and sent to other actors for use as local objects. When this happens, there is no maintained relationship between the original object and its copy.

AmbientTalk/2 uses the event loop model to enforce three essential concurrency control properties:

* _Serial execution_: Events are processed sequentially from an event queue, so the handling of a single event is atomic with respect to other events.
* _Non-blocking communication_: An event loop doesn't suspend computation to wait for other event loops, instead all communication happens strictly as asynchronous event notifications.
* _Exclusive state access_: Event handlers (object methods) and their associated state belong to a single event loop, which has access to their mutable state. Mutation of other event loop state is only possible indirectly by passing an event notification asking for mutation to occur.

The end result of all this decoupling and isolation of computation is that it is a natural fit for mobile ad hoc networks. In this domain, connections are volatile with limited range and transient failures. Removing coupling based on time or synchronization is a natural fit for the domain, and the communicating event-loop actor model is a natural model for programming these systems. AmbientTalk/2 provides additional features on top of the communicating event-loop model like service discovery. These enable ad hoc network creation as actors near each other can broadcast their existence and advertise common services that can be used for communication.

AmbientTalk/2 is most notable as a reimagining of the communicating event-loops actor model for a modern use case.

# Active Objects

Active object actors draw a distinction between two different types of objects: active and passive objects. Every active object has a single entry point defining a fixed set of messages that are understood. Passive objects are the objects that are actually sent between actors, and are copied around to guarantee isolation.

The active object model as initially described in the ABCL/1 language defines objects with a state and three modes:

* `dormant`: Initial state of no computation, simply waiting for a message to activate the behavior of the actor.
* `active`: A state in which computation is performed that is triggered when a message is received that satisfies the patterns and constraints that the actor has defined it can process.
* `waiting`: A state of blocked execution, where the actor is active, but waiting until a certain type or pattern of message arrives to continue computation.

## ABCL/1 Language

The ABCL/1 language implements the active object model described above, representing a system as a collection of objects, and the interactions between those objects as concurrent messages being passed around. One interesting aspect of ABCL/1 is the idea of explicitly different modes of message passing. Other actor models generally have a notion of priority around the values, types, or patterns of messages they process, but ABCL/1 implements tow different modes of message passing with different semantics. They have standard queued messages in the `ordinary` mode, but more interestingly they have `express` priority messages. When an object receives an express message it halts any other processing of ordinary messages it is performing, and processes the `express` message immediately. This enables an actor to accept high-priority messages while in `active` mode, and also enables monitoring and interrupting actors.

The language also offers different models of synchronization around message-passing between actors. Three different message-passing models are given that enable different use cases:

* `past`: Requests another actor to perform a task, while simultaneously proceeding with computation without waiting for the task to be completed.
* `now`: Waits for a message to be received, and to receive a response. This acts as a basic synchronization barrier across actors.
* `future`: Acts like a typical future, continuing computation until a remote result is needed, and then blocking until that result is received.

It is interesting to note that all of these modes can be expressed by the `past` style of message-passing, as long as the type of the message and which actor to reply to with results are known.

TODO: there should be something here to wrap up ABCL/1, and its impact?

## Orleans

Orleans takes the concept of lifecycle-less (not sure this is the term I want to use) actors, which are activated in response to asynchronous messages and places them in the context of cloud applications. Orleans does this via actors (called "grains") which are isolated units of computation and behavior that can have multiple instantiations (called "activations") for scalability. These actors also have persistence, meaning they have a persistent state that is kept in durable storage so that it can be used to manage things like user data.

TODO: something about the notion of identity of an actor here. There are words below, but they could flow better into other points.

It feels like Orleans uses a different notion of identity than other actor systems. In other systems an "actor" might refer to a behavior and instances of that actor might refer to identities that the actor represents like individual users. In Orleans, an actor represents that persistent identity, and the actual instantiations are in fact reconcilable copies of that identity.

The programmer essentially assumes that a single entity is handling requests to an actor, but the Orleans runtime actually allows for multiple instantiations for scalability. These instantiations are invoked in response to an RPC-like call from the programmer which immediately returns an asynchronous promise. Multiple instances of an actor can be running and modifying the state of that actor at the same time. The immediate question here is how does that actually work? It doesn't intuitively seem like transparently accessing and changing multiple isolated copies of the same state should produce anything but problems when its time to do something with that state.

Orleans solves this problem by providing mechanisms to reconcile conflicting changes. If multiple instances of an actor modify persistent state, they need to be reconciled into a consistent state in some meaningful way. The default here is a last-write-wins strategy, but Orleans also exposes the ability to create fine-grained reconciliation policies, as well as a number of common reconcilable data structures. If an application requires a certain reconciliation algorithm, the developer can implement it using Orleans. These reconciliation mechanisms are built upon Orleans' concept of transactions.

Transactions in Orleans are a way to causally reason about the different instances of actors that are involved in a computation. Because in this model computation happens in response to a single outside request, a given actor's chain of computation via. associated actors always contains a single instantiation of each actor. These causal chain of instantiations is treated as a single transaction. At reconciliation time Orleans uses these transactions, along with current instantiation state to reconcile to a consistent state.

All of this is a longwinded way of saying that Orleans' programmer-centric contributions are that it separates the concerns of running and managing actor lifecycles from the concerns of how data flows throughout your distributed system. It does this is a fault-tolerant way, and for most programming tasks, you likely wouldn't have to worry about scaling and reconciling data in response to requests. It provides many of the benefits of the actor model, through a programming model that attempts to abstract away many of the details that you would have to worry about when using actors in production.

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

Akka and Erlang provide modules that you can piece together to build various pieces of functionality into your system. Akka provides a huge number of modules and extensions to configure and monitor a distributed system built using actors. They provide a number of utilities to meet common use-case and deployment scenarios, and these are thoroughly listed and documented. Additionally they provide support for Akka Extensions, which are a mechanism for adding your own features to Akka. These are powerful enough that some core features of Akka like Typed Actors or Serialization are implemented as Akka Extensions. Erlang provides the Open Telecom Platform (OTP), which is a framework comprised of a set of modules and standards designed to help build applications. OTP takes the generic patterns and components of Erlang, and provides them as libraries that enable code reuse and best practices when developing new systems. Cloud Haskell also provides something analogous to Erlang's OTP called the Cloud Haskell Platform.

Orleans is different from these as it is built from the ground up with a more declarative style and runtime. This does a lot of the work of distributing and scaling actors for you, but it is still definitely a framework which handles a lot of the common problems of distribution so that programmers can focus on building the logic of their system.

## Module vs. managed runtime approaches

Based on my research there have been two prevalent approaches to frameworks which are actually used to build production actor systems in industry. These are high-level philosophies about the meta-organization of an actor system. They are the design philosophies that aren't even directly considered when just looking at the base actor programming and execution models. I think the easiest way to describe these is are as the "module approach" and the "managed runtime approach". A high-level analogy to describe these is that the module approach is similar to manually managing memory, while the managed runtime approach is similar to garbage collection. In the module approach, you care about the lifecycle and physical allocation of actors within your system, while in the managed runtime approach you care more about the reconciliation behavior and flow of persistent state between automatic instantiations of your actors.

Both Akka and Erlang take a module approach to building their actor systems. This means that when you build a system using these languages/frameworks, you are using smaller composable components as pieces of the larger system you want to build. You are explicitly dealing with the lifecycles and instantiations of actors within your system, where to distribute them across physical machines, and how to balance actors to scale. Some of these problems might be handled by libraries, but at some level you are specifying how all of the organization of your actors is happening. The JVM or Erlang VM isn't doing it for you.

Orleans goes in another direction, which I call the managed runtime approach. Instead of providing small components which let you build your own abstractions, they provide a runtime in the cloud that attempts to abstract away a lot of the details of managing actors. It does this to such an extent that you no longer even directly manage actor lifecycles, where they live on machines, or how they are replicated and scaled. Instead you program with actors in a more declarative style. You never explicitly instantiate actors, instead you assume that the runtime will figure it out for you in response to requests to your system. You program in strategies to deal with problems like domain-specific reconciliation of data across instances, but you generally leave it to the runtime to scale and distribute the actor instances within your system.

I don't have an opinion on which of these is right. Both approaches have been successful in industry. Erlang has the famous use case of a telephone exchange and a successful history since then. Akka has an entire page detailing its usage in giant companies. Orleans has been used as a backend to massive Microsoft-scale games and applications with millions of users. It seems like the module approach is more popular, but there's only really one example of the managed runtime approach out there. There's no equivalent to Orleans on the JVM or Erlang VM, so realistically it doesn't have as much exposure in the distributed programming community.

## Comparison to Communicating Sequential Processes (CSP)

TODO: where should this live in the chapter?

You might argue that I've ignored some other concurrency primitives that could be considered message-passing or actors at some level. After all, from a high level a Goroutine with channels feels a bit like an actor. As does an RPC system which can buffer sequential calls. I think a lot of discussions of actors are looking at them form a not-so-useful level of abstraction. A lot of the discussions of actors simply take them as something that is a lightweight concurrency primitive which passes messages. I think this view is zoomed out too far, and misses many of the subtleties that differentiate these programming models. Many of these differences stem from the flexibility and scalability of actors. Trying to use CSP-like channels to build a scalable system like you would an actor system would arguably be a tightly-coupled nightmare. The advantages of actors are around the looser coupling, variable topology, and focus on isolation of state and behavior. CSP has a place in building systems, and has proven to be a popular concurrency primitive, but lumping actors in with CSP misses the point of both. Actors are operating at a fundamentally different level of abstraction from CSP.

# References

TODO: Add non-journal references

{% bibliography --file message-passing %}
