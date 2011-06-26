import zope.interface
from z3c.searcher.interfaces import ISearchFilter
from z3c.searcher.criterium import TextCriterium, SearchCriterium
from z3c.searcher.criterium import factory
from z3c.searcher.filter import EmptyTerm, SearchFilter

from quotationtool.search.interfaces import ITypeExtent
from quotationtool.quotation.searcher import IQuotationSearchFilter

from quotationtool.figuresng.interfaces import _


class IExampleSearchFilter(ISearchFilter):
    """ Search filter for example objects."""


class ExampleSearchFilter(SearchFilter):
    """ Example search filter."""

    zope.interface.implements(IQuotationSearchFilter,
                              IExampleSearchFilter,
                              ITypeExtent)

    def getDefaultQuery(self):
        return EmptyTerm()

    def delimit(self):
        """ See ITypeExtent"""
        crit = self.createCriterium('type-field')
        crit.value = u'quotationtool.figuresng.interfaces.IExample'
        crit.connectorName='AND'
        self.addCriterium(crit)


class QuidTextCriterium(TextCriterium):
    """ Full text criterium for 'quid-fulltext' index."""

    indexOrName = 'quid-fulltext'
    
    label = _('quid-fulltext-label', u"Example")

quid_fulltext_factory = factory(QuidTextCriterium, 'quid-fulltext')


class ProquoTextCriterium(TextCriterium):
    """ Full text criterium for 'proquo-fulltext' index."""

    indexOrName = 'proquo-fulltext'
    
    label = _('proquo-fulltext-label', u"Denotation / Meaning")

proquo_fulltext_factory = factory(ProquoTextCriterium, 'proquo-fulltext')


class MarkerTextCriterium(TextCriterium):
    """ Full text criterium for 'marker-fulltext' index."""

    indexOrName = 'marker-fulltext'
    
    label = _('marker-fulltext-label', u"Marker")

marker_fulltext_factory = factory(MarkerTextCriterium, 'marker-fulltext')
