"""
Incentives
==========
Defines an Asset class.

"""


class Asset:
    """
    Assets are created in domains and are use as cryptocurrencies

    :Example:
    >>> from layers.admin.administrator import Domain
    >>> public = Domain('public', 'default_role')
    >>> Asset('coin', public, 3)

    :param str name: name of the asset
    :param Domain domain: Domain object
    :param int precision: precession of the asset, e.g. precession = 3, the asset has 3 decimal points

    """
    def __init__(self, name, domain, precision):
        self.name = name
        self.domain = domain
        self.precision = precision
