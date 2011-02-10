import zope.interface
from z3c.menu.ready2go.item import ContextMenuItem


class IEntryTab(zope.interface.Interface): pass
class EntryTab(ContextMenuItem):
    zope.interface.implements(IEntryTab)
