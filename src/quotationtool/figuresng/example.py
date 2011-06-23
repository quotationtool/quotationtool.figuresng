import zope.interface
from zope.schema.fieldproperty import FieldProperty
from zope.component.factory import Factory

from quotationtool.quotation.quotation import Quotation

from interfaces import IExample


class Example(Quotation):

    zope.interface.implements(IExample)

    quid = FieldProperty(IExample['quid'])
    pro_quo = FieldProperty(IExample['pro_quo'])
    marker = FieldProperty(IExample['marker'])


example_factory = Factory(Example)

def cmpExamplesByAttribute(some, other, attr_name):
    if not attr_name in IExample.names():
        # TODO: return default or raise error?
        return cmp(some, other)
    else:
        return cmp(getattr(some, attr_name, u''), getattr(other, attr_name, u''))
