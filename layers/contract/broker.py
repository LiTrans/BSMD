"""
========
Contract
========

Broker
======
Defines a Broker class

"""
from iroha import Iroha, IrohaCrypto, IrohaGrpc
from utils.iroha import send_transaction_and_print_status

class Broker:
    """
    Brokers look for users (passive nodes) in the BSMD and arrange transactions. Brokers are created in the public
    domain and can get the public details of all passive nodes

    :param str private_key: Private key of the broker. This is not save in the class is just used to generate
                        a public_key. In other functions the private_key must be used to sign transactions. You can
                        generate private keys with IrohaCrypto.private_key()
    :param str name: name of the user (lower case)
    :param str ip: ip of one node hosting the blockchain
    :param json public_info: public information of the broker, e.g., type of node: broker

    """
    def __init__(self, private_key, name, ip, public_info):
        self.public_key = IrohaCrypto.derive_public_key(private_key)
        self.name = name
        ip_address = ip + ':50051'
        self.network = IrohaGrpc(ip_address)
        self.public_info = public_info

    def create_account(self, private_key):
        """
        Create a broker account in the BSMD. Brokers are automatically created in the public domain. This function works
        in two steps

        #. The broker account in created in the public domain
        #. Set the public details of the broker

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "address": "123 Street, City", "type": "broker" }
        >>> public_info = json.dumps(x)
        >>> broker = Broker('private_key','broker', '123.456.789', public_info)
        >>> broker.create_account('private_key')

        :param str private_key: The private key of the user

        """
        account_id = self.name + '@public'
        iroha = Iroha(account_id)
        tx = iroha.transaction(
            [iroha.command('CreateAccount',
                           account_name=self.name,
                           domain_id='public',
                           public_key=self.public_key)])
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

        tx = iroha.transaction([
            iroha.command('SetAccountDetail',
                          account_id=account_id,
                          key='public information',
                          value=self.public_info)
        ])
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

    def get_details_from(self, user, private_key):
        """
        Consult all details of the node. Broker can only consult details in the 'public' domain

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> from layers.identification.identification import User
        >>> x = { "gender": 30, "address": "123 Tennis" }
        >>> user_info = json.dumps(x)
        >>> x = { "address": "123 Street, City", "type": "broker" }
        >>> broker_info = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David', domain, user_info)
        >>> broker = Broker('private_key','broker', '123.456.789', broker_info)
        >>> user_public_details = broker.get_details_from(user, 'private_key')
        >>> print(user_public_details)
        {
            "node@domain":{
                "Type":"user"
            }
        }

        :param str private_key: Key to sign the transaction
        :param User user: The user the broker want to consult
        :return: solicited details of the user
        :rtype: json

        """
        account_id = self.name + '@' + 'public'
        user_id = user.name + '@' + 'public'
        iroha = Iroha(account_id)
        query = iroha.query('GetAccountDetail',
                            account_id=account_id,
                            writer=user_id)
        IrohaCrypto.sign_query(query, private_key)
        response = self.network.send_query(query)
        data = response.account_detail_response
        print('Account id = {}, details = {}'.format(account_id, data.detail))
        return data.detail
