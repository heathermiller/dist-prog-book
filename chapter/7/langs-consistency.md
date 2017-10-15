---
layout: page
title:  "Formal, Yet Relaxed: Models for Consistency"
by: "James Larisch"
---
# Formal, Yet Relaxed: Models for Consistency

## What's the problem?
In many ways, web developers deal with distributed systems problems every day: your client and your server are in two different geographical locations, and thus, some coordination between computers is required.

As Aviral discussed in the previous section, many computer scientists have done a lot of thinking about the nature of distributed systems problems. As such, we realize that it's impossible to completely emulate the behavior of a single computational machine using multiple machines. For example, the network is simply not as reliable as, say, memory - and waiting for responses can result in untimeliness for the application's user base. After discussing the Consistency/Availability/Partition-tolerance theorem, Section 6 discussed how we can drill down into the CAP pyramid and choose the necessary and unnecessary properties of our systems. As stated, we can't perfectly emulate a single computer using multiple machines, but once we accept that fact and learn to work with it, there are plenty of things we *can* do!

## The Shopping Cart
Let's bring all this theorem talk back to reality. Let's say you're working at a new e-commerce startup, and you'd like to revolutionize the electronic shopping cart. You'd like to give the customer the ability to do the following:

1. Log in to the site and add a candle to the cart while traveling in Beijing.
2. Take a HyperLoop (3 hours) from Beijing to Los Angeles.
3. Log back in, remove the candle from the cart, and add a skateboard.
4. Take another HyperLoop train from Los Angeles to Paris (5 hours).
5. Log back into the site, add another skateboard, and checkout.

Let's assume you have a server in every single country, and customers connect to the geographically closest server.

How can we ensure that the client sees the same cart at every point in her trip?

If you only had one user of your website, this wouldn't be too hard. You could manually, constantly modify and check on all of your servers and personally make sure the state of the customer's shopping cart is consistent across every single server. But what happens when you have millions of customers and thus millions of shopping carts? That would be impossible to keep track of personally. Luckily, you're a programmer - this can be automated! You simply need to make sure that all of your computers stay in-sync, so if the customer checks her cart in Beijing, then in Paris, she sees the same thing.

But as Section 6 has already explained, this is not so trivial. Messages between your servers in Beijing and Paris could be dropped, corrupted, reordered, duplicated, or delayed. Servers can crash. Sharks can cut the network cables between countries. Since you have no guarantees about when you'll be able to synchronize state between two servers, it's possible that the customer could see two different cart-states depending on which country she's in (which server she asks).

It's possible to implement "consensus" protocols such as Paxos and Raft that provide coordination between your machines. When more failures than the system can tolerate occur, such as a network shark-attack, the protocol detects a lack of consistency and becomes *unavailable* - at least until it is consistent once more. For applications in which inconsistent state is dangerous, this is appropriate. For a shopping cart, this seems like overkill. If our shopping cart system experienced a failure and became unavailable, users would not be able to add or remove things from the cart. They also couldn't check out. This means our startup would lose money! Perhaps it's not so important that our clients' shopping carts be completely synchronized across the entire world at all times. After all, how often are people going to be doing such wanderlust shopping?

This is an important moment. By thinking about our specific problem, we've realized a compromise we're willing to make: our users always need to be able to add things, remove things, and checkout. In other words, our service needs to be as *available* as possible. Servers don't necessarily need to agree all the time. We'd like them to, but the system shouldn't shut down if they don't. We'll find a way to deal with it.

Turns out there's a company out there called Amazon.com - and they've been having a similar problem. Amazon sells things on their website too, and users can add and remove things from their cart. Amazon has lots of servers spread out across the world. They also have quite a few customers. They need to ensure their customers' carts are robust: if/when servers fail or lose communication with one another, a "best-effort" should be made to display the customer's cart. Amazon acknowledges that failure, latency, or HyperLoop-traveling users can cause inconsistent cart data, depending on which server you ask. How does Amazon resolve these issues?

## Dynamo

Amazon built DynamoDB {% cite Dynamo --file langs-consistency %}, which is basically a big distributed hash table. I won't go into the details of DHTs, but let's imagine Dynamo as a hashmap, replicated across multiple servers. A user's cart is stored as a value under the user's username as the key. (`{'james': ['candle', 'skateboard']}`) When a user adds a new item to her cart, either the entire cart or this update is sent to every other server (or, replica). Since, say, a network cable can fail, one replica may have *inconsistent state*: a different view of the universe (a shopping cart, in this case) than every other server.

Dynamo has a rather unique way of dealing with these types of inconsistencies. Since Dynamo always wants to be available for both writes and reads (add/removes, viewing/checkouts, resp) it must have a way of combining inconsistent data. Dynamo chooses to perform this resolution at read time. When a client performs a `get()` on the user's cart, Dynamo will query multiple servers for the cart data, for redunancy's sake. Dynamo recognizes the inconsistent state and will take the multiple conflicting carts and push them up to the application! Huh? I thought Dynamo resolves this for the programmer!? Actually, Dynamo is a rather unopinionated key-value store. It detects inconsistencies in the data - but once it does, it simply tells the application (in this case the application is the shopping cart code) that there are some conflicts. The application (shopping cart, in this case) is free to resolve these inconsistencies as it pleases.

How should Amazon's shopping cart procede with resolution? It may be fed two cart states like so:

```
James's Cart V1  |  James's Cart V2
-----------------------------------
Red Candle       |  Red Candle
Blue Skateboard  |  Green Umbrella
```

Amazon doesn't want to accidently *remove* anything from your cart, so it errs on the side of inclusion. If given this particular conflict, you may see:

```
James's Cart
------------
Red Candle
Blue Skateboard
Green Umbrella
```

Dynamo has multiple machines in charge of storing the contents of your cart. When you add something to your cart, Dynamo specifies a minimum number of nodes that must receive the new data before the write is considered complete. The same thing goes for reading the contents of your cart: Dynamo requires a minimum number of healthy, responsive nodes to return cart data before relaying this data to the user. Nodes periodically gossip their local state to their neighbors to ensure that any updates, which occurred while the node may have been offline, are eventually delivered. However, Dynamo sends updates to your carts asynchronously to all replicas. This means when you read the contents of your cart, it's possible to receive different results from different replicas.

## Dynamo Simplification

What do we love about Dynamo? It's a highly available key-value store. It replicates data well, and according to the paper, has high uptime and low latency. We love that it's *eventually consistent*. Nodes are constantly gossiping and `put`s are asynchronously propagated, so given enough time (and assuming failures are resolved), nodes' states will eventually converge. However, this property is *weak*. It's weak because when failures & conflicts occur, and [and they will occur](https://www.youtube.com/watch?v=JG2ESDGwHHY), it's up to the application developer to figure out how to handle it. Given a conflict, there isn't a one-size-fits-all solution for resolving them. In the case of the shopping cart, it's relatively trivial: our resolution strategy errs on the side of inclusion. But as a programmer, every time you use DynamoDB for a different purpose you need to consider your resolution strategy. The database doesn't provide a general solution.

Instead of constructing an all-purpose database and forcing the burden of resolution on programmers, what if we constructed multi-purpose (read: multi, not *all*) data structures that required no manual resolution? These data structures would resolve conflicts inherently, themselves, and depending on your application you could choose which data structure works best for you.

Let's try this transfiguration on the shopping cart. Let's strip it down: how does Amazon handle resolution, really? It treats shopping cart versions as sets of items. In order to perform resolution, Amazon unions the two sets.

```
{ Red Candle, Blue Skateboard } U { Red Candle, Green Umbrella } == { Red Candle, Blue Skateboard, Green Umbrella }
```

Using this knowledge, let's try to construct our own shopping cart that automatically resolves conflicts.

(Unfortunately Amazon has a leg up on our startup. Their programmers have figured out a way to add multiple instances of a single item into the cart. Users on our website can only add one "Red Candle"" to their shopping cart. This is due to a fundamental limitation in the type of CRDT I chose to exemplify. It's quite possible to have a fully functional cart. Take a look at OR-Sets. If these sentences made no sense to you, don't worry!)

### Example

Let's take a look at the following JavaScript. For simplicity's sake, let's pretend users can only add things to their shopping cart.

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

Hopefully it's clear that if a client adds an item to her cart in Beijing and then 10 seconds later checks her cart in Paris, she should see the same thing. Well, not exactly - remember, the network is unreliable, and Beijing's `synchronize` messages might have been dropped, delayed, or reordered. But no worries! Beijing is `synchronizing` again in another 10 seconds. This should remind you of Dynamo's gossip and propagation: nodes are constantly attempting to converge.

Both systems are eventually consistent - the difference here is our Javascript shopping cart displays *strong* eventual consistency. It's strong because the resolution strategy is built in. In order words, the carts know *how to handle inconsistency*, rather than simply asking the programmer what to do. When a node transmits its state to another node, there's absolutely no question about how to integrate that state into the current one. There's no conflict. This is certainly an improvement from Dynamo.

## The Intern: A Lack of Guarantees

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

> I want to delete things. If you delete something from node 1, and intersect it's state from node 2, the item will be deleted from node 2 as well.

```
Node1: { A, B }
Node2: { A, B }

delete(Node2, A)

Node1: { A, B }
Node2: { B }

Node1 = Node1.intersect(Node2)
Node1: { B }
```

The reasoning may be sound. However, there's a huge issue here. We've flipped the `union` operation on its head! Now, carts can *never* expand! They can only either stay the same size or shrink. So although Jerry's contrived example works, it's impossible to ever reach the beginning states of Node 1 and Node 2 unless those two nodes receive *the same writes*. Let's take it from the top:

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

## Logical Monotonicity

The original Javascript we wrote down exhibits the property from Section 6 known as logical *monotonicity*. The union operation ensures that a given node's state is always "greater than or equal to" the states of the other nodes. However, how can we be *sure* that this property is maintained throughout the development of this program? As we've seen, there's nothing stopping an intern from coming along, making a mindless change, and destroying this wonderful property. Ideally, we want to make it impossible (or at least very difficult) to write programs that violate this property. Or, at the very least, we want to make it very easy to write programs that maintain these types of properties.

But where should these guarantees live? In the above Javascript example, the guarantees aren't guarantees at all, really. There's no restriction on what the programmer is allowed to do - the programmer has simply constructed a program that mirrors guarantees that she has modeled in her brain. In order to maintain properties such as *monotonicity*, she must constantly check the model in her brain against the code. We haven't really helped the programmer out that much - she has a lot of thinking to do.

Databases such as PostgreSQL have issues like this as well, though they handle them quite differently, masters may need to ensure that writes have occurred on every slave before the database becomes available for reading. A database system like this has pushed consistency concerns to the IO-level, completely out of the users control. They are enforced on system reads and system writes. This approach gives programmers no flexibility: as demonstrated with our shopping cart example, there's no need for these type of restrictions; we can tolerate inconsistency in order to maintain availability.

Why not push the consistency guarantees in between the IO-level and the application-level? {% cite ConsistencyWithoutBorders --file langs-consistency %} Is there any reason why you as the programmer couldn't program using tools that facilitate these types of monotonic programs? If you're familiar with formal systems -- why not construct a formal system (programming language / library) in which every theorem (program) is formally guaranteed to be monotonic? If it's *impossible* to express a non-monotonic program, the programmer needn't worry about maintaining a direct mapping between their code and his or her mental model.

Wouldn't it be great if tools like this existed?

## Bloom

Before talking about such tools, I'd like you to forget almost everything you know about programming for a second (unless of course you've never programmed in a Von Neumann-based language in which you sequentially update pieces of memory).

Imagine the following scenario: you are "programming" a node in a cluster of computers. All of the other computers work as expected. As a node in this cluser, when you receive a message (all messages will include an integer), your task is to save the message, increment the integer, and resend the new message with the incremented integer back to its originator. You must also send any new messages you've received from `stdin`. Unfortunately, the programming environment is a little strange.

You have access to five sets:
* Messages you have received in the last 5 seconds (read)
* Inputs you've received from `stdin` in the last 5 seconds (read)
* An outgoing messages set: flushed & sent every 5 seconds (write)
* A bucket of saved messages: *never* flushed (read/write)

However, you're only given access to these sets *every 5 seconds*. If messages are formatted as such: `(SOURCE, INTEGER, T)`, your sets might look like when `t = 0`. (`t` is the number of seconds elapsed)

```
<T = 0>
RECV-BUFFER: {(A, 1, 0), (B, 2, 0)}
RSTDIN-INPUTS: {(A, 5, 0), (C, 10, 0)}
SEND-BUFFER: {}
SAVED: {(D, -1, 0), (E, -100, 0)}
```

If you don't write any code to manipulate these sets, when `t = 5`, your sets might look like:

```
<T = 5>
RECV-BUFFER: {(C, 10, 5)}
STDIN-INPUTS: {(X, 1, 5)}
SEND-BUFFER: {}
SAVED: {(D, -1, 0), (E, -100, 0)}
```

You can see that from `t = 0` to `t = 5`, you received one message from `C` and someone typed a message to `X` via `stdin`.

Remember our goals?
* Save received messages from the network
* Send out messages received from `stdin`
* For all received network messages, increment the integer and resend it back to the originator

In Javascript, perhaps you code up something like this:

```javascript
onFiveSecondInterval(function() {
  recvBuffer.forEach(function(msg) {
    savedBuffer.push(msg);            // save message
    let newMsg = msg.clone()
    newMsg.integer++;                 // increment recv'd message
    newMsg.flipSourceDestination()
    sendBuffer.push(newMsg);          // send it out
  });

  stdinInputBuffer.forEach(function(msg) {
    sendBuffer.push(msg);             // send stdin message
  });
});
```

or Ruby:

```ruby
on_five_second_interval do
  recv_set.each do |msg|
    saved_set << msg
    new_msg = msg.clone
    new_msg.integer += 1
    new_msg.flip_source_destination
    send_set << new_msg
  end

  stdin_input_set.each do |msg|
    send_set << msg
  end
end
```

We have expressed this model using an event-driven programming style: the callbacks are triggered when `t % 5 = 0`: when the sets populate & flush.

Notice we perform a few "copies". We read something from one set and place it into another one, perhaps after applying some modification. Perhaps we place a message from a given set into two sets (`recv_set` to `saved_set` & `send_set`).

This situation screams for a more functional approach:
```ruby
on_five_second_interval do
  saved_set += recv_set             # add everything in recv_set to saved_set

  send_set += recv_set.map do |msg| # map over the recv_set, increment integers, add to send_set
    new_msg = msg.clone
    new_msg.integer += 1
    new_msg.flip_source_destination       # send to originator
    new_msg                               # this block returns new_msg
  end

  send_set += stdin_input_set       # add stdin messages to the send set
end
```

After this block/callback is called, the system automatically flushes & routes messages as described above.

Bloom {% cite Bloom --file langs-consistency %}, a research language developed at UC Berkeley, has a similar programming model to the one described above. Execution is broken up into a series of "timesteps". In the above example, one "timestemp" would be the execution of one `on_five_second_interval` function. Bloom, like the theoretical system above, automatically flushes and populates certain sets before and after each timestep. In the above example, 5 seconds was an arbitrary amount of time. In Bloom, timesteps (rounds of evaluation) are logical tools - they may happen every second, 10 seconds, etc. Logically, it shouldn't affect how your program executes. In reality, Bud's timesteps correspond to evaluation iterations. Your code is evaluated, executed, and the process repeats.

So what does a Bloom program look like? Bloom's prototypal implementation is called Bud and is implemented in Ruby. There are two main parts to a Bloom program:

1. User defined sets: rather than the four sets I gave you above, Bloom users can define their own sets. There are different types of sets depending on the behavior you desire. Bloom refers to these sets as 'collections':
  * `channel`: Above, `recv_set` and `send_set` would be considered channels. They facilitate sending network messages to and from other nodes. Like the messages above, messages sent into these channels contain a "location-specifier", which tells Bloom where the message should be sent. If you wanted to send a message to `A`, you could push the message `(@A, 10)` into your send set (in Ruby, `["@A", 10]`). The `@` denotes the location-specifier. At the end of the timestep (or callback execution in the above example), these set are flushed.
  * `table`: Above, `saved_set` would be considered a table. The contents of tables persist across timesteps, which means tables are never flushed.
2. Code to be executed at each timestep. A Bloom (Bud) program can be seen as the inside of the block passed to `on_five_second_interval`. In fact, it looks very similar, as we'll see.

For the purposes of this chapter, let's assume `stdin_input_set` is a special kind of channel in which are sent in via `stdin`. Let's also assume this channel exists in all Bloom programs.

Let's take a look at an example Bud program.

First, let's declare our state.

```ruby
module Incrementer
  def state
    channel :network_channel ['@dst', 'src', 'integer']
    table :saved_set ['dst', 'src', 'integer']
    # implied channel :stdin_input_set ['@dst', 'src', 'integer']
  end
end
```

The first line of `state` means: declare a channel called `network_channel` in which messages are 3-tuples. The first field of the message is called `dst`, the second `src`, and the third is called `integer`. `@` is our location-specifier, so if a program wants to send a message to a node at a given identifier, they will place it in the first `dst` field. For example, a message destined for `A` would look like `['A', 'me', 10]`. The `@` denotes the location-specifier within the collection's "schema".

The second line means: declare a table (persists) called `saved_set` in which messages follow the same format as `network_channel`. There's no location specifier since this collection is not network-connected.

You can think of the Ruby array after the channel name as the "schema" of that collection.

Notice how we only have one network channel for both receiving and sending. Before, we had two sets, one for sending and one for receiving. When we place items *into* `network_channel`, Bud will automatically send messages to the appropriate `@dst`.

Next, let's write our code. This code will be executed at every timestamp. In fact, you can think of a Bud program as the code inside of a timestamp callback. Let's model the raw Ruby code we saw above.

```ruby
module Incrementer
  def state
    channel :network_channel ['@dst', 'src', 'integer']
    table :saved_set ['dst', 'src', 'integer']
    # implied channel :stdin_input_set ['@dst', 'src', 'integer']
  end

  declare
  def increment_messages
    network_channel <~ network_channel.map { |x| [x.src, x.dst, x.integer + 1] }
  end

  declare
  def save_messages
    saved_set <= network_channel
  end

  declare
  def send_messages
    network_channel <~ stdin_input_set
  end
end
```

Don't panic. Remember - the output of this program is identical to our Ruby callback program from earlier. Let's walk through it step by step.

```ruby
declare
def increment_messages
  network_channel <~ network_channel.map { |x| [x.src, x.dst, x.integer] }
end
```

Here, we take messages we've received from the network channel and send them back into the network channel. The `<~` operator says "copy all of the elements in the right-hand-side and eventually send them off onto the network in the channel on the left-hand-side". So, we map over the contents of network channel *in the current timestep*: switching the `src` and `dst` fields, and incrementing the integer. This mapped collection is passed back into the network channel. Bud will ensure that those messages are sent off at some point.

```ruby
declare
def save_messages
  saved_set <= network_channel
end
```

In `save_messages`, we use the `<=` operator. `<=` says "copy all of the elements in the right-hand-side and add them to the table on the left-hand-side." It's important to note that this movement occurs *within the current timestep*. This means if `saved_set` is referenced elsewhere in the code, it will include the contents of `network_channel`. If we had used the `<+` operator instead, the contents of `network_channel` would show up in `saved_set` in the *next* timestep. The latter is useful if you'd like to operate on the current contents of `saved_set` in the current timestep but want to specify how `saved_set` should be updated for the next timestep.

Remember, all of this code is executed in *each* timestep - the separation of code into separate methods is merely for readability.

```ruby
declare
def send_messages
  network_channel <~ stdin_input_set
end
```

`send_messages` operates very much like `increment_messages`, except it reads the contents of `stdin_input_set` and places them into the network channel to be sent off at an indeterminite time.

### Details

Examine Bloom's "style". Compare it to your standard way of programming. Compare it to the Javascript & Ruby timestep/callback examples. Bloom has a more "declarative" style: what does this mean? Look at our Javascript:

```javascript
onFiveSecondInterval(function() {
  recvBuffer.forEach(function(msg) {
    savedBuffer.push(msg);            // save message
    let newMsg = msg.clone()
    newMsg.integer++;                 // increment recv'd message
    newMsg.flipSourceDestination();
    sendBuffer.push(newMsg);          // send it out
  });

  stdinInputBuffer.forEach(function(msg) {
    sendBuffer.push(msg);             // send stdin message
  });
});
```

"Every five seconds, loop over the received messages. For each message, do this, then that, then that." We are telling the computer each step we'd like it to perform. In Bud, however, we describe the state of tables and channels at either the current or next timestep using operators and other tables and channels. We describe what we'd like our collections to include and look like, rather than what to do. You declare what you'd like the state of the world to be at the current instant and at following instants.

### Isn't this chapter about consistency?

It's time to implement our shopping cart in Bloom. We are going to introduce one more collection: a `periodic`. For example, `periodic :timer 10` instantiates a new periodic collection. This collection becomes "populated" every 10 seconds. Alone, it's not all that useful. However, when `join`'d with another table, it can be used to perform actions every `x` seconds.

```ruby
module ShoppingCart
  include MulticastProtocol

  def state
    table :cart ['item']
    channel :recv_channel ['@src', 'dst', 'item']
    # implied channel :stdin_input_set ['item']
    periodic :timer 10
  end

  declare
  def add_items
    cart <= stdin_input_set
  end

  declare
  def send_items
    send_mcast <= join([cart, timer]).map { |item, timer| item }
  end

  declare
  def receive_items
    cart <+ recv_channel.map { |x| x.item }
  end
end
```

`send_mcast` is a special type of channel we receive from the `MulticastProtocol` mixin. It sends all items in the right-hand-side to every known peer.
* `add_items`: receive items from stdin, add them to the cart
* `send_items`: join our cart with the 10-second timer. Since the timer only "appears" every 10 seconds, this `join` will produce a result every 10 seconds. When it does, send all cart items to all peers via `send_mcast`.
* `receive_items`: when we receive a message from a peer, add the item to our cart.

Functionally, this code is equivalent to our working Javascript shopping cart implementation. However, there are a few important things to note:
* In our Javascript example, we broadcasted our entire cart to all peers. When a peer received a message, they unioned their current cart with the received one. Here, each node broadcasts each element in the cart. When a node receives an item, it adds it to the current cart. Since tables are represented as sets, repeated or unordered additions do not matter. You can think of `{A, B, C}.add(D)` as equivalent to `{A, B, C}.union({D})`.
* You cannot add items twice. Since tables are represented as sets and we simply add items to our set, an item can only ever exist once. This was true of our Javascript example as well.
* You still cannot remove items!

Bloom has leveraged the montononic, add-only set and constructed a declarative programming model based around these sets. When you treat everything as sets (not unlike SQL) and you introduce the notion of "timestemps", you can express programs as descriptions of state rather than an order of operations. Besides being a rather unique model, Bloom presents an accessible and (perhaps...) safe model for programming eventually consistent programs.

### Sets only?

Bloom's programming model is built around the set. As Aviral discussed in the previous chapter, however, sets are not the only monotonic data structures. Other CRDTs are incredibly useful for programming eventually consistent distributed programs.

Recall that a *bounded join semilattice* (CRDT) can be represented as a 3-tuple: `(S, U, ⊥)`. `S` is the set of all elements within the semilattice. `U` is the `least-upper bound` operation. `⊥` is the "least" element within the set. For example, for add-only sets, `S = the set of all sets`, `U = union` and `⊥ = {}`. Elements of these semilattices, when `U` is applied, can only "stay the same or get larger". Sets can only stay the same size or get larger - they can never rollback. For some element `e` in `S`, `e U ⊥` must equal `e`.
For a semilattice we'll call `integerMax`, `S = the set of all integers`, `U = max(x, y)`, and `⊥ = -Infinity`. Hopefully you can see that elements of this lattice (integers) "merged" with other elements of this lattice never produce a result less than either of the merged elements.

These semilattices (and many more!) can be used to program other types of distributed, eventually consistent programs. Although sets are powerful, there might be more expressive ways to describe your program. It's not difficult to imagine using `integerMax` to keep a global counter across multiple machines.

Unfortunately, Bloom does not provide support for other CRDTs. In fact, you cannot define your own datatypes at all. You are bound by the collections described.

Bloom<sup>L</sup> {% cite BloomL --file langs-consistency %}, an addendum to the Bloom language, provides support for these types of data structures. Specifically, Bloom<sup>L</sup> does two things:
* Adds a number of built-in lattices such as `lmax` (`integerMax`), `lmin`, etc.
* Adds an "interface" for lattices: the user can define lattices that "implement" this interface.

This interface, if in an OO language like Java, would look something like:

```java
interface Lattice {
  static Lattice leastElement();
  Lattice merge(Lattice a, Lattice b);
}
```

Heather: [I am purposely leaving out morphisms & monotones for the sake of simplicity.]

This provides the user with much more freedom in terms of the types of Bloom programs she can write.

### Review

Bloom aims to provide a new model for writing distributed programs. And since bloom only allows for monotonic data structures with monotonicity-preserving operations, we're safe from Jerry the intern, right?

Wrong. Unfortunately, I left out an operator from Bloom's set of collection operators. `<-` removes all elements in the right-hand-size from the table in the left-hand-side. So Bloom's sets are *not* add-only. As we've seen from Jerry's work on our original Javascript shopping cart implementation, naively attempting to remove elements from a distributed set is not a safe operation. Rollbacks can potentially destroy the properties we worked so hard to achieve. So what gives? Why would the Bloom developers add this operation?

Despite putting so much emphasis on consistency via logical monotonicity, the Bloom programmers recognize that your program might need *some* coordination.

In our example, we don't require coordination. We accept the fact that a user may ask a given node for the current state of her shopping cart and may not receive the most up-to-date response. There's no need for coordination, because we've used our domain knowledge to accept a compromise.

For our shopping cart examples: when a client asks a given node what's in her cart, that node will respond with the information it's received so far. We know this information won't be *incorrect*, but this data could be *stale*. That client might be missing information.

The Bloom team calls points like the one above, the user asking to checkout the contents at the cart of a given node, *points of order*. These are points in your program where coordination may be required - depending on when and who you ask, you may receive a different response. In fact, the Bloom developers provide analysis tools for identifying points of order within your program. There's no reason why you couldn't implement a non-monotonic shopping cart in which all nodes must synchronize before giving a response to the user. The Bloom analysis tool would tell you where the points of order lie in your program, and you as the programmer could decide whether or not (and how!) to add coordination.

So what does Bloom really give us? First off, it demonstrates an unusual and possibly more expressive way to program distributed systems. Consistency-wise, it uses sets under the hood for its collections. As long as you shy away from `<-` operator, you can be confident that your collections will only monotonically grow. Since the order of packets is not guaranteed, structuring these eventually consistent applications is reasonably easy within Bloom. Bloom<sup>L</sup> also gives us the power to define our own monotonic data structures by "implementing" the lattice interface.

However, Bloom makes it easy to program non-monotonic distributed programs as well. Applications may require coordination and the `<-` operator in particular can cause serious harm to our desired formal properties. Luckily, Bloom attempts to let the programmer know exactly when coordination may be required within their programs. Whenever an operation may return a stale or non-up-to-date value, Bloom's analysis tools let the programmer know.

Another thing to consider: Bloom<sup>L</sup>'s user-defined lattices are just that - user-defined. It's up to the programmer to ensure that the data structures that implement the lattice interface are actually valid lattice structures. If your structures don't follow the rules, your program will behave in some seemingly strange ways.

Currently Bloom exists as a Ruby prototype: Bud. Hypothetically speaking, there's nothing stopping the programmer from writing normal, sequentially evaluated Ruby code within Bud. This can also cause harm to our formal properties.

All in all, Bloom provides programmers with a new model for writing distributed programs. If the user desires monotonic data structures and operations, it's relatively easy to use and reason about. Rather than blindly destroying the properties of your system, you will know exactly when you introduce a possible point of order into your program. It's up to you to decide whether or not you need to introduce coordination.

## Lasp

Lasp {% cite Lasp --file langs-consistency %} is an Erlang library which aims to facilitate this type of "disorderly" programming.

Lasp provides access to myriad of CRDTs. The programmer can have confidence that the CRDTs obey the lattice formal requirements. Like Bloom<sup>L</sup>, if the user desires a new lattice he or she may implement it using an interface.

A Simple Lasp Program is defined as either a:

* Single CRDT instance
* A "Lasp process" with *m* inputs, all Simple Lasp Programs, and one output CRDT instance

For those of you unfamiliar with Erlang: a *process* can be thought of as an independent piece of code executing asynchronously. Processes in Erlang are actors that act sequentially and exchange messages through asynchronous message passing.

Programming in Erlang is unique in comparison to programming in Ruby or Javascript. Erlang processes are spun off for just about everything - and they are independent actors of code acting independently while communicating with other processes. Naturally, distributed systems programming fits well here. Processes can be distributed within a single computer or distributed across a cluster of computers. So communication between processes may move over the network.

Distribution of a data structure, then, means the transmission of a data structure across network-distributed processes. If a client asks for the state of the shopping cart in Beijing, the processes located on the computer in Beijing will respond. However, the processes in New York may disagree. Thus, our task is to distribute our data structures (CRDTs, right?) across distributed processes.

So, what's a "Lasp process"? A Lasp process is a process that operates on lattice elements, or CRDTs. Three popular Lasp processes are `map`, `fold`, and `filter`.

* `map`: If you're familiar with functional programming, these functions shouldn't appear too foreign. `map` spins off a never-ending process which applies a user-supplied `f` to all the replicas of a given CRDT this processes receives.
* `fold`: Spins off a process that continously folds input CRDT values into another CRDT value using a user-provided function.
* `filter`: Spins off a process that continously picks specific CRDT input values based on a user-provided filtering function.

Drawing parallels to our mock-Bloom-Ruby-callback implementation, we remember that CRDT modifications and movements can be modeled using functional styles. In Bloom, we dealt with mapping values from "collections" to other "collections". These collections were backed by CRDT-like sets.

Here, we are mapping "streams" of CRDT instances to other CRDT instances using the same functional programming methods.

However, here, the stream manipulations occcur within unique processes distributed across a network of computers. These processes consume CRDTs and produce new ones based on functions provided by the user.

There's one hiccup though: the user can't provide *any* function to these processes. Since our datatypes must obey certain properties, the functions that operate on our datas must preserve these properties.

Recall that within a lattice, a partial order exists. One element is always `<=` another element. For example, with add-only sets, `{A} <= {A} <= {A, B} <= {A, B} <= {A, B, C}`. A *monotonic* function that operates over the domain of add-only sets must preserve this partial ordering. For example - if `{A} <= {A, B}` and `f` is a monotonic function that operates over add-only sets, `f({A}) <= f({A, B})`.

This ensures the preservation of our consistency properties across our ever-interacting processes.

### A Library

Remember that Lasp is an Erlang *library*. Within your existing Erlang program, you're free to drop in some interacting Lasp-processes. These processes will communicate using CRDTs and functions over CRDTs. As such, your Lasp sub-program is guaranteed to exhibit strong eventual consistency properties.

However, the rest of your Erlang program is not. Since Lasp is embeddable, it has no control over the rest of your Erlang program. You must be sure to use Lasp in a safe way. But since it doesn't provide the programmer with the ability to perform non-monotonic operations within the Lasp-context, the programmer can have significant confidence in the eventual consistency of the Lasp portion of the program. We still aren't totally safe from Jerry the intern, since Jerry can modify our outer-Erlang to do some dangerous things.

Bloom provided a new model for distributed programming, where Lasp aims to provide existing distributed systems with a drop-in solution for adding eventually consistent parts to their systems.

## Consistency Languages: Utilization

Compare Lasp and Bloom:

Lasp
* An Erlang library, meant to be used in every-day Erlang programs.
* Built-in CRDTs.
* All data structures are CRDTs and all operations are logically monotonic.
* Thus, it's essentially impossible to construct a non-monotonic program *using only the Lasp library*.
* It is possible to use Lasp in a non-monotonic way with disrupting outer Erlang code.
* Follows well-known functional programming patterns and is compatible with optimal Erlang style.

Bloom:
* Aims to be a full-featured language. Is not meant to be embeddable.
* Built-in set collections only. Allows user-defined CRDTs.
* Its sets are not add-only and thus not exclusively logically monotonic. User-defined lattices carry no formal proofs of their consistency gaurantees.
* It's possible to construct non-monotonic programs. Using the `<-` operator, for example.
* With the prototype, Bud, it's possible to use normal Ruby code to disrupt Bloom's properties. But this is more a result of the prototype implementation, not the design.
* Uses a unique programming model based on temporal logic.
* Contains an analysis tool that tells programmers which points in their code might require coordination, depending on the consistency concerns of the application.

Although they are fundamentally different in many ways, Lasp and Bloom accept a key reality: it's probably impossible to program using eventual consistency gaurantees only. It works for shopping carts, but there will always be situations where coordination between machines will need to occur. Lasp and Bloom's designs reflect the different approaches for dealing with this harsh truth.

Lasp, on one hand, plans to be an embeddable eventually-consistent library. If you're an Erlang developer and you recognized a situation in which you can accept eventual consistent properties, you can reach for the Lasp library. Within your existing code, you can add communication mechanisms using Lasp and be confident of the properties advertised by eventual consistent systems. No need to change your entire system or re-write code in a different language. Since Lasp does not allow the expression of non-monotonic programs, you express non-monotonicity *outside* of the Lasp sections in your code.

Bloom, on the other hand, aims to be an entirely new model for expressing distributed systems problems. By using CRDT-like sets for their collections, they can encourage a declarative way of programming without enforcing too much coordination. They even let the user define their own lattices with Bloom<sup>L</sup> to further encourage this type of programming. But since there will always be times where coordination is necessary, Bloom allows for operations that may require coordination. They even allow the user to perform non-monotonic operations such as `<-`. Bloom, in a way, must do this. They must provide the user with mechanisms for coordination, since they aim to create a new model for expressing distributed systems programs. Lasp is embeddable, so it can perform one specific job. Bloom is not, so it must allow many types of programs. In order to ameliorate this, Bloom provides the programmer with anaylsis tools to help the programmer identify points in the code that may not be totally safe. The programmer can then decide to coordinate or ignore these "points of order".

Most programming languages are "general-use". This works for single machine programming. As the world moves toward distributed programming, programmers must adopt models / languages / libraries that are built for their domain. It forces serious thought on the part of the programmer: what *exactly* am I trying to achieve, and what am I willing to sacrifice?

Bloom could potentially facilitate distributed systems programming through a new, temporal model. The Bloom developers have designed a language for a specific purpose: distributed programming. The Lasp developers take this philosophy even further: let's design a library for a specific subset of distributed systems programming. Although one goes deeper than the other, the two languages share an idea: languages / models should be build for subsets of the computing domain. Distributed systems produce difficult problems. When we put our heads together and develop tools to facilitate distributed systems programming (Bloom) and always *eventually consistent* distributed systems programming, programming gets easier. Fewer bugs pop up, and it becomes easier to formally reason about the behavior of our programs.

When a language or model tries to do everything well, it cannot provide formal guarantees or tools to facilitate certain problem solving. Since different domains have totally different needs and issues to deal with, general purpose programming languages simply try to provide the minimum required for a wide variety software problems.

If we shift our mindset as software developers and begin to develop and look for tools to help us with specific problems and domains of problems, we can leverage computers much more than we do today. Our tools can provide relevant feedback and help us design our systems. They can even provide formal properties that we need not question.

Critically, it requires a narrowing of our problem domain. It means inspecting our problem and asking what we need, and what's not so important?

In this chapter, we examined ways in which tools can help us leverage eventually consistent distributed systems. But there's no reason why this philosophy couldn't be applied to other subsections of the CAP pyramid. In fact, there's no reason why this philosophy couldn't be applied to other areas of computing in general. Why are both video games and distributed systems programmed using the same language & models?

Even if you don't encounter consistency issues in your day-to-day life, this idea applies to many areas of computing and tools in general. Hopefully you can begin to ask yourself and those around you: what tasks are we trying to accomplish, and how can our tools help us accomplish them?

## References

{% bibliography --file langs-consistency %}
