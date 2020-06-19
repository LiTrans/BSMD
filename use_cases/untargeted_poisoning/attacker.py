import numpy as np
import tensorflow as tf

def node_attacking_targeted(step_value):
    file = step_value - 1
    global_model = np.load('data_test/global_model_' + str(file) + '.npy', allow_pickle=True)
    malicious_model = np.load('data_test/malicious_matrix.npy', allow_pickle=True)
    total_workers = 10
    learning_rate = 0.001
    send_malicious = ((total_workers/learning_rate)*(malicious_model - global_model)) + global_model
    print('Attack!!!!!')
    return send_malicious

def node_attacking_un_targeted(step_value):
    global_m = np.load('data_test/global_model_1.npy', allow_pickle=True)
    malicious_matrix = []
    for i in range(0, 7):
        shape = global_m[i].shape
        mean = np.mean(global_m[i])
        std = np.std(global_m[i])
        matrix = np.random.normal(mean, std, shape)
        malicious_matrix.append(matrix)
    print('Attack!!!!!')
    return malicious_matrix
