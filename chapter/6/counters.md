---
layout: page
title:  "Counters"
by: "Aviral Goel"
---

Counters are replicated integers. They are the most basic distributed object. This chapter describes the different variations of counter CRDT in both state based and operation based form.

## G-counter - Increment only counter

As the name suggests, these counters only support increment operation. They can be used to implement the `like` button functionality of social media websites.

### CmRDT: Operation based design

In the operation based implementation, the increment operation is transmitted to all other replicas. 
This is straightforward to implement as there is only one update operation. 

```python
class Counter(CmRDT):
    def __init__(self):
        self._count = 0

    def value(self): 
        return self._count

    def increment(self):
        self._count += 1
        for replica in self.replicas():
            self.transmit("increment", replica)
```

Let's try to understand how it works through an example. The figure below shows an execution trace of three replicas confirming to this specification. In accordance with the specification, each increment request increments the counter locally by one unit and the operation is transmitted by the replica to all other replicas of the system.

<figure class="fullwidth">
    <img style="margin: auto; display: block;" src="{{ site.baseurl }}/chapter/6/resources/images/counters/operation-based-increment-only-counter.png" alt="Operation based increment only counter"/>
</figure>

We can make the following observations:

* **Eventually consistent** - At *t<sub>16</sub>*, the replicas are inconsistent. Eventually, they all attain consistency. This is because the increment operation happens immediately at one replica but takes time to be transmitted over the network to other replicas. Within this duration, the replicas may be inconsistent.

* **Reliable broadcast** - The increment operation has to be transmitted to all replicas. If the network fails to deliver the operation, the system will never be able to achieve consistency. For example - if the increment operation on **c<sub>2</sub>** at *t<sub>11</sub>* is not transmitted reliably to **c<sub>1</sub>**, then its value will always be one unit less than the correct value.

* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>19</sub>*, <b>c<sub>1</sub></b> encounters two increment operations. Since its the same operation, there is only one way to handle the situation. There is no conflict.

### CvRDT: State based design

In the state based implementation, the counter state is transmitted to all other replicas.
But how do we model the state? Of course, the counter's count is its state. 
Since the count always increases, modeling the state as count automatically makes it a join semilattice.

The code below provides the specification of this counter.

```python
class Counter(CvRDT):
    def __init__(self, count = 0):  
        self._count = count

    def value(self):                
        return self._count

    def increment(self):            
        self._count += 1

    def compare(self, other):       
        return self.value() <= other.value()

    def merge(self, other):         
        return Counter(max(self.value(), other.value()))
```

Let's try to understand how it works through an example. The figure below shows an execution trace of three replicas confirming to this specification. The replicas keep transmitting their state at random times to other randomly chosen replicas.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-only-counter-incorrect.png" alt="State based increment only counter (incorrect)"/>
</figure>

We can make the following observations:

* **Eventual convergence** - At *t<sub>26</sub>*, the replicas are inconsistent. Eventually, they all converge. This is because the replicas transmit state at random times to randomly chosen replicas. Until their states are merged, the replicas may be inconsistent.

* **Correctness** - The clients issue a total of four increment requests. But the eventually consistent value of replicas is 4. So, the design is **incorrect**.

* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>28</sub>*, <b>c<sub>1</sub></b> receives states of the other two replicas. Since the merge operation is commutative, the order in which these operations are handled does not matter.

* **Unreliable broadcast** - Messages may be lost during transmission. Message sent by <b>c<sub>2</sub></b> at *t<sub>9</sub>* is lost. But eventually, some messages from <b>c<sub>2</sub></b> reach other replicas. As long as messages eventually reach other replicas, directly or indirectly, the system will achieve consistency. A message can also be received out of order or duplicated. 

Let's figure out why our design is incorrect. We notice that the merge operation simply compares the state of the replicas and returns the bigger of the two counts. What we really need is to add the two counts as we need the total counts issued by all clients across all replicas. But this poses another problem. The merge operation is no longer idempotent, i.e. - repeated merging of same values will not return the same result. This means that if a message gets duplicated, then we will get incorrect count. What's more is that the merge operation will no longer compute the **least** upper bound. It will compute an upper bound but that will not be the least upper bound. This clearly violates the mathematical model we set out to implement. So we can't modify our merge method. This means that we need to change our representation of the state.
Let's observe the problem again. Our merge method only returns the state of that replica which handled the maximum number of counts. It loses counts of other replicas. Let's represent the state as a sequence of counts. Each value in the sequence corresponds to the count of a replica. So we have as many values in a state as the number of replicas. We also design the merge operation to compute the index-wise maximum of the state.

The specification below shows how this can be implemented.

```python
class Counter(CvRDT):
    def __init__(self, counts = None):
        if counts is None:
            self._counts = [0] * length(self.replicas())
        else:
            self._counts = counts

    def value(self):
        return sum(self._counts)

    def counts(self):
		# return a copy of the counts
        return list(self._counts)

    def increment(self):
        self._counts[self.replicaId()] += 1

    def compare(self, other):
        return all(v1 <= v2 for (v1, v2) in
                   zip(self.counts(),
                       other.counts()))

    def merge(self, other):
        return Counter(map(max, zip(self.counts(),
                                    other.counts())))
```

The figure below shows an execution trace of three replicas confirming to this specification.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-only-counter-correct.png" alt="State based increment only counter (correct) lattice"/>
</figure>

This design converges to the correct value. This provides us an eventually consistent state based increment only counter.

## PN-counter - Increment and Decrement counter

A PN-counter can be incremented and decremented. These can serve as a general purpose counters, as they also provide a decrement operation. For example - counting the number of users active one a social media website at any point. Note that the users can go offline and the counter will have to decremented. This can't be done with an increment only counter.

### CmRDT: Operation based design

The code below provides the specification of an operation based increment and decrement counter.

```python
class Counter(CmRDT):
    def __init__(self):
        self._count = 0

    def value(self):
        return self._count

    def increment(self):
        self._count += 1
        for replica in self.replicas():
            self.transmit("increment", replica)

    def decrement(self):
        self._count -= 1
        for replica in self.replicas():
            self.transmit("decrement", replica)
```

Let's try to understand how it works through an example. The figure below shows an execution trace of three replicas confirming to this specification. In accordance with the specification, each increment request increments the counter locally by one unit and each decrement request decrements the counter locally by one unit. The corresponding operation is transmitted by the replica to all other replicas of the system. 

<figure class="fullwidth">
    <img style="margin: auto; display: block;" src="{{ site.baseurl }}/chapter/6/resources/images/counters/operation-based-increment-and-decrement-counter.png" alt="Operation based increment and decrement counter"/>
</figure>

We can make the the following observations:

* **Eventual Consistency** - At *t<sub>26</sub>*, the replicas are inconsistent. Eventually, they all achieve consistency. This is because the operations happen immediately at one replica but take time to be transmitted over the network to other replicas. Within this duration, the replicas may be inconsistent.

* **Reliable broadcast** - Each operation has to be transmitted to all replicas. If the network fails to deliver an operation, the system will never be able to achieve consistency. For example - if the decrement operation on **c<sub>2</sub>** at *t<sub>6</sub>* is not transmitted reliably to **c<sub>1</sub>**, then its value will always be one unit more than the correct value.

* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>30</sub>*, <b>c<sub>1</sub></b> and <b>c<sub>2</sub></b> encounter increment and decrement operations concurrently. Let's take a look at the two choices:

<figure class="fullwidth">
    <img style="margin: auto; display: block;" src="{{ site.baseurl }}/chapter/6/resources/images/counters/increment-and-decrement-operations-commute.png" alt="Increment and decrement operations commute"/>
</figure>

In both cases the result is same because the two operations commute, i.e. - the order in which they are executed by the replicas does not matter. Both replicas perform them in different orders and still achieve consistency, eventually.

### CvRDT: State based design

The code below provides the specification of a state based increment and decrement counter. We take inspiration from the design of state based increment only counter and model the state of this counter in the same way.

```python
class Counter(CvRDT):

    def __init__(self, counts = None):
        if counts is None:
            self._counts = [0] * length(self.replicas())
        else:
            self._counts = counts

    def value(self):
        return sum(self._counts)

    def counts(self):
		# return a copy of the counts
        return list(self._counts)

    def increment(self):
        self._counts[self.replicaId()] += 1

    def decrement(self):
        self._counts[self.replicaId()] -= 1

    def compare(self, other):
        return all(v1 <= v2 for (v1, v2) in
                   zip(self.counts(),
                       other.counts()))

    def merge(self, other):
        return Counter(map(max, zip(self.counts(),
                                    other.counts())))
```

Let's try to understand how it works through an example. The figure below shows an execution trace of three replicas confirming to this specification. The replicas keep transmitting their state at random times to other randomly chosen replicas.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-and-decrement-counter-incorrect.png" alt="State based increment and decrement counter (incorrect)"/>
</figure>

We can make the the following observations:

* **Eventual convergence** - At *t<sub>26</sub>*, the replicas are inconsistent. Eventually, they all converge. This is because the replicas transmit state at random times to randomly chosen replicas. Until their states are merged, the replicas may be inconsistent.

* **Correctness** - The clients issue a total of four increment requests and 2 decrement requests. But the eventually consistent value of replicas is 4. So, the design is **incorrect**.

* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>27</sub>* <b>c<sub>1</sub></b> has to handle 2 merge operations concurrently. Since the state forms a partially ordered set and the merge operation computes its least upper bound, the order in which the merge operation happens does not affect the final outcome. Similarly, at *t<sub>21</sub>* and *t<sub>29</sub>*, two operations arrive concurrently at <b>c<sub>3</sub></b> and <b>c<sub>2</sub></b> respectively.

* **Unreliable broadcast** - Messages may be lost during transmission. Message sent by <b>c<sub>3</sub></b> at *t<sub>12</sub>* is lost. But eventually, message at *t<sub>25</sub>* reaches another replica. As long as messages eventually reach other replicas, directly or indirectly, the system will achieve consistency. A message can also be received out of order or duplicated. 

Though we modeled the state after the increment only state based counter, this design doesn't work. Let's try to figure out what went wrong. At *t<sub>12</sub>*, <b>c<sub>1</sub></b> merges the state from <b>c<sub>2</sub></b>. The merge operation computes the index wise maximum in accordance with the specification. In doing so, the *-1* value of *c<sub>2</sub>* due to the decrement operation at *t<sub>6</sub>* is lost. 
To make matters clearer, let's look at a section of the lattice formed by the state of this counter -

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-and-decrement-counter-incorrect-lattice.png" alt="State based increment and decrement counter(incorrect) lattice"/>
</figure>

Its clear that we have violated the basic constraint, the decrement operation does not take the state higher up in the lattice. In other words, the decrement operation is non monotonic. So, when the results of increment and decrement operations are merged together, then the result of the increment operation is returned, as it is always higher up in the lattice. So the replicas only count the total number of increments.

But we do gain two valuable insights from this design-

> Eventual convergence does not guarantee correctness.

> Incorrect designs may still converge eventually.


Let's try to correct this problem. We need a way to count the decrement operations without losing monotonicity. One solution is to model this counter using two increment only counters. The first counter counts the increment operations and the second one counts the decrement operations. The value of the actual counter is the difference between the two corresponding counters. The specification below shows how this can be implemented.

```python
class Counter(CvRDT):
    def __init__(self,
                 increments = None,
                 decrements = None):
        if increments is None:
            self._increments = [0] * length(replicas())
        else:
            self._increments = increments
        if decrements is None:
            self._decrements = [0] * length(replicas())
        else:
            self._decrements = decrements

    def increments(self):
		# return a copy of the increments
        return list(self._increments)

    def decrements(self):
		# return a copy of the decrements
        return list(self._decrements)

    def value(self):
        return (sum(self.increments()) -
                sum(self.decrements()))

    def increment(self):
        self._increments[self.replicaId()] += 1

    def decrement(self):
        self._decrements[self.replicaId()] += 1

    def compare(self, other):
        return (all(v1 <= v2 for (v1, v2) in
                    zip(self.increments(),
                        other.increments()))
                and
                all(v1 <= v2 for (v1, v2) in
                    zip(self.decrements(),
                        other.decrements())))

    def merge(self, other):
        return Counter(
			increments = map(max, zip(self.increments(),
                                      other.increments())),
            decrements = map(max, zip(self.decrements(),
                                      other.decrements())))
```

The figure below shows an execution trace of three replicas confirming to this specification.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-and-decrement-counter-correct.png" alt="State based increment and decrement counter (correct)"/>
</figure>

This design converges to the correct value. This provides us an eventually consistent state based increment and decrement counter. We can take a look at the lattice formed by the state to convince ourselves.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-and-decrement-counter-correct-lattice.png" alt="State based increment and decrement counter(correct) lattice"/>
</figure>

## References

{% bibliography --file counters %}

[increment-operation]: resources/images/counters/increment-operation.png
[decrement-operation]: resources/images/counters/decrement-operation.png
[operation-based-increment-only-counter]: resources/images/counters/operation-based-increment-only-counter.png
[state-based-increment-only-counter-incorrect]: resources/images/counters/state-based-increment-only-counter-incorrect.png
[state-based-increment-only-counter-correct]: resources/images/counters/state-based-increment-only-counter-correct.png
[operation-based-increment-and-decrement-counter]: resources/images/counters/operation-based-increment-and-decrement-counter.png
[state-based-increment-and-decrement-counter-incorrect]: resources/images/counters/state-based-increment-and-decrement-counter-incorrect.png
[state-based-increment-and-decrement-counter-correct]: resources/images/counters/state-based-increment-and-decrement-counter-correct.png
