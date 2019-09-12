from iroha import Iroha, IrohaCrypto, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
from utils.iroha import send_transaction_and_print_status


class Broker:

    def __init__(self, private_key, name, domain, ip, public_info):
        """
        Object user.
        :param private_key: (str) private key of the user. This is not save in the class is just used to generate
                            a public_key. In other functions the private_key must be used to sign transactions. You can
                            generate private keys with IrohaCrypto.private_key()
        :param name: (str) name of the user (lower case)
        :param domain: (obj) domain where the user will live. If
        :param ip: (ip_address) ip of one node hosting the blockchain
        :param public_info: (json) public information of the user, e.g., type of node: government, individual, etc
        """
        self.public_key = IrohaCrypto.derive_public_key(private_key)
        self.name = name
        self.domain = 'public'
        ip_address = ip + ':50051'
        self.network = IrohaGrpc(ip_address)
        self.public_info = public_info

    # ###############
    # get account information from a node
    # ###############
    def get_details_from(self, user, private_key):
        """
        Consult all details of the node. Broker can only consult details in the 'public' domain
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
