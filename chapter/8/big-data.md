---
layout: page
title:  "Large Scale Parallel Data Processing"
by: "Jingjing and Abhilash"
---
## Introduction
`JJ: Placeholder for introduction` The booming Internet has generated big data...

This chapter is organized in

- Programming Models
  - Data parallelism (most popular, standard map/reduce/functional pipelining)
    - PM of MapReduce: basic, limitation, pipelining > FlumeJava
    - PM of Dryad: can support DAG computation, limitations: low-level, `Q: Should this go to execution model?`
    - PM of Spark, RDD/lineage: can support iterative algorithm, interactive analytics
  - Large-scale Parallelism on Graphs
    - PM of Pregel/GraphX
  - Querying: more declarative `Q: put here or in the execution model?`
    - DryadLINQ, SQL-like, use Dryad as execution engine;
    - Pig, on top of Hadoop, independent of execution platform, in theory can compiled into DryadLINQ too; what is the performance gain/lost? Easier to debug?
    - Hive, SQL-like, on top of Hadoop, what is the performance gain/lost.
    - Dremel, query natively w/o translating into MP jobs
    - Spark SQL, on top of Spark

- Execution Models
  - MapReduce (intermediate writes to disk)
    - Limitations, iteration, performance
  - Spark (all in memory)
    - Limitations ?
  - Pregel
    - Limitations ?
- Performance
- Things people are building on top of MapReduce/Spark
  - // FlumeJava? ...Etc
  - Ecosystem, everything interoperates with GFS or HDFS, or makes use of stuff like protocol buffers so systems like Pregel and MapReduce and even MillWheel...

## Programming Model
### Data parallelism
The motivation for MapReduce {% cite dean2008mapreduce  --file big-data %} is that we want to use hundreds/thousands of machines to do data processing in parallel, but we don’t want to deal with low-level management. MapReduce can help this by abstracting computing logic into simple map and reduce functions and let the computation model handle the parallelization and distribution, provide fault tolerance, manage I/O scheduling and get proper status updates. The solution in the MapReduce paper is simple and powerful in terms of separating programming model and the executing model. This model applies to computations that are usually parallelizable: A `map` function can operate on each logical "record", this generates a set of intermediate key/value pairs, and then a `reduce` function applies on all values that share the same key and generate one or zero output value. Conceptually, the map and reduction functions have associated **types**:
```
map (k1,v1) -> → list(k2,v2)
reduce (k2,list(v2)) -> list(v2)
```
The input keys and values are drawn from a different domain than the output keys and values. The intermediate keys and values are from the same domain as the output keys and values.

**Execution** At high level, when the user program calls *MapReduce* function, the input files are split into *M* pieces and it runs *map* function on corresponding splits; then intermediate key space are partitioned into *R* pieces using a partitioning function; After the reduce functions all successfully complete, the output is available in *R* files. The sequences of actions are shown in the figure below. We can see from label (4) and (5) that the intermediate key/value pairs are written/read into disks, this is a key to fault-tolerance in MapReduce model and also a bottleneck for more complex computation algorithms.  

<figure class="main-container">
  <img src="{{ site.baseurl }}/resources/img/mapreduce-execution.png" alt="MapReduce Execution Overview" />
</figure>

**Limitations & Extensions**  
***Real-world applications often require a pipeline of MapReduce jobs and the management becomes an issue.***  
**FlumeJava** was introduced to make it easy to develop, test, and run efficient data-parallel pipelines. FlumeJava represents each dataset as an object and transformation is invoked by using methods on these objects. It constructs an efficient internal execution plan from a pipeline of MapReduce jobs using deferred evaluation and optimizers such as fusions. The debugging ability allows programmers to run on the local machine first and then deploy to large clusters.


***The iterative algorithm is hard to implement in MapReduce***   
  `TODO: FIX text and reference` Many a analytics workloads like K-means, logistic regression, graph processing applications like PageRank, shortest path using parallel breadth first search require multiple stages of map reduce jobs. In regular map reduce framework like Hadoop, this requires the developer to manually handle the iterations in the driver code. At every iteration, the result of each stage T is written to HDFS and loaded back again at stage T+1 causing a performance bottleneck. The reason being wastage of network bandwidth, CPU resources and mainly the disk I/O operations which are inherently slow. In order to address such challenges in iterative workloads on map reduce, frameworks like Haloop, Twister and iMapReduce adopt special techniques like caching the data between iterations and keeping the mapper and reducer alive across the iterations.

**Dryad/DrydaLINQ** Dryad is a more general and flexible execution engine that execute subroutines at a specified graph vertices. Developers can specify an arbitrary directed acyclic graph to combine computational "vertices" with communication channels (file, TCP pipe, shared-memory FIFO) and  build a dataflow graph. Compared with MapReduce, Dryad can specify an arbitrary DAG that have multiple number of inputs/outputs and support multiple stages. Also it can have more channels and boost the performance when using TCP pipes and shared-memory. But like writing a pipeline of MapReduce jobs, Dryad is a low-level programming model and hard for users to program, thus a more declarative model - DryadLINQ was created to fill in the gap. It exploits LINQ, a query language in .NET and automatically translates the data-parallel part into execution plan and passed to the Dryad execution engine.



### Large-scale Parallelism on Graphs
Map Reduce doesn’t scale easily and is highly inefficient for iterative / graph algorithms like page rank and machine learning algorithms. Iterative algorithms requires programmer to explicitly handle the intermediate results (writing to disks). Hence, every iteration requires reading the input file and writing the results to the disk resulting in high disk I/O which is a performance bottleneck for any batch processing system.

Also graph algorithms require exchange of messages between vertices. In case of PageRank, every vertex requires the contributions from all its adjacent nodes to calculate its score. Map reduce currently lacks this model of message passing which makes it complex to reason about graph algorithms. One model that is commonly employed for implementing distributed graph processing is the Bulk Synchronous Parallel model.

This model was introduced in 1980 to represent the hardware design features of parallel computers. It gained popularity as an alternative for map reduce since it addressed the above mentioned issues with map reduce<br />
BSP model is a message passing synchronous model where - 

 - Computation consists of several steps called as supersets.
 - The processors involved have their own local memory and every processor is connected to other via a point-to-point communication.
 - At every superstep, a processor receives input at the beginning, performs computation and outputs at the end.
 - A processor at superstep S can send message to another processor at superstep S+1 and can as well receive message from superstep S-1.
 - Barrier synchronization synchs all the processors at the end of every superstep.
 
A notable feature of the model is the complete control on data through communication between every processor at every superstep. Though similar to map reduce model, BSP preserves data in memory across supersteps and helps in reasoning iterative graph algorithms.

### Querying



## Execution Models
**MapReduce**, as mentioned in the programming model section, the execution model is interesting that all the intermediate key/value pairs are written to and read from disk. The output from distributed computation should be same as one from non-faulting sequential execution of the entire program. And the model relies on the atomic commits of map and reduce task outputs to achieve it. The basic idea is to create private temporary files and rename them only when the task has finished. This makes fault-tolerance easy, one could simple start another one if the worker failed. But this is also the bottleneck to run multiple stages.

**Spark**
Spark is a fast, in-memory data processing engine with an elegant and expressive development interface which enables developers to efficiently execute machine learning, SQL or streaming workloads that require fast iterative access to datasets. Spark takes advantage of the distributed in-memory storage (RDD), Scala’s collection API as well as functional style for high performance processing. 

Distributed in-memory storage - Resilient Distributed Data sets :
RDD is a partitioned, read only collection of objects which can be created from data in stable storage or by transforming other RDD. It can be distributed across multiple nodes in a cluster and is fault tolerant(Resilient). If a node fails, a RDD can always be recovered using its lineage graph (information on how it was derived from dataset). A RDD is stored in memory (as much as it can fit and rest is spilled to disk) and is immutable - It can only be transformed to a new RDD. These are the lazy transformations which are applied only if any action is performed on the RDD. Hence, RDD need not be materialized at all times. Lazy feature exists even in DyradLINQ.

The properties that power RDD with the above mentioned features :
	•	A list of dependencies on other RDD’s. 
	•	An array of partitions that a dataset is divided into.
	•	A compute function to do a computation on partitions.
	•	Optionally, a Partitioner for key-value RDDs (e.g. to say that the RDD is hash-partitioned)
	•	Optional preferred locations (aka locality info), (e.g. block locations for an HDFS file)

Spark API provide two kinds of operations on a RDD:
Transformations - lazy operations that return another RDD.
`map (f : T => U) : RDD[T] ⇒ RDD[U]` : Return a MappedRDD[U] by applying function f to each element
`flatMap( f : T ⇒ Seq[U]) : RDD[T] ⇒ RDD[U]` : Return a new FlatMappedRDD[U] by first applying a function to all elements and then flattening the results.
`filter(f:T⇒Bool) : RDD[T] ⇒ RDD[T]` : Return a FilteredRDD[T] having elemnts that f return true
`groupByKey()` : Being called on (K,V) Rdd, return a new RDD[([K], Iterable[V])]
`reduceByKey(f: (V, V) => V)` : Being called on (K, V) Rdd, return a new RDD[(K, V)] by aggregating values using eg: reduceByKey(_+_)
`join((RDD[(K, V)], RDD[(K, W)]) ⇒ RDD[(K, (V, W))]` :Being called on (K,V) Rdd, return a new RDD[(K, (V, W))] by joining them by key K.


Actions - operations that trigger computation on a RDD and return values.

`reduce(f:(T,T)⇒T) : RDD[T] ⇒ T` : return T by reducing the elements using specified commutative and associative binary operator
`collect()` : Return an Array[T] containing all elements
`count()` : Return the number of elements


Why RDD over Distributed Shared memory (DSM) ?
RDDs are immutable and can only be created through coarse grained transformation while DSM allows fine grained read and write operations to each memory location. Hence RDDs do not incur the overhead of checkpointing thats present in DSM and can be recovered using their lineages.
RDDs are immutable and hence a straggler(slow node) can be replaced with backup copy as in Map reduce. This is hard to implement in DSM as two copies point to the same location and can interfere in each other’s update.
Other benefits include the scheduling of tasks based on data locality to improve performance and the ability of the RDDs to degrade gracefully incase of memory shortage. Partitions that do not fit in RAM gets spilled to the disk (performance will then be equal to that of any data parallel system).


- Pig/HiveQL/SparkSQL
  - Limitations ?

**Pregel**
Pregel is an implementation of classic BSP model by Google (PageRank) to analyze large graphs exclusively. It was followed by open source implementations - Apache’s Giraph and Hama; which were BSP models built on top of Hadoop.

Pregel is highly scalable, fault-tolerant and can successfully represent larger complex graphs. Google claims the API becomes easy once a developer adopts “think like a vertex” mode.
Pregel’s computation system is iterative and every iteration is called as superstep. The system takes a directed graph as input with properties assigned to both vertices and graph. At each superstep, all vertices executes in parallel, a user-defined function which represents the behavior of the vertex. The function has access to message sent to its vertex from the previous superstep S-1 and can update the state of the vertex, its edges, the graph and even send messages to other vertices which would receive in the next superstep S+1. The synchronization happens only between two supersteps.  Every vertex is either active or inactive at any superstep. The iteration stops when all the vertices are inactive. A vertex can deactivate itself by voting for it and gets active if it receives a message. This asynchronous message passing feature eliminates the shared memory, remote reads and latency of Map reduce model.

Pregel’s API provides

- compute() method for the user to implement the logic to change the state of the graph/vertex at every superstep. It guarantees message delivery through an iterator at every superstep.
- User defined handler for handling issues like missing destination vertex etc.
- Combiners reduce the amount of messages passed from multiple vertices to the same destination vertex.
- Aggregators capture the global state of the graph. A reduce operation combines the value given by every vertex to the aggregator. The combined/aggregated value is passed onto to all the vertices in the next superstep.
- Fault tolerance is achieved through checkpointing and instructing the workers to save the state of nodes to a persistent storage. When a machine fails, all workers restart the execution with state of their recent checkpoint.
- Master and worker implementation : The master partitions graph into set of vertices (hash on vertex ID mod number of partitions) and outgoing edges per partition. Each partition is assigned to a worker who manages the state of all its vertices by executing compute() method and coordinating the message communication. The workers also notifies the master of the vertices that are active for the next superstep.

Pregel works good for sparse graphs. However, dense graph could cause communication overhead resulting in system to break. Also, the entire computation state resides in the main memory and hence constrained by the size of main memory.

Apache Giraph is an open source implementation of Pregel in which new features like master computation, sharded aggregators, edge-oriented input, out-of-core computation are added making it more efficient.  The most high performance graph processing framework is GraphLab which is developed at Carnegie Melon University and uses the BSP model and executes on MPI.


## Performance
`TODO: re-organize` There are some practices in this paper that make the model work very well in Google, one of them is **backup tasks**: when a MapReduce operation is close to completion, the master schedules backup executions of the remaining in-progress tasks ("straggler"). The task is marked as completed whenever either the primary or the backup execution completes.
In the paper, the authors measure the performance of MapReduce on two computations running on a large cluster of machines. One computation *grep* through approximately 1TB of data. The other computation *sort* approximately 1TB of data. Both computations take in the order of a hundred seconds. In addition, the backup tasks do help largely reduce execution time. In the experiment where 200 out of 1746 tasks were intentionally killed, the scheduler was able to recover quickly and finish the whole computation for just a 5% increased time.  
Overall, the performance is very good for conceptually unrelated computations.


## Things people are building on top of MapReduce/Spark
  - FlumeJava? ...Etc
  - Ecosystem, everything interoperates with GFS or HDFS, or makes use of stuff like protocol buffers so systems like Pregel and MapReduce and even MillWheel...

## References
{% bibliography --file big-data %}











## Trash


## Iterative processing in Map Reduce

Many a analytics workloads like K-means, logistic regression, graph processing applications like PageRank, shortest path using parallel breadth first search require multiple stages of map reduce jobs. In regular map reduce framework like Hadoop, this requires the developer to manually handle the iterations in the driver code. At every iteration, the result of each stage T is written to HDFS and loaded back again at stage T+1 causing a performance bottleneck. The reason being wastage of network bandwidth, CPU resources and mainly the disk I/O operations which are inherently slow. In order to address such challenges in iterative workloads on map reduce, frameworks like Haloop, Twister and iMapReduce adopt special techniques like caching the data between iterations and keeping the mapper and reducer alive across the iterations.




**Haloop** : HaLoop: Efficient Iterative Data Processing on Large Clusters.

**iMapReduce**: iMapReduce: A Distributed Computing Framework for Iterative Computation

**Twister** :  Twister: a runtime for iterative MapReduce.

## Map Reduce inspired large scale data processing systems

**Dryad/DryadLinq** :

**Spark (big one)** :

## Declarative interfaces for the Map Reduce framework
Map reduce provides only two high level primitives - map and reduce; that the programmers have to worry about. Map reduce takes care of all the processing over a cluster, failure and recovery, data partitioning etc. However, the framework still suffers from rigidity with respect to its one-input data format (key/value pair) and two-stage data flow. Several important patterns like joins (which could be highly complex depending on the data) are extremely hard to implement and reason about for a programmer. Sometimes the code could be become repetitive  when the programmer wants to implement most common operations like projection, filtering etc.
Non-programmers like data scientists would highly prefer SQL like interface over a cumbersome and rigid framework. Such a high level declarative language can easily express their task while leaving all of the execution optimization details to the backend engine. Also, these kind of abstractions provide ample opportunities for query optimizations.

**Introduce Sazwal** (its now no more used but one of the first ideas) : Parallel analysis with Sawzall. Scientific Programming, 13(4):277–298, 2005

** FlumeJava (2010) **

Many real-world computations involves a pipeline of MapReduces, and this motivates additional management to chain together those separate MapReduce stages in an efficient way. FlumeJava {% cite chambers2010flumejava --file big-data %} can help build those pipelines and keep computations modular. At core, FlumeJava are a couple of classes that represent immutable parallel collections. It defers evaluation and optimization by internally constructing an execution plan dataflow graph.

***Core Abstraction***

- `PCollection<T>`, a immutable bag of elements of type `T`
- `recordOf(...)`, specifies the encoding of the instance
- `PTable<K, V>`, a subclass of `PCollection<Pair<K,V>>`, a immutable multi-map with keys of type `K` and values of type `V`
- `parallelDo()`, can be expressed both the map and reduce parts of MapReduce
- `groupByKey()`, same as shuffle step of MapReduce `JJ: clear this in MapReduce`
- `combineValues()`, semantically a special case of `parallelDo()`, a combination of a MapReduce combiner and a MapReduce reducer, which is more efficient than doing all the combining in the reducer.

***Deferred Evaluation***
`(JJ: placehoder) join, deferred/materialized; execution plan; figure 1 initial execution plan`

***Optimizer***  
`(JJ: placehoder) parallelDo Fusion; MSCR;  overall goal to produce the fewest, most efficient MSCR operations in the final optimized plan`


**Pig Latin** : Pig latin: a not-so-foreign language for data processing. In SIGMOD, pages 1099–1110, 2008.

**Hive** :

**Dremel** :


## SparkSQL - Where Relational meets Procedural :
Relational interface to big data is good, however, it doesn’t cater to users who want to perform

- ETL to and from various semi or unstructured data sources.
- advanced analytics like machine learning or graph processing.

These user actions require best of both the worlds - relational queries and procedural algorithms. Spark SQL bridges this gap by letting users to seamlessly intermix both relational and procedural API.

Hence, the major contributions of Spark SQL are the Dataframe API and the Catalyst. Spark SQL intends to provide relational processing over native RDDs and on several external data sources, through a programmer friendly API, high performance through DBMS techniques, support semi-structured data and external databases, support for advanced analytical processing like machine learning algorithms and graph processing.

***Programming API***

Spark SQL runs on the top of Spark providing SQL interfaces. A user can interact with this interface though JDBC/ODBC, command line or Dataframe API.
A Dataframe API lets users to intermix both relational and procedural code with ease. Dataframe is a collection of schema based rows of data and named columns on which relational operations can be performed with optimized execution. Unlike a RDD, Dataframe allows developers to define structure for the data and can be related to tables in a relational database or R/Python’s Dataframe. Dataframe can be constructed from tables of external sources or existing native RDD’s. Dataframe is lazy and each object in it represents a logical plan which is not executed until an output operation like save or count is performed.
Spark SQL supports all the major SQL data types including complex data types like arrays, maps and unions.
Some of the Dataframe operations include projection (select), filter(where), join and aggregations(groupBy).
Illustrated below is an example of relational operations on employees data frame to compute the number of female employees in each department.

```
employees.join(dept, employees("deptId") === dept("id")) .where(employees("gender") === "female") .groupBy(dept("id"), dept("name")) .agg(count("name"))
```
Several of these operators like  === for equality test, > for greater than, a rithmetic ones (+, -, etc) and aggregators transforms to a abstract syntax tree of the expression which can be passed to Catalyst for optimization.
A cache() operation on the data frame helps Spark SQL store the data in memory so it can be used in iterative algorithms and for interactive queries. In case of Spark SQL, memory footprint is considerably less as it applies columnar compression schemes like dictionary encoding / run-length encoding.
MORE EXPLANATION NEEDED...



## Optimizers are the way to go (still thinking of a better heading..)

It is tough to understand the internals of a framework like Spark for any developer who has just started to program a Spark application. Also, with the advent of relational code, it becomes still more challenging when one has to program keeping in mind the rules for an efficient query - rightly ordered joins, early filtering of data or usage of available indexes. Even if the programmer is aware of such rules, it is still prone to human errors which can potentially lead to longer runtime applications. Query optimizers for map reduce frameworks can greatly improve performance of the queries developers write and also significantly reduce the development time. A good query optimizer should be able to optimize such user queries, extensible for user to provide information about the data and even dynamically include developer defined specific rules.
Catalyst is one such framework which leverages the Scala’s functional language features like pattern matching and runtime meta programming to allow developers to concisely specify complex relational optimizations. Most of the power of Spark SQL comes due to this optimizer.

Catalyst includes both rule-based and cost-based optimization. It is extensible to include new optimization techniques and features to Spark SQL and also let developers provide data source specific rules.


Catalyst executes the rules on its data type Tree - a composition of node objects where each node has a node type (subclasses of TreeNode class in Scala) and zero or more children. Node objects are immutable and can be manipulated. The transform method of a Tree applies pattern matching to match a subset of all possible input trees on which the optimization rules needs to be applied.

In Spark SQL, transformation happens in four phases :

- Analyzing a logical plan to resolve references  : In the analysis phase a relation either from the abstract syntax  tree (AST) returned by the SQL parser or from a DataFrame is analyzed to create a logical plan out of it, which is still unresolved (the columns referred may not exist or may be of wrong datatype). The logical plan is resolved using using the Catalyst’s Catalog object(tracks the table from all data sources) by mapping the named attributes to the input provided, looking up the relations by name from catalog, by propagating and coercing types through expressions.

- Logical plan optimization : In this phase, several of the rules like constant folding, predicate push down, projection pruning, null propagation, boolean expression simplification are applied on the logical plan.

- Physical planning : In this phase, Spark generates multiples physical plans out of the input logical plan and chooses the plan based on a cost model. The physical planner also performs rule-based physical optimizations, such as pipelining projections or filters into one Spark map operation. In addition, it can push operations from the logical plan into data sources that support predicate or projection pushdown.

- Code Generation : The final phase generates the Java byte code that should run on each machine.Catalyst transforms the Tree which is an expression in SQL to an AST for Scala code to evaluate, compile and run the generated code. A special scala feature namely quasiquotes aid in the construction of abstract syntax tree(AST).

STILL WORKING ON THIS..

## Large Scale Graph processing

Map Reduce doesn’t scale easily and is highly inefficient for iterative / graph algorithms like page rank and machine learning algorithms. Iterative algorithms requires programmer to explicitly handle the intermediate results (writing to disks). Hence, every iteration requires reading the input file and writing the results to the disk resulting in high disk I/O which is a performance bottleneck for any batch processing system.

Also graph algorithms require exchange of messages between vertices. In case of PageRank, every vertex requires the contributions from all its adjacent nodes to calculate its score. Map reduce currently lacks this model of message passing which makes it complex to reason about graph algorithms.

**Bulk synchronous parallel model**

This model was introduced in 1980 to represent the hardware design features of parallel computers. It gained popularity as an alternative for map reduce since it addressed the above mentioned issues with map reduce to an extent.<br />
In BSP model

 - Computation consists of several steps called as supersets.
 - The processors involved have their own local memory and every processor is connected to other via a point-to-point communication.
 - At every superstep, a processor receives input at the beginning, performs computation and outputs at the end.
 - Barrier synchronization synchs all the processors at the end of every superstep.
 - A notable feature of the model is the complete control on data through communication between every processor at every superstep.
 - Though similar to map reduce model, BSP preserves data in memory across supersteps and helps in reasoning iterative graph algorithms.



**Introduce GraphX and why it fares better than BSP model. Explain GraphX**

## Future and Discussion

- Current leader in distributed processing - Spark, Google's cloud dataflow
- Current challenges and upcoming improvements ?? - Apache thunder and any others?


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
