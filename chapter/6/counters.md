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


#### Figure

![Operation based increment only counter][operation-based-increment-only-counter]


### CvRDT: State based specification

In the state based implementation, the counter state is transmitted to all other replicas.
But how do we model the state? Of course, the counter's count is its state. 
Since the count always increases, modeling the state as count automatically makes it a monotonic semilattice.

#### Specification


#### Figure

![State based increment only counter (incorrect)][state-based-increment-only-counter-incorrect]
As it can be seen from the figure, the clients issue a total of 4 increment requests. However, the replicas finally converge to 2.
Something is clearly amiss! When two replicas are incremented, they should together converge to 2. But the `merge` function computes the maximum of two states. 


#### Specification


#### Figure

![State based increment only counter (correct)][state-based-increment-only-counter-correct]

As it can be seen from the figure, the clients issue a total of 4 increment requests. However, the replicas finally converge to 2.
Something is clearly amiss! When two replicas are incremented, they should together converge to 2. But the `merge` function computes the maximum of two states. 





## PN-counter - Increment and Decrement counter

### CmRDT: Operation based specification

#### Specification

#### Figure

![Operation based increment and decrement counter][operation-based-increment-and-decrement-counter]

### CvRDT: State based specification

#### Specification



#### Figure

![State based increment and decrement counter (incorrect)][state-based-increment-and-decrement-counter-incorrect]



#### Specification



#### Figure

![State based increment and decrement counter (correct)][state-based-increment-and-decrement-counter-correct]

## Non-negative Counter





### State based specification (CmRDT)

```javascript
class 
    counts = [0, 0, ..., 0]
    
    update increment()
        g <- getId()
        counts[g] <- counts[g] + 1
    
    // query function
    function value():
        sum = 0
        for count in counts:
            sum <- sum + count
        return sum
    
    function compare(other):
        for i in 0 : length(replicas()):
            if counts[i] > other.counts[i]:
                return False
        return True
    
```

[operation-based-increment-only-counter]: images/counters/operation-based-increment-only-counter.png
[state-based-increment-only-counter-incorrect]: images/counters/state-based-increment-only-counter-incorrect.png
[state-based-increment-only-counter-correct]: images/counters/state-based-increment-only-counter-correct.png
[operation-based-increment-and-decrement-counter]: images/counters/operation-based-increment-and-decrement-counter.png
[state-based-increment-and-decrement-counter-incorrect]: images/counters/state-based-increment-and-decrement-counter-incorrect.png
[state-based-increment-and-decrement-counter-correct]: images/counters/state-based-increment-and-decrement-counter-correct.png
