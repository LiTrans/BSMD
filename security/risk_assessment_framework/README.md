# Cyber-Security Risk Assessment Framework for Blockchains in Smart Mobility
Code of the paper Cyber-Security Risk Assessment Framework for Blockchains in Smart Mobility by Ranwa Al Malla, David 
López and Bilal Farooq

## Abstract
Blockchain technology is a crypto-based secure ledger for data storage and transfer through decentralized, trustless 
peer-to-peer systems. Blockchain carries historic immutability via linked blocks making it hard to tamper with the 
technology. Despite its advantages, previous studies have shown that the technology is not completely secure against 
cyberattacks. In transportation, cyber-security failures may occur at places where the blockchain system connects with 
the real world, thus creating entry points that may be used by the attackers. Although the majority of the 
vulnerabilities are based on strong assumptions, either about infeasibility in cryptographic primitives, in the 
characteristics of the consensus mechanism, or in the technology development, it remains crucial to perform a risk 
analysis specific to the transportation ecosystem to measure how viable the attacks are, their impact and 
consequently the risk exposure. In this paper, we propose a risk assessment framework for blockchain applications 
in smart mobility. As a case study, we carry out an analysis in terms of quantifying the risk associated to a 
multi-layered Blockchain framework for Smart Mobility Data-markets (BSMD). We first construct an actor-based analysis 
to determine the impact of the attacks. Then, a scenario-based analysis determines the probability of occurrence of 
each threat. Finally, a combined analysis is developed to determine which attack outcomes have the highest risk. 
In the case study of the public permissioned BSMD, the outcomes of the risk analysis highlight the highest risk 
factors according to their impact on the victims in terms of monetary, privacy, integrity and trust. 
The analysis uncovers specific blockchain technology security vulnerabilities in the transportation ecosystem by 
exposing new attack vectors. The systematic risk analysis here can be used to develop possible countermeasures 
against cybersecurity vulnerabilities in the smart mobility implementations of the blockchain technology. 

## Usage
The script [impact analysis](impact_analysis.py) has three main procedures:
1. On lines 18-24 there is simple calculator por computing <img src="https://latex.codecogs.com/gif.latex?P(G_i,S_j,A_k)"/>
2. 
## Authors
* **Ranwa Al Mallah** 
* **Bilal Farooq** [billjee](https://github.com/billjee/)
* **David López** [mitrailer](https://github.com/mitrailer)