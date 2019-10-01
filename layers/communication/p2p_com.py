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