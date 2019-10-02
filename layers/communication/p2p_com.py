"""

Peer-to-peer communications
===========================
This module is for p2p communication between two nodes. The communication is done via sockets, for now the messages
are not encrypted. For external networks you may need to open ports.

Assume you have two nodes. The ip:port of node1 is 123.456.789:5555 and while the ip:port of node2 is 987.654.321:5555.
To stat a p2p communication do the following:

:On node1 run:
>>> receiver = Receiver('123.456.789', '4444')
>>> sender = Sender('987.654.321', '5555')
>>> treads = [receiver.start(), sender.start()]

:On node2 run:
>>> receiver = Receiver('987.654.321', '5555')
>>> sender = Sender('123.456.789', '4444')
>>> treads = [receiver.start(), sender.start()]


This code was taken from https://www.webcodegeeks.com/python/python-network-programming-tutorial/

"""

import socket
import threading

ENCODING = 'utf-8'


class Receiver(threading.Thread):
    """
    This class will receive messages

    :param str my_host: My local ip address
    :param str my_port: My local port
    """

    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.host = my_host
        self.port = my_port

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)
        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    full_message = full_message + data.decode(ENCODING)
                    if not data:
                        print("{}: {}".format(client_address, full_message.strip()))
                        return full_message.strip()
                        break
            finally:
                connection.shutdown(2)
                connection.close()

    def run(self):
        self.listen()


class Sender(threading.Thread):
    """
    This class is for p2p communication between two nodes. The communication is done via sockets, for now the messages
    are not encrypted. This class will receive messages

    :param str my_friends_host: Ip address of the node you want to send a message
    :param str my_friends_port: Port of the node you want to send a message
    """
    def __init__(self, my_friends_host, my_friends_port):
        threading.Thread.__init__(self, name="messenger_sender")
        self.host = my_friends_host
        self.port = my_friends_port

    def run(self):
        while True:
            message = input("")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.sendall(message.encode(ENCODING))
            s.shutdown(2)
            s.close()


def main():
    """
    Main can be use to test the p2p service. Open two consoles try it.
    """
    my_host = input("which is my host? ")
    my_port = int(input("which is my port? "))
    receiver = Receiver(my_host, my_port)
    my_friends_host = input("what is your friend's host? ")
    my_friends_port = int(input("what is your friend's port?"))
    sender = Sender(my_friends_host, my_friends_port)
    treads = [receiver.start(), sender.start()]

    print(treads)


if __name__ == '__main__':
    main()


"""

Hook for federated learning
===========================

We use the bellow code for data transactions of large variables in the BSMD.
In particular we use the socket implementation of coMind for transferring weights
and we add a second layer to record all transactions in the BSMD
This code was taken from https://github.com/coMindOrg/federated-averaging-tutorials/tree/master/federated-sockets
https://comind.org/

Copyright 2018 coMind. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

https://INTERVAL_STEPS % step_value.org/
"""
import socket
import time
import ssl
import hmac
import tensorflow as tf
import numpy as np
import json
import hashlib
from utils.iroha import set_detail_to_node

SEND_RECEIVE_CONF = lambda x: x
SEND_RECEIVE_CONF.key = b'4C5jwen4wpNEjBeq1YmdBayIQ1oD'
SEND_RECEIVE_CONF.hashfunction = hashlib.sha1
SEND_RECEIVE_CONF.hashsize = int(160 / 8)
SEND_RECEIVE_CONF.error = b'error'
SEND_RECEIVE_CONF.recv = b'reciv'
SEND_RECEIVE_CONF.signal = b'go!go!go!'
SEND_RECEIVE_CONF.buffer = 8192*2
CHIEF_NAME = ''

SSL_CONF = lambda x: x
SSL_CONF.key_path = 'layers/communication/server.key'
SSL_CONF.cert_path = 'layers/communication/server.pem'


try:
    import cPickle as pickle
except ImportError:
    import pickle


def convert_weights_to_json(weights):
    weights = [w.tolist() for w in weights]
    weights_list = json.dumps(weights)
    return weights_list


class _FederatedHook(tf.train.SessionRunHook):
    """
    Provides a hook to implement federated averaging with tensorflow.

      In a typical synchronous training environment, gradients will be averaged each
      step and then applied to the variables in one shot, after which replicas can
      fetch the new variables and continue. In a federated average training environment,
      model variables will be averaged every 'interval_steps' steps, and then the
      replicas will fetch the new variables and continue training locally. In the
      interval between two average operations, there is no data transfer, which can
      accelerate training.

      The hook has two different ways of working depending if it is the chief worker or not.

      The chief starts creating a socket that will act as server. Then it stays
      waiting _wait_time seconds and accepting connections of all those workers that
      want to join the training, and distributes a task index to each of them.
      This task index is not always necessary. In our demos we use it to tell
      each worker which part of the data-set it has to use for the training and it
      could have other applications.

      Remember if you training is not going to be performed in a LAN you will
      need to do some port forwarding, we recommend you to have a look to this
      article we wrote about it:
      https://medium.com/comind/raspberry-pis-federated-learning-751b10fc92c9

      Once the training is going to start sends it's weights to the other workers,
      so that they all start with the same initial ones.
      After each batch is trained, it checks if _interval_steps has been completed,
      and if so, it gathers the weights of all the workers and its own, averages them
      and sends the average to all those workers.

      Workers open a socket connection with the chief and wait to get their worker number.
      Once the training is going to start they wait for the chief to send them its weights.
      After each training round they check if _interval_steps has been completed,
      and if so, they send their weights to the chief and wait for it's response,
      the averaged weights with which they will continue training.
      """

    def __init__(self, is_chief, name, private_ip, public_ip, private_key, list_of_workers, domain, ip,
                 wait_time=30, interval_steps=100):
        """
        Constructs a FederatedHook object
        :param is_chief (bool): whether it is going to act as chief or not.
        :param worker_name (str): name of the node in the BSMD
        :param private_ip (str): complete local ip in which the chief is going to serve its socket.
                                Example: 172.134.65.123:7777
        :param public_ip (str): ip to which the workers are going to connect.
        :param private_key (str): private key of the node for signing the transactions
        :param list_of_workers (list): list of all the nodes that are willing to participate. In theory the chief node
                                        knows the list as he creates the domain and accounts for the participants
        :param domain (str): name of the domain
        :param ip (str): ip address for connecting to the BSMD
        :param wait_time (int, optional): how long the chief should wait at the beginning for the workers to connect.
        :param interval_steps (int, optional): number of steps between two "average op", which specifies
                                            how frequent a model synchronization is performed
        """

        self._is_chief = is_chief
        self._name = name
        self._private_ip = private_ip.split(':')[0]
        self._private_port = int(private_ip.split(':')[1])
        self._public_ip = public_ip.split(':')[0]
        self._public_port = int(public_ip.split(':')[1])
        self._private_key = private_key
        self._list_of_workers = list_of_workers
        self._domain = domain
        self._ip = ip
        self._interval_steps = interval_steps
        self._wait_time = wait_time
        self._nex_task_index = 0
        # We get the number of connections that have been made, and which task_index
        # corresponds to this worker.
        self.task_index, self.num_workers = self._get_task_index()

    def _get_task_index(self):
        """
        Chief distributes task index number to workers that connect to it and lets them know how many workers are
        there in total.
        :return:
          task_index: (int) task index corresponding to this worker.
          num_workers: (int) number of total workers.
         """
        if self._is_chief:
            self._server_socket = self._start_socket_server()
            self._server_socket.settimeout(5)
            users = []
            t_end = time.time() + self._wait_time

            while time.time() < t_end:
                try:
                    sock, _ = self._server_socket.accept()
                    connection_socket = ssl.wrap_socket(
                        sock,
                        server_side=True,
                        certfile=SSL_CONF.cert_path,
                        keyfile=SSL_CONF.key_path,
                        ssl_version=ssl.PROTOCOL_TLSv1)
                    if connection_socket not in users:
                        users.append(connection_socket)
                except socket.timeout:
                    pass

            num_workers = len(users) + 1
            _ = [us.send((str(i + 1) + ':' + str(num_workers)).encode('utf-8')) \
                 for i, us in enumerate(users)]
            self._nex_task_index = len(users) + 1
            _ = [us.close() for us in users]

            self._server_socket.settimeout(120)
            return 0, num_workers

        client_socket = self._start_socket_worker()
        message = client_socket.recv(1024).decode('utf-8').split(':')
        client_socket.close()
        return int(message[0]), int(message[1])

    def _create_placeholders(self):
        """
        Creates the placeholders that we will use to inject the weights into the graph
        """
        for var in tf.trainable_variables():
            self._placeholders.append(tf.placeholder_with_default(var, var.shape,
                                                                  name="%s/%s" % ("FedAvg",
                                                                                  var.op.name)))

    def _assign_vars(self, local_vars):
        """
        Utility to refresh local variables.
        :param local_vars: List of local variables
        :return: The ops to assign value of global vars to local vars.
        """
        reassign_ops = []
        for var, fvar in zip(local_vars, self._placeholders):
            reassign_ops.append(tf.assign(var, fvar))
        return tf.group(*(reassign_ops))

    @staticmethod
    def _receiving_subroutine(connection_socket):
        """
        Subroutine inside _get_np_array to receive a list of numpy arrays.
        If the sending was not correctly received it sends back an error message
        to the sender in order to try it again.
        :param connection_socket: a socket with a connection already established.
        :return:
        """
        timeout = 0.5
        while True:
            ultimate_buffer = b''
            connection_socket.settimeout(240)
            first_round = True
            while True:
                try:
                    receiving_buffer = connection_socket.recv(SEND_RECEIVE_CONF.buffer)
                except socket.timeout:
                    break
                if first_round:
                    connection_socket.settimeout(timeout)
                    first_round = False
                if not receiving_buffer:
                    break
                ultimate_buffer += receiving_buffer

            pos_signature = SEND_RECEIVE_CONF.hashsize
            signature = ultimate_buffer[:pos_signature]
            message = ultimate_buffer[pos_signature:]
            good_signature = hmac.new(SEND_RECEIVE_CONF.key, message, SEND_RECEIVE_CONF.hashfunction).digest()

            if signature != good_signature:
                connection_socket.send(SEND_RECEIVE_CONF.error)
                timeout += 0.5
                continue
            else:
                connection_socket.send(SEND_RECEIVE_CONF.recv)
                connection_socket.settimeout(120)
                return message

    def _get_np_array(self, connection_socket):
        """
        Routine to receive a list of numpy arrays.
        :param connection_socket: a socket with a connection already established.
        """
        message = self._receiving_subroutine(connection_socket)
        received_from, final_image = pickle.loads(message)
        return received_from, final_image

    @staticmethod
    def _send_np_array(arrays_to_send, connection_socket, iteration, tot_workers, sender, private_key, receiver, domain,
                       ip, list_participants=None):

        """
        Send weights to nodes via a socket. Also write the transaction in the BSMD
        :param arrays_to_send: weight to be send
        :param connection_socket:
        :param iteration: iteration number in the federated process
        :param tot_workers: total number of node in the federated process
        :param sender: name of the node sending the information
        :param private_key: private key of the node sending the transaction
        :param receiver: name of the receiver
        :param list_participants (array, optional): list of participants in the federated process. This variable is
                                                    just need in the first loop
        :return:
        """

        if list_participants is None:
            list_participants = []
        serialized = pickle.dumps([sender, arrays_to_send])

        transaction_data = dict()
        transaction_data['Process'] = 'BSMD-ML'
        transaction_data['Received from'] = sender
        # in this example weights are send using a socket, but you can write the address
        # were the weight is stored (e.g., see https://ipfs.io/)
        transaction_data['address'] = 'address'
        transaction_data['Total workers'] = str(tot_workers)
        transaction_data['iteration'] = str(iteration)
        transaction_json = json.dumps(transaction_data)
        json_in_ledger = str(transaction_json)
        transaction = json_in_ledger.replace('"', '')

        # Send transactions to the blockchain
        detail_key = sender + '_weight'
        if iteration == 0:
            for rec in list_participants:
                set_detail_to_node(sender, rec, private_key, detail_key, transaction, domain, ip)
        else:
            set_detail_to_node(sender, receiver, private_key, detail_key, transaction, domain, ip)

        # Send weight using a socket
        signature = hmac.new(SEND_RECEIVE_CONF.key, serialized, SEND_RECEIVE_CONF.hashfunction).digest()
        assert len(signature) == SEND_RECEIVE_CONF.hashsize
        message = signature + serialized
        print('byte size:', len(serialized))
        print('byte size:', len(message))

        connection_socket.settimeout(240)
        start = time.time()
        connection_socket.sendall(message)
        end = time.time()
        print('send weghts in: ' + str(end - start) + '\n')
        while True:
            check = connection_socket.recv(len(SEND_RECEIVE_CONF.error))
            if check == SEND_RECEIVE_CONF.error:
                connection_socket.sendall(message)
            elif check == SEND_RECEIVE_CONF.recv:
                connection_socket.settimeout(120)
                break

    def _start_socket_server(self):
        """
        Creates a socket with ssl protection that will act as server.
        :return:
            sever_socket (socket): ssl secured socket that will act as server.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
        server_socket.bind((self._private_ip, self._private_port))
        server_socket.listen()
        return server_socket

    def _start_socket_worker(self):
        """
        Creates a socket with ssl protection that will act as client.
        :return:
              sever_socket (socket): ssl secured socket that will work as client.
         """
        to_wrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional

        client_socket = ssl.wrap_socket(to_wrap_socket)
        client_socket.connect((self._public_ip, self._public_port))
        return client_socket

    def begin(self):
        """
        Session begin
        """
        self._placeholders = []
        self._create_placeholders()
        self._update_local_vars_op = self._assign_vars(tf.trainable_variables())
        self._global_step = tf.get_collection(tf.GraphKeys.GLOBAL_STEP)[0]

    def after_create_session(self, session, coord):
        """
        If chief:
            Once the training is going to start sends it's weights to the other
            workers, so that they all start with the same initial ones.
            Once it has send the weights to all the workers it sends them a
            signal to start training.
        Workers:
            Wait for the chief to send them its weights and inject them into
            the graph.
        :param session:
        :param coord:
        :return:
        """
        if self._is_chief:
            users = []
            addresses = []
            while len(users) < (self.num_workers - 1):
                try:
                    self._server_socket.settimeout(30)
                    sock, address = self._server_socket.accept()
                    connection_socket = ssl.wrap_socket(
                        sock,
                        server_side=True,
                        certfile=SSL_CONF.cert_path,
                        keyfile=SSL_CONF.key_path,
                        ssl_version=ssl.PROTOCOL_TLSv1)

                    print('Connected: ' + address[0] + ':' + str(address[1]))
                except socket.timeout:
                    print('Some workers could not connect')
                    break
                try:
                    print('SENDING Worker: ' + address[0] + ':' + str(address[1]))

                    self._send_np_array(session.run(tf.trainable_variables()), connection_socket, 0, self.num_workers,
                                        self._name, self._private_key, 'first_loop_federated_learning', self._domain,
                                        self._ip, self._list_of_workers)
                    print('SENT Worker {}'.format(len(users)))
                    users.append(connection_socket)
                    addresses.append(address)
                except (ConnectionResetError, BrokenPipeError):
                    print('Could not send to : '
                          + address[0] + ':' + str(address[1])
                          + ', fallen worker')
                    connection_socket.close()
            for i, user in enumerate(users):
                try:
                    user.send(SEND_RECEIVE_CONF.signal)
                    user.close()
                except (ConnectionResetError, BrokenPipeError):
                    print('Fallen Worker: ' + addresses[i][0] + ':' + str(address[i][1]))
                    self.num_workers -= 1
                    try:
                        user.close()
                    except (ConnectionResetError, BrokenPipeError):
                        pass
        else:
            print('Starting Initialization')
            client_socket = self._start_socket_worker()
            CHIEF_NAME, broadcast_weights = self._get_np_array(client_socket)
            feed_dict = {}
            for placeh, brweigh in zip(self._placeholders, broadcast_weights):
                feed_dict[placeh] = brweigh
            session.run(self._update_local_vars_op, feed_dict=feed_dict)
            print('Initialization finished')
            client_socket.settimeout(120)
            client_socket.recv(len(SEND_RECEIVE_CONF.signal))
            client_socket.close()

    def before_run(self, run_context):
        """ Session before_run"""
        return tf.train.SessionRunArgs(self._global_step)

    def after_run(self, run_context, run_values):
        """
         Both chief and workers, check if they should average their weights in
        this round. Is this is the case:

        If chief:
            Tries to gather the weights of all the workers, but ignores those
            that lost connection at some point.
            It averages them and then send them back to the workers.
            Finally in injects the averaged weights to its own graph.
        Workers:
            Send their weights to the chief.
            Wait for the chief to send them the averaged weights and inject them into
            their graph.
        :param run_context:
        :param run_values:
        :return:
        """
        step_value = run_values.results
        session = run_context.session
        if step_value % self._interval_steps == 0 and not step_value == 0:
            if self._is_chief:
                self._server_socket.listen(self.num_workers - 1)
                gathered_weights = [session.run(tf.trainable_variables())]
                users = []
                names = []
                addresses = []
                for i in range(self.num_workers - 1):
                    try:
                        self._server_socket.settimeout(30)
                        sock, address = self._server_socket.accept()
                        connection_socket = ssl.wrap_socket(
                            sock,
                            server_side=True,
                            certfile=SSL_CONF.cert_path,
                            keyfile=SSL_CONF.key_path,
                            ssl_version=ssl.PROTOCOL_TLSv1)

                        print('Connected: ' + address[0] + ':' + str(address[1]))
                    except socket.timeout:
                        print('Some workers could not connect')
                        break
                    try:
                        name, received = self._get_np_array(connection_socket)
                        gathered_weights.append(received)
                        users.append(connection_socket)
                        names.append(name)
                        addresses.append(address)
                        print('Received from ' + address[0] + ':' + str(address[1]))
                    except (ConnectionResetError, BrokenPipeError):
                        print('Could not recieve from : '
                              + address[0] + ':' + str(address[1])
                              + ', fallen worker')
                        connection_socket.close()

                self.num_workers = len(users) + 1

                print('Average applied '
                      + 'with {} workers, iter: {}'.format(self.num_workers, step_value))
                rearranged_weights = []

                # In gathered_weights, each list represents the weights of each worker.
                # We want to gather in each list the weights of a single layer so
                # to average them afterwards
                for i in range(len(gathered_weights[0])):
                    rearranged_weights.append([elem[i] for elem in gathered_weights])
                for i, elem in enumerate(rearranged_weights):
                    rearranged_weights[i] = np.mean(elem, axis=0)

                for i, user in enumerate(users):
                    try:
                        self._send_np_array(rearranged_weights, user, step_value, self.num_workers, self._name,
                                            self._private_key, self._domain, self._ip, names[i])
                        user.close()
                    except (ConnectionResetError, BrokenPipeError):
                        print('Fallen Worker: ' + addresses[i][0] + ':' + str(address[i][1]))
                        self.num_workers -= 1
                        try:
                            user.close()
                        except socket.timeout:
                            pass

                feed_dict = {}
                for placeh, reweigh in zip(self._placeholders, rearranged_weights):
                    feed_dict[placeh] = reweigh
                session.run(self._update_local_vars_op, feed_dict=feed_dict)

            else:
                worker_socket = self._start_socket_worker()
                print('Sending weights')
                value = session.run(tf.trainable_variables())

                self._send_np_array(value, worker_socket, step_value, self.num_workers, self._name,
                                    self._private_key, self._domain, self._ip, CHIEF_NAME)

                name, broadcasted_weights = self._get_np_array(worker_socket)
                feed_dict = {}
                for placeh, brweigh in zip(self._placeholders, broadcasted_weights):
                    feed_dict[placeh] = brweigh
                session.run(self._update_local_vars_op, feed_dict=feed_dict)
                print('Weights successfully updated, iter: {}'.format(step_value))
                worker_socket.close()

    def end(self, session):
        """
         Session end
        :param session:
        :return:
        """
        if self._is_chief:
            self._server_socket.close()

