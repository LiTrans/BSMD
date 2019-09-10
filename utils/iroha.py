#!/usr/bin/env python3
from iroha import IrohaCrypto, Iroha, IrohaGrpc
import binascii
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


# Iroha configuration
######################
# This parameters are for the admin of the BSMD
# Replace localhost with an IP address of a node running the blockchain
NETWORK = IrohaGrpc('localhost:50051')
ADMIN_PRIVATE_KEY = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
IROHA_ADMIN = Iroha('admin@test')
# New users will be created with the default role *user* which consists in the following permissions
# "can_add_signatory",
# "can_get_my_acc_ast",
# "can_get_my_acc_ast_txs",
# "can_get_my_acc_detail",
# "can_get_my_acc_txs",
# "can_get_my_account",
# "can_get_my_signatories",
# "can_get_my_txs",
# "can_grant_can_add_my_signatory",
# "can_grant_can_remove_my_signatory",
# "can_grant_can_set_my_account_detail",
# "can_grant_can_set_my_quorum",
# "can_grant_can_transfer_my_assets",
# "can_receive",
# "can_remove_signatory",
# "can_set_quorum",
# "can_transfer"
DEFAULT_ROLE = 'user'

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
def send_transaction_and_print_status(transaction):
    """
    Send a transaction to the Blockchain (BSMD)
    :param transaction: Transaction we are sending to the BSMD
    :return: null:
    """
    print('This print will make the transactions run slower. When developing is useful to have this for debugging')
    print('Comment all prints in function send_transaction_and_print_status to make faster transactions')
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    NETWORK.send_tx(transaction)
    for status in NETWORK.tx_status_stream(transaction):
        print(status)