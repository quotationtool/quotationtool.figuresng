import zope.interface
import zope.component
from z3c.searcher.interfaces import ISearchFilter, CONNECTOR_OR, CONNECTOR_AND
from z3c.searcher.criterium import TextCriterium, SearchCriterium
from z3c.searcher.criterium import factory
from z3c.searcher.filter import EmptyTerm, SearchFilter
from zope.traversing.browser import absoluteURL

from quotationtool.search.interfaces import IQuotationtoolSearchFilter
from quotationtool.search.interfaces import ITypeExtent, ICriteriaChainSpecifier, IResultSpecifier
from quotationtool.search.interfaces import ICriteriumDescription
from quotationtool.quotation.interfaces import IQuotationSearchFilter

from quotationtool.figuresng.interfaces import _, IExampleSearchFilter, IExampleContainer


class ExampleSearchFilter(SearchFilter):
    """ Example search filter."""

    zope.interface.implements(IQuotationtoolSearchFilter,
                              IQuotationSearchFilter,
                              IExampleSearchFilter,
                              ITypeExtent,
                              ICriteriaChainSpecifier,
                              IResultSpecifier)

    def getDefaultQuery(self):
        return EmptyTerm()

    def delimit(self):
        """ See ITypeExtent"""
        crit = self.createCriterium('type-field')
        crit.value = u'quotationtool.figuresng.interfaces.IExample'
        crit.connectorName = CONNECTOR_AND
        self.addCriterium(crit)

    first_criterium_connector_name = CONNECTOR_OR

    ignore_empty_criteria = True

    def resultURL(self, context, request):
        examples = zope.component.getUtility(
            IExampleContainer,
            context=context)
        return absoluteURL(examples, request) + u"/@@searchResult.html"

    session_name = 'examples'


example_search_filter_factory = zope.component.factory.Factory(
    ExampleSearchFilter,
    _('ExampleSearchFilter-title', u"Examples"),
    _('ExampleSearchFilter-desc', u"Search for examples.")
    )


class QuidTextCriterium(TextCriterium):
    """ Full text criterium for 'quid-fulltext' index."""

    zope.interface.implements(ICriteriumDescription)

    indexOrName = 'quid-fulltext'
    
    label = _('quid-fulltext-label', u"Example")

    description = _('quid-fulltext-desc', u"Matches in example field.")

    ui_weight = 15

quid_fulltext_factory = factory(QuidTextCriterium, 'quid-fulltext')


class ProquoTextCriterium(TextCriterium):
    """ Full text criterium for 'proquo-fulltext' index."""

    zope.interface.implements(ICriteriumDescription)

    indexOrName = 'proquo-fulltext'
    
    label = _('proquo-fulltext-label', u"Denotation / Meaning")

    description = _('proquo-fulltext-desc', u"Matches in denotation or meaning field.")

    ui_weight = 20

proquo_fulltext_factory = factory(ProquoTextCriterium, 'proquo-fulltext')


class MarkerTextCriterium(TextCriterium):
    """ Full text criterium for 'marker-fulltext' index."""

    zope.interface.implements(ICriteriumDescription)

    indexOrName = 'marker-fulltext'
    
    label = _('marker-fulltext-label', u"Marker")

    description = _('marker-fulltext-desc', u"Matches in marker field.")

    ui_weight = 30

marker_fulltext_factory = factory(MarkerTextCriterium, 'marker-fulltext')
