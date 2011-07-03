# needed for ZODB for historical reasons
from interfaces import *

#BBB: to be removed in 1.0
from zope.interface import Interface, Attribute
class IExampleIndexCatalog(Interface):
    """A collection of indexes for example objects. """

    quid = Attribute('BBB')
    pro_quo = Attribute('BBB')
    quid_pro_quo = Attribute('BBB')
    marker = Attribute('BBB')
    quotation = Attribute('BBB')
    any = Attribute('BBB')
