
from iroha import Iroha, IrohaCrypto, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
from utils.iroha import send_transaction_and_print_status


class User:

    def __init__(self, private_key, name, domain, ip):
        """
        Object user.
        :param private_key: (str) private key of the user. This is not save in the class is just used to generate
                            a public_key. In other functions the private_key must be used to sign transactions. You can
                            generate private keys with IrohaCrypto.private_key()
        :param name: (str) name of the user (lower case)
        :param domain: (obj) domain where the user will live
        :param ip: (ip_address) ip of one node hosting the blockchain
        """
        self.public_key = IrohaCrypto.derive_public_key(private_key)
        self.name = name
        self.domain = domain.id_name
        ip_address = ip + ':50051'
        self.network = IrohaGrpc(ip_address)

    # ###############
    # asset functions
    # ###############
    def get_balance(self, private_key):
        """
        Get the balance of my account
        :param private_key: (str) key to sign the transaction
        :return: data: (array) asset id and assets quantity
        Return example:
        [asset_id: "fedcoin#federated"
        account_id: "generator@federated"
        balance: "1000"
        ]
        """
        account_id = self.name + '@' + self.domain
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
        Transfer assets from one account to another. Both users must be in the same domain
        :param user: (obj) user you want to transfer the assets
        :param asset_name: (str) name of the asset to be transferred
        :param quantity: (float) Number of assets we want to transfer
        :param description: (str) Small message to the receiver of assets
        :param private_key: (str) key to sign the transaction
        :return:
        Example:
        transfer_assets(Dante, 'coin', '2', 'Shut up and take my money')
        """

        account_id = self.name + '@' + self.domain
        iroha = Iroha(account_id)
        destination_account = user.name + '@' + self.domain
        asset_id = asset_name + '#' + self.domain
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
        Consult all details of the node
        :param private_key: (str) key to sign the transaction
        :return: data: (json) solicited details of the user
        Return example:
        {
            "node@domainA":{
                "Age":"35",
                "Name":"Quetzacoatl"
            },
            "node@domainB":{
                "Location":"35.3333535,-45.2141556464",
                "Status":"valid"
            },
            "nodeA@domainC":{
                "FederatingParam":"35.242553",
                "Loop":"3"
            }
        }
        """
        account_id = self.name + '@' + self.domain
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
        Consult all details of the node
        :param private_key: (str) key to sign the transaction
        :param detail_key: (str) name of the detail to be consulted
        :return: data: (json) solicited details of the user
        Return example:
        {
            "node@domainA":{
                "Age":"35"
            }
        }
        """
        account_id = self.name + '@' + self.domain
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
        Consult all details of the node
        :param private_key: (str) key to sign the transaction
        :param user: (obj) user who write information on your identification
        :return: data: (json) solicited details of the user
        Return example:
        {
            "nodeA@domainC":{
                "FederatingParam":"35.242553",
                "Loop":"3"
            }
        }
        """
        account_id = self.name + '@' + self.domain
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
        Consult all details of the node
        :param private_key: (str) key to sign the transaction
        :param user: (obj) user who write information on your identification
        :param detail_key: (str) name of the detail to be consulted
        :return: data: (json) solicited details of the user
        Return example:
        {
            "nodeA@domainC":{
                "FederatingParam":"35.242553",
                "Loop":"3"
            }
        }
        """
        account_id = self.name + '@' + self.domain
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
        :param detail_key: (str) Name of the detail we want to set
        :param detail_value: (str) Value of the detail
        :param private_key: (str) key to sign the transaction
        :return: null:
        Usage example:
        set_detail('age', '33')
        """
        print(self.name, self.domain, self.public_key, private_key, detail_key, detail_value)
        account_id = self.name + '@' + self.domain
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
        :param user: (obj) user you want to set the details
        :param detail_key: (str) Name of the detail we want to set
        :param detail_value: (str) Value of the detail
        :param private_key: (str) key to sign the transaction
        :return: null:
        Usage example:
        set_detail(Lucas, 'key', 'age', '33')
        """
        account = self.name + '@' + self.domain
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
        :param user: (obj) user you want to grant permissions to set detail on your behalf
        :param private_key: (str) key to sign the transaction
        :return:
        """
        my_id_account = self.name + '@' + self.domain
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

