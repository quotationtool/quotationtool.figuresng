import zope.interface
import zope.component
from z3c.table import table, column
from z3c.table.interfaces import ITable
from z3c.pagelet.browser import BrowserPagelet
from zope.contentprovider.interfaces import IContentProvider

from quotationtool.bibliography.interfaces import IBibliographyCatalog

from quotationtool.figuresng.interfaces import _
from quotationtool.figuresng.iexample import IExample


class IAuthorTitleExampleTable(ITable):
    """ A table for example objects with columns for author and
    title."""


class IExamplesFromReferenceTable(ITable):
    """ A table of example objects all taken from the same reference
    (or somehow else it is clear who the author, title etc. is). """


class ExampleContainerTable(table.Table, BrowserPagelet):
    """ A table with all examples in the example container."""

    zope.interface.implements(IAuthorTitleExampleTable)

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u'head',
        }

    cssClassEven = u'even'
    cssClassOdd = u'odd'


class ExamplesInReferenceTable(table.SequenceTable, BrowserPagelet):
    """ A table with all examples from a certain reference."""

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u'head',
        }

    cssClassEven = u'even'
    cssClassOdd = u'odd'


class QuidColumn(column.LinkColumn):
    """ The quid attribute of an example object."""

    header = IExample['quid'].title
    weight = 10

    def getLinkContent(self, item):
        return getattr(item, 'quid', u"")


class ProQuoColumn(column.GetAttrColumn):
    """ The pro_quo attribute of an example object."""

    header = IExample['pro_quo'].title
    attrName = 'pro_quo'
    weight = 20


class MarkerColumn(column.GetAttrColumn):
    """ The pro_quo attribute of an example object."""

    header = IExample['marker'].title
    attrName = 'marker'
    weight = 30


class YearColumn(column.Column):
    """ The year attribute of a bibliographic entry."""

    header = IBibliographyCatalog['year'].title
    weight = 105

    def renderCell(self, item):
        view = zope.component.getMultiAdapter(
            (item.reference, self.request),
            name='year')
        return view()


class AuthorColumn(column.Column):
    """ The year attribute of a bibliographic entry."""

    header = IBibliographyCatalog['author'].title
    weight = 110

    def renderCell(self, item):
        view = zope.component.getMultiAdapter(
            (item.reference, self.request),
            name='author')
        return view()


class TitleColumn(column.Column):
    """ The year attribute of a bibliographic entry."""

    header = IBibliographyCatalog['title'].title
    weight = 120

    def renderCell(self, item):
        view = zope.component.getMultiAdapter(
            (item.reference, self.request),
            name='title')
        return view()
    

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
