import zope.interface
import zope.component
import zc.catalog
from zope.catalog.text import TextIndex
from zc.catalog.catalogindex import ValueIndex

from zope.catalog.interfaces import ICatalog
import BTrees

import iexample
import interfaces
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent


class IndexDescriptor(object):
    """A python descriptor helping to index the attributes inherited from
    IReferenceIndexCatalog.

    The class needs an indexer attribute."""

    def __init__(self, name):
        self.name = name

    def __get__(self, inst, class_ = None):
        return getattr(inst.indexer, self.name, u'')

    def __set__(self, inst, val):
        pass


class ReferenceIndexer(object):
    """An adapter for indexing iexample objects in a
    IReferenceIndexCatalog."""

    zope.interface.implements(interfaces.IReferenceIndexCatalog)

    zope.component.adapts(iexample.IExample)

    def __init__(self, context):
        self.context = context
        self.indexer = interfaces.IReferenceIndexCatalog(context.reference)
        
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

    def getQuidProQuo(self):
        rc = getattr(self.context, 'quid', u'') + u' '
        rc += getattr(self.context, 'pro_quo', u'')
        return rc
    quid_pro_quo = property(getQuidProQuo)

    marker = IndexDescriptor('marker')


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


def createReferenceIndices(cat, interface = interfaces.IReferenceIndexCatalog):
    """Add indexes to the catalog passed in."""

    cat['author'] = TextIndex(
        interface = interface,
        field_name = 'author')
    
    cat['title'] = TextIndex(
        interface = interface,
        field_name = 'title')

    cat['post'] = ValueIndex(
        interface = interface,
        field_name = 'post')

    cat['ante'] = ValueIndex(
        interface = interface,
        field_name = 'ante')

    cat['year'] = ValueIndex(
        interface = interface,
        field_name = 'year')

    cat['language'] = ValueIndex(
        interface = interface,
        field_name = 'language')
        

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

    createReferenceIndices(cat)

    createExampleIndices(cat)

    sm.registerUtility(cat, ICatalog,
                       name = "examples")
