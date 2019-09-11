
class Asset:
    def __init__(self, name, precision, domain):
        """
        Object asset
        :param name: (str) name of the asset
        :param precision: (int) precision of the asset
        :param domain: (obj) domain to be included
        """
        self.name = name
        self.precision = precision
        self.domain = domain.id_name
