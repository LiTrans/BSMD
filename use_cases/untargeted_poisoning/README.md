# Reference
Code of the paper submitted to the [USENIX summer call](https://www.usenix.org/conference/usenixsecurity21) 

**Untargeted Poisoning Attack Detection via Blockchain in Federated Learning** by Ranwa Al Mallah, David López,
Bilal Farooq and Ali Yazdizadeh

# Summary
This experiment runs targeted and untargetted attacks on a Federated Learning (FL) process 
with up to 20 nodes, 1 *chief* and 19 *workers*. 
The experiment follows the next steps.
1. The *chief* node opens a connection socket and send the trained model to the *workers* nodes 
2. The *worker* nodes re-train the model with their local data and send the results to the *chief* node
3. At a designated EPOCH malicious *workers* send targeted or untargetted attacks
3. The *chief* node averages the results (including the malicious model) and send the average to all *workers*
4. A defense mechanism called REALLY!? algorithm may be used to defend the FL from being poisoned 

All transactions are recorded in the BSMD and we use sockets for p2p data transfers. 
You must have at least one Iroha node running

# Setup
1. To set up the the Blockchain follow [this procedure](../../utils/README.md)
2. To set up the the Federated learning go to the 'setup' 
   section of [this procedure](../federated_learning/README.md)
3. In the repository we provide a malicious matrix for the targeted attack, however you can creat your own
   by running the script [create_MM](create_MM.py). Note: you will need to run the experiment at least for
   one EPOCH for this script to function. The thing is that it need an example 'good' matrix to recreate a 
   malicious one.

# Run experiment
You can try targeted and untargeted at different stages. To do so go to line 565 in the [hook](hook.py) file 
and follow the instructions. To defend the FL process from the attack go to line 492 in the [hook](hook.py) 
file and follow the instructions.

You can run the experiment in up to 20 machines. However you can also run the experiment in different shells.

On the chief-computer (shell) run
```bash
python3 federated_classifier.py --is_chief=True --worker_name=chief --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_1 --file_Y=Y_Worker_1
```
On the worker1-computer (shell) run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker1 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_2 --file_Y=Y_Worker_2
```
On the worker2-computer (shell) run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker2 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_3 --file_Y=Y_Worker_3 
```
On the worker3-computer (shell) run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker3 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_4 --file_Y=Y_Worker_4
```
**.**  
**.**  
**.**  
On the worker20-computer (shell) run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker19 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_20 --file_Y=Y_Worker_20
```

