import os
import time

"""
Use this script to run the whole procces in a single terminal. Adjust the taskset number to correspond to
the number of cores of your computer. Also you run up to 20 workers
"""
os.system('taskset -c 0 python3 federated_classifier.py --is_chief=True --worker_name=chief --file_X=X_Worker_1 --file_Y=Y_Worker_1 & '
          'sleep 7s &&'
          'taskset -c 1 python3 federated_classifier.py --is_chief=False --worker_name=worker1 --file_X=X_Worker_2 --file_Y=Y_Worker_2 & '
          'sleep 3s &&'
          'taskset -c 2 python3 federated_classifier.py --is_chief=False --worker_name=worker2 --file_X=X_Worker_3 --file_Y=Y_Worker_3 & '
          'sleep 3s &&'
          'taskset -c 3 python3 federated_classifier.py --is_chief=False --worker_name=worker3 --file_X=X_Worker_4 --file_Y=Y_Worker_4 & '
          'sleep 3s &&'
          'taskset -c 4 python3 federated_classifier.py --is_chief=False --worker_name=worker4 --file_X=X_Worker_5 --file_Y=Y_Worker_5 & '
          'sleep 3s &&'
          'taskset -c 5 python3 federated_classifier.py --is_chief=False --worker_name=worker5 --file_X=X_Worker_6 --file_Y=Y_Worker_6 & '
          'sleep 3s &&'
          'taskset -c 6 python3 federated_classifier.py --is_chief=False --worker_name=worker6 --file_X=X_Worker_7 --file_Y=Y_Worker_7 & '
          'sleep 3s &&'
          'taskset -c 7 python3 federated_classifier.py --is_chief=False --worker_name=worker7 --file_X=X_Worker_8 --file_Y=Y_Worker_8 & '
          'sleep 3s &&'
          'taskset -c 8 python3 federated_classifier.py --is_chief=False --worker_name=worker8 --file_X=X_Worker_9 --file_Y=Y_Worker_9 & '
          'sleep 3s &&'
          'taskset -c 9 python3 federated_classifier.py --is_chief=False --worker_name=worker9 --file_X=X_Worker_10 --file_Y=Y_Worker_10')