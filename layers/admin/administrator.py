from iroha import Iroha, IrohaCrypto, IrohaGrpc
from utils.iroha import send_transaction_and_print_status


class Admin:
    def __init__(self, ip):
        """
        Object admin. This will handle all administrative issues in the BSMD
        :param ip: (ip_address) ip of one node hosting the Blockchain
        """
        self.private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
        self.iroha = Iroha('admin@test')
        ip_address = ip + ':50051'
        self.network = IrohaGrpc(ip_address)

    def create_user_in_iroha(self, user):
        """
        Create a personal account in a domain.
        :return: null:
        """
        tx = self.iroha.transaction(
            [self.iroha.command('CreateAccount',
                                account_name=user.name,
                                domain_id=user.domain,
                                public_key=user.public_key)])
        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)

    def create_asset(self, asset):
        """
        Creates an asset in the domain's asset
         :param asset: (obj) Asset to be created
        :return:
        """
        tx = self.iroha.transaction(
            [self.iroha.command('CreateAsset',
                                asset_name=asset.name,
                                domain_id=asset.domain,
                                precision=asset.precision)])
        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)

    def add_assets_to_user(self, user, asset, asset_qty):
        """
        Create a personal account. This function works in three steps
            1. The admin create credit (assets) for the account (credit is created only if the user
               buy it)
            2. The admin transfer the credit to the user
        :param user: (obj) user receiving the assets
        :param asset: (obj) asset to be transferred
        :param asset_qty: (float) Quantity of assets the node buy
        :return: null:
        """
        # 1. Admin create the asset for the user
        asset_id = asset.name + '#' + asset.domain
        tx = self.iroha.transaction(
            [self.iroha.command('AddAssetQuantity',
                                asset_id=asset_id,
                                amount=asset_qty)])
        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)

        # 2. Admin transfer the assets to the user
        dest_account_id = user.name + '@' + user.domain
        tx = self.iroha.transaction([
            self.iroha.command('TransferAsset',
                               src_account_id='admin@test',
                               dest_account_id=dest_account_id,
                               asset_id=asset_id,
                               description='asset created for node',
                               amount=asset_qty)])
        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)

    def create_domain_and_asset(self, domain, asset):
        """
        Creates a domain and an asset in the domain
        :param domain: (obj) domain to be created
        :param asset: (obj) asset to be create in the domain
        :return: null
        """
        print(domain.id, domain.default_role, asset.name, asset.precision)
        commands = [self.iroha.command('CreateDomain',
                                       domain_id=domain.id,
                                       default_role=domain.default_role),
                    self.iroha.command('CreateAsset',
                                       asset_name=asset.name,
                                       domain_id=asset.domain,
                                       precision=asset.precision)]

        tx = IrohaCrypto.sign_transaction(self.iroha.transaction(commands),
                                          self.private_key)
        send_transaction_and_print_status(tx, self.network)

    def create_domain(self, domain):
        """
        Creates a domain
        :param domain: (obj) domain to be created
        """
        tx = self.iroha.transaction(
            [self.iroha.command('CreateDomain',
                                domain_id=domain.id_name,
                                default_role=domain.default_role)])

        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)


class Domain:
    def __init__(self, id_name, default_role):
        """
        Object domain
        :param id_name: (str) name of the domain
        :param default_role:  (str) default role in the domain
        """
        self.id_name = id_name
        self.default_role = default_role
