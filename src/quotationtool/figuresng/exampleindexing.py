import zope.interface
import zope.component
import zc.catalog
from zope.catalog.text import TextIndex
from zc.catalog.catalogindex import ValueIndex
from zope.catalog.interfaces import ICatalog
import BTrees

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
from quotationtool.bibliography.interfaces import IBibliographyCatalog
from quotationtool.bibliography.indexing import createBibliographyCatalogIndices

import iexample
import interfaces


class IndexDescriptor(object):
    """A python descriptor helping to index the attributes inherited from
    IBibliographyCatalog.

    The class needs an indexer attribute."""

    def __init__(self, name):
        self.name = name

    def __get__(self, inst, class_ = None):
        return getattr(inst.indexer, self.name, u'')

    def __set__(self, inst, val):
        pass


class ReferenceIndexer(object):
    """An adapter for indexing iexample objects in a
    IBibliographyCatalog."""

    zope.interface.implements(IBibliographyCatalog)

    zope.component.adapts(iexample.IExample)

    def __init__(self, context):
        self.context = context
        self.indexer = IBibliographyCatalog(context.reference)
        
    any = IndexDescriptor('any')
    author = IndexDescriptor('author')
    title = IndexDescriptor('title')
    post = IndexDescriptor('post')
    ante = IndexDescriptor('ante')
    year = IndexDescriptor('year')
    language = IndexDescriptor('language')
    edition_year = IndexDescriptor('edition_year')
    editor = IndexDescriptor('editor')
    publisher = IndexDescriptor('publisher')
    location = IndexDescriptor('location')
    

class ExampleIndexer(object):
    """An adapter for indexing example objects."""

    zope.interface.implements(iexample.IExampleIndexCatalog)

    zope.component.adapts(iexample.IExample)

    def __init__(self, context):
        self.context = self.indexer = context

    quotation = IndexDescriptor('quotation')
    quid = IndexDescriptor('quid')
    pro_quo = IndexDescriptor('pro_quo')
    marker = IndexDescriptor('marker')

    @property
    def quid_pro_quo(self):
        rc = getattr(self.context, 'quid', u'') + u' '
        rc += getattr(self.context, 'pro_quo', u'')
        return rc

    @property
    def any(self):
        rc = u""
        rc += self.quotation + u" "
        rc += self.quid_pro + u" "
        rc += self.marker + u" "
        rc += IBibliographyCatalog(self.context.reference).any
        return rc


def createExampleIndices(cat, interface = iexample.IExampleIndexCatalog):
    """Add indexes to the catalog passed in."""

    cat['quotation'] = TextIndex(
        interface = interface,
        field_name = 'quotation')
    
    cat['quid'] = TextIndex(
        interface = interface,
        field_name = 'quid')

    cat['pro_quo'] = TextIndex(
        interface = interface,
        field_name = 'pro_quo')
        
    cat['quid_pro_quo'] = TextIndex(
        interface = interface,
        field_name = 'quid_pro_quo')

    cat['marker'] = TextIndex(
        interface = interface,
        field_name = 'marker')


def filter(extent, uid, obj):
    assert zc.catalog.interfaces.IFilterExtent.providedBy(extent)
    return iexample.IExample.providedBy(obj)


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createExampleCatalog(event):
    """Create an example catalog when a new quotationtool site is
    created.
    
    Yes, we don't perform joins for searching an example from a book
    with a certain author but simply multiply the indexes and indexed
    data. This was a decision with performance in mind: Minimize cpu
    cycles for a search query at the price of disk space. Lesson
    learned form google app engine..."""

    sm = event.object.getSiteManager()

    from zc.catalog.extentcatalog import FilterExtent, Catalog
    extent = FilterExtent(filter)#, family = BTrees.family64)

    sm['default']['examples_search_catalog'] = cat = Catalog(extent)

    createBibliographyCatalogIndices(cat)

    # this should redefine the 'any' index
    createExampleIndices(cat)

    cat['any'] = TextIndex(
        interface = iexample.IExampleIndexCatalog,
        field_name = 'any')

    sm.registerUtility(cat, ICatalog,
                       name = "examples")
