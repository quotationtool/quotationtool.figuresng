from zope.interface import implements
from zope.component import adapter
from zope.container.btree import BTreeContainer
from zope.schema.fieldproperty import FieldProperty
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.exceptions.interfaces import UserError

from iexample import IExampleContainer, IExampleContainerContainer
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
from i18n import _


class ExampleContainer(BTreeContainer):
    """Implementation of a container for example objects."""

    implements(IExampleContainer,
               IExampleContainerContainer)

    count = FieldProperty(IExampleContainer['count'])

    def __setitem__(self, key, val):
        if not key == unicode(self.count+1):
            raise UserError(_(u"You want to use $KEY as key for the example, but it should be %COUNT!", mapping={'KEY': key, 'COUNT': self.count}))
        super(ExampleContainer, self).__setitem__(key, val)
        self.count += 1


@adapter(INewQuotationtoolSiteEvent)
def createExampleContainer(event):
    sm = event.object.getSiteManager()
    container = event.object['examples'] = ExampleContainer()
    sm.registerUtility(container, IExampleContainer)

    IWriteZopeDublinCore(container).title = u"Examples"

    IWriteZopeDublinCore(container).description = u"""The collection of examples lives in the 'Examples' container."""
