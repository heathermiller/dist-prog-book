---
layout: page
title:  "Futures"
by: "Kisalaya Prasad and Avanti Patil"
---

# Introduction

As human beings we have an ability to multitask ie. we can walk, talk and eat at the same time except when you sneeze. Sneeze is like a blocking activity from the normal course of action, because it forces you to stop what you’re doing for a brief moment and then you resume where you left off. Activities like multitasking are called multithreading in computer lingo. In contrast to this behaviour, computer processors are single threaded. So when we say that a computer system has multi-threaded environment, it is actually just an illusion created by processor where processor’s time is shared between multiple processes. Sometimes processor gets blocked when some tasks are hindered from normal execution due to blocking calls. Such blocking calls can range from IO operations like read/write to disk or sending/receiving packets to/from network. Blocking calls can take disproportionate amount of time compared to the processor’s task execution i.e. iterating over a list.


The processor can either handle blocking calls in two ways:
- **Synchronous method**: As a part of running task in synchronous method, processor continues to wait for the blocking call to complete the task and return the result. After this processor will resume processing next task. Problem with this kind of method is CPU time not utilized in an ideal manner.
- **Asynchronous method**: When you add asynchrony, you can utilize the time of CPU to work on some other task using one of the preemptive time sharing algorithm. Now when the asynchronous call returns the result, processor can again switch back to the previous process using preemption and resume the process from the point where it’d left off.

In the world of asynchronous communications many terminologies were defined to help programmers reach the ideal level of resource utilization. As a part of this article we will talk about motivation behind rise of Promises and Futures, we will explain programming model associated with it and discuss evolution of this programming construct, finally we will end this discussion with how this construct helps us today in different general purpose programming languages.


<figure>
  <img src="./images/1.png" alt="timeline" />
</figure>

# Motivation


A “Promise” object represents a value that may not be available yet. A Promise is an object that represents a task with two possible outcomes, success or failure and holds callbacks that fire when one outcome or the other has occurred.


The rise of promises and futures as a topic of relevance can be traced parallel to the rise of asynchronous or distributed systems. This seems natural, since futures represent a value available in Future which fits in very naturally with the latency which is inherent to these heterogeneous systems. The recent adoption of NodeJS and server side Javascript has only made promises more relevant. But, the idea of having a placeholder for a result came in significantly before than the current notion of futures and promises.


Thunks can be thought of as a primitive notion of a Future or Promise. According to its inventor P. Z. Ingerman, thunks are "A piece of coding which provides an address". They were designed as a way of binding actual parameters to their formal definitions in Algol-60 procedure calls. If a procedure is called with an expression in the place of a formal parameter, the compiler generates a thunk which computes the expression and leaves the address of the result in some standard location.


The first mention of Futures was by Baker and Hewitt in a paper on Incremental Garbage Collection of Processes. They coined the term - call-by-futures to describe a calling convention in which each formal parameter to a method is bound to a process which evaluates the expression in the parameter in parallel with other parameters. Before this paper, Algol 68 also presented a way to make this kind of concurrent parameter evaluation possible, using the collateral clauses and parallel clauses for parameter binding.


In their paper, Baker and Hewitt introduced a notion of Futures as a 3-tuple representing an expression E consisting of (1) A process which evaluates E, (2) A memory location where the result of E needs to be stored, (3) A list of processes which are waiting on E. But, the major focus of their work was not on role of futures and the role they play in Asynchronous distributed computing, and focused on garbage collecting the processes which evaluate expressions not needed by the function.


The Multilisp language, presented by Halestead in 1985 built upon this call-by-future with a Future annotation. Binding a variable to a future expression creates a process which evaluates that expression and binds x to a token which represents its (eventual) result. This design of futures influenced the paper of design of Promises in Argus by Liskov and Shrira in 1988. Building upon the initial design of Future in Multilisp, they extended the original idea by introducing strongly typed Promises and integration with call streams.This made it easier to handle exception propagation from callee to the caller and also to handle the typical problems in a multi-computer system like network failures. This paper also talked about stream composition, a notion which is similar to promise pipelining today.


E is an object-oriented programming language for secure distributed computing, created by Mark S. Miller, Dan Bornstein, and others at Electric Communities in 1997. One of the major contribution of E was the first non-blocking implementation of Promises. It traces its routes to Joule which was a dataflow programming language. The notion of promise pipelining in E is inherited from Joule.


Among the modern languages, Python was perhaps the first to come up with something on the lines of E’s promises with the Twisted library. Coming out in 2002, it had a concept of Deferred objects, which were used to receive the result of an operation not yet completed. They were just like normal objects and could be passed along, but they didn’t have a value. They supported a callback which would get called once the result of the operation was complete.  


Promises and javascript have an interesting history. In 2007 inspired by Python’s twisted, dojo came up with it’s own implementation of of dojo.Deferred. This inspired Kris Zyp to then come up with the CommonJS Promises/A spec in 2009. Ryan Dahl introduced the world to NodeJS in the same year. In it’s early versions, Node used promises for the non-blocking API. When NodeJS moved away from promises to its now familiar error-first callback API, it left a void for a promises API.  Q.js was an implementation of Promises/A spec by Kris Kowal around this time. FuturesJS library by AJ ONeal was another library which aimed to solve flow-control problems without using Promises in the strictest of senses. In 2011, JQuery v1.5 first introduced Promises to its wider and ever-growing audience. The API for JQuery was subtly different than the Promises/A spec. With the rise of HTML5 and different APIs, there came a problem of different and messy interfaces. A+ promises aimed to solve this problem. From this point on, leading from widespread adoption of A+ spec, promises was finally made a part of ECMAScript® 2015 Language Specification. Still, a lack of backward compatibility and additional features provided means that libraries like BlueBird and Q.js still have a place in the javascript ecosystem.


# Different Definitions


Future, promise, Delay or Deferred generally refer to same synchronisation mechanism where an object acts as a proxy for a yet unknown result. When the result is discovered, promises hold some code which then gets executed.

In some languages however, there is a subtle difference between what is a Future and a Promise.
“A ‘Future’ is a read-only reference to a yet-to-be-computed value”.
“A ‘Promise’ is a pretty much the same except that you can write to it as well.”


In other words, you can read from both Futures and Promises, but you can only write to Promises. You can get the Future associated with a Promise by calling the future method on it, but conversion in the other direction is not possible. Another way to look at it would be, if you Promise something, you are responsible for keeping it, but if someone else makes a Promise to you, you expect them to honor it in Future.


More technically, in Scala, “SIP-14 – Futures and Promises” defines them as follows:
A future is as a placeholder object for a result that does not yet exist.
A promise is a writable, single-assignment container, which completes a future. Promises can complete the future with a result to indicate success, or with an exception to indicate failure.


C# also makes the distinction between futures and promises. In C#, futures are implemented as Task<T> and in fact in earlier versions of the Task Parallel Library futures were implemented with a class Future<T> which later became Task<T>. The result of the future is available in the readonly property Task<T>.Result which returns T


In Javascript world, Jquery introduces a notion of Deferred objects which are used to represent a unit of work which is not yet finished. Deferred object contains a promise object which represent the result of that unit of work. Promises are values returned by a function, while the deferred object can be canceled by its caller.


In Java 8, the Future<T> interface has methods to check if the computation is complete, to wait for its completion, and to retrieve the result of the computation when it is complete. CompletableFutures can be thought of as Promises as their value can be set. But it also implements the Future interface and therefore it can be used as a Future too. Promises can be thought of as a future with a public set method which the caller (or anybody else) can use to set the value of the future.

# Semantics of Execution

Over the years promises and futures have been implemented in different programming languages. Different languages chose to implement  futures/promises in a different way. In this section, we try to introduce some different ways in which futures and promises actually get executed and resolved underneath their APIs.

## Thread Pools

Doing things in parallel is usually an effective way of doing things in modern systems. The systems are getting more and more capable of running more than one things at once, and the latency associated with doing things in a distributed environment is not going away anytime soon. Inside the JVM, threads are a basic unit of concurrency. Threads are independent, heap-sharing execution contexts. Threads are generally considered to be lightweight when compared to a process, and can share both code and data. The cost of context switching between threads is cheap. But, even if we claim that threads are lightweight, the cost of creation and destruction of threads in a long running threads can add up to something significant. A practical way is address this problem is to manage a pool of worker threads.


In Java executor is an object which executes the Runnable tasks. Executors provides a way of abstracting out how the details of how a task will actually run. These details, like selecting a thread to run the task, how the task is scheduled are managed by the object implementing the Executor interface. Threads are an example of a Runnable in java. Executors can be used instead of creating a thread explicitly.


Similar to Executor, there is an ExecutionContext as part of scala.concurrent. The basic intent behind it is same as an Executor : it is responsible for executing computations. How it does it can is opaque to the caller. It can create a new thread, use a pool of threads or run it on the same thread as the caller, although the last option is generally not recommended. Scala.concurrent package comes with an implementation of ExecutionContext by default, which is a global static thread pool.


ExecutionContext.global is an execution context backed by a ForkJoinPool. ForkJoin is a thread pool implementation designed to take advantage of a multiprocessor environment. What makes fork join unique is that it implements a type of work-stealing algorithm : idle threads pick up work from still busy threads. ForkJoinPool manages a small number of threads, usually limited to the number of processor cores available. It is possible to increase the number of threads, if all of the available threads are busy and wrapped inside a blocking call, although such situation would typically come with a bad system design. ForkJoin framework work to avoid pool-induced deadlock and minimize the amount of time spent switching between the threads.


Futures are generally a good way to reason about asynchronous code. A good way to call a webservice, add a block of code to do something when you get back the response, and move on without waiting for the response. They’re also a good framework to reason about concurrency as they can be executed in parallel, waited on, are composable, immutable once written and most importantly, are non blocking. in Scala, futures (and promises) are based on ExecutionContext.


In Scala, futures are created using an ExecutionContext. This gives the users flexibility to implement their own ExecutionContext if they need a specific behavior, like blocking futures. The default ForkJoin pool works well in most of the scenarios. Futures in scala are placeholders for a yet unknown value. A promise then can be thought of as a way to provide that value. A promise p completes the future returned by p.future.


Scala futures api expects an ExecutionContext to be passed along. This parameter is implicit, and usually ExecutionContext.global. An example :


```scala
implicit val ec = ExecutionContext.global
val f : Future[String] = Future { “hello world” }
```

In this example, the global execution context is used to asynchronously run the created future.  Taking another example,


```scala
implicit val ec = ExecutionContext.global

val f = Future {
  Http("http://api.fixed.io/latest?base=USD").asString
}

f.onComplete {
  case success(response) => println(response.body)
  case Failure(t) => println(t)
}
```


It is generally a good idea to use callbacks with Futures, as the value may not be available when you want to use it.

So, how does it all work together ?

As we mentioned, Futures require an ExecutionContext, which is an implicit parameter to virtually all of the futures API. This ExecutionContext is used to execute the future. Scala is flexible enough to let users implement their own Execution Contexts, but let’s talk about the default ExecutionContext, which is a ForkJoinPool.


ForkJoinPool is ideal for many small computations that spawn off and then come back together. Scala’s ForkJoinPool requires the tasks submitted to it to be a ForkJoinTask. The tasks submitted to the global ExecutionContext is quietly wrapped inside a ForkJoinTask and then executed. ForkJoinPool also supports a possibly blocking task, using ManagedBlock method which creates a spare thread if required to ensure that there is sufficient parallelism if the current thread is blocked. To summarize, ForkJoinPool is an really good general purpose ExecutionContext, which works really well in most of the scenarios.


## Event Loops

Modern systems typically rely on many other systems to provide the functionality they do. There’s a file system underneath, a database system, and other web services to rely on for the information. Interaction with these components typically involves a period where we’re doing nothing but waiting for the response back. This is single largest waste of computing resources.


Javascript is a single threaded asynchronous runtime. Now, conventionally async programming is generally associated with multi-threading, but we’re not allowed to create new threads in Javascript. Instead, asynchronicity in Javascript is achieved using an event-loop mechanism.


Javascript has historically been used to interact with the DOM and user interactions in the browser, and thus an event-driven programming model was a natural fit for the language. This has scaled up surprisingly well in high throughput scenarios in NodeJS.


The general idea behind event-driven programming model is that the logic flow control is determined by the order in which events are processed. This is underpinned by a mechanism which is constantly listening for events and fires a callback when it is detected. This is the Javascript’s event loop in a nutshell.


A typical Javascript engine has a few basic components. They are :
- **Heap**
Used to allocate memory for objects
- **Stack**
Function call frames go into a stack from where they’re picked up from top to be executed.
- **Queue**
	A message queue holds the messages to be processed.


Each message has a callback function which is fired when the message is processed. These messages can be generated by user actions like button clicks or scrolling, or by actions like HTTP requests, request to a database to fetch records or reading/writing to a file.


Separating when a message is queued from when it is executed means the single thread doesn’t have to wait for an action to complete before moving on to another. We attach a callback to the action we want to do, and when the time comes, the callback is run with the result of our action. Callbacks work good in isolation, but they force us into a continuation passing style of execution, what is otherwise known as Callback hell.


```javascript

getData = function(param, callback){
  $.get('http://example.com/get/'+param,
    function(responseText){
      callback(responseText);
    });
}

getData(0, function(a){  
    getData(a, function(b){
        getData(b, function(c){
            getData(c, function(d){
                getData(d, function(e){

                });
            });
        });
    });
});

```

<center><h4> VS </h4></center>

```javascript

getData = function(param, callback){
  return new Promise(function(resolve, reject) {
    $.get('http://example.com/get/'+param,
    function(responseText){
      resolve(responseText);
    });
  });
}

getData(0).then(getData)
  .then(getData).
    then(getData).
      then(getData);


```

> **Programs must be written for people to read, and only incidentally for machines to execute.** - *Harold Abelson and Gerald Jay Sussman*

Promises are an abstraction which make working with async operations in javascript much more fun. Moving on from a continuation passing style, where you specify what needs to be done once the action is done, the callee simply returns a Promise object. This inverts the chain of responsibility, as now the caller is responsible for handling the result of the promise when it is settled.

The ES2015 spec specifies that “promises must not fire their resolution/rejection function on the same turn of the event loop that they are created on.” This is an important property because it ensures deterministic order of execution. Also, once a promise is fulfilled or failed, the promise’s value MUST not be changed. This ensures that a promise cannot be resolved more than once.

Let’s take an example to understand the promise resolution workflow as it happens inside the Javascript Engine.

Suppose we execute a function, here g() which in turn, calls function f(). Function f returns a promise, which, after counting down for 1000 ms, resolves the promise with a single value, true. Once f gets resolved, a value true or false is alerted based on the value of the promise.


<figure>
  <img src="./images/5.png" alt="timeline" />
</figure>

Now, javascript’s runtime is single threaded. This statement is true, and not true. The thread which executes the user code is single threaded. It executes what is on top of the stack, runs it to completion, and then moves onto what is next on the stack. But, there are also a number of helper threads which handle things like network or timer/settimeout type events. This timing thread handles the counter for setTimeout.

<figure>
  <img src="./images/6.png" alt="timeline" />
</figure>

Once the timer expires, the timer thread puts a message on the message queue. The queued up messages are then handled by the event loop. The event loop as described above, is simply an infinite loop which checks if a message is ready to be processed, picks it up and puts it on the stack for it’s callback to be executed.

<figure>
  <img src="./images/7.png" alt="timeline" />
</figure>

Here, since the future is resolved with a value of true, we are alerted with a value true when the callback is picked up for execution.

<figure>
  <img src="./images/8.png" alt="timeline" />
</figure>

Some finer details :
We’ve ignored the heap here, but all the functions, variables and callbacks are stored on heap.
As we’ve seen here, even though Javascript is said to be single threaded, there are number of helper threads to help main thread do things like timeout, UI, network operations, file operations etc.
Run-to-completion helps us reason about the code in a nice way. Whenever a function starts, it needs to finish before yielding the main thread. The data it accesses cannot be modified by someone else. This also means every function needs to finish in a reasonable amount of time, otherwise the program seems hung. This makes Javascript well suited for I/O tasks which are queued up and then picked up when finished, but not for data processing intensive tasks which generally take long time to finish.
We haven’t talked about error handling, but it gets handled the same exact way, with the error callback being called with the error object the promise is rejected with.


Event loops have proven to be surprisingly performant. When network servers are designed around multithreading, as soon as you end up with a few hundred concurrent connections, the CPU spends so much of its time task switching that you start to lose overall performance. Switching from one thread to another has overhead which can add up significantly at scale. Apache used to choke even as low as a few hundred concurrent users when using a thread per connection while Node can scale up to a 100,000 concurrent connections based on event loops and asynchronous IO.


## Thread Model


Oz programming language introduced an idea of dataflow concurrency model. In Oz, whenever the program comes across an unbound variable, it waits for it to be resolved. This dataflow property of variables helps us write threads in Oz that communicate through streams in a producer-consumer pattern. The major benefit of dataflow based concurrency model is that it’s deterministic - same operation called with same parameters always produces the same result. It makes it a lot easier to reason about concurrent programs, if the code is side-effect free.


Alice ML is a dialect of Standard ML with support for lazy evaluation, concurrent, distributed, and constraint programming. The early aim of Alice project was to reconstruct the functionalities of Oz programming language on top of a typed programming language. Building on the Standard ML dialect, Alice also provides concurrency features as part of the language through the use of a future type. Futures in Alice represent an undetermined result of a concurrent operation. Promises in Alice ML are explicit handles for futures.


Any expression in Alice can be evaluated in it's own thread using spawn keyword. Spawn always returns a future which acts as a placeholder for the result of the operation. Futures in Alice ML can be thought of as functional threads, in a sense that threads in Alice always have a result. A thread is said to be touching a future if it performs an operation that requires the value future is a placeholder for. All threads touching a future are blocked until the future is resolved. If a thread raises an exception, the future is failed and this exception is re-raised in the threads touching it. Futures can also be passed along as values. This helps us achieve the dataflow model of concurrency in Alice.


Alice also allows for lazy evaluation of expressions. Expressions preceded with the lazy keyword are evaluated to a lazy future. The lazy future is evaluated when it is needed. If the computation associated with a concurrent or lazy future ends with an exception, it results in a failed future. Requesting a failed future does not block, it simply raises the exception that was the cause of the failure.

# Implicit vs. Explicit Promises


We define Implicit promises as ones where we don’t have to manually trigger the computation vs Explicit promises where we have to trigger the resolution of future manually, either by calling a start function or by requiring the value. This distinction can be understood in terms of what triggers the calculation : With Implicit promises, the creation of a promise also triggers the computation, while with Explicit futures, one needs to triggers the resolution of a promise. This trigger can in turn be explicit, like calling a start method, or implicit, like lazy evaluation where the first use of a promise’s value triggers its evaluation.


The idea for explicit futures were introduced in the Baker and Hewitt paper. They’re a little trickier to implement, and require some support from the underlying language, and as such they aren’t that common. The Baker and Hewitt paper talked about using futures as placeholders for arguments to a function, which get evaluated in parallel, but when they’re needed. Also, lazy futures in Alice ML have a similar explicit invocation mechanism, the first thread touching a future triggers its evaluation.

Implicit futures were introduced originally by Friedman and Wise in a paper in 1978. The ideas presented in that paper inspired the design of promises in MultiLisp. Futures are also implicit in Scala and Javascript, where they’re supported as libraries on top of the core languages. Implicit futures can be implemented this way as they don’t require support from language itself. Alice ML’s concurrent futures are also an example of implicit invocation.

# Promise Pipelining
One of the criticism of traditional RPC systems would be that they’re blocking. Imagine a scenario where you need to call an API ‘a’ and another API ‘b’, then aggregate the results of both the calls and use that result as a parameter to another API ‘c’. Now, the logical way to go about doing this would be to call A and B in parallel, then once both finish, aggregate the result and call C. Unfortunately, in a blocking system, the way to go about is call a, wait for it to finish, call b, wait, then aggregate and call c. This seems like a waste of time, but in absence of asynchronicity, it is impossible. Even with asynchronicity, it gets a little difficult to manage or scale up the system linearly. Fortunately, we have promises.

<figure>
  <img src="./images/9.png" alt="timeline" />
</figure>

Futures/Promises can be passed along, waited upon, or chained and joined together. These properties helps make life easier for the programmers working with them. This also reduces the latency associated with distributed computing. Promises enable dataflow concurrency, which is also deterministic, and easier to reason.

The history of promise pipelining can be traced back to the call-streams in Argus and channels in Joule. In Argus, Call streams are a mechanism for communication between distributed components. The communicating entities, a sender and a receiver are connected by a stream, and sender can make calls to receiver over it. Streams can be thought of as RPC, except that these allow callers to run in parallel with the receiver while processing the call. When making a call in Argus, the caller receives a promise for the result. In the paper on Promises by Liskov and Shrira, they mention that having integrated futures into call streams, next logical step would be to talk about stream composition. This means arranging streams into pipelines where output of one stream can be used as input of the next stream. They talk about composing streams using fork and coenter.


Modern promise specifications, like one in Javascript comes with methods which help working with promise pipelining easier. In javascript, a Promises.all method is provided, which takes in an iterable over Promises, and returns a new Promise which gets resolved when all the promises in the iterable get resolved. There’s also a race method, which returns a promise which is resolved when the first promise in the iterable gets resolved.


In scala, futures have a onSuccess method which acts as a callback to when the future is complete. This callback itself can be used to sequentially chain futures together. But this results in bulkier code. Fortunately, Scala api comes with combinators which allow for easier combination of results from futures. Examples of combinators are map, flatmap, filter, withFilter.

# Handling Errors

In a synchronous programming model, the most logical way of handling errors is a try...catch block.

```javascript

try{
    do something1;
    do something2;
    do something3;
    ...
} catch ( exception ){
    HandleException;
}

```

Unfortunately, the same thing doesn’t directly translate to asynchronous code.


```javascript

foo = doSomethingAsync();

try{
    foo();
    // This doesn’t work as the error might not have been thrown yet
} catch ( exception ){
    handleException;
}


```

In javascript world, some patterns emerged, most noticeably the error-first callback style, also adopted by Node. Although this works, but it is not very composable, and eventually takes us back to what is called callback hell. Fortunately, Promises come to the rescue.


Although most of the earlier papers did not talk about error handling, the Promises paper by Liskov and Shrira did acknowledge the possibility of failure in a distributed environment. They talked about propagation of exceptions from the called procedure to the caller and also about call streams, and how broken streams could be handled. E language also talked about broken promises and setting a promise to the exception of broken references.

In modern languages, Promises generally come with two callbacks. One to handle  the success case and other to handle the failure.


#### In Scala
```scala

f onComplete {
   case Success(data) => handleSuccess(data)
   case Failure(e) => handleFailure(e)
}
```

#### In Javascript
```javascript

promise.then(function (data) {
    // success callback
    console.log(data);
}, function (error) {
   // failure callback
   console.error(error);
});

```

In Javascript, Promises have a catch method, which help deal with errors in a composition. Exceptions in promises behave the same way as they do in a synchronous block of code : they jump to the nearest exception handler.


```javascript
function work(data) {
    return Promise.resolve(data+"1");
}

function error(data) {
    return Promise.reject(data+"2");
}

function handleError(error) {
    return error +"3";
}


work("")
.then(work)
.then(error)
.then(work) // this will be skipped
.then(work, handleError)
.then(check);

function check(data) {
    console.log(data == "1123");
    return Promise.resolve();
}

```

The same behavior can be written using catch block.


```javascript

work("")
.then(work)
.then(error)
.then(work)
.catch(handleError)
.then(check);

function check(data) {
    console.log(data == "1123");
    return Promise.resolve();
}

```

# Futures and Promises in Action


## Twitter Finagle


Finagle is a protocol-agnostic, asynchronous RPC system for the JVM that makes it easy to build robust clients and servers in Java, Scala, or any JVM-hosted language. It uses idea of Futures to encapsulate concurrent tasks and are analogous to threads, but even more lightweight.


## Correctables
Correctables were introduced by Rachid Guerraoui, Matej Pavlovic, and Dragos-Adrian Seredinschi at OSDI ‘16, in a paper titled Incremental Consistency Guarantees for Replicated Objects. As the title suggests, Correctables aim to solve the problems with consistency in  replicated objects. They provide incremental consistency guarantees by capturing successive changes to the value of a replicated object. Applications can opt to receive a fast but possibly inconsistent result if eventual consistency is acceptable, or to wait for a strongly consistent result. Correctables API draws inspiration from, and builds on the API of Promises.  Promises have a two state model to represent an asynchronous task, it starts in blocked state and proceeds to a ready state when the value is available. This cannot represent the incremental nature of correctables. Instead, Correctables have a updating state when it starts. From there on, it remains in updating state during intermediate updates, and when the final result is available, it transitions to final state. If an error occurs in between, it moves into an error state. Each state change triggers a callback.

<figure>
  <img src="./images/15.png" alt="timeline" />
</figure>

## Folly Futures
Folly is a library by Facebook for asynchronous C++ inspired by the implementation of Futures by Twitter for Scala. It builds upon the Futures in the C++11 Standard. Like Scala’s futures, they also allow for implementing a custom executor which provides different ways of running a Future (thread pool, event loop etc).


## NodeJS Fiber
Fibers provide coroutine support for v8 and node. Applications can use Fibers to allow users to write code without using a ton of callbacks, without sacrificing the performance benefits of asynchronous IO.  Think of fibers as light-weight threads for nodejs where the scheduling is in the hands of the programmer. The node-fibers library doesn’t recommend using raw API and code together without any abstractions, and provides a Futures implementation which is ‘fiber-aware’.

## References

{% bibliography --file futures %}
