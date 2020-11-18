# Cyber-Security Risk Assessment Framework for Blockchains in Smart Mobility
Supplementary material of the paper _Cyber-Security Risk Assessment Framework for Blockchains in Smart Mobility_ by 
Ranwa Al Malla, David López, and Bilal Farooq. 

## Abstract
Blockchain is a digital database containing information that can be simultaneously used and shared within a large decentralized network. Blockchain carries historic immutability via linked blocks making it hard to tamper with the technology. However, a blockchain network is only as secure as its sub-systems. Cyber-security failures may occur at places where the blockchain connects with the real world, thus creating entry points that may be used by the attackers. Although the majority of the vulnerabilities of the sub-systems are based on strong assumptions, either about infeasibility in cryptographic primitives, in the characteristics of the consensus mechanism, or in the technology development, it is important to perform a risk assessment specific to the transportation ecosystem to understand the attacks, their specific impact and associated risk. In this work, we propose a novel risk assessment framework for blockchain applications in smart mobility aiming at quantifying the risk. As a case study, we analyse a multi-layered Blockchain framework for Smart Mobility Data-markets (BSMD). We first construct an actor-based analysis to determine the impact of the attacks. Then, a scenario-based analysis determines the probability of occurrence of each threat. Finally, a combined analysis is developed to determine which attack outcomes have the highest risk. The analysis uncovers specific blockchain technology security vulnerabilities in the transportation ecosystem by exposing new attack vectors. The proposed risk assessment may be used to deploy countermeasures and protect against  cyberattakcs on the blockchain network for smart mobility. 

## Pre-requisites
1. Python 2.7 or above 

## Set-up
1. Install and run a python virtual environment. Please follow [this guide](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)
2. On the virtual environment run:
```console
pip install pandas
pip install numpy
pip install matplotlib 
```

## Script
To run the [impact analysis](impact_analysis.py) script simply run on a virtual environment
```console
python impact_analysis.py
```
The script has three main procedures:
1. On lines 18-24 there is simple calculator por computing the the probability of occurrence of threats. See 
the file [Detailed computation of probabilities of occurrence](supporting_files/Detailed_computation_of_probabilities_of_occurrence__sup__mat__.pdf)
or see page 8 on the paper
2. On line 30 is created the risk characterization table for all attack goals at all scenarios and impacts. See 
the file [Detailed computation of the risk assessment](supporting_files/Detailed_computation_of_the_risk_assessment__sup__mat__.pdf)
or see page 9 on the paper
3. On lines 40-139 are shown the results of the actor-based risk analysis for all attack goals at its corresponded 
scenario. The results are saved and can be consulted by opening the file [risk_assessment.png](supporting_files/risk_assessment.png)

## Databases
1. The rates assigned to the capacity, opportunity and motivation are located in the file [threats.csv](supporting_files/threats.csv).
See page 9 in the paper
2. The combined risk assessment table for all attack goals at the corresponding scenarios are located in the file [combined_risk_assessment_table](supporting_files/combined_risk_assessment_table.csv)


## Authors
* **Ranwa Al Mallah** [ranwaalmallah](https://github.com/ranwaalmallah)
* **David López** [mitrailer](https://github.com/mitrailer)
* **Bilal Farooq** [billjee](https://github.com/billjee/)
