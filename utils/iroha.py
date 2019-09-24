#!/usr/bin/env python3
from iroha import IrohaCrypto, Iroha, IrohaGrpc
import binascii
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


# Transactions request iroha
def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """
    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result
    return tracer


@trace
def send_transaction_and_print_status(transaction, network):
    """
    Send a transaction to the Blockchain (BSMD)
    :param transaction: Transaction we are sending to the BSMD
    :param network: address of the a node hosting the Blockchain
    :return: null:
    """
    print('This print will make the transactions run slower. When developing is useful to have this for debugging')
    print('Comment all prints in function send_transaction_and_print_status to make faster transactions')
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    network.send_tx(transaction)
    for status in network.tx_status_stream(transaction):
        print(status)


# functions available to all users
def set_detail_to_node(sender, receiver, private_key, detail_key, detail_value, domain, ip):
    """
    Set the details of a node. In federated learning the details are in JSON format and
    contains the address (location) where the weight is stored (if the weight is small enough it can be
    embedded to the block if needed)
    :param sender: (str) name of the node sending the information
    :param receiver: (str) name of the node receiving the information
    :param private_key: (str) Private key of the user
    :param detail_key: (str) Name of the detail we want to set
    :param detail_value: (str) Value of the detail
    :param domain: (str) Name of the domain
    :param ip: (ip) address for connecting to the BSMD
    """
    account = sender + '@' + domain
    iroha = Iroha(account)
    account_id = receiver + '@' + domain
    ip_address = ip + ':50051'
    network = IrohaGrpc(ip_address)
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id,
                      key=detail_key,
                      value=detail_value)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx, network)