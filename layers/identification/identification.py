
from iroha import Iroha


class User:
    def _init_(self, private_key, public_key, name, domain):
        self.private_key = private_key
        self.public_key = public_key
        self.name = name
        self.domain = domain
        account_id = name + '@' + domain
        domain_to_create = Iroha(account_id)