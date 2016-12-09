---
layout: page
title:  "RPC is Not Dead: Rise, Fall and the Rise of Remote Procedure Calls"
by: "Muzammil Abdul Rehman and Paul Grosu"
---

## Introduction

*Remote Procedure Call* (RPC) is a design *paradigm* that allow two entities to communicate over a communication channel in a general request-response mechanism. It was initially built as a tool for outsourcing computation to a server in a distributed system, however, it has evolved over the years to build modular, scalable, distributed, language-agnostic ecosystem of applications. This RPC *paradigm* has been part of the driving force in creating truly revolutionizing distributed systems and giving rise to various communication schemes and protocols between diverse systems.

RPC *paradigm* has been implemented in various forms in our every-day systems. From lower level applications like Network File Systems{% cite sunnfs --file rpc %} and Remote Direct Memory Access{% cite rpcoverrdma --file rpc %} to access protocols to developing an ecosystem of microservices, RPC has been used everywhere. Some of the major examples of RPC include SunNFS{% cite sunnfs --file rpc %}, Twitter's Finagle{% cite finagle --file rpc %}, Apache Thrift{% cite thrift --file rpc %}, Java RMI{% cite rmipaper --file rpc %}, SOAP, CORBA{% cite corba --file rpc %}, Google's gRPC{% cite grpc --file rpc %}. 

RPC has evolved over the years. Starting off as a synchronous, insecure, request-response system, RPC has evolved into a secure, asynchronous, resilient *paradigm* that has influenced protocols and programming designs, like, HTTP, REST, and just about anything with a request-response system. It has transitioned to an asynchronous bidirectional communication for connecting services and devices across the internet. RPC has influenced various design paradigms and communication protocols. 

## Remote Procedure Calls:

*Remote Procedure Call paradigm* can be defined, at a high level, as a set of two language-agnostic communication *endpoints* connected over a network with one endpoint sending a request and the other endpoint generating a response based on that request. In the simplest terms, it's a request-response paradigm where the two *endpoints*/hosts have different *address space*. The host that requests a remote procedure can be referred to as *caller* and the host that responds to this can be referred to as *callee*.

The *endpoints* in the RPC can either be a client and a server, two nodes in a peer-to-peer network, two hosts in a grid computation system, or even two microservices. The RPC communication is not limited to two hosts, rather could have multiple hosts or *endpoints* involved {% cite anycastrpc --file rpc %}.

<figure>
  <img src="{{ site.baseurl }}/resources/img/rpc_chapter_1_ycog_10_steps.png" alt="RPC in 10 Steps." />
<p>Fig1. - Remote Procedure Call{% cite rpcimage --file rpc %}.</p>
</figure>

The simplest RPC implementation looks like Fig1. In this case, the *client*(or *caller*) and the *server*(or *callee*) are separated by a physical network. The main components of the system are the client routine/program, the client stub, the server routine/program, the server stub, and the network routines. The client program can only interact with the client stub that provides the interface of the remote server to the client. This stub also provides marshalling/pickling/serialization of the input arguments sent to the stub by the client routine. Similarly, the server stub provides a client interface to the server routines. Whenever a client routine has to perform a *remote procedure*, it calls the client stub, which serializes the input argument. This serialized data is sent to the server using OS network routines (TCP/IP). The data is serialized by the server stub, present to the server routines for the given arguments. The return value from the server routines is serialized again and sent over the network back to the client where it's deserialized by the client stub and presented to the client routine. This *remote procedure* is generally hidden from the client routine and it appears as a *local procedure* to the client. RPC services also require a discovery service/host-resolution mechanism to bootstrap the communication between the client and the server.

One important feature of RPC is different *address space* {% cite implementingrpc --file rpc %} for all the endpoints, however, passing the locations to a global storage(Amazon S3, Microsoft Azure, Google Cloud Store) is not impossible. In RPC,  all the hosts have separate *address spaces*. They can't share pointers or references to a memory location in one host. This *address space* isolation means that all the information is passed in the messages between the host communicating as a value (objects or variables) but not by reference.  Since RPC is a *remote* procedure call, the values sent to the *remote* host cannot be pointers or references to a *local* memory. However, passing links to a global shared memory location is not impossible but rather dependent on the type of system (see *Applications* section for detail).

Originally, RPC was developed as a synchronous, language-specific marshalling service with a custom network protocol to outsource computation {% cite implementingrpc --file rpc %}. It had registry-system to register all the servers. One of the earliest RPC-based system {% cite implementingrpc --file rpc %} was implemented in the Cedar programming language in early 1980's. The goal of this system was to provide similar programming semantics as local procedure calls. Developed for a LAN network with an inefficient network protocol and a *serialization* scheme to transfer information using the said network protocol, this system aimed at executing a *procedure*(also referred as *method* or a *function*) in a remote *address space*. The single-thread synchronous client and the server were written in an old *Cedar* programming language with a registry system used by the servers to *bind*(or register) their procedures. The clients used this registry system to find a specific server to execute their *remote* procedures.

Modern RPC-based systems are language-agnostic, asynchronous, load-balanced systems. Authentication and authorization to these systems have been added as needed along with other security features. Most of these systems have fault-handling built into them as modules.

RPC programs have a network (or a communication channel), therefore, they need to handle remote errors and be able to communication information successfully. Error handling generally varies and is categorized as *remote-host* or *network* failure handling. Depending on the type of the system, and the error, the caller (or the callee) return an error and these errors can be handled accordingly. For asynchronous RPC calls, it's possible to specify events to ensure progress.

RPC implementations use a *serialization*(also referred to as *marshalling* or *pickling*) scheme on top of an underlying communication protocol (traditionally TCP over IP). These *serialization* schemes allow both the caller *caller* and *callee* to become language agnostic allowing both these systems to be developed in parallel without any language restrictions. Some examples of serialization schemes are JSON, XML, or Protocol Buffers {% cite grpc --file rpc %}.

RPC allows different components of a larger system to be developed independently of one another. The language-agnostic nature combined with a decoupling of some parts of the system allows the two components (caller and callee) to scale separately and add new functionalities. This independent scaling of the system might lead to a mesh of interconnected RPC *services* facilitating one another.

### Examples of RPC

RPC has become very predominant in modern systems. In the simplest RPC systems, a client connects to a server over a network connection and performs a *procedure*. This procedure could be as simple as `return "Hello World"` in your favorite programming language. However, the complexity of the of this remote procedure has no upper bound.

Here's the code of this simple RPC server, written in Python3.
```python
from xmlrpc.server import SimpleXMLRPCServer

# a simple RPC function that returns "Hello World!"
def remote_procedure(n):
    return "Hello World!"

server = SimpleXMLRPCServer(("localhost", 8080))
print("RPC Server listening on port 8080...")
server.register_function(remote_procedure, "remote_procedure")
server.serve_forever()
```

This code for a simple RPC client for the above server, written in Python3, is as follows.

```python
import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8080/") as proxy:
    print(proxy.remote_procedure())
```

In the above example, we create a simple function called `remote_procedure` and *bind* it to port *8080* on *localhost*. The RPC client then connects to the server and *request* the `remote_procedure` with no input arguments. The server then *responds* with a return value of the `remote_procedure`. 

One can even view the *three-way handshake* as an example of RPC paradigm. The  *three-way handshake* is most commonly used in establishing a TCP connection. Here, a server-side application *binds* to a port on the server, and adds a hostname resolution entry is added to a DNS server(can be seen as a *registry* in RPC). Now, when the client has to connect to the server, it requests a DNS server to resolve the hostname to an IP address and the client sends a SYN packet. This SYN packet can be seen as a *request* to another *address space*. The server, upon receiving this, returns a SYN-ACK packet. This SYN-ACK packet from the server can be seen as *response* from the server, as well as a *request* to establish the connection. The client then *responds* with an ACK packet.

## Evolution of RPC:

RPC paradigm was first proposed in 1980’s and still continues as a relevant model of performing distributed computation, which initially was developed for a LAN and now can be globally implemented. It has had a long and arduous journey to its current state. Here are the three main(overlapping) stages that RPC went through.

### The Rise: All Hail RPC(Early 1970's - Mid 1980's)

RPC started off strong. With RFCs{% cite rfc674 rfc707 --file rpc %} coming out and specifying the design of Remote Procedure Calls, followed by Nelson et. al{% cite implementingrpc --file rpc %} coming up with a first implementation for the Cedar programming language, RPC revolutionized systems in general and gave rise to one of the earliest distributed systems(apart from the internet, of course).

With these early achievements, people started using RPC as the defacto design choice. It became a Holy Grail in the systems community for a few years after the first implementation.

### The Fall: RPC is Dead(Late 1970's - Late 1980's)

RPC, despite being an initial success, wasn't without flaws. Within a year of its inception, the limitation of the RPC started to catch up with it. RFC 684 criticized RPC for latency, failures, and the cost. It also focussed on message-passing systems as an alternative to RPC design. Similarly, a few years down the road, in 1988, Tenenbaum et. al presented similar concerns against RPC {%cite critiqueofrpc --file rpc %}. It talked about problems heterogeneous devices, message passing as an alternative, packet loss, network failure, RPC's synchronous nature, and highlighted that RPC is not a one-size-fits-all model.

### The Rise, Again: Long Live RPC(Early 1990's - Today)

Despite facing problems in its early days, RPC withstood the test of time. Researchers realized the limitations of RPC and focussed on rectifying and instead of enforcing RPC, they started to use RPC in applications where it was needed. The designer started adding exception-handling, async, network failure handling and heterogenity between different languages/devices to RPC. 

Perhaps, the earliest system in this era was SunRPC {% cite sunnfs --file rpc %} used for the Sun Network File System(NFS). This SunRPC has gone under various additions and is now referred to as Open Network Computing RPC(ONC RPC). 

Soon to follow SunRPC was the language-agnostic CORBA{% cite corba --file rpc %} which was followed by Java RMI{% cite rmipaper --file rpc %}. CORBA and RMI have also undergone various modifications as internet standards were set and TCP/IP became the norm.

A new breed of RPC also started in this era(early 2000's), Async RPC, giving rise to systems that use *futures* and *promises*, like Finagle{% cite finagle --file rpc %} and Cap'n Proto(post-2010).

In the post-2000 era, MAUI{% cite maui --file rpc %}, Cap'n Proto{% cite capnproto --file rpc %}, gRPC{% cite grpc --file rpc %}, Thrift{% cite thrift --file rpc %} and Finagle{% cite finagle --file rpc %} have been released, which have significantly boosted the widespread use of RPC. A level overview of some of the most important RPC implementation is as follows.

#### Java Remote Method Invocation
Java RMI (Java Remote Method Invocation){% cite rmibook --file rpc %} is a Java implementation for performing RPC (Remote Procedure Calls) between a client and a server.  The client using a stub passes via a socket connection the information over the network to the server.  The Remote Object Registry (ROR){% cite rmipaper --file rpc %} on the server contains the references to objects that can be accessed remotely and through which the client will connect to.  The client then can request of the invocation of methods on the server for processing the requested call and then responds with the answer.  RMI provides some security by being encoded but not encrypted, though that can be augmented by tunneling over a secure connection or other methods.

#### CORBA
CORBA (Common Object Request Broker Architecture){% cite corba --file rpc %} was created by the Object Management Group {% cite corbasite --file rpc %} to allow for language-agnostic communication among multiple computers.  It is an object-oriented model defined via an Interface Definition Language (IDL) and the communication is managed through an Object Request Broker (ORB).  Each client and server have an ORB by which they communicate.  The benefits of CORBA is that it allows for multi-language implementations that can communicate with each other, but much of the criticism around CORBA relates to poor consistency among implementations.

#### XML-RPC and SOAP
SOAP (Simple Object Access Protocol) is a successor of XML-RPC as a web-services protocol for communicating between a client and server. It was initially designed by a group at Microsoft {% cite soaparticle1 --file rpc %}.  The SOAP message is an XML-formatted message composed of an envelope inside which a header and a body are provided.  The body of the message contains the request and response of the message, which is transmitted over HTTP or SMTP.  The benefit of such a protocol is that it provides the flexibility for transmission over multiple transport protocol, though parsing such messages could become a bottleneck.

#### Thrift
Thrift is an RPC system created by Facebook and now part of the Apache Foundation {% cite thrift --file rpc %}. It is a language-agnostic IDL by which one generates the code for the client and server. It provides the opportunity for compressed serialization by customizing the protocol and the transport after the description file has been processed.

#### Finagle
Finagle was generated by Twitter and is an RPC system written in Scala and can run on a JVM.  It is based on three object types: Service objects, Filter objects and Future objects {% cite finagle --file rpc %}. The Future objects act by asynchronously being requested for a computation that would return a response at some time in the future.  The Service objects are an endpoint that will return a Future upon processing a request.  A Filter object transforms requests for further processing in case additional customization is required from a request.

#### Open Network Computing RPC
* Pros and Cons

#### Mobile Assistance Using Infrastructure(MAUI) 

The MAUI project {% cite maui --file rpc %}, developed by Microsoft is a computation offloading system for mobile systems. It's an automated system that offloads a mobile code to a dedicated infrastructure in order to increase the battery life of the mobile, minimize the load on the programmer and perform complex computations offsite. MAUI uses RPC as the communication protocol between the mobile and the infrastructure.

#### gRPC

gRPC has been built as a collaboration between Google and Square as a public replacement of Stubby, ARCWire, and Sake {% cite Apigee --file rpc %}.  The IDL for gRPC is Protocol Buffers(also referred as ProtoBuf).

gRPC provides a platform for scalable, bi-directional streaming using both synchronized and asynchronous communication. It multiplexes the requests over a single connection using header compression. This makes it possible for gRPC to be used for mobile clients where battery life and data usage are important.
The core library is in C -- except for Java and GO -- and surface APIs are implemented for all the other languages connecting through it{% cite CoreSurfaceAPIs --file rpc %}.

Since Protocol Buffers has been utilized by many individuals and companies, gRPC makes it natural to extend their RPC ecosystems via gRPC. Companies like Cisco, Juniper and Netflix {% cite gRPCCompanies --file rpc %} have found it practical to adopt it.
A majority of the Google Public APIs, like their places and maps APIs, have been ported to gRPC ProtoBuf {% cite gRPCProtos --file rpc %} as well.

#### Cap'n Proto
CapnProto{% cite capnproto --file rpc %} is a data interchange RPC system between that bypasses data-encoding step(like JSON or ProtoBuf) to significantly improve the performance. It's developed by the original author of gRPC's ProtoBuf, but since it uses bytes(binary data) for encoding/decoding, it outperforms gRPC's ProtoBuf. It uses futures and promises to combine various remote operations into a single to save the transportation round-trips.

### The Heir to the Throne: gRPC or Thrift

Although there are many candidates to be considered as top contenders for RPC throne, most of these are targeted for a specific type of application. ONC is generally specific to the Network File System(though it's being pushed as a standard), Cap'n Proto is relatively new and untested, MAUI is specific to mobile systems, the open-source Finagle is primarily being used at Twitter(not widespread), and the Java RMI simply doesn't even close anyways(sorry to burst your bubble Java fans). 

Probably, the most powerful, and practical systems out there are Apache Thrift and Google's gRPC, primarily because *variants* of these two systems have been developed and used by Facebook and Google, respectively. This might be considered as biased view against other RPC implementations, however, when one considers Big Data and Internet-scale, only these two companies (and these two systems) come close.

Thrift was actually released a few years ago, while the first stable release for gRPC came out in August 2016. However, despite being 'out there', Thrift is currently less popular than gRPC {%cite trendrpcthrift --file rpc %}.

gRPC {% cite gRPCLanguages --file rpc %} and Thrift, both, support most of the popular languages, including Java, C/C++, and Python. Thrift supports other languages, like Ruby, Erlang, Perl, Javascript, Node.js and OCaml while gRPC currently supports Node.js and Go.

Thrift provides exception-handling as a message while the programmer has to handle exceptions in gRPC.

Although custom authentication mechanisms can be implemented in both these system, gRPC come with a Google-backed authentication using SSL/TLS and Google Tokens {% cite grpcauth --file rpc %}.

The major differences between gRPC and Thrift can be summed in this table.

| Comparison | Thrift | gRPC |
| ----- | ----- | ----- |
| License | Apache2 | BSD |
| Supported Languages | C++, Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk, and OCaml | C/C++, Python, Go, Java, Ruby, PHP, C#, Node.js, Objective-C |
| Exceptions | Allows being built in the message | Implemented by the programmer |
| Authentication | Custom | Custom + Google Tokens |
| Bi-Directionality | Not straightforward | Core Implementation via HTTP/2 |
| Multiplexing | Some functionality via multiplexed server | Core Implementation via HTTP/2 |

Although, it's difficult to specifically choose one over the other, however, with increasing popularity of gRPC, and the fact that it's still in early stages of development, the general trend{%cite trendrpcthrift --file rpc %} over the past year has started to shift in favor of gRPC and it's giving Thrift a run for its money.

**Note:** This study is performed in December 2016 so the results are expected to change with time.

## Applications

Since its inception, various papers have been published in applying RPC paradigm to different domains, as well as using RPC implementations to create new systems. Here are some of applications and systems that incorporated RPC.

#### Shared State and Persistence Layer

One major limitation (and the advantage) of RPC is considered the separate *address space* of all the machines in the network. This means that *pointers* or *references* to a data object cannot be passed between the caller and the callee. Therefore, Interweave {% cite interweave2 interweave1 interweave3 --file rpc %} is a middleware system that allows scalable sharing of arbitrary data-types and language-independent processes running heterogeneous hardware. Interweave is specifically designed and is compatible with RPC-based systems and allows easier access to the shared resources between different applications. It even allows passing C *pointers* between the caller and the callee.

#### GridRPC

Grid computing is one of the most widely used applications of RPC paradigm. At a high level, it can be seen as a mesh (or a network) of computers connected with each other to for *grid* such each system can leverage resources from any other system in the network.

In the GridRPC paradigm, each computer in the network can act as the *caller* or the *callee* depending on the amount of resources required {% cite grid1 --file rpc %}. It's also possible for the same computer to act as the *caller* as well as the *callee* for *different* computations. 

Some of the most popular implementations that allow one to have GridRPC-compliant middleware are GridSolve{% cite gridsolve1 gridsolve2 --file rpc %} and Ninf-G{% cite ninf --file rpc %}. Ninf is relatively older than GridSolve and was first published in the late 1990's. It's a simple RPC layer that also provides authentication and secure communication between the two parties. GridSolve, on the other hand, is relatively complex and provides a middleware for the communications using a client-agent-server model.

#### Mobile Systems and Computation Offloading

Mobile systems have become very powerful these days. With multi-core processors and gigabytes of RAM, they can undertake relatively complex computations without a hassle. Due to this advancement, they consume a larger amount of energy and hence, their batteries, despite becoming larger, drain quickly with usage. Moreover, mobile data (network bandwidth) is still limited and expensive. Due to these requirements, it's better to offload mobile computations from mobile systems when possible. RPC plays an important role in the communication for this *computation offloading*. Some of these services use Grid RPC technologies to offload this computation. Whereas, other technologies use an RMI(Remote Method Invocation) system for this. 

The Ibis Project {% cite ibis --file rpc %} builds an RMI and GMI (Group Method Invocation) model to facilitate outsourcing computation. Cuckoo {% cite cuckoo --file rpc %} uses this Ibis communication middleware to offload computation.

The Microsoft's MAUI Project {% cite maui --file rpc %} uses RPC communication and allows partitioning of .NET applications and "fine-grained code offload to maximize energy savings with minimal burden on the programmer". MAUI decides the methods to offload to the external MAUI server at runtime.

#### Async RPC, Futures and Promises

Remote Procedure Calls can be asynchronous. Not only that but these async RPCs play in integral role in the *futures* and *promises*. *Future* and *promises* are programming constructs that where a *future* is seen as variable/data/return type/error while a *promise* is seen as a *future* that doesn't have a value, yet. We follow Finagle's {% cite finagle --file rpc %} definition of *futures* and *promises*, where the *promise* of a *future*(an empty *future*) is considered as a *request* while the async fulfillment of this *promise* by a *future* is seen as the *response*. This construct is primarily used for concurrent programming.

Perhaps the most renowned systems using this type of RPC model are Twitter's Finagle{% cite finagle --file rpc %} and Cap'n Proto{% cite capnproto --file rpc %}.

#### RPC in Microservices Ecosystem:

RPC implementations have moved from a one-server model to multiple servers and on to dynamically-created, load-balanced microservices. RPC started as a separate implementations of REST, Streaming RPC, MAUI, gRPC, Cap'n Proto, and has now made it possible for integration of all these implementations as a single abstraction as a user *endpoint* service. The endpoints are the building blocks of *microservices*. These *microservices* interact with each other and applications and combine to give the feel of one large monolithic service.

The use of RPC has allowed us to create new microservices on-the-fly. The microservices can not only created and bootstrapped at runtime but also have inherent features like load-balancing and failure-recovery. This bootstrapping might occur on the same machine, adding to a Docker container {% cite docker --file rpc %}, or across a network (using any combination of DNS, NATs or other mechanisms).

RPC can be defined as the "glue" that holds all the microservices together{% cite microservices1rpc --file rpc %}. This means that RPC is one of the primary communication mechanism between different microservices running on different systems. A microservice requests another microservice to perform an operation/query. The other microservice, upon receiving such request, performs an operation and returns a response. This operation could vary from a simple computation to invoking another microservice creating a series of RPC events to creating new microservices on the fly to dynamically load balance the microservices system.

An example of a microservices ecosystem that uses futures/promises is Finagle at Twitter.

## Security in RPC:

The initial RPC implementation {% cite implementingrpc --file rpc %} was developed for an isolated LAN network and didn't focus much on security. There're various attack surfaces in that model, from the malicious registry, to a malicious server, to a client targeting for Denial-of-Service to Man-in-the-Middle attack between client and server.

As time progressed and internet evolved, new standards came along, and RPC implementations became much more secure. Security, in RPC, is generally added as a *module* or a *package*. These modules have libraries for authentication and authorization of the communication services (caller and callee). These modules are not always bug-free and it's possible to gain unauthorized access to the system. Efforts are being made to rectify these situations by the security in general, using code inspection and bug bounty programs to catch these bugs before-hand. However, with time new bugs arise and this cycle continues. It's a vicious cycle between attackers and security experts, both of whom tries to outdo their opponent.

For example, the Oracle Network File System uses a *Secure RPC*{% cite oraclenfs --file rpc %} to perform authentication in the NFS. This *Secure RPC* uses Diffie-Hellman authentication mechanism with DES encryption to allow only authorized users to access the NFS. Similarly, Cap'n Proto {% cite capnprotosecure --file rpc %} claims that it is resilient to memory leaks, segfaults, and malicious inputs and can be used between mutually untrusting parties. However, in Cap'n Proto "the RPC layer is not robust against resource exhaustion attacks, possibly allowing denials of service", nor has it undergone any formal verification {% cite capnprotosecure --file rpc %}.

Although, it's possible to come up with a *Threat Model* that would make an RPC implementation insecure to use, however, one has to understand that using any distributed system increases the attack surface anyways and claiming one *paradigm* to be more secure than another would be a biased statement, since *paradigms* are generally an idea and it depends on different system designers to use these *paradigms* to build their systems and take care of features specific to real systems, like security and load-balancing. There's always a possibility of rerouting a request to a malicious server(if the registry gets hacked), or there's no trust between the *caller* and *callee*. However, we maintain that RPC *paradigm* is not secure or insecure(for that matter), and that the most secure systems are the ones that are in an isolated environment, disconnected from the public internet with a self-destruct mechanism{% cite self --file rpc %} in place, in an impenetrable bunker, and guarded by the Knights Templar(*they don't exist! Well, maybe Fort Meade comes close*).

## Discussion:

RPC *paradigm* shines the most in *request-response* mechanisms. Futures and Promises also appear to a new breed of RPC. This leads one to question, as to whether every *request-response* system is a modified implementation to of the RPC *paradigm*, or does it actually bring anything new to the table? These modern communication protocols, like HTTP and REST, might just be a different flavor of RPC. In HTTP, a client *requests* a web page(or some other content), the server then *responds* with the required content. The dynamics of this communication might be slightly different from your traditional RPC, however, an HTTP Stateless server adheres to most of the concepts behind RPC *paradigm*. Similarly, consider sending a request to your favorite Google API. Say, you want to translate your latitude/longitude to an address using their Reverse Geocoding API, or maybe want to find out a good restaurant in your vicinity using their Places API, you'll send a *request* to their server to perform a *procedure* that would take a few input arguments, like the coordinates, and return the result. Even though these APIs follow a RESTful design, it appears to be an extension to the RPC *paradigm*.

RPC paradigm has evolved over time. It has evolved to the extent that, currently, it's become very difficult differentiate RPC from non-RPC. For the past decades, researchers and industry leaders have tried to come up with *their* definition of RPC. The proponents of RPC paradigm view every *request-response* communication as an implementation the RPC paradigm while those against RPC try to explicitly come up with the bounds of RPC. RPC supporters consider it as the Holy Grail of distributed systems. They view it as the foundation of modern distributed communication. From Apache Thrift and ONC to HTTP and REST, they advocate it all as RPC while REST developers have strong opinions against RPC.

Moreover, with modern global storage mechanisms, the need for RPC systems to have a separate *address space* seems to be slowly dissolving and disappearing into thin air. So, the question remains what *is* RPC and what * is not* RPC? This is an open-ended question. There is no unanimous agreement about what RPC should look like, except that it has communication between two *endpoints*. What we think of RPC is:

*"In the world of distributed systems, where every individual component of a system, be it a hard disk, a multi-core processor, or a microservice, is an extension of the RPC, it's difficult to come with a concrete definition of the RPC paradigm. Therefore, anything loosely associated with a request-response mechanism can be considered as RPC".*

<blockquote>
<p align="center">
**RPC is not dead, long live RPC!**
</p>
</blockquote>

## References

{% bibliography --file rpc --cited %}
