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

### CmRDT: Operation based specification

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

    def decrement(self):        # update function
        self._count -= 1
        for replica in self.replicas():
            self.transmit("decrement", replica)

```

#### Figure

![Operation based increment and decrement counter][operation-based-increment-and-decrement-counter]

### CvRDT: State based specification

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

    def decrement(self):                # update function
        self._counts[self.replicaId()] -= 1

    def compare(self, other):           # comparison function
        return all(v1 <= v2 for (v1, v2) in
                   zip(self.counts(),
                       other.counts()))

    def merge(self, other):             # merge function
        return Counter(map(max, zip(self.counts(),
                                    other.counts())))

```

#### Figure

![State based increment and decrement counter (incorrect)][state-based-increment-and-decrement-counter-incorrect]



#### Specification

```python

class CvRDT:
    pass

class Counter(CvRDT):

    def __init__(self,
                 increments = None,
                 decrements = None):   # constructor function
        if increments is None:
            self._increments = [0] * length(replicas())
        else:
            self._increments = increments
        if decrements is None:
            self._decrements = [0] * length(replicas())
        else:
            self._decrements = decrements

    def increments(self):               # query function
        return list(self._increments)   # return a clone

    def decrements(self):               # query function
        return list(self._decrements)   # return a clone

    def value(self):                    # query function
        return (sum(self.increments()) -
                sum(self.decrements()))

    def increment(self):                # update function
        self._increments[self.replicaId()] += 1

    def decrement(self):                # update function
        self._decrements[self.replicaId()] += 1

    def compare(self, other):           # comparison function
        return (all(v1 <= v2 for (v1, v2) in
                    zip(self.increments(),
                        other.increments()))
                and
                all(v1 <= v2 for (v1, v2) in
                    zip(self.decrements(),
                        other.decrements())))

    def merge(self, other):             # merge function
        return Counter(increments = map(max, zip(self.increments(),
                                                 other.increments())),
                       decrements = map(max, zip(self.decrements(),
                                                 other.decrements())))

```

#### Figure

![State based increment and decrement counter (correct)][state-based-increment-and-decrement-counter-correct]


[operation-based-increment-only-counter]: resources/images/counters/operation-based-increment-only-counter.png
[state-based-increment-only-counter-incorrect]: resources/images/counters/state-based-increment-only-counter-incorrect.png
[state-based-increment-only-counter-correct]: resources/images/counters/state-based-increment-only-counter-correct.png
[operation-based-increment-and-decrement-counter]: resources/images/counters/operation-based-increment-and-decrement-counter.png
[state-based-increment-and-decrement-counter-incorrect]: resources/images/counters/state-based-increment-and-decrement-counter-incorrect.png
[state-based-increment-and-decrement-counter-correct]: resources/images/counters/state-based-increment-and-decrement-counter-correct.png
