import numpy as np
import tensorflow as tf
import math
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from scipy import stats


def attestedfl_1(step, worker, warm_up):
    previous_step = step - 1
    n_matrix = np.load('data_test/' + worker + '/local_model_' + str(step) + '.npy', allow_pickle=True)
    global_m = np.load('data_test/global_model_' + str(previous_step) + '.npy', allow_pickle=True)
    # Load previous Euclidean distances if exists
    try:
        euclidean_distances = np.load('data_test/' + worker + '/euclidean_distances_' + str(step) + '.npy',
                                      allow_pickle=True)
    except:
        print("step:", step)
    # Compute euclidean Distance in the current step
    # Skip first iteration
    if step == 1:
        euclidean_distance = tf.norm(n_matrix - global_m, ord='euclidean')
        e_d_array = np.asarray([[euclidean_distance]])
        np.save('data_test/' + worker + '/euclidean_distances_' + str(step) + '.npy', e_d_array)
    else:
        euclidean_distance = tf.norm(n_matrix - global_m, ord='euclidean')
        e_d_array = np.asarray([[euclidean_distance]])
        euclidean_distances = np.append(euclidean_distances,e_d_array)
        np.save('data_test/' + worker + '/euclidean_distances_' + str(step) + '.npy', euclidean_distances)

    if step > warm_up:
        euclidean_distances = np.load('data_test/' + worker + '/euclidean_distances_' + str(step) + '.npy',
                                      allow_pickle=True)
        c = step - warm_up
        euclidean_distance_to_test = euclidean_distances[warm_up:5]
        delta_array = []
        for idx, e_d in euclidean_distance_to_test:
            delta = e_d
            delta_1 = euclidean_distances[warm_up + idx + 1]
            t = warm_up + idx
            delta_sum = 1 - math.exp(t/c(delta_1 + delta))
            delta_array.append(delta_sum)
        delta_avg = np.sum(delta_array) / c
        delta_mean = np.mean(delta_array)
        delta_std = np.std(delta_array)

        if delta_avg <= delta_mean - 4 * delta_std:
            return True
        else:
            return False
    return True


def attestedfl_2(step, worker, warm_up):
    """
    The attestedFL_2 algorithms checks the cosine similarity on the last layer of the CNN model
    """
    if step > warm_up:
        previous_step = step - 1
        reliable = False
        n_1_matrix = np.load('data_test/' + worker + '/local_model_' + str(previous_step) + '.npy', allow_pickle=True)
        n_matrix = np.load('data_test/' + worker + '/local_model_' + str(step) + '.npy', allow_pickle=True)
        global_m = np.load('data_test/global_model_' + str(previous_step) + '.npy', allow_pickle=True)
        first = []
        second = []
        n_1 = n_1_matrix[6].reshape(1, -1)
        n = n_matrix[6].reshape(1, -1)
        g = global_m[6].reshape(1, -1)
        similarities = cosine_similarity(n_1, g)
        similarities_two = cosine_similarity(n, g)
        first.append(abs(similarities))
        second.append(abs(similarities_two))
        total = np.array([first, second])
        # print(total)
        chi2_stat, p_val, dof, ex = stats.chi2_contingency(total)
        logger = open('data_paper/logs/cosine_attacker_' + worker + '.csv', "a")
        logger.write("{},{},{},{}".format(step, worker, float(abs(similarities)), float(abs(similarities_two))) + '\n')
        logger.close()
        if p_val < 0.1:
            reliable = False
            print(str(worker) + ' is not reliable')
            return reliable
        else:
            reliable = True
            return reliable
    else:
        return True


def attestedfl_3(step, worker, warm_up):
    reliable = True
    # for the sake of the example we consider a worker is training as follows:
    # 1. Get the errors at each iteration (epoch)
    # 2. Fit a logarithmic curve to the data that contains errors (y-axis) over iteration (x-axis)
    # 3. If the slop of the logarithmic curve is negative or small (less than .2) the worker is training.
    # A negative o small slop means that the errors are approaching to a small number. In any other case, the worker is
    # not training
    if step > warm_up:
        reliable = False
        errors_table = pd.read_csv('data_paper/logs/attestedFL-3/errors_' + worker + '.csv', header=None)
        iteration = errors_table[0]
        errors = errors_table[2]
        fittedParameters = np.polyfit(np.log(iteration), errors, 1)
        first_prediction =  np.polyval(fittedParameters, 1)
        last_prediction = np.polyval(fittedParameters, step)
        slope = ((last_prediction - first_prediction)/(step - 1))

        if slope <= 0:
            reliable = True
            return reliable
        else:
            if slope <= .4:
                reliable = True
                return reliable
            else:
                reliable = False
                return reliable
    return reliable


def attestedfl(step, worker):
    # For the sake of the example let assume that the warmup period is 30 epochs
    warm_up = 30
    reliable = False
    if attestedfl_1(step, worker, warm_up):
        if attestedfl_2(step, worker, warm_up):
            if attestedfl_3(step, worker, warm_up):
                reliable = True
                return reliable
    return reliable