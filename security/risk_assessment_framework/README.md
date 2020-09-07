# Cyber-Security Risk Assessment Framework for Blockchains in Smart Mobility
Code of the paper Cyber-Security Risk Assessment Framework for Blockchains in Smart Mobility by Ranwa Al Malla, David 
López and Bilal Farooq. For more information about how the risk assessment is performed please refer to the paper

## Abstract
We propose a risk assessment framework for blockchain applications 
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
The [impact analysis](impact_analysis.py) script has three main procedures:
1. On lines 18-24 there is simple calculator por computing the the probability of occurrence of threats
2. On line 30 is created the risk characterization table for all attack goals at all scenarios and impacts
3. On lines 40-139 are shown the results of the actor-based risk analysis for all attack goals at its corresponded 
scenario
## Authors
* **Ranwa Al Mallah** 
* **Bilal Farooq** [billjee](https://github.com/billjee/)
* **David López** [mitrailer](https://github.com/mitrailer)