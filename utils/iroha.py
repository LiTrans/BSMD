"""
Iroha
=====
Functions to post transactions in the iroha implementation of the BSMD

"""
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

    """
    print('This print will make the transactions run slower. When developing is useful to have this for debugging')
    print('Comment all prints in function send_transaction_and_print_status to make faster transactions')
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    network.send_tx(transaction)
    for status in network.tx_status_stream(transaction):
        print(status)


# #################################
# functions available to all users
# #################################
def set_detail_to_node(sender, receiver, private_key, detail_key, detail_value, domain, ip):
    """
    This function can be use when the User object is no available. The sender must have permission to write in the
    details of the receiver.

    In federated learning the details are in JSON format and contains the address (location) where the weight is stored
    if the weight is small enough it can be embedded to the block if needed)

    :Example:
    >>> set_detail_to_node('David', 'Juan', 'private key of david', 'detail key of Juan', 'detail value', 'domain' \
    'ip')

    :param str sender: Name of the node sending the information
    :param str receiver: Name of the node receiving the information
    :param str private_key: Private key of the user
    :param str detail_key: Name of the detail we want to set
    :param str detail_value: Value of the detail
    :param str domain: Name of the domain
    :param str ip: address for connecting to the BSMD

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


def get_a_detail_written_by(name, writer, private_key, detail_key, domain, ip):
    """
    This function can be use when the User object is no available. Consult a details of the node writen by other node

    :Example:
    >>> juan_detail = get_a_detail_written_by('David', 'Juan', 'private key of david', 'detail_key of Juan', 'domain', \
    'ip')
    >>> print(juan_detail)
    {
        "nodeA@domain":{
        "Age":"35"
    }

    :param str name: Name of the node consulting the information
    :param str writer: Name of the node who write the detail
    :param str private_key: Private key of the user
    :param str detail_key: Name of the detail we want to consult
    :param str domain: Name of the domain
    :param str ip: Address for connecting to the BSMD
    :return: returns the detail writen by "the writer"
    :rtype: json

    """

    account_id = name + '@' + domain
    user_id = writer + '@' + domain
    iroha = Iroha(account_id)
    ip_address = ip + ':50051'
    network = IrohaGrpc(ip_address)
    query = iroha.query('GetAccountDetail',
                        account_id=account_id,
                        key=detail_key,
                        writer=user_id)
    IrohaCrypto.sign_query(query, private_key)
    response = network.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail
