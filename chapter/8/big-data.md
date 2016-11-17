---
layout: page
title:  "Large Scale Parallel Data Processing"
by: "Joe Schmoe and Mary Jane"
---

Though highly efficient and one of the first major programming models for distributed batch processing, it too has a few limitations.<br />
Map Reduce doesn’t scale easily and is highly inefficient for iterative / graph algorithms like page rank and machine learning algorithms. Iterative algorithms requires programmer to explicitly handle the intermediate results (writing to disks). Hence, every iteration requires reading the input file and writing the results to the disk resulting in high disk I/O which is a performance bottleneck for any batch processing system. <br />
Also graph algorithms require exchange of messages between vertices. In case of PageRank, every vertex requires the contributions from all its adjacent nodes to calculate its score. Map reduce currently lacks this model of message passing which makes it complex to reason about graph algorithms. <br />
### Bulk synchronous parallel model
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
