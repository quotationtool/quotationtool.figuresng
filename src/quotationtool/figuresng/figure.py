import zope.interface
import zope.component
import zc.relation
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from interfaces import IFigure
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
from quotationtool.relation import dump, load


class Figure(Persistent):
    """Implementation of figure object. This is a base class for more
    specific figure types.

        >>> from quotationtool.figuresng.figure import Figure
        >>> simile = Figure()



        >>> simile.reference = bad = object()
        Traceback (most recent call last):
        ...
        RelationPreconditionError

        >>> import zope.interface
        >>> from quotationtool.bibliography.interfaces import IEntry
        >>> class Reference(object):
        ...     pass
        >>> zope.interface.classImplements(Reference, IEntry)

        >>> updikescunts = Reference()
        >>> simile.reference = updikescunts



        >>> shark = u"She feels like a shark, slimy and abrasive."
        >>> simile.quotation = shark
        >>> len(shark) == simile.length
        True

        >>> simile.position = u"23"
        >>> simile.source_type = 'plaintext'


    """
    
    zope.interface.implements(IFigure)

    __name__ = __parent__ = None

    reference = FieldProperty(IFigure['reference'])
    _quotation = FieldProperty(IFigure['quotation'])
    length = FieldProperty(IFigure['length'])
    source_type = FieldProperty(IFigure['source_type'])
    position = FieldProperty(IFigure['position'])

    def setQuotation(self, val):
        self._quotation = val
        self.length = len(val)
    def getQuotation(self):
        return self._quotation
    quotation = property(getQuotation, setQuotation)


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createRelationIndex(event):
    """ Create a new index in the relation catalog.

    This requires configure.zcml from quotationtool.relation included
    before the config of this package because of the order of the
    subscribers.
    """
    sm = event.object.getSiteManager()
    cat = zope.component.getUtility(
        zc.relation.interfaces.ICatalog,
        context = event.object)
    cat.addValueIndex(
        IFigure['reference'],
        dump = dump, load = load,
        name = 'ifigure-reference')
        
