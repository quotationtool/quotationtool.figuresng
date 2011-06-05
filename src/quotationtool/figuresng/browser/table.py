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

from quotationtool.bibliography.interfaces import IBibliographyCatalog, IEntry
from quotationtool.skin.interfaces import ITabbedContentLayout
from quotationtool.renderer.interfaces import IHTMLRenderer

from quotationtool.figuresng.interfaces import _
from quotationtool.figuresng.iexample import IExample


class IExamplesTable(ITable):
    """ A table for example objects."""


class IAuthorTitleExamplesTable(ITable):
    """ A table for example objects with columns for author and
    title."""


class IExamplesInReferenceTable(ITable):
    """ A table of example objects all taken from the same reference
    (or somehow else it is clear who the author, title etc. is). """


class ISortingColumn(IColumn):
    """ A column that offers sorting."""


class ExampleContainerTable(table.Table, BrowserPagelet):
    """ A table with all examples in the example container."""

    zope.interface.implements(IExamplesTable, 
                              IAuthorTitleExamplesTable)

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
                              IExamplesInReferenceTable, 
                              ITabbedContentLayout)

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u'head',
        }

    cssClassEven = u'even'
    cssClassOdd = u'odd'


class ExamplesInReference(value.ValuesMixin):
    """ Values (examples) from a reference."""

    zope.component.adapts(IEntry,
                          IBrowserRequest, 
                          IExamplesInReferenceTable)

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
            cat.tokenizeQuery({'ifigure-reference': self.context}))
        return ResultSet(examples, intids)


class QuidColumn(column.LinkColumn):
    """ The quid attribute of an example object."""

    zope.interface.implements(ISortingColumn)

    header = IExample['quid'].title
    weight = 10

    def getLinkContent(self, item):
        return getattr(item, 'quid', u"")

    def getSortKey(self, item):
        if item.__name__ == '359':
            pass
            #raise Exception(item.quid)
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


class YearColumn(column.Column):
    """ The year attribute of a bibliographic entry."""

    zope.interface.implements(ISortingColumn)

    header = IBibliographyCatalog['year'].title
    weight = 105

    def renderCell(self, item):
        view = zope.component.getMultiAdapter(
            (item.reference, self.request),
            name='year')
        return view()

    def getSortKey(self, item):
        return IBibliographyCatalog(item).year


class AuthorColumn(column.Column):
    """ The year attribute of a bibliographic entry."""

    zope.interface.implements(ISortingColumn)

    header = IBibliographyCatalog['author'].title
    weight = 110

    def renderCell(self, item):
        view = zope.component.getMultiAdapter(
            (item.reference, self.request),
            name='author')
        return view()

    def getSortKey(self, item):
        return IBibliographyCatalog(item).author


class TitleColumn(column.Column):
    """ The year attribute of a bibliographic entry."""

    zope.interface.implements(ISortingColumn)

    header = IBibliographyCatalog['title'].title
    weight = 120

    def renderCell(self, item):
        view = zope.component.getMultiAdapter(
            (item.reference, self.request),
            name='title')
        return view()

    def getSortKey(self, item):
        return IBibliographyCatalog(item).title


class PositionColumn(column.GetAttrColumn):
    """ The position of the example in the entry."""

    #zope.interface.implements(ISortingColumn)

    header = IExample['position'].title
    weight = 5
    attrName = 'position'

    def getSortKey(self, item):
        return getattr(item, 'position', u"")#TODO


class QuotationColumn(column.Column):
    """ The quotation."""

    header = IExample['quotation'].title
    weight = 210

    def renderCell(self, item):
        source = zope.component.createObject(
            item.source_type,
            item.quotation)
        renderer = zope.component.getMultiAdapter(
            (removeAllProxies(source), self.request),
            IHTMLRenderer, name = u'')
        return renderer.render(limit=200)

    def getSortKey(self, item):
        return self.renderCell(item)


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


class SortingColumnHeader(header.ColumnHeader):
    """ As SortingColumnHeader from z3c.table, but offers css for
    headers."""

    def render(self):
        table = self.table
        prefix = table.prefix
        colID = self.column.id

        # this may return a string 'id-name-idx' if coming from request,
        # otherwise in Table class it is intialised as a integer string
        currentSortID = table.getSortOn()
        try:
            currentSortID = int(currentSortID)
        except ValueError:
            currentSortID = currentSortID.rsplit('-', 1)[-1]

        currentSortOrder = table.getSortOrder()

        sortID = colID.rsplit('-', 1)[-1]

        sortOrder = table.sortOrder
        if int(sortID) == int(currentSortID):
            # ordering the same column so we want to reverse the order
            if currentSortOrder in table.reverseSortOrderNames:
                sortOrder = 'ascending'
            elif currentSortOrder == 'ascending':
                sortOrder = table.reverseSortOrderNames[0]

        args = self.getQueryStringArgs()
        args.update({'%s-sortOn' % prefix: colID,
                     '%s-sortOrder' % prefix: sortOrder})
        queryString = '?%s' % (urllib.urlencode(args))

        #CSS
        if table.getSortOn() == self.column.id:
            cssClass = u' class="active %s"' % sortOrder
        else:
            cssClass = u""

        return '<a href="%s" title="%s"%s>%s</a>' % (
            queryString,
            zope.i18n.translate(_('Sort'), context=self.request),
            cssClass,
            zope.i18n.translate(self.column.header, context=self.request))
