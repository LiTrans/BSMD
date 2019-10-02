# Blockchain for smart mobility
Blockchain framework for Smart Mobility Data-market (BSMD) is designed to solve the privacy, security and management 
issues related to the sharing of passively as well as actively solicited large-scale data. Data from the individuals, 
governments, universities and companies are distributed on the network and stored in a decentralized manner, 
the data transactions are recorded and must have the authorization of the owners.

Nodes in BSMD are divided into passive nodes and active nodes. *Passive* nodes may read or host copies of the ledger. 
This type of node is suitable for individuals or small businesses who want to participate and take advantage of the 
network, but do not have the resources for running nodes for extended periods of time. *Active* nodes can write blocks 
and store updated versions of the ledger for other nodes to connect. This type of node is suitable for governments, 
universities or companies who have the resources for these tasks. 

## Layers

The BSMD frameworks is described in [Layers](layers). The [Identification layer](layers/identification) is 
composed of mobility and other information that the nodes own. In the [Contract layer](layers/contract) are the brokers
who facilitate data transactions between nodes. The [Communication](layers/communication) layer contains functions to 
establish *peer-to-peer* connections. Finally, in the [Incentive](layers/incentive) layer are the rewards 
the *active* nodes receive for participating in consensus and the reward nodes receive for sharing (selling) 
their information.

## Use cases

We demonstrate the BSMD by showing a distributed tool for behavioural choice modelling where participants do not share 
personal raw data, while all computations are done locally. This example can be found 
in the [simulated annealing](use_cases/simulated_annealing) folder.

We also present a federated learning model over the BSMD for choice modelling which is able to process distributed 
data from different sources This example can be found in the [federated learning](use_cases/federated_learning) folder.

## Documentation

Our documentation is hosted at ReadTheDocs service here: [https://bsmd.readthedocs.io](https://bsmd.readthedocs.io). 

## Prerequisites

To start using the BSMD you must have at least one *Iroha* node running. Read the [Iroha docs](https://iroha.readthedocs.io) 
for building and installing an Iroha network

## Built With

* [Hyperledger Iroha](https://github.com/hyperledger/iroha)
* [Python3](https://www.python.org/download/releases/3.0/)
* [TensorFlow](https://www.tensorflow.org/)

## Authors

* **David Lopez** [mitrailer](https://github.com/mitrailer)
* **Bilal Farooq** [billjee](https://github.com/billjee/)

## License

* Hyperledger Iroha is [licensed](https://github.com/hyperledger/iroha/blob/master/LICENSE) under the Apache License 2.0 
* This project is [licensed](LICENSE.md) under the Apache License 2.0
