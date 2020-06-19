from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy as np
from scipy import stats
from scipy.stats import chisquare


def really_algorithm(step, worker):
    """
    The REALLY!? algorithms checks the cosine similarity on the last layer of the CNN model
    """
    if step > 1:
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
