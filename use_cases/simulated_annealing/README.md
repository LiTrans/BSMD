The experiment follows the next steps:
1. The chief node use the BSMD (Iroha) to send the beta parameters to the worker nodes. 
2. The worker node get the beta parameters from the BSMD and run the model using his personal observations 
(e.g. the personal observations of worker 1 are in the [worker1.csv](data/worker1.csv) file)
3. The worker nodes use the BSMD to send the results of the model
4. Master node collect all results from the BSMD and start the annealing process. In this process chief and 
workers will share beta parameters and model results
5. Once the annealing process finish the chief node will have the result of the _loglikehood_ method 

## Setup

To setup the distributed simulated annealing run.
```bash
python3 setup.py
```
The script will create; (1) an admin of the BSDM, a domain and 10 *passive nodes* (9 worker and 1 chief) 

### Run the expermient
This experiment is meant to work on a local machine, but with a fewer modification you can make it work on different
machines

#### Start the worker nodes:
On the worker1-computer run
```bash
python3 worker_node.py --name='worker1' --private_key=private_key_of_node --port=9990
```
On the worker2-computer run
```bash
python3 worker_node.py --name='worker2' --private_key=private_key_of_node --port=9991

```
On the worker3-computer run
```bash
python3 worker_node.py --name='worker3' --private_key=private_key_of_node --port=9992
```
On the worker4-computer run
```bash
python3 worker_node.py --name='worker4' --private_key=private_key_of_node --port=9993
```

#### Start the chief node
```bash
python3 chief_node --name='chief' --private_key=private_key_of_node
```
