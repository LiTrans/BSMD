#!/usr/bin/env python3
import rpyc
import csv
import json
from absl import flags
from utils.iroha import get_a_detail_written_by, set_detail_to_node
from rpyc.utils.server import ThreadedServer

FLAGS = flags.FLAGS
flags.DEFINE_string('name', None, 'Your name')
flags.DEFINE_string('private_key', None, 'Your private key to sign transactions')


class RunNode(rpyc.Service):

    @staticmethod
    def compute_cost(self, writer, domain, ip, model):
        # get_a_detail_written_by(name, writer, detail_key, private_key, domain, ip)
        b = get_a_detail_written_by(FLAGS.name, writer, FLAGS.private_key, 'betas', domain, ip)
        result = json.loads(b)

        from_node = writer + '@' + domain
        beta = result[from_node]['betas'].split(',')
        b_car = float(beta[0])
        b_cost = float(beta[1])
        b_tt = float(beta[2])

        observations = []
        with open('data_one.csv') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                is_car = int(row[1])
                is_train = int(row[2])
                car_cost = int(row[3])
                car_tt = int(row[4])
                train_cost = int(row[5])
                train_tt = int(row[6])
                # model(beta_car, beta_cost, beta_tt, is_car, is_train, car_cost, car_tt, train_cost, train_tt):
                observation = model(b_car, b_cost, b_tt, is_car, is_train, car_cost, car_tt, train_cost, train_tt)
                observations.append(observation)
        c = sum(observations)
        observations.clear()
        cost = str(c)
        # set_detail_to_node(sender, receiver, private_key, detail_key, detail_value, domain, ip):
        set_detail_to_node(FLAGS.name, writer, FLAGS.private_key, 'cost', cost, domain, ip)


t = ThreadedServer(RunNode, port=18861)
t.start()







