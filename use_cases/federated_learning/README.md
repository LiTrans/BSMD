This experiment runs a federated learning algorithm with 10 nodes, 1 chief and 9 workers. 
The experiment follows the next steps.
1. The chief node opens a connection socket and send the trained model to the workers nodes 
2. The worker nodes re-train the model with their local data and send the results to the chief node
3. The chief node averages the results and send the average to all workers
4. Step 2 and 3 are repeated until EPOCH = 100

All transactions are recorded in the BSMD and we use sockets for p2p data transfers. You must have at lear one Iroha 
node running

# Setup

In a shell generate a private key and certificate with: 
```bash
openssl req -new -x509 -days 365 -nodes -out server.pem -keyout server.key
```

In the [federated_hook.py](../../layers/communication/federated_hook.py) file modify the lines 
```python
SSL_CONF.key_path = Path/to/your/private_key
SSL_CONF.cert_path = Path/to/your/certificate
```
In the [federated_learnig.py](federated_learning.py) file modify the lines 
```python
# Set these IPs of the computer associated to the chief node
# for local testing use localhost
CHIEF_PUBLIC_IP = 'localhost:7777' # Public IP of the chief worker
CHIEF_PRIVATE_IP = 'localhost:7777' # Private IP of the chief worker
```
In the [iroha_config](iroha_config.py) file modify the lines 
```python
# Set the ip of one iroha node
ip_iroha_node = '123.456.789'
```

To setup the federated nodes run. This script will create; (1) an admin of the BSDM, a domain and 10 *passive nodes* (9 worker and 1 chief) 
```bash
python3 setup.py
```

flags.DEFINE_boolean("is_chief", False, "True if this worker is chief")
flags.DEFINE_string("name", None, "name of the node in the BSMD")
flags.DEFINE_string("domain", None, "name of the domain")
flags.DEFINE_string("ip", None, "ip address for connecting to the BSMD")
flags.DEFINE_string("private_key", None, "private ket of the node")
flags.DEFINE_string("file_X", None, "X information file of the node")
flags.DEFINE_string("file_Y", None, "Y information file of the node")

# Run experiment

You can run the experiment on 10 machines. However you can also run the experiment in different shells.

On the chief-computer run
```bash
python3 federated_classifier.py --is_chief=True --worker_name=chief --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_1 --file_Y=Y_Worker_1
```
On the worker1-computer run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker1 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_2 --file_Y=Y_Worker_2
```
On the worker2-computer run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker2 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_3 --file_Y=Y_Worker_3 
```
On the worker3-computer run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker3 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_4 --file_Y=Y_Worker_4
```
**.**  
**.**  
**.**  
On the worker9-computer run
```bash
python3 federated_classifier.py --is_chief=False --worker_name=worker9 --domain=public --ip=ip_iroha_node \
--private_key=private_key_of_node --file_X=X_Worker_10 --file_Y=Y_Worker_10
```

