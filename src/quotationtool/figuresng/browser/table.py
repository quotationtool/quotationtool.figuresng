import zope.interface
import zope.component
from z3c.table import table, column, value, header
from z3c.table.interfaces import ITable, IColumn
from z3c.pagelet.browser import BrowserPagelet
from zope.contentprovider.interfaces import IContentProvider
from zope.publisher.interfaces.browser import IBrowserRequest
from z3c.indexer.search import ResultSet
import zc.relation
from zope.intid.interfaces import IIntIds
from zope.proxy import removeAllProxies
import urllib
from z3c.searcher.interfaces import ISearchSession

from quotationtool.skin.interfaces import ITabbedContentLayout
from quotationtool.renderer.interfaces import IHTMLRenderer
from quotationtool.quotation.interfaces import IReference
from quotationtool.quotation.browser.table import IAuthorTitleYearTable, IQuotationsInReferenceTable, ISortingColumn
from quotationtool.search.interfaces import ISearchResultPage

from quotationtool.figuresng.interfaces import _, IExample, IExampleContainer


class IExamplesTable(ITable):
    """ A table for example objects."""


class IQuotationExamplesTable(ITable):
    """ A table with a quotation column."""
 

class ExampleContainerTable(table.Table, BrowserPagelet):
    """ A table with all examples in the example container."""

    zope.interface.implements(IExamplesTable,
                              IAuthorTitleYearTable)

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u'head',
        }

    cssClassEven = u'even'
    cssClassOdd = u'odd'


class ExamplesInReferenceTable(table.SequenceTable, BrowserPagelet):
    """ A table with all examples from a certain reference."""

    zope.interface.implements(IExamplesTable,
                              IQuotationExamplesTable,
                              IQuotationsInReferenceTable, 
                              ITabbedContentLayout)

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u'head',
        }

    cssClassEven = u'even'
    cssClassOdd = u'odd'

    batchSize = 10
    startBatchingAt = 10


class ExamplesInReference(value.ValuesMixin):
    """ Values (examples) from a reference."""

    zope.component.adapts(IReference,
                          IBrowserRequest, 
                          ExamplesInReferenceTable)

    @property
    def values(self):
        """ We use ResultSet from the z3c.indexer package because it
        is slicable and fast."""
        intids = zope.component.getUtility(
            IIntIds,
            context=self.context)
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context=self.context)
        examples = cat.findRelationTokens(
            cat.tokenizeQuery({'iquotation-reference': self.context}))
        return ResultSet(examples, intids)


class SearchResultTable(ExampleContainerTable):
    """ A table that displays the result of a search for examples."""

    zope.interface.implements(ISearchResultPage)


class ResultingExamples(value.ValuesMixin):

    zope.component.adapts(IExampleContainer,
                          IBrowserRequest,
                          SearchResultTable)
    
    from quotationtool.figuresng.searcher import ExampleSearchFilter
    search_filter_factory = ExampleSearchFilter

    session_name = 'examples'

    @property
    def values(self):
        session = ISearchSession(self.request)
        search_filter = session.getFilter(self.session_name)
        query = search_filter.generateQuery()
        return query.searchResults()
        

class QuidColumn(column.LinkColumn):
    """ The quid attribute of an example object."""

    zope.interface.implements(ISortingColumn)

    header = IExample['quid'].title
    weight = 10

    def getLinkContent(self, item):
        return getattr(item, 'quid', u"")

    def getSortKey(self, item):
        return getattr(item, 'quid', u"")


class ProQuoColumn(column.GetAttrColumn):
    """ The pro_quo attribute of an example object."""

    zope.interface.implements(ISortingColumn)

    header = IExample['pro_quo'].title
    attrName = 'pro_quo'
    weight = 20

    def getSortKey(self, item):
        return getattr(item, 'pro_quo', u"")


class MarkerColumn(column.GetAttrColumn):
    """ The pro_quo attribute of an example object."""

    zope.interface.implements(ISortingColumn)

    header = IExample['marker'].title
    attrName = 'marker'
    weight = 30

    def getSortKey(self, item):
        return getattr(item, 'marker', u"")


class FlagsColumn(column.Column):
    """ The flags of a example."""

    header = _(u"flags")
    weight = 99999
    
    def renderCell(self, item):
        flags = zope.component.getMultiAdapter(
            (item, self.request, self.table),
            IContentProvider, name='flags')
        flags.update()
        return flags.render()
