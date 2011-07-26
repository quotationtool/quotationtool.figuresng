import zope.interface
import zope.component
from z3c.indexer.interfaces import IIndex, IValueIndexer
from z3c.indexer.indexer import MultiIndexer, ValueIndexer
from z3c.indexer.index import TextIndex, FieldIndex

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent

from quotationtool.figuresng.interfaces import IExample


def extractMarkup(example, cssClass=u""):
    #TODO
    return u""


class ExampleIndexer(MultiIndexer):

    zope.component.adapts(IExample)
    
    def _quid(self):
        rc = getattr(self.context, 'quid', u"")
        rc += u" "
        rc += extractMarkup(self.context, cssClass='quotationtool-example-quid')
        return rc

    def _proquo(self):
        rc = getattr(self.context, 'pro_quo', u"")
        rc += u" "
        rc += extractMarkup(self.context, cssClass='quotationtool-example-proquo')
        return rc

    def _marker(self):
        rc = getattr(self.context, 'marker', u"")
        rc += u" "
        rc += extractMarkup(self.context, cssClass='quotationtool-example-marker')
        return rc

    def doIndex(self):

        quid_fulltext = self.getIndex('quid-fulltext')
        quid_fulltext.doIndex(self.oid, self._quid())

        quid_field = self.getIndex('quid-field')
        quid_field.doIndex(self.oid, self._quid())

        proquo_fulltext = self.getIndex('proquo-fulltext')
        proquo_fulltext.doIndex(self.oid, self._proquo())

        proquo_field = self.getIndex('proquo-field')
        proquo_field.doIndex(self.oid, self._proquo())

        marker_fulltext = self.getIndex('marker-fulltext')
        marker_fulltext.doIndex(self.oid, self._marker())

        marker_field = self.getIndex('marker-field')
        marker_field.doIndex(self.oid, self._marker())

    def doUnIndex(self):
        
        quid_fulltext = self.getIndex('quid-fulltext')
        quid_fulltext.doUnIndex(self.oid)

        quid_field = self.getIndex('quid-field')
        quid_field.doUnIndex(self.oid)

        proquo_fulltext = self.getIndex('proquo-fulltext')
        proquo_fulltext.doUnIndex(self.oid)

        proquo_field = self.getIndex('proquo-field')
        proquo_field.doUnIndex(self.oid)

        marker_fulltext = self.getIndex('marker-fulltext')
        marker_fulltext.doUnIndex(self.oid)

        marker_field = self.getIndex('marker-field')
        marker_field.doUnIndex(self.oid)


class AnyValueIndexer(ValueIndexer):

    indexName = 'any-fulltext'
    
    @property
    def value(self):
        rc = u""
        for attr in ('quid', 'pro_quo', 'quotation', 'page', 'volume', 'position'):
            rc += getattr(self.context, attr, u"") + u" "
        reference_indexer = zope.component.queryAdapter(
            self.context.reference,
            IValueIndexer, name='any-fulltext')
        if reference_indexer is not None:
            rc += reference_indexer.value + u" "
        return rc


class TypeValueIndexer(ValueIndexer):

    indexName = 'type-field'

    @property
    def value(self):
        return u'quotationtool.figuresng.interfaces.IExample'


def createExampleIndices(site):
    """create indexes on the site's site-manager."""

    sm = site.getSiteManager()
    default = sm['default']

    quid_fulltext = default['quid-fulltext'] = TextIndex()
    sm.registerUtility(quid_fulltext, IIndex, name='quid-fulltext')

    quid_field = default['quid-field'] = FieldIndex()
    sm.registerUtility(quid_field, IIndex, name='quid-field')

    proquo_fulltext = default['proquo-fulltext'] = TextIndex()
    sm.registerUtility(proquo_fulltext, IIndex, name='proquo-fulltext')

    proquo_field = default['proquo-field'] = FieldIndex()
    sm.registerUtility(proquo_field, IIndex, name='proquo-field')

    marker_fulltext = default['marker-fulltext'] = TextIndex()
    sm.registerUtility(marker_fulltext, IIndex, name='marker-fulltext')

    marker_field = default['marker-field'] = FieldIndex()
    sm.registerUtility(marker_field, IIndex, name='marker-field')



@zope.component.adapter(INewQuotationtoolSiteEvent)
def createExampleIndicesSubscriber(event):
    """Create example indices when a new quotationtool site is
    created.
    """

    createExampleIndices(event.object)

