import zope.interface
from zope.container.interfaces import IContained, IContainer
from zope.container.constraints import containers, contains
from zope.schema import TextLine

from i18n import _
from interfaces import IFigure, IFigureIndexCatalog


class IExampleContainer(zope.interface.Interface):
    """The schema part of an example container interface."""

    count = zope.schema.Int(
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
        required = False,
        default = u'',
        missing_value = u'',
        )

    pro_quo = TextLine(
        title = _('iexample-proquo-title',
                  u"Denotation/Meaning"),
        description = _('iexample-proquo-desc',
                        u"What is the example associated with? What does it stand for?"),
        required = False,
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
                  u"Rule"),
        description = _('iexampleindexcatalog-proquo-desc',
                        u"Search by the rule or general sentence illustrated by the example."),
        required = False,
        default = u'',
        )

    quid_pro_quo = TextLine(
        title = _('iexampleindexcatalog-quidproquo-title',
                  u"Example OR Rule"),
        description = _('iexampleindexcatalog-quidproquo-desc',
                        u"Search by example OR rule. Matches both fields. Even used for the quick search."),
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
