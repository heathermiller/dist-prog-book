---
layout: page
title:  "Large Scale Parallel Data Processing"
by: "Jingjing and Abhilash"
---
## Introduction
`JJ: Placeholder for introduction` The booming Internet has generated big data...


This chapter is organized in <label for="note1" class="margin-toggle sidenote-number"></label><input type="checkbox" id="note1" class="margin-toggle"/><span class="sidenote">JJ: need to fill in more stuff</span>

- **Data paralleling**:
  - MapReduce {% cite dean2008mapreduce  --file big-data %}
  - FlumeJava {% cite chambers2010flumejava --file big-data %}
  - ...
- **Graph paralleling**:
  - Pregel 
  - ...

For each programming model, we will discuss the motivation, basic model, execution model, fault-tolerance and performance.


Ideas: get a table of what to include in the context
Idea: instead of data/graph, maybe add one more layer (unstructured vs. structured)

# Data paralleling

## MapReduce (2004)
MapReduce {% cite dean2008mapreduce  --file big-data %} is a programming model that allows programmers to express the simple computations for terabytes data on thousands of commodity machines.

**Basic & Examples**  
This model applies to computations that are usually parallelizable: A `map` function can operate on each logical "record", this generates a set of intermediate key/value pairs, and then a `reduce` function applies on all values that share the same key and generate one or zero output value.

Concretely, considering the problem of counting the number of occurrence of each word in a large collection of documents: each time, a `map` function that emits a word plus its count 1; a `reduce` function sums together all counts emitted for the same word

```
map(String key, String value):
  // key: document name
  // value: document contents
  for each word w in value:
    EmitIntermediate(w, "1");

reduce(String key, Iterator values):
  // key: a word
  // values: a list of counts
  int result = 0;
  for each v in values:
    result += ParseInt(v);
  Emit(AsString(result));
```

Conceptually, the map and reduction functions have associated **types**:
```
map (k1,v1) -> → list(k2,v2)
reduce (k2,list(v2)) -> list(v2)
```
The input keys and values are drawn from a different domain than the output keys and values. The intermediate keys and values are from the same domain as the output keys and values. The implementation given by the authors essentially pass strings and it is users' responsibility to convert between strings and appropriate types.

More formalized descriptions about the `map` and `reduce` function can be found in the original paper {% cite dean2008mapreduce  --file big-data %}.

**Execution**   
At high level, when the user program calls *MapReduce* function, the input files are split into *M* pieces and it runs *map* function on corresponding splits; then intermediate key space are partitioned into *R* pieces using a partitioning function; After the reduce functions all successfully complete, the output is available in *R* files. The sequences of actions {% cite dean2008mapreduce  --file big-data %} are shown in the figure below. We can see from label (4) and (5) that the intermediate key/value pairs are written/read into disks, this is a key to fault-tolerance in MapReduce model and also a bottleneck for more complex computation algorithms.  

<figure class="main-container">
  <img src="{{ site.baseurl }}/resources/img/mapreduce-execution.png" alt="MapReduce Execution Overview" />
</figure>


**Fault Tolerance**  
In this model, there are two parts that could fail: the master and the worker.  
- Worker failure: The master pings every worker periodically and if no response in a certain amount of time, master marks the worker as failed and re-assign it to an idle worker.
- Master Failure: If the master fail, MapReduce function fails. The model itself assumes that master won't fail and they have separate mechanics to backup the master, which is out of the scope of our discussion.  

The output from distributed computation should be same as one from non-faulting sequential execution of the entire program. And the model relies on the atomic commits of map and reduce task outputs to achieve this. The basic idea is to create private temporary files and rename them only when the task has finished.

There are some practices in this paper that make the model work very well in Google, one of them is **backup tasks**: when a MapReduce operation is close to completion, the master schedules backup executions of the remaining in-progress tasks ("straggler"). The task is marked as completed whenever either the primary or the backup execution completes.

`JJ: what about other refinement: `

**Performance**  
In the paper, the authors measure the performance of MapReduce on two computations running on a large cluster of machines. One computation *grep* through approximately 1TB of data. The other computation *sort* approximately 1TB of data. Both computations take in the order of a hundred seconds. In addition, the backup tasks do help largely reduce execution time. In the experiment where 200 out of 1746 tasks were intentionally killed, the scheduler was able to recover quickly and finish the whole computation for just a 5% increased time.  
Overall, the performance is very good for conceptually unrelated computations.


## FlumeJava (2010)
Many real-world computations involves a pipeline of MapReduces, and this motivates additional management to chain together those separate MapReduce stages in an efficient way. FlumeJava {% cite chambers2010flumejava --file big-data %} can help build those pipelines and keep computations modular. At core, FlumeJava are a couple of classes that represent immutable parallel collections. It defers evaluation and optimization by internally constructing an execution plan dataflow graph.

**Core Abstraction**  

- `PCollection<T>`, a immutable bag of elements of type `T`
- `recordOf(...)`, specifies the encoding of the instance
- `PTable<K, V>`, a subclass of `PCollection<Pair<K,V>>`, a immutable multi-map with keys of type `K` and values of type `V`
- `parallelDo()`, can be expressed both the map and reduce parts of MapReduce
- `groupByKey()`, same as shuffle step of MapReduce `JJ: clear this in MapReduce`
- `combineValues()`, semantically a special case of `parallelDo()`, a combination of a MapReduce combiner and a MapReduce reducer, which is more efficient than doing all the combining in the reducer.

**Deferred Evaluation**  
`(JJ: placehoder) join, deferred/materialized; execution plan; figure 1 initial execution plan`

**Optimizer**  
`(JJ: placehoder) parallelDo Fusion; MSCR;  overall goal to produce the fewest, most efficient MSCR operations in the final optimized plan`

# Graph paralleling

Though highly efficient and one of the first major programming models for distributed batch processing, it too has a few limitations.<br />
Map Reduce doesn’t scale easily and is highly inefficient for iterative / graph algorithms like page rank and machine learning algorithms. Iterative algorithms requires programmer to explicitly handle the intermediate results (writing to disks). Hence, every iteration requires reading the input file and writing the results to the disk resulting in high disk I/O which is a performance bottleneck for any batch processing system. <br />
Also graph algorithms require exchange of messages between vertices. In case of PageRank, every vertex requires the contributions from all its adjacent nodes to calculate its score. Map reduce currently lacks this model of message passing which makes it complex to reason about graph algorithms. <br />
## Bulk synchronous parallel model
This model was introduced in 1980 to represent the hardware design features of parallel computers. It gained popularity as an alternative for map reduce since it addressed the above mentioned issues with map reduce to an extent.<br />
In BSP model
+ Computation consists of several steps called as supersets.
+ The processors involved have their own local memory and every processor is connected to other via a point-to-point communication.
+ At every superstep, a processor receives input at the beginning, performs computation and outputs at the end.
+ Barrier synchronization synchs all the processors at the end of every superstep.<br />

A notable feature of the model is the complete control on data through communication between every processor at every superstep. BSP preserves data in memory across supersteps and helps in reasoning iterative graph algorithms.<br />
`Pregel` is an implementation of classic BSP model by Google (PageRank) to analyze large graphs exclusively. It was followed by open source implementations - Apache’s Giraph and Hama; which were BSP models built on top of Hadoop.
Pregel is highly scalable, fault-tolerant and can successfully represent larger complex graphs. Google claims the API becomes easy once a developer adopts “think like a vertex” mode.
Pregel’s computation system is iterative and every iteration is called as superstep. The system takes a directed graph as input with properties assigned to both vertices and graph. At each superstep, all vertices executes in parallel, a user-defined function which represents the behavior of the vertex. The function has access to message sent to its vertex from the previous superstep S-1 and can update the state of the vertex, its edges, the graph and even send messages to other vertices which would receive in the next superstep S+1. The synchronization happens only between two supersteps.  Every vertex is either active or inactive at any superstep. The iteration stops when all the vertices are inactive. A vertex can deactivate itself by voting for it and gets active if it receives a message. This asynchronous message passing feature eliminates the shared memory, remote reads and latency of Map reduce model.<br />
Pregel’s API provides <br />
+ compute() method for the user to implement the logic to change the state of the graph/vertex at every superstep. It guarantees message delivery through an iterator at every superstep.
+ User defined handler for handling issues like missing destination vertex etc.
+ Combiners reduce the amount of messages passed from multiple vertices to the same destination vertex.
+ Aggregators capture the global state of the graph. A reduce operation combines the value given by every vertex to the aggregator. The combined/aggregated value is passed onto to all the vertices in the next superstep.
+ Fault tolerance is achieved through checkpointing and instructing the workers to save the state of nodes to a persistent storage. When a machine fails, all workers restart the execution with state of their recent checkpoint.
+ Master and worker implementation : The master partitions graph into set of vertices (hash on vertex ID mod number of partitions) and outgoing edges per partition. Each partition is assigned to a worker who manages the state of all its vertices by executing compute() method and coordinating the message communication. The workers also notifies the master of the vertices that are active for the next superstep.<br/>

Pregel works good for sparse graphs. However, dense graph could cause communication overhead resulting in system to break. Also, the entire computation state resides in the main memory.
Apache Giraph is an open source implementation of Pregel in which new features like master computation, sharded aggregators, edge-oriented input, out-of-core computation are added making it more efficient.  The most high performance graph processing framework is GraphLab which is developed at Carnegie Melon University and uses the BSP model and executes on MPI.


## References
{% bibliography --file big-data %}

"Bulk synchronous model" http://www.cse.unt.edu/~tarau/teaching/parpro/papers/Bulk%20synchronous%20parallel.pdf.
"Pregel: A System for Large-Scale Graph Processing." <br />
"One Trillion Edges: Graph Processing at Facebook-Scale." Accessed November 17, 2016. http://www.vldb.org/pvldb/vol8/p1804-ching.pdf.
