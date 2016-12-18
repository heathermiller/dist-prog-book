---
layout: page
title:  "Being Consistent"
by: "Aviral Goel"
---

## Replication and Consistency
Availability and Consistency are the defining characteristics of any distributed system. As dictated by the CAP theorem, accommodating network partitions requires a trade off between the two properties. Modern day large scale internet based distributed systems have to be highly available. To manage huge volumes of data (big data) and to reduce access latency for geographically diverse user base, their data centers also have to be geographically spread out. Network partitions which would otherwise happen with a low probability on a local network become certain events in such systems. To ensure availability in the event of partitions, these systems have to replicate data objects. This begs the question, how to ensure consistency of these replicas? It turns out there are different notions of consistency which the system can adhere to.

* **Strong Consistency** implies linearizability of updates, i.e., all updates applied to a replicated data type are serialized in a global total order. This means that any update will have to be simultaneously applied to all other replicas. Its obvious that this notion of consistency is too restrictive. A single unavailable node will violate this condition. Forcing all updates to happen synchronously will impact system availability negatively. This notion clearly does not fit the requirements of highly available fault tolerant systems.

* **Eventual Consistency** is a weaker model of consistency that does not guarantee immediate consistency of all replicas. Any local update is immediately executed on the replica. The replica then sends its state asynchronously to other replicas. As long as all replicas share their states with each other, the system eventually achieves stability. Each replica finally contains the same value. During the execution, all updates happen asynchronously at all replicas in a non-deterministic order. So replicas can be inconsistent between updates. If updates arrive concurrently at a replica, a consensus protocol can be employed to ensure that both updates taken together do not violate an invariant. If they do, a rollback has to be performed and the new state is communicated to all the other replicas.

Most large scale distributed systems try to be **Eventually Consistent** to ensure high availability and partition-tolerance. But conflict resolution is hard. There is little guidance on correct approaches to consensus and its easy to come up with an error prone ad-hoc approach. What if we side-step conflict resolution and rollback completely? Is there a way to design data structures which do not require any consensus protocols to merge concurrent updates?

## A Distributed Setting

### TODO need to write pseudocode. Will finish this part with the detailed explanation of CRDTs in the next chapter.
Consider a replicated counter. Each node can increment the value of its local copy. The figure below shows three nodes which increment their local copies at arbitrary time points and each replica sends its value asynchronously to the other two replicas. Whenever it recieves the value of its replica, it adds it to its current value. If two values are received concurrently, both will be added together to its current value. So merging replicas in this example becomes trivial.

Let's take a look at another interesting generalization of this. Integer Vector


We can make an interesting observation from the previous examples:
    
__*All distributed data structures don't need conflict resolution*__

This raises the following question:
    
__*How can we design a distributed structure such that we don't need conflict resolution?*__

The answer to this question lies in an algebraic structure called the **join semilattice**.

## Join Semilattice
A join-semilattice or upper semilattice is a *partial order* `≤` with a *least upper bound* (LUB) `⊔` for all pairs.
`m = x ⊔ y` is a Least Upper Bound of `{` `x` `,` `y` `}` under `≤` iff `∀m′, x ≤ m′ ∧ y ≤ m′ ⇒ x ≤ m ∧ y ≤ m ∧ m ≤ m′`.

`⊔` is:

**Associative**

`(x ⊔ y) ⊔ z = x ⊔ (y ⊔ z)`

**Commutative**

`x ⊔ y = y ⊔ x`

**Idempotent**

`x ⊔ x = x`

The examples we saw earlier were of structures that could be modeled as join semilattices. The merge operation for the increment only counter is the summation function and for the integer vector it is the per-index maximum of the vectors being merged.
So, if we can model the state of the data structure as a partially ordered set and design the merge operation to always compute the "larger" of the two states, its replicas will never need consensus. They will always converge as execution proceeds. Such data structures are called CRDTs (Conflict-free Replicated Data Type). But what about consistency of these replicas?

## Strong Eventual Consistency (SEC)
We discussed a notion of consistency, *Eventual Consistency*, in which replicas eventually become consistent if there are no more updates to be merged. But the update operation is left unspecified. Its possible for an update to render the replica in a state that causes it to conflict with a later update. In this case the replica may have to roll back and use consensus to ensure that all replicas do the same to ensure consistency. This is complicated and wasteful. But if replicas are modeled as CRDTs, the updates never conflict. Regardless of the order in which the updates are applied, all replicas will eventually have equivalent state. Note that no conflict arbitration is necessary. This kind of Eventual Consistency is a stronger notion of consistency than the one that requires conflict arbitration and hence is called *Strong Eventual Consistency*.

### Strong Eventual Consistency and CAP Theorem

Let's study SEC data objects from the perspective of CAP theorem.

#### 1. Consistency and Network Partition
Each distributed replica will communicate asynchronously with other reachable replicas. These replicas will eventually converge to the same value. There is no consistency guarantee on the value of replicas not reachable due to network conditions and hence this condition is strictly weaker than strong consistency. But as soon as those replicas can be reached, they will also converge in a self-stabilizing manner.

#### 2. Availability and Network Partition
Each distributed replica will always be available for local reads and writes regardless of network partitions. In fact, if there are n replicas, a single replica will function even if the remaining n - 1 replicas crash simultaneously. This **provides an extreme form of availability**. 

SEC facilitates maximum consistency and availability in the event of network partitions by relaxing the requirement of global consistency. Note that this is achieved by virtue of modeling the data objects as join semilattices.

#### Strong Eventual Consistency and Linearizability
In a distributed setting, a replica has to handle concurrent updates. In addition to its sequential behavior, a CRDT also has to ensure that its concurrent behavior also ensures strong eventual consistency. This makes it possible for CRDTs to exhibit behavior that is simply not possible for sequentially consistent objects. 
Consider a set CRDT used in a distributed setting. One of the replicas p<sub>i</sub> executes the sequence `add(a); remove(b)`. Another replica p<sub>j</sub> executes the sequence `add(b); remove(a)`. Now both send their states asynchronously to another replica p<sub>k</sub> which has to merge them concurrently. Same element exists in one of the sets and does not exist in the other set. There are multiple choices that the CRDT designer can make. Let's assume that the implementation always prefers inclusion over exclusion. So in this case, p<sub>k</sub> will include both `a` and `b`.
Now consider a sequential execution of the two sequences on set data structure. The order of execution will be either `add(a); remove(b); add(b); remove(a)` or `add(b); remove(a); add(a); remove(b)`. In both cases one of the elements is excluded. This is different from the state of the CRDT set implementation. 
Thus, strong eventually consistent data structures can be sequentially inconsistent.
Similarly, if there are `n` sequentially consistent replicas, then they would need consensus to ensure a single order of execution of operations across all replicas. But if `n - 1` replicas crash, then consensus cannot happen. This makes the idea of sequential consistency incomparable to that of strong eventual consistency.

## What Next?
This chapter introduced Strong Eventual Consistency and the formalism behind CRDTs, join semilattices, which enables CRDTs to exhibit strong eventual consistency. The discussion however does not answer an important question:

__*Can all standard data structures be designed as CRDTs?*__

The next chapter sheds more light on the design of CRDTs and attempts to answer this question.
