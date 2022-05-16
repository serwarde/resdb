# Resilient Databases

## Introduction
In many domains, such as security, financial services, and the well-known e-commerce operations, the consequences of failure are unacceptable, even the slightest outage has significant financial consequences and impacts customer trust. In addition, applications experience workload changes. How to make a database resilient to failures and workload changes? 

To set out for an answer, we refer to Amazon’s Dynamo storage system and designed a distributed Key-Value store, to achieve: high availability, elasticity, and load balance automatically. In the implementation, we used Consistent Hashing and Rendezvous Hashing algorithm as a comparison.
***
## Research Questions:
- How to build a distributed database that's resilient to the failure of one of its components while also balance itself for fluctuating data processing demands?
- Can we provide the missing details from the Dynamo paper about how to maintain replication when network topology changes. 
- Is the "folklore" true that Rendezvous Hashing is an alternative to Consistent Hashing?  Where do they differ (if any) in the context of resilience such as replication?
- Can we develop a deployable distributed system with minimal setup?

***
## Contribution

In the project, a distributed Key-Value storage system was implemented that has high availability, elasticity, and automatic load balance. Our central contributions would be:

For **Consistent Hashing**:
- Compare with the paper Dynamo, we completed missing details from the literature. Many details of the implementation are not mentioned in the paper, such as how to handle replication when adding or removing nodes.  
- Random selection of coordinator. Therefore, the data distribution is more balanced.
- Conservative writes to quorum only. It is advantageous when the network is stable. The main limitation would be that when the network is unstable, we need to attempt repeatedly and wait for a response, which is time-consuming.

For **Rendezvous Hashing**:
- Dynamo with different consensus algorithm.
- Different failure handling methods.
- Architecture separation of router and nodes.

To implement the storage system, we used more "modern" tools such as Python, Docker, and gRPC. With Rendezvous Hashing, we implement another Hashing method and check the "folklore" knowledge that Consistent Hashing and Rendezvous Hashing are interchangeable. 

***
## Evaluation

For evaluating consistent hashing, we built a network consisting of four nodes and several clients. Each node runs independently and has a different IP address, hostname, and HTTP port. They can communicate with each other by using the corresponding IP and port. First, the client sends a “add object” request to the corresponding node to add different data items. Then, we test the “get object” request and the replica is added to the replication node. After that, we remove some objects from several nodes and check whether the replicas were also deleted on replication nodes. Finally, we remove a node from the hash ring and find this request was successfully broadcast to all nodes in the hash ring, this node was successfully deleted on all nodes. So far, this consistent hashing system is fully functional and can run as scheduled.

Rendezvous Hashing is evaluated and tested by building a small network of Docker containers and then testing the functionality of the features implemented (Replication and Failure handling). Additionally, we will evaluate how long a query takes and how many queries we can process in a second. This is done with different combinations of nodes and replications.