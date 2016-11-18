---
layout: page
title:  "ACIDic to BASEic: How the database pH has changed"
by: "Aviral Goel"
---

## 1. The **ACID**ic Database Systems

Relational Database Management Systems are the most ubiquitous database systems for persisting state. Their properties are defined in terms of transactions on their data. A database transaction can be either a single operation or a sequence of operations, but is treated as a single logical operation on the data by the database. The properties of these transactions provide certain guarantees to the application developer. The acronym **ACID** was coined by Andreas Reuter and Theo Härder in 1983 to describe them.

* **Atomicity** guarantees that any transaction will either complete or leave the database unchanged. If any operation of the transaction fails, the entire transaction fails. Thus, a transaction is perceived as an atomic operation on the database. This property is guaranteed even during power failures, system crashes and other erroneous situations. 

* **Consistency** guarantees that any transaction will always result in a valid database state, i.e., the transaction preserves all database rules, such as unique keys, etc. 

* **Isolation** guarantees that concurrent transactions do not interfere with each other. No transaction views the effects of other transactions prematurely. In other words, they execute on the database as if they were invoked serially (though a read and write can still be executed in parallel). 

* **Durability** guarantees that upon the completion of a transaction, the effects are applied permanently on the database and cannot be undone. They remain visible even in the event of power failures or crashes. This is done by ensuring that the changes are committed to disk (non-volatile memory).

<blockquote><p><b>ACID</b>ity implies that if a transaction is complete, the database state is structurally consistent (adhering to the rules of the schema) and stored on disk to prevent any loss.</p></blockquote>

Because of the strong guarantees this model simplifies the life of the developer and has been traditionally the go to approach in application development. It is instructive to examine how these properties are enforced. 

Single node databases can simply rely upon locking to ensure *ACID*ity. Each transaction marks the data it operates upon, thus enabling the database to block other concurrent transactions from modifying the same data. The lock has to be acquired both while reading and writing data. The locking mechanism enforces a strict linearizable consistency. An alternative, *multiversioning* allows a read and write operation to execute in parallel. Each transaction which reads data from the database is provided the earlier unmodified version of the data that is being modified by a write operation. This means that read operations don't have to acquire locks on the database. This enables read operations to execute without blocking write operations and write operations to execute without blocking read operations.

This model works well on a single node. But it exposes a serious limitation when too many concurrent transactions are performed. A single node database server will only be able to process so many concurrent read operations. The situation worsens when many concurrent write operations are performed. To guarantee *ACID*ity, the write operations will be performed in sequence. The last write request will have to wait for an arbitrary amount of time, a totally unacceptable situation for many real time systems. This requires the application developer to decide on a **Scaling** strategy.

## 2. Transaction Volume 

To increase the volume of transactions against a database, two scaling strategies can be considered

**Vertical Scaling** is the easiest approach to scale a relational database. The database is simply moved to a larger computer which provides more transactional capacity. Unfortunately, its far too easy to outgrow the capacity of the largest system available and it is costly to purchase a bigger system each time that happens. Since its not commodity hardware, vendor lock-in will add to further costs.

**Horizontal Scaling** is a more viable option and can be implemented in two ways. Data can be segregated into functional groups spread across databases. This is called *Functional Scaling*. Data within a functional group can be further split across multiple databases, enabling functional areas to be scaled independently of one another for even more transactional capacity. This is called *sharding*.

Horizontal Scaling through functional partitioning enables high degree of scalability. However, the functionally separate tables employ constraints such as foreign keys. For these constraints to be enforced by the database itself, all tables have to reside on a single database server. This limits horizontal scaling. To work around this limitation the tables in a functional group have to be stored on different database servers. But now, a single database server can no longer enforce constraints between the tables. In order to ensure *ACID*ity of distributed transactions, distributed databases employ a two-phase commit (2PC) protocol. 

* In the first phase, a coordinator node interrogates all other nodes to ensure that a commit is possible. If all databases agree then the next phase begins, else the transaction is canceled.

* In the second phase, the coordinator asks each database to commit the data.

2PC is a blocking protocol and is usually employed for updates which can take from a few milliseconds up to a few minutes to commit. This means that while a transaction is being processed, other transactions will be blocked. So the application that initiated the transaction will be blocked. Another option is to handle the consistency across databases at the application level. This only complicates the situation for the application developer who is likely to implement a similar strategy if *ACID*ity is to be maintained.

# The part below is in bits and pieces. A lot of details need to be filled in.

## 3. A Distributed Concoction

**I am a cute diagram for the paragraph below.**

In the network above, all messages between the node set G1 and G2 are lost due to a network issue. The system as a whole detects this situation. There are two options -

* The system allows any application to read and write to data objects on these nodes as they are **available**. The application writes to a data object. This write operation completes in one of the nodes of G1. Due to **network partition**, this change is not propagated to replicas of the data object in G2. Subsequently the application tries to read the value of that data object and the read operation executes in one of the nodes of G2. The read operation returns the older value of the data object, thus making the application state not **consistent**.

## 4. The volatile network 

Network Partition is a contentious subject among distributed database architects. While some maintain that network partitions are rare, other point to their. 9


## 4. The spicy ingredients


This simple observation shows a tension between three issues concerning distributed systems -

**Consistency** is the guarantee of total ordering of all operations on a data object such that each operation appears indivisible. This means that any read operation must return the most recently written value. This provides a very convenient invariant to the client application that uses the distributed data store. This definition of consistency is the same as the **Atomic**ity guarantee provided by relational database transactions.

**Availability** is the guarantee that every request to a distributed system must result in a response. However, this is too vague a definition. Whether a node failed in the process of responding or it ran a really long computation to generate a response or whether the request or the response got lost due to network issues is generally impossible to determine by the client and willHence, for all practical purposes, availability can be defined as the service responding to a request in a timely fashion, the amount of delay an application can bear depends on the application domain.

**Partitioning** is the loss of messages between the nodes of a distributed system. 


This observation led Eric Brewer to conjecture in an invited talk at PODC 2000 - 

<blockquote>It is impossible for a web service to provide the following three guarantees:
Consistency
Availability
Partition Tolerance</blockquote>

It is clear that the prime culprit here is network partition. If there are no network partitions, any distributed service will be both highly available and provide strong consistency of shared data objects. Unfortunately, network partitions cannot be remedied in a distributed system. 





## 3. Strong Consistency









We observed how in the event of a network partition, we could not have both availability and consistency at the same time. Let's study their pairwise interaction -


For many applications *ACID*ic datastores impose a more severe consistency guarantee than is actually needed and this reduces their availability. By relaxing the constraints on data consistency one can achieve higher scalability and availability. 

### 2. The **BASE**ic distributed state

When viewed through the lens of CAP theorem and its consequences on distributed applications we realize that we cannot commit to perfect availability and strong consistency. But surely we can explore the middle ground. We can guarantee availability most of the time with sometimes inconsistent view of the data. The consistency is eventually achieved when the communication between the nodes resumes. This leads to the following properties of the current distributed applications, referred to by the acronym BASE.

**Basically Available** services are those which are partially available when partitions happen. Thus, they appear to work most of the time.
**Soft State** services provide no strong consistency guarantees. They are not write consistent. Since replicas may not be mutually consistent, applications have to accept stale data.
**Eventually Consistent** services try to make application state consistent whenever possible.


### What's the right pH for my distributed solution?

Whether an application chooses to an *ACID*ic or *BASE*ic service depends on the domain. An application developer has to consider the consistency-availability tradeoff on a case by case basis. *ACID*ic databases provide a very simple and strong consistency model making application development easy for domains where data inconsistency cannot be tolerated. *BASE*ic databases provide a very loose consistency model, placing more burden on the application developer to understand the limitations of the database and work around that, retaining sane application behavior. 

## References

https://neo4j.com/blog/acid-vs-base-consistency-models-explained/
https://en.wikipedia.org/wiki/Eventual_consistency/
https://en.wikipedia.org/wiki/Distributed_transaction
https://en.wikipedia.org/wiki/Distributed_database
https://en.wikipedia.org/wiki/ACID
http://searchstorage.techtarget.com/definition/data-availability
https://aphyr.com/posts/288-the-network-is-reliable
http://research.microsoft.com/en-us/um/people/navendu/papers/sigcomm11netwiser.pdf
http://web.archive.org/web/20140327023856/http://voltdb.com/clarifications-cap-theorem-and-data-related-errors/
http://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf
http://www.hpl.hp.com/techreports/2012/HPL-2012-101.pdf
http://research.microsoft.com/en-us/um/people/navendu/papers/sigcomm11netwiser.pdf
http://www.cs.cornell.edu/projects/ladis2009/talks/dean-keynote-ladis2009.pdf
http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
https://people.mpi-sws.org/~druschel/courses/ds/papers/cooper-pnuts.pdf
http://blog.gigaspaces.com/nocap-part-ii-availability-and-partition-tolerance/
http://stackoverflow.com/questions/39664619/what-if-we-partition-a-ca-distributed-system
https://people.eecs.berkeley.edu/~istoica/classes/cs268/06/notes/20-BFTx2.pdf
http://ivoroshilin.com/2012/12/13/brewers-cap-theorem-explained-base-versus-acid/
https://www.quora.com/What-is-the-difference-between-CAP-and-BASE-and-how-are-they-related-with-each-other
http://berb.github.io/diploma-thesis/original/061_challenge.html
http://dssresources.com/faq/index.php?action=artikel&id=281
https://saipraveenblog.wordpress.com/2015/12/25/cap-theorem-for-distributed-systems-explained/
https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed
https://dzone.com/articles/better-explaining-cap-theorem
http://www.julianbrowne.com/article/viewer/brewers-cap-theorem
http://delivery.acm.org/10.1145/1400000/1394128/p48-pritchett.pdf?ip=73.69.60.168&id=1394128&acc=OPEN&key=4D4702B0C3E38B35%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35%2E6D218144511F3437&CFID=694281010&CFTOKEN=94478194&__acm__=1479326744_f7b98c8bf4e23bdfe8f17b43e4f14231
http://dl.acm.org/citation.cfm?doid=1394127.1394128
https://en.wikipedia.org/wiki/Eventual_consistency
https://en.wikipedia.org/wiki/Two-phase_commit_protocol
https://en.wikipedia.org/wiki/ACID
https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf
http://www.johndcook.com/blog/2009/07/06/brewer-cap-theorem-base/
http://searchsqlserver.techtarget.com/definition/ACID
http://queue.acm.org/detail.cfm?id=1394128
http://www.dataversity.net/acid-vs-base-the-shifting-ph-of-database-transaction-processing/
https://neo4j.com/developer/graph-db-vs-nosql/#_navigate_document_stores_with_graph_databases
https://neo4j.com/blog/aggregate-stores-tour/
https://en.wikipedia.org/wiki/Eventual_consistency
https://en.wikipedia.org/wiki/Distributed_transaction
https://en.wikipedia.org/wiki/Distributed_database
https://en.wikipedia.org/wiki/ACID
http://searchstorage.techtarget.com/definition/data-availability
https://datatechnologytoday.wordpress.com/2013/06/24/defining-database-availability/
{% bibliography --file rpc %}
