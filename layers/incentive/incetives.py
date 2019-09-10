from iroha import IrohaCrypto
from utils.iroha import IROHA_ADMIN, ADMIN_PRIVATE_KEY, send_transaction_and_print_status


class Asset:
    def __init__(self, name, precision, domain):
        self.name = name
        self.precision = precision
        self.domain = domain

    def create_asset(self):
        """
        Creates an asset domain's asset
        :return:
        """
        tx = IROHA_ADMIN.transaction(
            [IROHA_ADMIN.command('CreateAsset',
                                 asset_name=self.name,
                                 domain_id=self.domain,
                                 precision=self.precision)])
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        send_transaction_and_print_status(tx)





