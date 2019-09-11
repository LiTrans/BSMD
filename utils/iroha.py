#!/usr/bin/env python3
from iroha import IrohaCrypto
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
