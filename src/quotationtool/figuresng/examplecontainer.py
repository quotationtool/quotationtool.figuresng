from zope.interface import implements
from zope.component import adapter
from zope.container.btree import BTreeContainer
from zope.schema.fieldproperty import FieldProperty
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.exceptions.interfaces import UserError
from zope.container.contained import NameChooser

from interfaces import IExampleContainer, IExampleContainerContainer

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent


class ExampleContainer(BTreeContainer):
    """Implementation of a container for example objects."""

    implements(IExampleContainer,
               IExampleContainerContainer)

    _count = FieldProperty(IExampleContainer['_count'])

    def __setitem__(self, key, val):
        super(ExampleContainer, self).__setitem__(key, val)
        self._count += 1


class ExampleNameChooser(NameChooser):
    """ A name chooser for example objects in the container context."""
    
    def chooseName(self, name, obj):
        self.checkName(unicode(self.context._count + 1), obj)
        return unicode(self.context._count + 1)


@adapter(INewQuotationtoolSiteEvent)
def createExampleContainer(event):
    sm = event.object.getSiteManager()
    container = event.object['examples'] = ExampleContainer()
    sm.registerUtility(container, IExampleContainer)

    IWriteZopeDublinCore(container).title = u"Examples"

    IWriteZopeDublinCore(container).description = u"""The collection of examples lives in the 'Examples' container."""
