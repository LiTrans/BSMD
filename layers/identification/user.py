"""
==============
Identification
==============

User
====
Defines a User class.

"""

from iroha import Iroha, IrohaCrypto, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
from utils.iroha import send_transaction_and_print_status


class User:
    """
    Create an User object. This object can be use to create a passive node in the BSMD
    
    :Example:
    >>> import json
    >>> from admin.administrator import Domain
    >>> x = { "age": 30, "city": "New York" }
    >>> account_information = json.dumps(x)
    >>> me = User('private_key', 'My Name', 'My domain', '123.456.789', account_information)
    >>> print(me.name)
    My name

    :param str private_key: private key of the user. This is not save in the class is just used to generate
                    a public_key. In other functions the private_key must be used to sign transactions. You can
                    generate private keys with IrohaCrypto.private_key()

    :param str name: name of the user (lower case)
    :param Domain domain: domain where the user will live
    :param str ip: ip of one node hosting the blockchain
    :param json public_info: public information of the user. If domain is public this field can't be null
    
    """

    def __init__(self, private_key, name, domain, ip, public_info):
        self.public_key = IrohaCrypto.derive_public_key(private_key)
        self.name = name
        self.domain = domain
        self.domain.name = domain.name
        ip_address = ip + ':50051'
        self.network = IrohaGrpc(ip_address)
        if domain.name == 'public':
            self.public_info = public_info

    # ###############
    # create my own account
    # ###############
    def create_account(self, private_key):
        """
        Create a personal account in the BSMD. In the public domain all your public information is automatically
        populated

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> public = Domain('public', 'default_role')
        >>> user = User('private_key','David', public, '123.456.789', account_information)
        >>> user.create_account('private_key')

        :param str private_key: The private key of the user

        """
        account_id = self.name + '@' + self.domain.name
        iroha = Iroha(account_id)
        tx = iroha.transaction(
            [iroha.command('CreateAccount',
                           account_name=self.name,
                           domain_id=self.domain,
                           public_key=self.public_key)])
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

        if self.domain == 'public':
            self.set_detail('public', self.public_info, private_key)

    # ###############
    # Domain related functions
    # ###############
    def create_domain(self, domain, private_key):
        """
        Creates a domain for personal use. You can create a domain for a particular process, e.g., Federated Learning

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key', 'My Name', 'My domain', '123.456.789', account_information)
        >>> user.create_domain(domain, 'private_key')

        :param Domain domain: domain to be created
        :param str private_key: key to sign the transaction

        """
        account_id = self.name + '@' + self.domain.name
        iroha = Iroha(account_id)
        tx = iroha.transaction(
            [iroha.command('CreateDomain',
                           domain_id=domain.name,
                           default_role=domain.default_role)])

        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

    # ###############
    # asset functions
    # ###############
    def get_balance(self, private_key):
        """
        Get the balance of my account. Use the private key of the user to get his current balance. The function will
        return a dictionary with the id of the asset, the account id  and the balance.

        :Example:
        >>> import json
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> user = User('private_key', 'My Name', 'My domain', '123.456.789', account_information)
        >>> balance = user.get_balance('private_key')
        >>> print(balance)
        {asset_id: "fedcoin#federated",
        account_id: "generator@federated",
        balance: "1000"}

        :param str private_key: key to sign the transaction
        :return: A a dictionary with the id of the asset, the account id  and the balance
        :rtype: dict

        """
        account_id = self.name + '@' + self.domain.name
        iroha = Iroha(account_id)
        query = iroha.query('GetAccountAssets',
                            account_id=account_id)
        IrohaCrypto.sign_query(query, private_key)

        response = self.network.send_query(query)
        data = response.account_assets_response.account_assets
        for asset in data:
            print('Asset id = {}, balance = {}'.format(asset.asset_id, asset.balance))
        return data

    def transfer_assets_to(self, user, asset_name, quantity, description, private_key):
        """
        Transfer assets from one account to another. Both users must be in the same domain.

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> x = { "age": 34, "city": "Mexico" }
        >>> account_information_dante = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> dante = User('dante_private_key','Dante',domain, account_information_dante)
        >>> user.transfer_assets_to(dante, 'coin', '2', 'Shut up and take my money')

        :param User user: User you want to transfer the assets
        :param str asset_name: Name of the asset to be transferred
        :param float quantity: Number of assets we want to transfer
        :param str description: Small message to the receiver of assets
        :param str private_key: Key to sign the transaction

        """

        account_id = self.name + '@' + self.domain.name
        iroha = Iroha(account_id)
        destination_account = user.name + '@' + self.domain.name
        asset_id = asset_name + '#' + self.domain.name
        tx = iroha.transaction([
            iroha.command('TransferAsset',
                          src_account_id=account_id,
                          dest_account_id=destination_account,
                          asset_id=asset_id,
                          description=description,
                          amount=quantity)
        ])
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

    # ###############
    # get own account information
    # ###############
    def get_all_details(self, private_key):
        """
        Consult all details of the user in all the domains

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> details = user.get_all_details('private_key')
        >>> print(details)

        :param str private_key: Key to sign the transaction
        :return: solicited details of the user
        :rtype: json

        {
            "user@domainA":{
                "Age":"35",
                "Name":"Quetzalcoatl"
            },
            "user@domainB":{
                "Location":"35.3333535,-45.2141556464",
                "Status":"valid"
            },
            "user@domainC":{
                "FederatingParam":"35.242553",
                "Loop":"3"
            }
        }

        """
        account_id = self.name + '@' + self.domain.name.name
        iroha = Iroha(account_id)
        query = iroha.query('GetAccountDetail',
                            account_id=account_id)
        IrohaCrypto.sign_query(query, private_key)
        response = self.network.send_query(query)
        data = response.account_detail_response
        print('Account id = {}, details = {}'.format(account_id, data.detail))
        return data.detail

    def get_a_detail(self, detail_key, private_key):
        """
        Consult a detail of the user

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> details = user.get_a_detail('private_key', 'age')
        >>> print(details)
        {
            "user@domainA":{
                "Age":"35"
            }
        }

        :param str private_key: key to sign the transaction
        :param str detail_key: name of the detail to be consulted
        :return: solicited details of the user
        :rtype: json

        """

        account_id = self.name + '@' + self.domain.name
        iroha = Iroha(account_id)
        query = iroha.query('GetAccountDetail',
                            account_id=account_id,
                            key=detail_key)
        IrohaCrypto.sign_query(query, private_key)
        response = self.network.send_query(query)
        data = response.account_detail_response
        print('Account id = {}, details = {}'.format(account_id, data.detail))
        return data.detail

    def get_all_details_written_by(self, user, private_key):
        """
        Consult all details writen by some other node

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> x = { "age": 34, "city": "Mexico" }
        >>> account_information_juan = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> juan = User('private_key_juan','Juan',domain, account_information_juan)
        >>> details = user.get_all_details_written_by(juan, 'private_key')
        >>> print(details)
        {
            "user@domain":{
                "FederatingParam":"35.242553",
                "Loop":"3"
            },
            "user@domain":{
                "sa_param":"44",
                "Loop":"3"
            }
        }

        :param str private_key: key to sign the transaction
        :param User user: user who write information on your identification
        :return: solicited details of the user
        :rtype: json

        """
        account_id = self.name + '@' + self.domain.name
        user_id = user.name + '@' + user.domain
        iroha = Iroha(account_id)
        query = iroha.query('GetAccountDetail',
                            account_id=account_id,
                            writer=user_id)
        IrohaCrypto.sign_query(query, private_key)
        response = self.network.send_query(query)
        data = response.account_detail_response
        print('Account id = {}, details = {}'.format(account_id, data.detail))
        return data.detail

    def get_a_detail_written_by(self, user, detail_key, private_key):
        """
        Consult a detail of the node writen by other node

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> x = { "age": 34, "city": "Mexico" }
        >>> account_information_juan = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> juan = User('private_key_juan','Juan',domain, account_information_juan)
        >>> details = user.get_a_detail_written_by(juan, 'FederatingParam',  'private_key')
        >>> print(details)
        {
            "user@domainC":{
                "FederatingParam":"35.242553"
            }
        }

        :param str private_key: key to sign the transaction
        :param User user: user who write information on your identification
        :param str detail_key: name of the detail to be consulted
        :return: solicited details of the user
        :rtype: json

        """
        account_id = self.name + '@' + self.domain.name
        user_id = user.name + '@' + user.domain
        iroha = Iroha(account_id)
        query = iroha.query('GetAccountDetail',
                            account_id=account_id,
                            key=detail_key,
                            writer=user_id)
        IrohaCrypto.sign_query(query, private_key)
        response = self.network.send_query(query)
        data = response.account_detail_response
        print('Account id = {}, details = {}'.format(account_id, data.detail))
        return data.detail

    # ###############
    # set own account information
    # ###############
    def set_detail(self, detail_key, detail_value, private_key):
        """
        Set a detail in my account. The details can be stored in JSON format with limit of 4096 characters per detail

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "gender": 30, "address": "123 Tennis" }
        >>> account_information = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David', domain, account_information)
        >>> user.set_detail('personal information', account_information, 'private_key')

        :param str detail_key: Name of the detail we want to set
        :param json detail_value: Value of the detail
        :param str private_key: Key to sign the transaction

        """

        account_id = self.name + '@' + self.domain.name
        iroha = Iroha(account_id)
        tx = iroha.transaction([
            iroha.command('SetAccountDetail',
                          account_id=account_id,
                          key=detail_key,
                          value=detail_value)
        ])
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

    # ###############
    # set information to other account
    # ###############
    def set_detail_to(self, user, detail_key, detail_value, private_key):
        """
        Set a detail to a node. The details can be stored in JSON format with limit of 4096 characters per detail.
        You must have the permission from the node to set information on his identification

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> x = { "age": 34, "city": "Mexico" }
        >>> account_information_juan = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> juan = User('private_key_juan','Juan',domain, account_information_juan)
        >>> user.set_detail_to(juan, 'Job', 'Bartender', 'private_key')

        :param User user: user you want to set the details
        :param str detail_key: Name of the detail we want to set
        :param str detail_value: Value of the detail
        :param str private_key: key to sign the transaction

        """
        account = self.name + '@' + self.domain.name
        iroha = Iroha(account)
        account_id = user.name + '@' + user.domain
        tx = iroha.transaction([
            iroha.command('SetAccountDetail',
                          account_id=account_id,
                          key=detail_key,
                          value=detail_value)
        ])
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

    # ###############
    # grant permissions
    # ###############
    def grants_access_set_details_to(self, user, private_key):
        """
        Grant permission to a node to set details on your identification

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> x = { "age": 34, "city": "Mexico" }
        >>> account_information_juan = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> juan = User('private_key_juan','Juan',domain, account_information_juan)
        >>> user.grants_access_set_details_to(juan, 'private_key')

        :param User user: User you want to grant permissions to set detail on your behalf
        :param str private_key: Key to sign the transaction

        """
        my_id_account = self.name + '@' + self.domain.name
        grant_account_id = user.name + '@' + user.domain
        iroha = Iroha(my_id_account)
        tx = iroha.transaction([
            iroha.command('GrantPermission',
                          account_id=grant_account_id,
                          permission=can_set_my_account_detail)
        ],
            creator_account=my_id_account)
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)

    def revoke_access_set_details_to(self, user, private_key):
        """
        Revoke permission to a node to set details on your identification

        :Example:
        >>> import json
        >>> from admin.administrator import Domain
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> x = { "age": 34, "city": "Mexico" }
        >>> account_information_juan = json.dumps(x)
        >>> domain = Domain('name', 'default_role')
        >>> user = User('private_key','David',domain, account_information)
        >>> juan = User('private_key_juan','Juan',domain, account_information_juan)
        >>> user.revoke_access_set_details_to(juan, 'private_key')

        :param User user: User you want to revoke permissions to set details on your behalf
        :param str private_key: Key to sign the transaction

        """
        my_id_account = self.name + '@' + self.domain.name
        grant_account_id = user.name + '@' + user.domain
        iroha = Iroha(my_id_account)
        tx = iroha.transaction([
            iroha.command('RevokePermission',
                          account_id=grant_account_id,
                          permission=can_set_my_account_detail)
        ],
            creator_account=my_id_account)
        IrohaCrypto.sign_transaction(tx, private_key)
        send_transaction_and_print_status(tx, self.network)
