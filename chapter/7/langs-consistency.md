---
layout: page
title:  "Formal, Yet Relaxed: Models for Consistency"
by: "James Larisch"
---
# Formal, Yet Relaxed: Models for Consistency

## What's the problem?
  As processors become expensive and the limits of Moore's Law are pushed, programmers find themselves in situations where they need to connect multiple computers together using a network cable. Perhaps it's not even due to cost or performance constraints; perhaps your company has servers in New York and San Fransisco, and there is some global state that requires synchronization across the country. Problems requiring solutions of this nature can be described as "distributed systems" problems. Your data / processing power / entry points are distributed for some reason. In many ways, web developers deal with distributed systems problems every day: your client and your server are in two different geographical locations, and thus, some coordination is required.

  As Aviral discussed in the previous section, many computer scientists have done a lot of thinking about the nature of distributed systems problems. As such, we realize that it's impossible to completely emulate the behavior of a single computational machine using multiple machines. For example, the network is simply not as reliable as, say, memory - and waiting for responses can result in a lack of timeliness for the application's client. After discussing the Consistency/Availability/Partition-tolerance theorem, Section 6 discussed how we can make drill down into the CAP pyramid and choose the properties of our systems. As stated, we can't perfectly emulate a single computer using multiple machines, but once we accept that fact and learn to work with it... there are plenty of things we *can* do!

## The Shopping Cart
  Let's bring all these theorem talk back to reality. Let's say you're working at a new e-commerce startup, and you'd like to revolutionize the electronic shopping cart. You'd like to give the customer the ability to do the following:
  1. Log in to the site and add a candle to the cart while traveling in Beijing.
  1. Take a HyperLoop (3 hours) from Beijing to Los Angeles.
  1. Log back in, remove the candle from the cart, and add a skateboard.
  1. Take another HyperLoop train from Los Angeles to Paris (5 hours).
  1. Log back into the site, add another skateboard, and checkout.

Let's assume you have a server in every single country, and customers connect to the geographically closest server.

How can we ensure that the client sees the same cart at every point in her trip?

If you only had one user of your website, this wouldn't be too hard. You could manually, constantly modify and check on all of your servers and personally make sure the state of the customer's shopping cart is consistent across every single server. But what happens when you have millions of customers and thus millions of shopping carts? That would be impossible to keep track of personally. Luckily, you're a programmer - this can be automated! You simply need to make sure that all of your computers stay in-sync, so if the customer checks her cart in Beijing, then in Paris, she sees the same thing.

But as Section 6 already explained, this is not so trivial. Messages between your servers in Beijing and Paris could get dropped, corrupted, reordered, duplicated, or delayed. Servers can crash. Sharks can cut the network cables between countries. Since you have no guarantees about when you'll be able to synchronize state between two servers, it's possible that the customer could see two different cart-states depending on which country she's in (which server she asks).

It's possible to implement "consensus" protocols such as Paxos and 3-Phase-Commit that provide coordination between your machines. When failure happens, such as a network shark-attack, the protocol detects a lack of consistency and becomes *unavailable*. For some applications, this is appropriate. For a shopping cart, this seems like overkill. If our shopping cart distributed systems experienced a failure, it means users would not be able to add or remove things from the cart. They also couldn't check out. This means our startup would lose money! Perhaps it's not so important that our clients' shopping carts be completely synchronized across the entire world at all times. After all, how often are people going to be doing such wanderlust shopping?

This is an important moment. By thinking about our specific problem, we've realized a compromise we're willing to make: our users always need to be able to add things, remove things, and checkout. In other words, our service needs to be *available*. Servers don't necessarily need to agree all the time. We'd like them to, but the system shouldn't shut down if they don't. We'll find a way to deal with it.

Turns out there's a company out there called Amazon.com - and they've been having a similar problem. Amazon sells things on their website too, and users can add and remove things from their cart. Amazon has lots of servers spread out across the world. They also have quite a few customers. They need to ensure their customers' carts are robust: if/when servers fail or lose communication with one another, a "best-effort" should be made to display the customer's cart. Amazon acknowledges that failure, latency, or HyperLoop-traveling users can cause inconsistent cart data, depending on which server you ask. How does Amazon resolve these issues?

## Dynamo
Amazon built DynamoDB, which is basically a big distributed hash table. In other words, it's a hashmap spread across multiple computers. A user's cart would be stored as a value under the user's username as the key. When a user adds a new item to her cart, the cart data is replicated across a multiple machines within the network. If the client changes locations and performs another write or a few machines fail and later recover, it's possible for different machines to have different opinions about the state of a given user's cart.

Dynamo has a rather unique way of dealing with these types of conflicts. Since Dynamo always wants to be available for both writes and reads (add/removes, viewing/checkouts, resp) it must have a way of combining inconsistent data. Dynamo chooses to perform this resolution at read time. When a client performs a `get()` on the user's cart, Dynamo will take the multiple conflicting carts...aaaaaand... push it all up to the application! Huh? I thought Dynamo resolves this for the programmer!? Actually, Dynamo is a generic key-value store. It detects inconsistencies in the data - but once it does, it simply tells the application (in this case the application is the shopping cart code) that there are some conflicts. The application (shopping cart, in this case) is free to resolve these inconsistencies as it pleases.

How should Amazon's shopping cart procede with resolution? It may be fed two cart states like so:

```
James's Cart V1  |  James's Cart V2
-----------------------------------
Red Candle       |  Red Candle
Blue Skateboard  |  Green Umbrella
```

Amazon doesn't want to accidently *remove* anything from your cart, so it errs on the side of inclusion. If given this particular conflict, you would see:

```
James's Cart
------------
Red Candle
Blue Skateboard
Green Umbrella
```

It's important to understand that Amazon has multiple machines storing the contents of your cart. These machines are asynchronously communicating in order to tell each other about updates they've received. Conflicts like this can happen when you try to read before the nodes have had time to gossip about your cart. More likely, however, is the situation in which one of the machines holding your cart goes offline and missing some updates. When it comes back online, you try to read, and this resolution process must occur.

### Good & Bad
What do we love about Dynamo? It's a highly available key-value store. It replicates data well, and according to the paper, has an insanely high uptime and low latency. We love that it's *eventually consistent*. Nodes are constantly gossiping, so given enough time (and assuming failures are resolved), nodes' states will eventually converge. However, this property is *weak*. It's weak because when failures+conflicts occur, and [and they will occur](https://www.youtube.com/watch?v=JG2ESDGwHHY), it's up to the application developer to figure out how to handle it. In the case of the shopping cart, it's relatively trivial. But as a programmer, every time you'd like to use DynamoDB you need to consider your resolution strategy. The database doesn't provide a general solution.

Instead of constructing an all-purpose database and forcing the burden of resolution on programmers, what if we constructed general-purpose data structures that required no manual resolution? These data structures would resolve conflicts inherently, themselves, and depending on your application you could choose which data structure works best for you.

Let's try this transfiguration on the shopping cart. Let's strip it down: how does Amazon handle resolution, really? It treats shopping cart versions as sets of items. In order to perform resolution, Amazon unions the two sets.

```
{ Red Candle, Blue Skateboard } U { Red Candle, Green Umbrella } == { Red Candle, Blue Skateboard, Green Umbrella }
```

Cool. Using this knowledge, let's try to construct our own shopping cart that automatically resolves conflicts.


(Unfortunately Amazon has a leg up on our startup. Their programmers have figured out a way to add multiple instances of a single item into the cart. Users on our website can only add one "Red Candle"" to their shopping cart. This is due to a fundamental limitation in the type of CRDT I chose to exemplify. It's quite possible to have a fully functional cart. Take a look at LWW-Sets.)

### Example

Let's take a look at the following Javascript. For simplicity's sake, let's pretend users can only add things to their shopping cart.

```javascript
class Cart {
  constructor(peers, socket) {
    this.mySocket = socket;
    this.peers = peers;
    this.items = new Set();
  }

  addItem(item) {
    this.items.add(item);
  }

  synchronize() {
    peers.forEach(function(peer) {
      peer.send(items);
    });
  }

  receiveState(items) {
    this.items = this.items.union(items);
  }

  run() {
    var clientAddition = Interface.nonBlockingReceiveInput(); // invented
    if (clientAddition !== undefined) {
      this.addItem(clientAddition);
    }
    var receivedState = mySocket.nonBlockingRead(); // invented
    if (receivedState !== undefined) {
      this.receiveState(receivedState);
    }
    synchronize();
    sleep(10);
    run();
  }
}

// theoretical usage

var socket = new UDPSocket(); // invented
var cart = new Cart(peerSockets, socket); // peerSockets is an array of UDP sockets
cart.run();
cart.items // the cart's items
```

Here is an (almost) fully functional shopping cart program. You can imagine this code running across multiple nodes scattered over the world. The meat of the program lies in the `run()` method. Let's walk through that:
  1. Program receives an addition to the cart from the user.
  2. Program adds that item to the current local state if it exists.
  3. Program checks its UDP socket for any messages.
  4. If it received one, it's means another instance of this program has sent us its state. What is state in this case? Simply a set of cart items. Let's handle this set of items by unioning it with our current set.
  5. Synchronize our current state by sending our state to every peer that we know about.
  6. Sleep for 10 seconds.
  7. Repeat!

Hopefully it's clear that if a client adds an item to her cart in Beijing and then 10 seconds later checks her cart in Paris, she should see the same thing. Well, not exactly - remember, the network is unreliable, and Beijing's `synchronize` messages might have been dropped. But no worries! Beijing is `synchronizing` again in another 10 seconds. This should remind you of Dynamo's gossiping: nodes are constantly attempting to converge.

Both systems are eventually consistent - the difference here is our Javascript shopping cart displays *strong* eventual consistency. It's strong because it requires no specialized resolution. When a node transmits its state to another node, there's absolutely no question about how to integrate that state into the current one. There's no conflict.

### The Intern
Unfortunately Jerry, the intern, has found your code. He'd like to add `remove` functionality to the cart. So he makes the following changes:

```javascript
class Cart {
  constructor(peers, socket) {
    this.mySocket = socket;
    this.peers = peers;
    this.items = new Set();
  }

  addItem(item) {
    this.items.add(item);
  }

  synchronize() {
    peers.forEach(function(peer) {
      peer.send(items);
    });
  }

  receiveState(items) {
    // JERRY WAS HERE
    this.items = this.items.intersection(items);
    // END JERRY WAS HERE
  }

  run() {
    var clientAddition = Interface.nonBlockingReceiveInput(); // invented
    if (clientAddition !== undefined) {
      this.addItem(clientAddition);
    }
    // JERRY WAS HERE
    var clientDeletion = Interface.nonBlockingReceiveInput():
    if (clientDeletion !== undefined) {
      this.items.delete(clientDeletion);
    }
    // END JERRY WAS HERE
    var receivedState = mySocket.nonBlockingRead(); // invented
    if (receivedState !== undefined) {
      this.receiveState(receivedState);
    }
    synchronize();
    sleep(10);
    run();
  }
}

// theoretical usage

var socket = new UDPSocket(); // invented
var cart = new Cart(peerSockets, socket); // peerSockets is an array of UDP sockets
cart.run();
cart.items // the cart's items
```

Uh-oh. Can you spot the problem? Let's break it down. In the original code, the current node's cart items were *unioned* with the communicating node's cart. Since there was no deletion, carts could only ever expand. Here was Jerry's plan:

```
> I want to delete things. If you delete something from node 1, and intersect it's state from node 2, the item will be deleted from node 2 as well.

Node 1: { A, B }
Node 2: { A, B }

delete(Node2, A)

Node 1: { A, B }
Node 2: { B }

Node1 = Node1.intersect(Node2)
Node1: { B }
```

The reasoning is sound. However, there's a huge issue here. We've flipped the `union` operation on its head! Now, carts can *never* expand! They can only either stay the same size or shrink. So although Jerry's contrived example works, it's impossible to ever reach the beginning states of Node 1 and Node 2 unless those two nodes receive *the same writes*. Let's take it from the top:

```
Node 1: { }
Node 2: { }

add(Node1, A)
add(Node2, B)

Node 1: { A }
Node 2: { B }

Node1_temp = Node1.intersect(Node2)
Node2_temp = Node2.intersect(Node1)
Node1 = Node1_temp
Node2 = Node2_temp

Node 1: { }
Node 2: { }
```

This is pretty nasty. Jerry has come along and with a few lines of code he's obliterated our nice strong eventually consistent code. Surely there's a better way.

### Guarantees
The original Javascript we wrote down exhibits the property from Section 6 known as *monotonicity*. The union operation ensures that a given node's state is always "greater than or equal to" the states of the other nodes. However, how can we be *sure* that this property is maintained throughout the development of this program? As we've seen, there's nothing stopping an intern from coming along, making a mindless change, and destroying this wonderful property. Ideally, we want to make it impossible (or at least very difficult) to write programs that violate this property. Or, at the very least, we want to make it very easy to write programs that maintain these types of properties.

But where should these guarantees live? In the above Javascript example, the guarantees aren't guarantees at all, really. There's no restriction on what the programmer is allowed to do - the programmer has simply constructed a program that mirrors guarantees that she has modeled in her brain. In order to maintain properties such as *monotonicity*, she must constantly check the model in her brain against the code. We haven't really helped the programmer out that much - she has a lot of thinking to do.

Databases such as PostgreSQL have issues like this as well, though they handle them quite differently, masters may need to ensure that write have occurred on every slave before the database becomes available for reading. A database system like this has pushed consistency concerns to the IO-level, completely out of the users control. They are enforced on system reads and system writes. This approach gives programmers no flexibility: as demonstrated with our shopping cart example, there's no need for these type of restrictions; we can tolerate inconsistency in order to maintain availability.

Why not push the consistency guarantees in between the IO-level and the application-level? Is there any reason why you as the programmer couldn't program using tools that facilitate these types of monotonic programs? If you're familiar with formal systems -- why not construct a formal system (programming language / library) in which every theorem (program) is formally guarunteed to be monotonic? If it's *impossible* to express a non-monotonic program, the programmer needn't worry about maintaining a direct mapping between their code and their mental model.

Wouldn't it be great if tools like this existed?

### Bloom
[ Introduce Bloom ]

#### Restriction & Danger
[Bloom restricts you, it's different, and it's dangerous]

### Lasp
[ Introduce Lasp ]
Instead of trying to do it all (and accepting danger), it tries to be embeddable (and truly restrictive.)

### Utilization

Lasp is an Erlang library, and for good reason. Remember the initial discussion and reasoning for models such as Bloom and Lasp: we have a specific type of application that doesn't require tight consistency constraints. The constraints that do exist have been formalized, and we can be quite sure that by using a DSL like Lasp, we'll be safe from interns like Jerry. But Lasp can't do everything. More generally, eventual consistency doesn't solve every problem.

PostgreSQL enforce very specific and restrictive IO-level consistency, and this was too much for our needs. But it's certainly not too much for *all* needs. There certainly are applications (take banking, for example) in which consistency is extremely important. You certainly are not allowed to double spend your money depending on how fast you can travel to a different server, so eventual consistency is not enough! All servers must coordinate.

There's a key principle here, however: distributed programming models that attempt to accomdate everything end up doing nothing well; models that accept compromises and formalize certain properties end up being extremely useful for a subset of domains.

Most programming languages are "general-use". This works for single machine programming. As the world moves toward distributed programming, programmers must adopt models / languages / libraries that are built for their domain. It forces serious thought on the part of the programmer: what *exactly* am I trying to achieve, and what am I willing to sacrifice?

We've known for quite a while that when we're talking about multiple machines, we can't have it all. Our tools must now reflect this mantra. Our sanity and the safety of our programs depends on it.

## References

{% bibliography --file langs-consistency %}
