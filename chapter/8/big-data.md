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


## Iterative processing in Map Reduce:

Many a analytics workloads like K-means, logistic regression, graph processing applications like PageRank, shortest path using parallel breadth first search require multiple stages of map reduce jobs. In regular map reduce framework like Hadoop, this requires the developer to manually handle the iterations in the driver code. At every iteration, the result of each stage T is written to HDFS and loaded back again at stage T+1 causing a performance bottleneck. The reason being wastage of network bandwidth, CPU resources and mainly the disk I/O operations which are inherently slow. In order to address such challenges in iterative workloads on map reduce, frameworks like Haloop, Twister and iMapReduce adopt special techniques like caching the data between iterations and keeping the mapper and reducer alive across the iterations.

Haloop : HaLoop: Efficient Iterative Data Processing on Large Clusters.

iMapReduce: iMapReduce: A Distributed Computing Framework for Iterative Computation

Twister :  Twister: a runtime for iterative MapReduce.

## Map Reduce inspired other large scale data processing systems :

Dryad/DryadLinq : 

Spark (big one) : content is ready, need to format a bit and paste

## Declarative interfaces for the Map Reduce framework:
Map reduce provides only two high level primitives - map and reduce; that the programmers have to worry about. Map reduce takes care of all the processing over a cluster, failure and recovery, data partitioning etc. However, the framework still suffers from rigidity with respect to its one-input data format (key/value pair) and two-stage data flow. Several important patterns like joins (which could be highly complex depending on the data) are extremely hard to implement and reason about for a programmer. Sometimes the code could be become repetitive  when the programmer wants to implement most common operations like projection, filtering etc.
Non-programmers like data scientists would highly prefer SQL like interface over a cumbersome and rigid framework. Such a high level declarative language can easily express their task while leaving all of the execution optimization details to the backend engine. Also, these kind of abstractions provide ample opportunities for query optimizations.

Introduce Sazwal (its now no more used but one of the first ideas) : Parallel analysis with Sawzall. Scientific Programming, 13(4):277–298, 2005

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


Pig Latin : Pig latin: a not-so-foreign language for data processing. In SIGMOD, pages 1099–1110, 2008.

Hive : 

Dremel :


## Where Relational meets Procedural : 
Relational interface to big data is good, however, it doesn’t cater to users who want to perform
1> ETL to and from various semi or unstructured data sources.
2> advanced analytics like machine learning or graph processing.
These user actions require best of both the worlds - relational queries and procedural algorithms. Spark SQL bridges this gap by letting users to seamlessly intermix both relational and procedural API.
Hence, the major contributions of Spark SQL are the Dataframe API and the Catalyst.
Spark SQL intends to provide relational processing over native RDDs and on several external data sources, through a programmer friendly API, high performance through DBMS techniques, support semi-structured data and external databases, support for advanced analytical processing like machine learning algorithms and graph processing.
Programming API : 
Spark SQL runs on the top of Spark providing SQL interfaces. A user can interact with this interface though JDBC/ODBC, command line or Dataframe API.
A Dataframe API lets users to intermix both relational and procedural code with ease. Dataframe is a collection of schema based rows of data and named columns on which relational operations can be performed with optimized execution. Unlike a RDD, Dataframe allows developers to define structure for the data and can be related to tables in a relational database or R/Python’s Dataframe. Dataframe can be constructed from tables of external sources or existing native RDD’s. Dataframe is lazy and each object in it represents a logical plan which is not executed until an output operation like save or count is performed.
Spark SQL supports all the major SQL data types including complex data types like arrays, maps and unions.
Some of the Dataframe operations include projection (select), filter(where), join and aggregations(groupBy).
Illustrated below is an example of relational operations on employees data frame to compute the number of female employees in each department.
employees
.join(dept, employees("deptId") === dept("id")) .where(employees("gender") === "female") .groupBy(dept("id"), dept("name")) .agg(count("name"))
Several of these operators like  === for equality test, > for greater than, a rithmetic ones (+, -, etc) and aggregators transforms to a abstract syntax tree of the expression which can be passed to Catalyst for optimization.
A cache() operation on the data frame helps Spark SQL store the data in memory so it can be used in iterative algorithms and for interactive queries. In case of Spark SQL, memory footprint is considerably less as it applies columnar compression schemes like dictionary encoding / run-length encoding. 
MORE EXPLANATION NEEDED...



## Optimizers are the way to go :
It is tough to understand the internals of a framework like Spark for any developer who has just started to program a Spark application. Also, with the advent of relational code, it becomes still more challenging when one has to program keeping in mind the rules for an efficient query - rightly ordered joins, early filtering of data or usage of available indexes. Even if the programmer is aware of such rules, it is still prone to human errors which can potentially lead to longer runtime applications. Query optimizers for map reduce frameworks can greatly improve performance of the queries developers write and also significantly reduce the development time. A good query optimizer should be able to optimize such user queries, extensible for user to provide information about the data and even dynamically include developer defined specific rules. 
Catalyst is one such framework which leverages the Scala’s functional language features like pattern matching and runtime meta programming to allow developers to concisely specify complex relational optimizations. Most of the power of Spark SQL comes due to this optimizer.

Catalyst includes both rule-based and cost-based optimization. It is extensible to include new optimization techniques and features to Spark SQL and also let developers provide data source specific rules. 
Catalyst executes the rules on its data type Tree - a composition of node objects where each node has a node type (subclasses of TreeNode class in Scala) and zero or more children. Node objects are immutable and can be manipulated. The transform method of a Tree applies pattern matching to match a subset of all possible input trees on which the optimization rules needs to be applied.
In Spark SQL, transformation happens in four phases :
Analyzing a logical plan to resolve references  : In the analysis phase a relation either from the abstract syntax  tree (AST) returned by the SQL parser or from a DataFrame is analyzed to create a logical plan out of it, which is still unresolved (the columns referred may not exist or may be of wrong datatype). The logical plan is resolved using using the Catalyst’s Catalog object(tracks the table from all data sources) by mapping the named attributes to the input provided, looking up the relations by name from catalog, by propagating and coercing types through expressions.

Logical plan optimization : In this phase, several of the rules like constant folding, predicate push down, projection pruning, null propagation, boolean expression simplification are applied on the logical plan.

Physical planning : In this phase, Spark generates multiples physical plans out of the input logical plan and chooses the plan based on a cost model. The physical planner also performs rule-based physical optimizations, such as pipelining projections or filters into one Spark map operation. In addition, it can push operations from the logical plan into data sources that support predicate or projection pushdown.


Code Generation : The final phase generates the Java byte code that should run on each machine.Catalyst transforms the Tree which is an expression in SQL to an AST for Scala code to evaluate, compile and run the generated code. A special scala feature namely quasiquotes aid in the construction of abstract syntax tree(AST).






## References
{% bibliography --file big-data %}
