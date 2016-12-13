## Trash


## Performance
`TODO: re-organize` There are some practices in this paper that make the model work very well in Google, one of them is **backup tasks**: when a MapReduce operation is close to completion, the master schedules backup executions of the remaining in-progress tasks ("straggler"). The task is marked as completed whenever either the primary or the backup execution completes.
In the paper, the authors measure the performance of MapReduce on two computations running on a large cluster of machines. One computation *grep* through approximately 1TB of data. The other computation *sort* approximately 1TB of data. Both computations take in the order of a hundred seconds. In addition, the backup tasks do help largely reduce execution time. In the experiment where 200 out of 1746 tasks were intentionally killed, the scheduler was able to recover quickly and finish the whole computation for just a 5% increased time.  
Overall, the performance is very good for conceptually unrelated computations.



## Outline
- 1. Programming Models
  - 1.1. Data parallelism: what is data parallelism and how do the following models relate to each other?
    - 1.1.1 MapReduce
    - 1.1.2 FlumeJava
    - 1.1.3 Dryad
    - 1.1.4 Spark

  - 1.2. Querying: we need more declarative interfaces, built on top MR models.
    - Sawzall {%cite pike2005interpreting --file big-data %}: first one propose
    - Pig {% cite olston2008pig --file big-data %}: on top of Hadoop, independent of execution platform, in theory can compiled into DryadLINQ too; what is the performance gain/lost? Easier to debug?   
    - Hive {%cite thusoo2009hive --file big-data %}
    - DryadLINQ: SQL-like, uses Dryad as execution engine;   
    `Suggestion: Merge this with Dryad above?`
    - Dremel, query natively w/o translating into MR jobs
    - Spark SQL {%cite --file big-data %} - Limitations of Relational alone models? how SparkSQL model overcomes it? goals of SparkSQL? how it leverages the Spark programming model? what is a DataFrame and how is it different from a RDD? what are the operations a DataFrame provides? how is in-memory caching different from Spark?

  - 1.3. Large-scale Parallelism on Graphs
    - Why a separate graph processing model? what is a BSP? working of BSP? Do not stress more since its not a map reduce world exactly.
    - GraphX programming model - discuss disadvantages graph-parallel model to data parallel model for large scale graph processing? how graphX combines the advantages of both the models? representation of a graph in GraphX?  discuss the model, vertex cut partitioning and its importance? graph operations ?


- 2. Execution Models
  - 2.1 MapReduce (intermediate writes to disk): What is the sequence of actions when a MapReduce functions are called? How is write-to-disk good/bad (fault-tolerant/slow)? How does the data are transmitted across clusters efficiently (store locally)? To shorten the total time for MR operations, it uses backup tasks. When MR jobs are pipelined, what optimizations can be performed by FlumeJava? In spite of optimizations and pipelining, what is the inherent limitation (not support iterative algorithm?)
  - 2.2 Spark (all in memory): introduce spark architecture, different layers, what happens when a spark job is executed? what is the role of a driver/master/worker, how does a scheduler schedule the tasks and what performance measures are considered while scheduling? how does a scheduler manage node failures and missing partitions? how are the user defined transformations passed to the workers? how are the RDDs stored and memory management measures on workers? do we need checkpointing at all given RDDs leverage lineage for recovery? if so why ?
  - 2.3 Graphs :
    - Pregel :Overview of Pregel. Its implementation and working. its limitations. Do not  stress more since we have a better model GraphX to explain a lot.
    - GraphX : Working on this.
  - SparkSQL Catalyst & Spark execution model : Discuss Parser, LogicalPlan, Optimizer, PhysicalPlan, Execution Plan. Why catalyst? how catalyst helps in SparkSQL , data flow from sql-core-> catalyst->spark-core

- 3. Evaluation: Given same algorithm, what is the performance differences between Hadoop, Spark, Dryad? There are no direct comparison for all those models, so we may want to compare separately:
  - Hadoop vs. Spark
  - Spark vs. SparkSQL from SparkSQL paper

- 4. Big Data Ecosystem   
  Everything interoperates with GFS or HDFS, or makes use of stuff like protocol buffers so systems like Pregel and MapReduce and even MillWheel...
  - GFS/HDFS for MapReduce/Hadoop: Machines are unreliable, how do they provide fault-tolerance? How does GFS deal with single point of failure (shadow masters)? How does the master manage partition, transmission of data chunks? Which
  - Resource Management: Mesos. New frameworks keep emerging and users have to use multiple different frameworks(MR, Spark etc.) in the same clusters, so how should they share access to the large datasets instead of costly replicate across clusters?
  - Introducing streaming: what happens when data cannot be complete? How does different programming model adapt? windowing `todo: more`

  2015 NSDI Ousterhout

  latency numbers that every programmer should know
