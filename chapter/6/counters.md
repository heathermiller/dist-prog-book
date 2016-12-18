---
layout: page
title:  "Counters"
by: "Aviral Goel"
---

Counters are replicated integers. They are the most basic distributed object. This chapter describes the different variations of counter CRDT in both state based and operation based form.

## G-counter - Increment only counter

As the name suggests, these counters only support increment operation. They can be used to implement the `like` button functionality of social media websites.

### CmRDT: Operation based G-counter

In the operation based implementation, the increment operation is transmitted to all other replicas. 
This is straightforward to implement as there is only one update operation. 

#### Specification

```python

class CmRDT:
    pass

class Counter(CmRDT):

    def __init__(self):         # constructor function
        self._count = 0

    def value(self):            # query function
        return self._count

    def increment(self):        # update function
        self._count += 1
        for replica in self.replicas():
            self.transmit("increment", replica)

```

#### Figure

![Operation based increment only counter][operation-based-increment-only-counter]

The figure above shows three replicas (<b>c<sub>1</sub></b>, <b>c<sub>2</sub></b> and <b>c<sub>3</sub></b>) of an operation based increment only counter <b>C<sub>operation</sub></b>. The clients issue increment requests depicted as <increment-request>. In accordance with the specification, each increment request increments the counter by 1 unit and the operation is transmitted by the replica to all other replicas of the system. 
There are a few interesting observations:

* **Eventually consistent** - At *t<sub>16</sub>*, the replicas are inconsistent. Eventually, they all attain consistency. This is because the increment operation happens immediately at one replica but takes time to be transmitted over the network to other replicas. Within this duration, the replicas may be inconsistent.

* **Reliable broadcast** - The increment operation has to be transmitted to all replicas. If the network fails to deliver the operation, the system will never be able to achieve consistency.

* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>19</sub>*, <b>c<sub>1</sub></b> encounters two increment operations. Since the increment operation commutes with itself, the order does not matter. The replica can decide to handle the increments in arbitrary order.


### CvRDT: State based specification

In the state based implementation, the counter state is transmitted to all other replicas.
But how do we model the state? Of course, the counter's count is its state. 
Since the count always increases, modeling the state as count automatically makes it a monotonic semilattice.

#### Specification

```python

class CvRDT:
    pass

class Counter(CvRDT):

    def __init__(self, count = 0):  # constructor function
        self._count = count

    def value(self):                # query function
        return self._count

    def increment(self):            # update function
        self._count += 1

    def compare(self, other):       # comparison function
        return self.value() <= other.value()

    def merge(self, other):         # merge function
        return Counter(max(self.value(), other.value()))

```

#### Figure

![State based increment only counter (incorrect)][state-based-increment-only-counter-incorrect]
The figure above shows three replicas (<b>c<sub>1</sub></b>, <b>c<sub>2</sub></b> and <b>c<sub>3</sub></b>) of a state based increment only counter <b>C<sub>state</sub></b>. The clients issue increment requests depicted as <increment-request>. In accordance with the specification, each increment request increments the counter by 1 unit.  and the operation is transmitted by the replica to all other replicas of the system. 
There are a few interesting observations:

* **Eventual convergence** - At *t<sub>26</sub>*, the replicas are inconsistent. Eventually, they all converge. This is because the increment operation happens immediately at one replica but takes time to be transmitted over the network to other replicas. Within this duration, the replicas may be inconsistent.

> Eventual convergence does not guarantee correctness.

> Incorrect design may still converge eventually.

* **Unreliable broadcast** - Messages may be lost increment operation has to be transmitted to all replicas. If the network fails to deliver the operation, the system will never be able to achieve consistency.

* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>19</sub>*, <b>c<sub>1</sub></b> encounters two increment operations. Since the increment operation commutes with itself, the order does not matter. The replica can decide to handle the increments in arbitrary order.

As it can be seen from the figure, the clients issue a total of 4 increment requests. However, the replicas finally converge to 2.
Something is clearly amiss! When two replicas are incremented, they should together converge to 2. But the `merge` function computes the maximum of two states. 


#### Specification

```python

class CvRDT:
    pass

class Counter(CvRDT):

    def __init__(self, counts = None):  # constructor function
        if counts is None:
            self._counts = [0] * length(self.replicas())
        else:
            self._counts = counts

    def value(self):                    # query function
        return sum(self._counts)

    def counts(self):                   # query function
        return list(self._counts)       # return a clone

    def increment(self):                # update function
        self._counts[self.replicaId()] += 1

    def compare(self, other):           # comparison function
        return all(v1 <= v2 for (v1, v2) in
                   zip(self.counts(),
                       other.counts()))

    def merge(self, other):             # merge function
        return Counter(map(max, zip(self.counts(),
                                    other.counts())))

```

#### Figure

![State based increment only counter (correct)][state-based-increment-only-counter-correct]

As it can be seen from the figure, the clients issue a total of 4 increment requests. However, the replicas finally converge to 2.
Something is clearly amiss! When two replicas are incremented, they should together converge to 2. But the `merge` function computes the maximum of two states. 

## PN-counter - Increment and Decrement counter

A PN-counter can be incremented and decremented.

### CmRDT: Operation based specification

The code below provides the specification of an operation based increment and decrement counter.

<pre style="background:#fff;color:#000">

<span style="color:#ff5600">class</span> <span style="color:#21439c">Counter</span>(CmRDT):

    <span style="color:#ff5600">def</span> <span style="color:#21439c"><span style="color:#a535ae">__init__</span></span>(self):         <span style="color:#919191"># constructor function</span>
        self._count <span style="color:#ff5600">=</span> 0

    <span style="color:#ff5600">def</span> <span style="color:#21439c">value</span>(self):            <span style="color:#919191"># query function</span>
        <span style="color:#ff5600">return</span> self._count

    <span style="color:#ff5600">def</span> <span style="color:#21439c">increment</span>(self):        <span style="color:#919191"># update function</span>
        self._count <span style="color:#ff5600">+=</span> 1
        <span style="color:#ff5600">for</span> replica <span style="color:#ff5600">in</span> self.replicas():
            self.transmit(<span style="color:#00a33f">"increment"</span>, replica)

    <span style="color:#ff5600">def</span> <span style="color:#21439c">decrement</span>(self):        <span style="color:#919191"># update function</span>
        self._count <span style="color:#ff5600">-=</span> 1
        <span style="color:#ff5600">for</span> replica <span style="color:#ff5600">in</span> self.replicas():
            self.transmit(<span style="color:#00a33f">"decrement"</span>, replica)
</pre>

Let's try to understand how it works through an example. The figure below shows three replicas (<b>c<sub>1</sub></b>, <b>c<sub>2</sub></b> and <b>c<sub>3</sub></b>) of an operation based increment and decrement counter <b>C<sub>operation</sub></b>. 

* ![increment operation][increment-operation] depicts increment request issued by the client.
* ![decrement operation][decrement-operation] depicts decrement request issued by the client.

In accordance with the specification, each increment request increments the counter locally by one unit and each decrement request decrements the counter locally by one unit. The corresponding operation is transmitted by the replica to all other replicas of the system. 

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/operation-based-increment-and-decrement-counter.png" alt="Operation based increment and decrement counter"/>
</figure>

One can make the the following observations:

* **Eventually consistent** - At *t<sub>26</sub>*, the replicas are inconsistent. Eventually, they all achieve consistency. This is because the operations happen immediately at one replica but take time to be transmitted over the network to other replicas. Within this duration, the replicas may be inconsistent.
* **Reliable broadcast** - The operations have to be transmitted to all replicas. If the network fails to deliver an operation, the system will never be able to achieve consistency.
* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>30</sub>*, <b>c<sub>1</sub></b> and <b>c<sub>2</sub></b> encounter increment and decrement operations concurrently. Since the increment and decrement  operations commute, the order in which they are executed by the replicas does not matter. Both replicas perform them in different orders and still achieve consistency, eventually.

### CvRDT: State based specification

The code below provides the specification of a state based increment and decrement counter.

<pre style="background:#fff;color:#000"><span style="color:#ff5600">class</span> <span style="color:#21439c">Counter</span>(CvRDT):

    <span style="color:#ff5600">def</span> <span style="color:#21439c"><span style="color:#a535ae">__init__</span></span>(self, counts <span style="color:#ff5600">=</span> <span style="color:#a535ae">None</span>):  <span style="color:#919191"># constructor function</span>
        <span style="color:#ff5600">if</span> counts <span style="color:#ff5600">is</span> <span style="color:#a535ae">None</span>:
            self._counts <span style="color:#ff5600">=</span> [0] <span style="color:#ff5600">*</span> length(self.replicas())
        <span style="color:#ff5600">else</span>:
            self._counts <span style="color:#ff5600">=</span> counts

    <span style="color:#ff5600">def</span> <span style="color:#21439c">value</span>(self):                    <span style="color:#919191"># query function</span>
        <span style="color:#ff5600">return</span> <span style="color:#a535ae">sum</span>(self._counts)

    <span style="color:#ff5600">def</span> <span style="color:#21439c">counts</span>(self):                   <span style="color:#919191"># query function</span>
        <span style="color:#ff5600">return</span> <span style="color:#a535ae">list</span>(self._counts)       <span style="color:#919191"># return a clone</span>

    <span style="color:#ff5600">def</span> <span style="color:#21439c">increment</span>(self):                <span style="color:#919191"># update function</span>
        self._counts[self.replicaId()] <span style="color:#ff5600">+=</span> 1

    <span style="color:#ff5600">def</span> <span style="color:#21439c">decrement</span>(self):                <span style="color:#919191"># update function</span>
        self._counts[self.replicaId()] <span style="color:#ff5600">-=</span> 1

    <span style="color:#ff5600">def</span> <span style="color:#21439c">compare</span>(self, other):           <span style="color:#919191"># comparison function</span>
        <span style="color:#ff5600">return</span> <span style="color:#a535ae">all</span>(v1 <span style="color:#ff5600">&lt;=</span> v2 <span style="color:#ff5600">for</span> (v1, v2) <span style="color:#ff5600">in</span>
                   <span style="color:#a535ae">zip</span>(self.counts(),
                       other.counts()))

    <span style="color:#ff5600">def</span> <span style="color:#21439c">merge</span>(self, other):             <span style="color:#919191"># merge function</span>
        <span style="color:#ff5600">return</span> Counter(<span style="color:#a535ae">map</span>(<span style="color:#a535ae">max</span>, <span style="color:#a535ae">zip</span>(self.counts(),
                                    other.counts())))

</pre>

Let's try to understand how it works through an example. The figure below shows three replicas (<b>c<sub>1</sub></b>, <b>c<sub>2</sub></b> and <b>c<sub>3</sub></b>) of a state based increment and decrement counter <b>C<sub>state</sub></b>. 

* ![increment operation][increment-operation] depicts increment request issued by the client.
* ![decrement operation][decrement-operation] depicts decrement request issued by the client.

In accordance with the specification, each increment request increments the counter by one unit and each decrement request decrements the counte by one unit. The replica transmits its state at random times to a random replica.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-and-decrement-counter-incorrect.png" alt="State based increment and decrement counter (incorrect)"/>
</figure>

We can make the the following observations:

* **Eventual convergence** - At *t<sub>26</sub>*, the replicas are inconsistent. Eventually, they all converge. This is because the increment operation happens immediately at one replica but takes time to be transmitted over the network to other replicas. Within this duration, the replicas may be inconsistent.
* **Correctness** - The clients issue a total of four increment requests and 2 decrement requests. But the eventually consistent value of replicas is 4. So, the design is **incorrect**.
* **Concurrent operations** - A replica may have to handle concurrent operations. For example, at *t<sub>27</sub>* <b>c<sub>1</sub></b> has to handle 2 merge operations concurrently. Since the state forms a partially ordered set and the merge operation computes its least upper bound, the order in which the merge operation happens does not affect the final outcome. Similarly, at *t<sub>21</sub>* and *t<sub>29</sub>*, two operations arrive concurrently at <b>c<sub>3</sub></b> and <b>c<sub>2</sub></b> respectively.
* **Unreliable broadcast** - Messages may be lost during transmission. Message sent by <b>c<sub>3</sub></b> at *t<sub>12</sub>* is lost. But eventually, message at *t<sub>25</sub>* reaches another replica. As long as messages eventually reach other replicas, directly or indirectly, the system will achieve consistency. A message can also be received out of order or duplicated. 

Let's try to figure out why the design is incorrect. At *t<sub>12</sub>*, <b>c<sub>1</sub></b> merges the state from <b>c<sub>2</sub></b>. The merge operation computes the index wise maximum in accordance with the specification. In doing so, the *-1* value of *c<sub>2</sub>* due to the decrement operation at *t<sub>6</sub>* is lost. Its clear that we have violated the basic constraint, the decrement operation does not take the state higher up in the lattice. In other words, the decrement operation is non monotonic. This causes us to lose the decrements and we are eventually left with replicas which only count the total number of increment requests.
But we do gain two valuable insights from this design-

> Eventual convergence does not guarantee correctness.

> Incorrect designs may still converge eventually.


Let's try to correct this problem. The problem happens because the decrement operation is non-monotonic. So we need a way to count the decrement operations without losing monotonicity. One solution is to model this counter using two increment only counters. The first counter counts the increment operations and the second one counts the decrement operations. The value of the actual counter is the difference between the two corresponding counters. The specification below shows how this can be implemented.

<pre style="background:#fff;color:#000"><span style="color:#ff5600">class</span> <span style="color:#21439c">Counter</span>(CvRDT):

    <span style="color:#ff5600">def</span> <span style="color:#21439c"><span style="color:#a535ae">__init__</span></span>(self,
                 increments <span style="color:#ff5600">=</span> <span style="color:#a535ae">None</span>,
                 decrements <span style="color:#ff5600">=</span> <span style="color:#a535ae">None</span>):   <span style="color:#919191"># constructor function</span>
        <span style="color:#ff5600">if</span> increments <span style="color:#ff5600">is</span> <span style="color:#a535ae">None</span>:
            self._increments <span style="color:#ff5600">=</span> [0] <span style="color:#ff5600">*</span> length(replicas())
        <span style="color:#ff5600">else</span>:
            self._increments <span style="color:#ff5600">=</span> increments
        <span style="color:#ff5600">if</span> decrements <span style="color:#ff5600">is</span> <span style="color:#a535ae">None</span>:
            self._decrements <span style="color:#ff5600">=</span> [0] <span style="color:#ff5600">*</span> length(replicas())
        <span style="color:#ff5600">else</span>:
            self._decrements <span style="color:#ff5600">=</span> decrements

    <span style="color:#ff5600">def</span> <span style="color:#21439c">increments</span>(self):               <span style="color:#919191"># query function</span>
        <span style="color:#ff5600">return</span> <span style="color:#a535ae">list</span>(self._increments)   <span style="color:#919191"># return a clone</span>

    <span style="color:#ff5600">def</span> <span style="color:#21439c">decrements</span>(self):               <span style="color:#919191"># query function</span>
        <span style="color:#ff5600">return</span> <span style="color:#a535ae">list</span>(self._decrements)   <span style="color:#919191"># return a clone</span>

    <span style="color:#ff5600">def</span> <span style="color:#21439c">value</span>(self):                    <span style="color:#919191"># query function</span>
        <span style="color:#ff5600">return</span> (<span style="color:#a535ae">sum</span>(self.increments()) <span style="color:#ff5600">-</span>
                <span style="color:#a535ae">sum</span>(self.decrements()))

    <span style="color:#ff5600">def</span> <span style="color:#21439c">increment</span>(self):                <span style="color:#919191"># update function</span>
        self._increments[self.replicaId()] <span style="color:#ff5600">+=</span> 1

    <span style="color:#ff5600">def</span> <span style="color:#21439c">decrement</span>(self):                <span style="color:#919191"># update function</span>
        self._decrements[self.replicaId()] <span style="color:#ff5600">+=</span> 1

    <span style="color:#ff5600">def</span> <span style="color:#21439c">compare</span>(self, other):           <span style="color:#919191"># comparison function</span>
        <span style="color:#ff5600">return</span> (<span style="color:#a535ae">all</span>(v1 <span style="color:#ff5600">&lt;=</span> v2 <span style="color:#ff5600">for</span> (v1, v2) <span style="color:#ff5600">in</span>
                    <span style="color:#a535ae">zip</span>(self.increments(),
                        other.increments()))
                <span style="color:#ff5600">and</span>
                <span style="color:#a535ae">all</span>(v1 <span style="color:#ff5600">&lt;=</span> v2 <span style="color:#ff5600">for</span> (v1, v2) <span style="color:#ff5600">in</span>
                    <span style="color:#a535ae">zip</span>(self.decrements(),
                        other.decrements())))

    <span style="color:#ff5600">def</span> <span style="color:#21439c">merge</span>(self, other):             <span style="color:#919191"># merge function</span>
        <span style="color:#ff5600">return</span> Counter(increments <span style="color:#ff5600">=</span> <span style="color:#a535ae">map</span>(<span style="color:#a535ae">max</span>, <span style="color:#a535ae">zip</span>(self.increments(),
                                                 other.increments())),
                       decrements <span style="color:#ff5600">=</span> <span style="color:#a535ae">map</span>(<span style="color:#a535ae">max</span>, <span style="color:#a535ae">zip</span>(self.decrements(),
                                                 other.decrements())))

</pre>

The figure below shows an execution trace of three replicas (<b>c<sub>1</sub></b>, <b>c<sub>2</sub></b> and <b>c<sub>3</sub></b>) of this counter.

* ![increment operation][increment-operation] depicts increment request issued by the client.
* ![decrement operation][decrement-operation] depicts decrement request issued by the client.

The values in the top row in the replica state depict the increments and the bottom ones depict the decrements. In accordance with the specification, each increment request increments the value in the top row by one unit and each decrement request increments the value in the lower row by one unit. Once the operation materializes locally, the new state is transmitted by the replica to some other randomly chosen replica.

<figure class="fullwidth">
    <img src="{{ site.baseurl }}/chapter/6/resources/images/counters/state-based-increment-and-decrement-counter-correct.png" alt="State based increment and decrement counter (correct)"/>
</figure>

This design converges to the correct value.


[increment-operation]: resources/images/counters/increment-operation.png
[decrement-operation]: resources/images/counters/decrement-operation.png
[operation-based-increment-only-counter]: resources/images/counters/operation-based-increment-only-counter.png
[state-based-increment-only-counter-incorrect]: resources/images/counters/state-based-increment-only-counter-incorrect.png
[state-based-increment-only-counter-correct]: resources/images/counters/state-based-increment-only-counter-correct.png
[operation-based-increment-and-decrement-counter]: resources/images/counters/operation-based-increment-and-decrement-counter.png
[state-based-increment-and-decrement-counter-incorrect]: resources/images/counters/state-based-increment-and-decrement-counter-incorrect.png
[state-based-increment-and-decrement-counter-correct]: resources/images/counters/state-based-increment-and-decrement-counter-correct.png
