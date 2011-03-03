import zope.interface
from zope.container.interfaces import IContained, IContainer
from zope.container.constraints import containers, contains
from zope.schema import TextLine
import re

from i18n import _
from interfaces import IFigure, IFigureIndexCatalog

quid_html_tag = re.compile('<span class=(\"|\')quotationtool-example-quid(\"|\')>.*</span>')
proquo_html_tag = re.compile('<span class=(\"|\')quotationtool-example-proquo(\"|\')>.*</span>')


class IExampleContainer(zope.interface.Interface):
    """The schema part of an example container interface."""

    _count = zope.schema.Int(
        title = _('iexampelcontainer-count-title',
                  u"Count"),
        description = _('iexamplecontainer-count-desc',
                        u"How many examples there are"),
        required = True,
        default = 0,
        )


class IExampleContainerContainer(IContainer):
    """The container interface part of an example container interface."""

    contains('.IExample')


class IExample(IFigure, IContained):
    """An example"""

    containers(IExampleContainerContainer)

    quid = TextLine(
        title = _('iexample-quid-title',
                  u"Example"),
        description = _('iexample-quid-desc',
                        u"What is given as example?"),
        required = True,
        default = u'',
        missing_value = u'',
        )

    pro_quo = TextLine(
        title = _('iexample-proquo-title',
                  u"Denotation/Meaning"),
        description = _('iexample-proquo-desc',
                        u"What is the example associated with? What does it stand for?"),
        required = True,
        default = u'',
        missing_value = u'',
        )

    marker = TextLine(
        title = _('iexample-marker-title',
                  u"Marker"),
        description = _('iexample-marker-desc',
                        u"How is the example indicated? ('e.g.', 'for instance', paranthesis etc.)"),
        required = False,
        default = u'',
        missing_value = u'',
        )

    @zope.interface.invariant
    def checkQuidProQuo(example):
        if not (example.quid or example.pro_quo):
            raise zope.interface.Invalid(
                _('netherquidnorproquo',
                  u"Ether 'Example' or 'Denotation/Meaning' must be given!")
                ) 

    @zope.interface.invariant
    def checkTagsInHTMLQuotation(example):
        if example.source_type != 'html':
            return
        has_quid = has_proquo = False
        if quid_html_tag.search(example.quotation):
            has_quid = True
        if proquo_html_tag.search(example.quotation):
            has_proquo = True
        if not (has_quid or has_proquo):
            raise zope.interface.Invalid(
                _('nether-quid-nor-proquo-tag',
                  u"Missing tags for 'Example' and for 'Denotation/Meaning' in the quotation"))
        if not has_quid:
            raise zope.interface.Invalid(
                _('no-quid-tag',
                  u"Missing 'Example' tag in the quotation"))
        if not has_proquo:
            raise zope.interface.Invalid(
                _('no-proquo-tag',
                  u"Missing 'Denotation/Meaning' tag in the quotation"))


class IExampleIndexCatalog(IFigureIndexCatalog):
    """A collection of indexes for example search and destroy missions... """

    quid = TextLine(
        title = _('iexampleindexcatalog-quid-title',
                  u"Example"),
        description = _('iexampleindexcatalog-quid-desc',
                        u"Search by example."),
        required = False,
        default = u'',
        )

    pro_quo = TextLine(
        title = _('iexampleindexcatalog-proquo-title',
                  u"Denotation/Meaning"),
        description = _('iexampleindexcatalog-proquo-desc',
                        u"Search by the denotation or meaning (general sentence or rule) illustrated by the example."),
        required = False,
        default = u'',
        )

    quid_pro_quo = TextLine(
        title = _('iexampleindexcatalog-quidproquo-title',
                  u"Example OR Denotation/Meaning"),
        description = _('iexampleindexcatalog-quidproquo-desc',
                        u"Search by example OR denotation/meaning. Matches both fields."),
        required = False,
        default = u'',
        )

    marker = TextLine(
        title = _('iexampleindexcatalog-marker-title',
                  u"Marker"),
        description = _('iexampleindexcatalog-marker-desc',
                        u"Search by example-marker."),
        required = False,
        default = u'',
        )
