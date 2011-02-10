from zope.interface import Interface, Attribute
from zope.container.interfaces import IContained, IContainer
from zope.container.constraints import containers, contains
from zope.schema import Text, TextLine, List, Int, Choice, Object
from zope.i18nmessageid import MessageFactory

from quotationtool.relation.schema import Relation
from quotationtool.bibliography.interfaces import IEntry


_ = MessageFactory('quotationtool')


class IFigure(Interface):
    """A base interface for more specific figure objects.

        >>> from quotationtool.figuresng.interfaces import IFigure
        >>> import zope.interface
        >>> IFigure.names()
        ['reference', 'source_type', 'length', 'position', 'quotation']

        >>> import zope.schema
        >>> zope.schema.getFields(IFigure).keys()
        ['source_type', 'length', 'position', 'reference', 'quotation']
        

        >>> bad = object()
        >>> IFigure['reference'].validate(bad)
        Traceback (most recent call last):
        ...
        RelationPreconditionError

        >>> from quotationtool.bibliography.interfaces import IEntry
        >>> class Book(object):
        ...     pass
        >>> zope.interface.classImplements(Book, IEntry)

        >>> somebook = Book()
        >>> IFigure['reference'].validate(somebook)


        >>> IFigure['quotation'].validate(u"She feels like a shark, slimy and abrasive.")
        >>> IFigure['position'].validate(u"42")
        >>> IFigure['source_type'].validate('plaintext')
        >>> IFigure['source_type'].validate(IFigure['source_type'].default)
    """

    reference = Relation(
        title = _('ifigure-reference-title',
                  u"Cited from"),
        description = _('ifigure-reference-desc',
                        u"The publication (book, article etc.) the text is taken from"),
        required = True,
        precondition = [IEntry],
        )

    quotation = Text(
        title = _('ifigure-quotation-title',
                  u"Quotation"),
        description = _('ifigure-quotation-desc',
                        u"Passage in the text; without quotationmarks."),
        required = True,
        )

    length = Int(
        title = _('ifigure-length-title',
                  u"Lenght"),
        description = _('ifigure-length-desc',
                        u"Length in bytes of the quotation attribute. Calculated automatically when quotation is set."),
        required = True,
        )

    source_type = Choice(
        title = _('ifigure-source-type-title', u"Text Format"),
        description = _('ifigure-source-type-desc',
                        u"Choose text format"),
        required = True,
        default = 'plaintext',
        vocabulary = 'quotationtool.figuresng.SourceTypes',
        )

    position = TextLine(
        title = _('ifigure-position-title',
                  u"Page"),
        description = _('ifigure-position-desc',
                        u"Without ''p.''; date for newspaper articles."),
        required = True,
        )


class IQuotationSourceFactory(Interface):
    """A source format for a quotation text (attribute 'quotation' of
    ISimpleComment objects)."""



class IFigureIndexCatalog(Interface):
    """A catalog of indices for searching figures."""

    quotation = TextLine(
        title = _('ifigureindexcatalog-quotation-title', u"Quotation"),
        description = _('ifigureindexcatalog-quotation-desc',
                        u"Search by words from the quotation field."),
        required = True,
        )

    any = TextLine(
        title = _('catalog-any-title',
                  u"Any field / free"),
        description = _('catalog-any-desc',
                        u"Free text."),
        required = False,
        default = u'',
        )
