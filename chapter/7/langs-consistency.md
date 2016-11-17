---
layout: page
title:  "Languages Built For Consistency"
by: "James Larisch"
---
# Languages Built For Consistency

## What's the problem?
  As processors become expensive and the limits of Moore's Law are pushed, programmers lately find themselves in situations where they need to connect multiple computers together using a network cable. Perhaps it's not even due to cost or performance constraints; perhaps your company has servers in New York and San Fransisco, and there is some global state that requires synchronization across the country. Problems requiring solutions of this nature can be described as "distributed systems" problems. Your data / processing power / entry points are distributed for some reason. In many ways, web developers deal with distributed systems problems every day: your client and your server are in two different geographical locations, and thus, some coordination is required.

  As Aviral discussed in the previous section, many computer scientists have done a lot of thinking about the nature of distributed systems problems. As such, we realize that it's impossible to completely emulate the behavior of a single computational machine using multiple machines. For example, the network simply is not reliable - and if we wait for it to be reliable, we sacrifice things like timeliness. After discussing the Consistency/Availability/Partition-tolerance theorem, Section 6 discussed how we can make drill down into the CAP pyramid and choose the properties of our systems. As stated, we can't perfectly emulate a single computer, but once we accept that fact... there are plenty of things we *can* do!

## The Shopping Cart
  Let's bring all these theorem talk back to reality. Let's say you're working at a new e-commerce startup, and you'd like to revolutionize the electronic shopping cart. You'd like to give the customer the ability to do the following:
  * Log in to the site and add a candle to the cart while traveling Beijing.
  * Take a HyperLoop train (3 hours) from Beijing to Los Angeles.
  * Log back into the site, remove the candle from their cart, and add a skateboard to their cart.
  * Take another HyperLoop train from Los Angeles to Paris (5 hours).
  * Log back into the site, add another skateboard, and checkout.

  Let's assume you have a server in every single country, and customers connect to the geographically closest server.

  If you only had 1 user of your website, this wouldn't be too hard. You could constantly send out messages to all of your servers and personally make sure the state of the customer's shopping cart is consistent across every single server. But what happens when you have millions of customers and thus millions of shopping carts? That would be impossible to keep track of personally. Luckily, you're a programmer - this can be automated! You simply need to make sure that all of your computers stay i-sync, so if the customer checks her cart in Beijing, then in Paris, she sees the same thing.

  But as Section 6 already explained, this is not so trivial. Messages between your servers in Beijing and Paris could get dropped, corrupted, reordered, duplicated, or delayed. Since you have no guarantees about when you'll be able to synchronize state between two servers, it's possible that the customer could see two different cart-states depending on which server she asks.

  If you're confident that the servers' state will eventually converge, you could present the user with an error message until the states have converged. That way, you know the user is looking at consistent state. [I may be overlapping too much with Aviral's section here. will wait until I see his draft before continuing.

  Mention Amazon's Dynamo + shopping cart.

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
      var clientAddition = Interface.receiveInput(); // contrived
      this.addItem(clientAddition);
      var receivedState = mySocket.nonBlockingRead(); // contrived
      if (receivedState !== undefined) {
        this.receiveState(receivedState);
      }
      synchronize();
      sleep(10);
      run();
    }
  }

  // theoretical usage

  var socket = new UDPSocket(); // contrived
  var cart = new Cart(peerSockets, socket); // peerSockets is an array of UDP sockets
  cart.run();
  ```

  Here is an (almost) fully functional shopping cart program. You can imagine this code running across multiple nodes scattered over the world. The meat of the program lies in the `run()` method. Let's walk through that:
  1. Program receives an addition to the cart from the user.
  2. Program adds that item to the current local state.
  3. Program checks its UDP socket for any messages.
  4. If it received one, it's means another instance of this program has sent us its state. What is state in this case? Simply a set of cart items. Let's handle this set of items by unioning it with our current set.
  5. Synchronize our current state by sending our state to every peer that we know about.
  6. Sleep for 10 seconds.
  7. Repeat!

  Hopefully it's clear that if a client adds an item to her cart in Beijing and then 10 seconds later checks her cart in Paris, she should see the same thing. Well, not exactly - remember, the network is unreliable, and Beijing's `synchronize` messages might have been dropped. But no worries! Beijing is `synchronizing` again in another 10 seconds.

  This is the *Strong Eventual Consistency* concept that Aviral introduced in Section 6. It's *eventual* because given a long enough timeline the clients' states will sync up: they are constantly trying to synchronize. [mention you can't remove things trivially, this is actually a CRDT, union is a monotonic operation]

### The Intern
  Unfortunately Jerry, the intern, has found your code. He'd like to make a few changes. He messes it up somehow. I'm not entirely sure how yet.

### Guarantees
  The original Javascript we wrote down exhibits the property from Section 6 known as *monotonicity*. The union operation ensures that a given node's state is always "greater than or equal to" the states of the other nodes. However, how can we be *sure* that this property is maintained throughout the development of this program? As we've seen, there's nothing stopping an intern from coming along, making a mindless change, and destroying this wonderful property. Ideally, we want to make it impossible (or at least very difficult) to write programs that violate this property. Or, at the very least, we want to make it very easy to write programs that maintain these types of properties.

  But where should these guarantees live? In the above Javascript example, the guarantees aren't guarantees at all, really. There's no restriction on what the programmer is allowed to do - the programmer has simply constructed a program that mirrors guarantees that she has modeled in her brain. In order to maintain properties such as *monotonicity*, she must constantly check the model in her brain against the code. We haven't really helped the programmer out that much - she has a lot of thinking to do.

  At the disk hardward level, there are certain mechanisms in place to ensure that data does not become corrupted when multiple things attempt to write bits to the same physical location. This is considered a type of IO-consistency. It doesn't help much with our shopping cart, but it's certainly necessary. These important guarantees facilitate the higher level abstractions by ensuring low-level safety. It would be unreasonable to expect our disks to enforce monotonicity, for example, since this would restrict usage of disks to monotonic programs only (more on this later!). But on the other hand, as we've seen, pushing the consistency to the application/programmer level is also unreasonable. Our tools should work for us.

  Why not push the consistency guarantees in between? Is there any reason why you as the programmer couldn't program using tools that facilitate these types of monotonic programs? If you're familiar with formal systems -- why not construct a formal system (programming language / library) in which every theorem (program) is formally guarunteed to be monotonic? If it's *impossible* to express a non-monotonic program, the programmer needn't worry about maintaining a direct mapping between their code and their mental model.

  Wouldn't it be great if tools like this existed?

### Bloom
  The dudes/dudettes at Berkeley seem to think so too.

#### Restriction & Danger
  [Bloom restricts you, it's different, and it's dangerous]

### Lasp
  [Library not language, embeddable, not dangerous]
  Instead of trying to do it all (and accepting danger), it tries to be embeddable (and truly restrictive.)



## References

{% bibliography --file langs-consistency %}
