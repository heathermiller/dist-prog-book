---
layout: page
title:  "Large Scale Streaming Processing"
by: "Fangfan Li"
---

The previous chapter discusses the systems around batch layer, where the computation involves the pieces of data stored across the distributed file system. Those systems satisfy the requirements such as scalablibility and fault-tolerance for applications that deal with 'big data' stored in a distributed way. The batch processing systems are suitable for processing *static* datasets, where the input data do not change overtime during the whole process, thus the system can distribute the computation and perform synchronization assuming the inputs would stay the same during the whole computation. In such *static* model, the processing system can first *pull* data from the disk, and then perform the computation over the pulled data. However, a large number of networking applications are not *static*, instead, the data is constantly in motion, and the inputs would be provided as *stream*, as new data constantly arrives. In the *stream* model, data is *pushed* to the processor. This fundamental difference makes the traditional batch processing system un-suitable for streaming applications, as even the slightest change in the dataset would require the batch processer to *pull* the whole dataset and perform the computation again. Thus in this chapter, we would introduce the history and systems that are created for the streaming processing. 

There are many challenges for implementing large scale streaming processing system. Similar to large scale batch processing sytems, large scale streaming systems also have to deal with consistency and fault-tolenrace due to the distributed nature of those systems. Moreover, latency at the scale of several minutes is at most a nuisance in batch processing while latency is not as tolerable in large streaming processing.

In the rest of this chapter, we would fist introduce the 1) History of streaming processing 2) How to represent the input data stream 3) What are the practices to process data stream 4) The state-of-the-art systems used by applications.

1.Data in constant motion

This concept of streaming data can trace back to TelegraphCQ, which aims at meeting the challenges that arise in handling large streams of continuous queries over high-volume, high-variable data streams. In contrast to trafitional view that data can be found statically in known locations, the authors of TelegraphCQ realized that data becomes fluid and being constantly moving and changing. The examples of applications that use *data in motion* include: event-based processing, query processing over streaming data sources such as network monitoring. TelegraphCQ is one example of the query processing systems that deals with data stream. The fundamental difference between TelegraphCQ to other traditional query system is the view of input data, instead of handling a query with detailed static data, TelegraphCQ has to react to the newly arrived data and process the queries *on-the-fly*. 

The important concepts of TelegraphCQ include *continuous queries*, where the queries are constantly running and as new data arrives, the processor would route it to the set of active queries that are listening. TelegraphCQ also uses *shared processing* to avoid the overhead of processing each query individually, the queries with some commonality can be combined together to improve the performance.

TelegraphCQ shows the importance of modeling data as stream and how can we process such data stream. But TelegraphCQ was only implemented in a non-distributed prototype, we would then discuss how data steam is processed in a large scale.

2.How to represent data stream

Before dive into the details of the large scale processing, we would first introduce a few concepts: producer, processor and consumer. In this section, we would discuss the component between producers and processors-the data stream.

We have been talking about the stream of data, but this is a bit under-specified, since the data can be collected from many producers (i.e. different monitors), how do we combine those data into actual streams and send the them to the processors? What does a data stream really look like?

A natural view of a data stream can be an infinite sequence of tuples reading from a queue. However, a traditional queue would not be sufficient in large scale system since the consumed tuple might got lost or the consumer might fail thus it might request the previous tuple after a restart. The alternative queue design is a multi-consumer queue, for example Apache Kafka provides que that allows users to rewind the stream and replay everything from the point of failure, ensuring that the processed events are in the order of their origination.

3.How to process data stream

We would then talk about the processors that cosume the data stream. There are two main approaches in processing data stream. The first approach is the continuous queries model, similar TelegraphCQ, where the queries keep running and the arrival of data intiates the processing. Another approach is micro-batching, where the streaming computation becomes a series of stateless, deterministic batch computations on small time intervals, and the timer would triger the processing in those systems. We would discuss Apach Storm as an example for the fist design and Spark Streaming as an example for the second approach.

a) Continuous queries(operators)

Apache Storm

b) Micro-batch

Spark Streaming

4.The systems being used nowadays, how ideas combined and products produced

a) Twitter's Heron (real-time analytic platform that is fully API-compatible with Storm)

b) Spotify (Google's DataFlow)

{% cite Uniqueness --file streaming %}

## References

{% bibliography --file streaming %}