---
layout: page
title:  "RPC is Not Dead: Rise, Fall and the Rise of RPC"
by: "Muzammil Abdul Rehman and Paul Grosu"
---

## Introduction

*Remote Procedure Call* (RPC) is a design *paradigm* that allow two entities to communicate over a communication channel in a general request-response mechanism. It was initially built as a tool for outsourcing computation to a server in a distributed system, however, it has evolved over the years to build modular, scalable, distributed, language-agnostic ecosystem of applications. This RPC *paradigm* has been part of the driving force in creating truly revolutionizing distributed systems and giving rise to various communication schemes and protocols between diverse systems.

RPC *paradigm* has been implemented in various forms in our every-day systems. From lower level applications like Network File Systems{% cite sunnfs --file rpc %} and Remote Direct Memory Access{% cite rpcoverrdma --file rpc %} to access protocols to developing an ecosystem of microservices, RPC has been used everywhere. Some of the major examples of RPC include SunNFS{% cite sunnfs --file rpc %}, Twitter's Finagle{% cite finalge --file rpc %}, Apache Thrift{% cite thrift --file rpc %}, Java RMI{% cite rmipaper --file rpc %}, SOAP, CORBA{% cite corba --file rpc %}, Google's gRPC{% cite grpc --file rpc %}. 

* adds paragraph about rise and fall

RPC has evolved over the years. Starting off as a synchronous, insecure, request-response system, RPC has evolved into a secure, asynchronous, fault-tolerant, resilient *paradigm* that has influenced protocols and programming designs, like, HTTP, REST, and just about anything with a request-response system. It has transitioned to an asynchronous bidirectional communication for connecting services and devices across the internet. RPC has influenced various design paradigms and communication protocols. 

## Remote Procedure Calls:

* Diagram of RPC: Local and remote endpoints, communication protocol.

*Remote Procedure Call paradigm* can be defined, at a high level, as a set of two language-agnostic communication *endpoints* connected over a network with one endpoint sending a request and the other endpoint generating a response based on that request. In the simplest terms, it's a request-response paradigm where the two *endpoints*/hosts have different *address space*. The host that requests a remote procedure can be referred to as *caller* and the host that responds to this can be referred to as *callee*.

The *endpoints* in the RPC can either be a client and a server, two nodes in a peer-to-peer network, two hosts in a grid computation system, or even two microservices. The RPC communcation is not limited to two hosts, rather could have multiple hosts or *endpoints* involved {% cite anycastrpc --file rpc %}. 

* explain the diagram here.

One important feature of RPC is different *address space* {% cite implementingrpc --file rpc %} for all the endpoints, however, passing the locations to a global storage(Amazon S3, Microsoft Azure, Google Cloud Store) is not impossible.In RPC,  all the hosts have separate *address spaces*. They can't share pointers or references to a memory location in one host. This *address space* isolation means that all the information is passed in the messages between the host communicating as a value (objects or variables) but not by reference.  Since RPC is a *remote* procedure call, the values sent to the *remote* host cannot be pointers or references to a *local* memory. However, passing links to a global shared memory location is not impossible but rather dependent on the type of system(see *Applications* section for detail).

Originally, RPC was developed as a synchronous, language-specific marshalling service with a custom network protocol to outsource computation{% cite implementingrpc --file rpc %}. It had registry-system to register all the servers. One of the earliest RPC-based system{% cite implementingrpc --file rpc %} was implemented in the Cedar programming language in early 1980's. The goal of this system was to provide similar progamming semantics as local procedure calls. Developed for a LAN network with an inefficient network protocol and a *serialization* scheme to transfer information using the said network protocol, this system aimed at executing a *procedure*(also referred as *method* or a *function*) in a remote *address space*. The single-thread synchronous client and the server were written in an old *Cedar* programming language with a registry system used by the servers to *bind*(or register) their procedures. The clients used this registry system to find a specific server to execute their *remote* procedures.

Modern RPC-based systems are language-agnostic, fault-tolerant, asynchronous, load-balanced systems. Authenticaiton and authorization to these systems have been added as needed along with other security features.

RPC programs have a network, therefore, they need to handle remote errors and be able to communication information successfully. Error handling generally varies and is categorized as *remote-host* or *network* failure handling. Depending on the type of the system, and the error, the caller(or the callee) return an error and these errors can be handled accordingly. For asynchronous RPC calls, it's possible to specify events to ensure progress.

RPC implementations use a *serialization*(also referred to as *marshalling* or *pickling*) scheme on top of an underlying communication protocol(traditionally TCP over IP). These *serialization* schemes allow both the caller *caller* and *callee* to become language agnostic allowing both these systems to be developed in parallel without any language restrictions. Some examples of serialization schemes are JSON, XML, or Protocol Buffers{% cite grpc --file rpc %}.

RPC allows different components of a larger system to be developed independtly of one another. The language-agnostic nature combined with a decoupling of some parts of the system allows the two components(caller and callee) to scale separately and add new functionalities.

Some RPC implementations have moved from a one-server model to a dynamically-created, load-balanced microservices.

* Examples:
    * One could view the internet as example of RPC.e.g  TCP handshake(both act as server and client).
    * First: Google Maps API(REST)
    * SSL Handshake.


## Evolution of RPC:

RPC started in 1980’s and still continues as a relevant model of performing distributed computation, which initially was developed for a LAN and now can be globally implemented.

* RPC has evolved from what it was originally proposed.
* Chris’s thing: https://christophermeiklejohn.com/pl/2016/04/12/rpc.html
* diagram(maybe not): 4 lines, (y-axis: -1 to 1, x-axis 1980's 2016)

### The Rise: All Hail RPC

* RPC origin.

    * Implementing RPC: [https://dl.acm.org/citation.cfm?id=357392](https://dl.acm.org/citation.cfm?id=357392)
    * The RPC thesis(Nelson)
    * More examples

### The Fall: RPC is Dead

* The fall of RPC/Criticism of RPC
    * Limitations
    * http://www.cs.vu.nl//~ast/afscheid/publications/euteco-1988.pdf
    * Systems that use message passing.

### The Rise, Again: Long Live RPC

* gRPC
* XML SOAP
* Java RMI
* Finagle
* Thrift
* Apache Etch
* Sun RPC(ONC RPC)


#### Java Remote Method Invocation:
Java RMI (Java Remote Method Invocation){% cite rmibook --file rpc %} is a Java implementation for performing RPC (Remote Procedure Calls) between a client and a server.  The client using a stub passes via a socket connection the information over the network to the server.  The Remote Object Registry (ROR){% cite rmipaper --file rpc %} on the server contains the references to objects that can be accessed remotely and through which the client will connect to.  The client then can request of the invocation of methods on the server for processing the requested call and then responds with the answer.  RMI provides some security by being encoded but not encrypted, though that can be augmented by tunneling over a secure connection or other methods.



#### CORBA:
CORBA (Common Object Request Broker Architecture){% cite corba --file rpc %} was created by the Object Management Group {% cite corbasite --file rpc %} to allow for language-agnostic communication among multiple computers.  It is an object-oriented model defined via an Interface Definition Language (IDL) and the communication is managed through an Object Request Broker (ORB).  Each client and server have an ORB by which they communicate.  The benefits of CORBA is that it allows for multi-language implementations that can communicate with each other, but much of the criticism around CORBA relates to poor consistency among implementations.

#### XML-RPC and SOAP:

SOAP (Simple Object Access Protocol) is a successor of XML-RPC as a web-services protocol for communicating between a client and server.  It was initially designed by a group at Microsoft {% cite soaparticle1 --file rpc %}.  The SOAP message is a XML-formatted message composed of an envelope inside which a header and a body is provided.  The body of the message contains the request and response of the message, which is transmitted over HTTP or SMTP.  The benefits of such a protocol is that provides the flexibility for transmission of multiple tranport protocol, though parsing such messages could become a bottleneck.


#### Thrift:
Thrift is a RPC created by Facebook and now part of the Apache Foundation {% cite thrift --file rpc %}.  It is a language-agnostic IDL by which one generates the code for the client and server.  It provides the opportunity for compressed serialization by customizing the protocol and the transport after the description file has been processed.

#### Finagle:
Finagle was generated by Twitter and is an RPC written in Scala and can run on an JVM.  It is based on three object types: Service objects, Filter objects and Future objects{% cite finagle --file rpc %}. The Future objects acts by asynchronously being requested for a computation that would return a response at some time in the future.  The Service objects are an endpoint that will return a Future upon processing a request.  A Filter object transforms requests for further processing in case additional customization is required from a request.

#### Open Network Computing RPC:
* Pros and Cons

#### gRPC:

### The Contenders for the Throne: gRPC, Thrift or RMI

* gRPC vs Thrift (maybe also Finagle)

## Applications:

* RPC and shared state (Persistence Layer):
    * http://ieeexplore.ieee.org/document/1302942/?arnumber=1302942&tag=1
    * http://ieeexplore.ieee.org/document/918991/?arnumber=918991

* Grid computing: 
    * https://link.springer.com/article/10.1023/A:1024083511032

* Mobile Systems(offloading and battery requirements): 
	* https://link.springer.com/article/10.1007/s11036-012-0368-0

* Embedded RPC:
    * https://dl.acm.org/citation.cfm?id=1127840

* Micro services architecture(ecosystem)

* RPC can be async

* Shared State

* microservices

* Futures and promises: RPC?

### Streaming requests and buffered responses

### RPC in microservices ecosystem:

RPC started as a separate implements of REST, Streaming RPC, and now made possible of integration of all these implementations as a single abstraction for a user endpoint service.

* Creating new services.

* Bootstrapping

* Load balancing
    * Creating new services in Actor-Like model
    * Fault tolerance
    * Self-recovery

* Business and Persistence Layer were combined and the Persistence layer is not shared anymore, where each endpoints has its own persistent state:
    * https://help.sap.com/saphelp_nwmobile711/helpdata/de/7e/d1a40b5bc84868b1606ce0dc72d88b/content.htm

## Security in RPC:
* Initially it was separate.
    * Authentication, authorization issues have been resolved
* Now embedded in the protocol
* Security and Privacy in RPC
    * Bugs in the libraries.
    * Trust Issues between client and the server.
    * http://static.usenix.org/publications/library/proceedings/sec02/full_papers/giffin/giffin_html/
    * Brewer’s view: https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf
    * E programming language: distributed object model/VAT

## Discussion:
* RPC vs REST and other services. RPC influence.
* The future of RPC
    * Where it shines. Not in message passing.
    * RPC is not XYZ (HTTP, REST, …) though it has influenced. 

## Conclusions(maybe not a heading):

RPC is not dead: long live the Remote Procedure calls.


## References

{% bibliography --file rpc %}