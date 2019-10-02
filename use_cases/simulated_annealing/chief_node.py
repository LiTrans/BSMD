#!/usr/bin/env python3
import rpyc
import random
import json
from math import exp, log
from utils.iroha import set_detail_to_node, get_a_detail_written_by
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('name', None, 'Your name')
flags.DEFINE_string('private_key', None, 'Your private key to sign transactions')

# Connect to the working nodes
workers_proxies = []
# List all ports for connecting
ports = [9990, 9991, 9993, 9994]
# type the names of all workers
workers = ['worker1', 'worker2', 'worker3', 'worker4']

# Get the proxies of all workers
for port in ports:
    worker_proxy = rpyc.connect('localhost', port, config={'allow_public_attrs': True})
    workers_proxies.append(worker_proxy)


def new_state(b_car, b_cost, b_tt):
    """
    Computes a new beta using a random error. The new beta is part of the annealing process
    :param b_car: beta parameter of the car
    :param b_cost: beta parameter of the cost
    :param b_tt: beta parameter of the travel time
    :return: beta plus an error
    """
    chose_beta = random.randint(1, 3)
    error = random.uniform(-0.01, 0.01)
    new_b_car = 0
    new_b_cost = 0
    new_b_tt = 0
    if chose_beta == 1:
        new_b_car = b_car + error
        new_b_cost = b_cost
        new_b_tt = b_tt
    if chose_beta == 2:
        new_b_car = b_car
        new_b_cost = b_cost + error
        new_b_tt = b_tt
    if chose_beta == 3:
        new_b_car = b_car
        new_b_cost = b_cost
        new_b_tt = b_tt + error
    return new_b_car, new_b_cost, new_b_tt


def acceptance_probability(old_cost, new_cost, t):
    """
    Acceptance probability that the new cost improves the old cost.
    Part of the annealing process
    :param old_cost: old cost obtained from the slave nodes
    :param new_cost: new cost obtained from the slave nodes. The new cost use the parameter beta plus an error
    :param t: temperature of the annealing process
    :return: probability that the new cost improves the old cost
    """
    accept_prob = exp((new_cost - old_cost) / t)
    return accept_prob


def model(b_car, b_cost, b_tt, is_car, is_train, car_cost, car_tt, train_cost, train_tt):
    """
    This model is sent to all workers
    :param b_car:  (float) beta parameter of the car
    :param b_cost:  (float) beta parameter of the cost
    :param b_tt: (float) beta parameter of the travel time 
    :param is_car: (bool) 1 is user is traveling by car, 0 otherwise 
    :param is_train: (bool) 1 is user is traveling by train, 0 otherwise
    :param car_cost: (float)  cost fo traveling by car
    :param car_tt: (float) car travel time
    :param train_cost: (float) cost of traveling by train
    :param train_tt: (float) train travel time
    :return: 
    """
    prob_car = exp(b_car + b_cost * (car_cost - train_cost) + b_tt * (car_tt - train_tt)) / \
                  (1 + exp(b_car + b_cost * (car_cost - train_cost) + b_tt * (car_tt - train_tt)))
    observation = log(is_car * prob_car + is_train * (1 - prob_car))
    return observation


"""
Simulated annealing algorithm for solving the loglikehood choice model.
1. Use the blockchain to send the model to the worker nodes.
2. Use the blockchain to receive the cost from the worker nodes.
3. By using simulated annealing and sending-receiving information the master node solves the loglikehood choice
model without the need of personal information
:param beta_car: beta parameter of the car
:param beta_cost: beta parameter of the cost
:param beta_tt: beta parameter of the travel time
"""
beta_car = .00123
beta_cost = .00664
beta_tt = .006463
solutions = []
betas_car = []
betas_cost = []
betas_tt = []
cost = 0
cost_i = 0
x = 0
betas = str(beta_car) + ',' + str(beta_cost) + ',' + str(beta_tt)

# send parameters to workers
for worker in workers:
    # set_detail_to_node(sender, receiver, private_key, detail_key, detail_value, domain, ip):
    set_detail_to_node(FLAGS.name, worker, FLAGS.private_key, 'betas', betas, FLAGS.domain, FLAGS.ip)

# start workers
for proxy in workers_proxies:
    # this function will send the model to all workers. Also will automatically start all workers
    proxy.root.compute_cost(FLAGS.name, FLAGS.domain, FLAGS.ip, model)
all_cost = []

# get cost from all workers
for worker in workers:
    b = get_a_detail_written_by(FLAGS.name, worker, FLAGS.private_key, 'cost', FLAGS.domain, FLAGS.ip)
    result = json.loads(b)
    from_node = worker + '@' + FLAGS.domain
    c = result[from_node]['cost']
    all_cost.append(float(c))
# added cost of all workers
initial_cost = sum(all_cost)

print('initial solution = ', initial_cost)
print('initial beta_car = ', beta_car)
print('initial beta_cost = ', beta_cost)
print('initial beta_tt = ', beta_tt)
betas_car.append(beta_car)
betas_cost.append(beta_cost)
betas_tt.append(beta_tt)
solutions.append(cost)
temp = 1.0
temp_min = 0.00001
alpha = 0.9
j = 0
while temp > temp_min:
    i = 1
    while i <= 500:
        new_beta_car, new_beta_cost, new_beta_tt = new_state(beta_car, beta_cost, beta_tt)
        betas = str(new_beta_car) + ',' + str(new_beta_cost) + ',' + str(new_beta_tt)
        # send parameters to workers
        for worker in workers:
            # set_detail_to_node(sender, receiver, private_key, detail_key, detail_value, domain, ip):
            set_detail_to_node(FLAGS.name, worker, FLAGS.private_key, 'betas', betas, FLAGS.domain, FLAGS.ip)

        # get cost from all workers
        all_cost = []
        for worker in workers:
            b = get_a_detail_written_by(FLAGS.name, worker, FLAGS.private_key, 'cost', FLAGS.domain, FLAGS.ip)
            result = json.loads(b)
            from_node = worker + '@' + FLAGS.domain
            c = result[from_node]['cost']
            all_cost.append(float(c))
        # added cost of all slaves
        cost_i = sum(all_cost)

        ap = acceptance_probability(cost, cost_i, temp)
        rand = random.uniform(0, 1)
        if ap > rand:
            beta_car = new_beta_car
            beta_cost = new_beta_cost
            beta_tt = new_beta_tt
            cost = cost_i
            solutions.append(cost)
            betas_car.append(beta_car)
            betas_cost.append(beta_cost)
            betas_tt.append(beta_tt)
            print('results: ', beta_car, beta_cost, beta_tt, cost, initial_cost)
        i += 1
    temp = temp * alpha
    j += 1
print(beta_car, beta_cost, beta_tt, cost, initial_cost, solutions, betas_car, betas_cost, betas_tt)
