"""
=====
Admin
=====

Administrator
=============
Defines an Admin of the BSMD. This module also defines the domains

"""
from iroha import Iroha, IrohaCrypto, IrohaGrpc
from utils.iroha import send_transaction_and_print_status


class Admin:
    """
    The administrator object of the BSMD. This object can create assets, add active nodes, add passive nodes and creates
    de public domain in the BSMD

    :param str ip: ip address of one node hosting the Blockchain

    :Example:
    >>> Admin('123.456.789')
    """

    def __init__(self, ip):
        self.private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
        self.iroha = Iroha('admin@public')
        ip_address = ip + ':50051'
        self.network = IrohaGrpc(ip_address)

    def create_user_in_iroha(self, user):
        """
        Creates a personal account in a domain

        :Example:
        >>> import json
        >>> from layers.identification.user import User
        >>> x = { "age": 30, "city": "New York" }
        >>> account_information = json.dumps(x)
        >>> public = Domain('public', 'default_role')
        >>> user = User('private_key','David',public, account_information)
        >>> admin = Admin('123.456.789')
        >>> admin.create_user_in_iroha(user)

        :param User user: a user object

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
        Creates an asset

        :Example:
        >>> from layers.incentive.asset import Asset
        >>> public = Domain('public', 'default_role')
        >>> asset = Asset('coin', public, 3)
        >>> admin = Admin('123.456.789')
        >>> admin.create_asset(asset)

        :param Asset asset: Asset to be created
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
        The admin creates credit for a user. Users can buy credit in the BSMD to pay for services. This functions works
        in two step:

        #. admin add assets to his own wallet
        #. admin transfers the asset to the user

        :Example:
        >>> import json
        >>> from layers.identification.user import User
        >>> from layers.incentive.asset import Asset
        >>> x = { "age": 30, "city": "Cartagena" }
        >>> account_information = json.dumps(x)
        >>> public = Domain('public', 'default_role')
        >>> user = User('private_key','David',public, account_information)
        >>> asset = Asset('coin', public, 3)
        >>> asset.domain
        >>> admin = Admin('123.456.789')
        >>> admin.add_assets_to_user(user, asset, 330.2)

        :param User user: User receiving the assets
        :param Asset asset: Asset to be transferred
        :param float asset_qty: Quantity of assets the node buy

        """
        # 1. Admin creates the asset for the user
        asset_id = asset.name + '#' + asset.domain.name
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
                               src_account_id='admin@public',
                               dest_account_id=dest_account_id,
                               asset_id=asset_id,
                               description='asset created for node',
                               amount=asset_qty)])
        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)

    def create_domain(self, domain):
        """
        Creates a domain

        :Example:
        >>> public = Domain('public', 'default_role')
        >>> admin = Admin('123.456.789')
        >>> admin.create_domain(public)

        :param Domain domain: domain to be created

        """
        tx = self.iroha.transaction(
            [self.iroha.command('CreateDomain',
                                domain_id=domain.name,
                                default_role=domain.default_role)])

        IrohaCrypto.sign_transaction(tx, self.private_key)
        send_transaction_and_print_status(tx, self.network)


class Domain:
    """
    The domain can be use to run distributed processes. Or to constantly share information of an specific
    type

    :Example:
    >>> Domain('public', 'default_role')

    :param str name: name of the domain
    :param str default_role: default role in the domain

    """
    def __init__(self, name, default_role):

        self.name = name
        self.default_role = default_role
