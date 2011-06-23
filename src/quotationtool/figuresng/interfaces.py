import zope.interface
from zope.container.interfaces import IContained, IContainer
from zope.container.constraints import containers, contains
from zope.schema import TextLine
import re
from zope.i18nmessageid import MessageFactory

from quotationtool.quotation.interfaces import IQuotation
from quotationtool.quotation.interfaces import IQuotationContainer

_ = MessageFactory('quotationtool')

quid_html_tag = re.compile('<span class=(\"|\')quotationtool-example-quid(\"|\')>.*</span>')
proquo_html_tag = re.compile('<span class=(\"|\')quotationtool-example-proquo(\"|\')>.*</span>')


class IExampleContainer(IQuotationContainer):
    """The schema part of an example container interface."""


class IExampleContainerContainer(IContainer):
    """The container interface part of an example container interface."""

    contains('.IExample')


class IExample(IQuotation, IContained):
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
    def assertQuidProQuo(example):
        if not (example.quid or example.pro_quo):
            raise zope.interface.Invalid(
                _('neitherquidnorproquo',
                  u"Either 'Example' or 'Denotation/Meaning' must be given!")
                ) 

    @zope.interface.invariant
    def assertTagsInHTMLQuotation(example):
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


#BBB
class IFigure(IQuotation):
    pass
