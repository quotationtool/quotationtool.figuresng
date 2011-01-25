from zope.interface import Interface, Attribute
from zope.container.interfaces import IContained, IContainer
from zope.container.constraints import containers, contains
from zope.schema import Text, TextLine, List, Int, Choice, Object

from i18n import _
from quotationtool.relation.schema import Relation


class IReference(Interface):
    """A marker interface for objects that can be referenced by
    IFigure objects.""" 


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

        >>> from quotationtool.figuresng.interfaces import IReference
        >>> class Book(object):
        ...     pass
        >>> zope.interface.classImplements(Book, IReference)

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
        precondition = [IReference],
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


class IReferenceIndexCatalog(Interface):
    """A catalog of indexes that we want to search for in the
    referatory."""

    author = TextLine(
        title = _('ireferenceindexcatalog-author-title',
                  u"Author / Uniform Author"),
        description = _('ireferenceindexcatalog-author-desc',
                        u"Search by author. Even matches the author-field of the uniform title."),
        required = False,
        default = u'',
        )

    title = TextLine(
        title = _('ireferenceindexcatalog-title-title',
                  u"Title / Uniform Title"),
        description = _('ireferenceindexercatalog-title-desc',
                        u"Search by title or uniform title."
                        ),
        required = False,
        default = u'',
        )

    post = Int(
        title = _('ireferenceindexcatalog-post-title',
                  u"Published/Written After"),
        description = _('ireferenceindexcatalog-post-desc',
                  u"Matches, if published after."),
        required = False,
        )

    ante = Int(
        title = _('ireferenceindexcatalog-ante-title',
                  u"Published/Writter Before"),
        description = _('ireferenceindexcatalog-ante-desc',
                  u"Matsches, if published before."),
        required = False,
        )

    year = Int(
        title = _('ireferenceindexcatalog-year-title',
                  u"Year first published"),
        description = _('ireferenceindexcatalog-year-desc',
                  u"Matches the exact year of origin."),
        required = False,
        )

    language = TextLine(
        title = _('ireferenceindexcatalog-language-title',
                  u"Language / Original Language"),
        description = _('ireferenceindexcatalog-language-desc',
                  u"Search for items by language."),
        required = False,
        default = u'',
        )

    edition_year = TextLine(
        title = _('irefenceindexer-editionyear-title',
                  u"Year of edition"),
        description = _('ireferenceindexcatalog-edtionyear-desc',
                  u"Matches the year of the edition."),
        required = True,
        )

    editor = TextLine(
        title = _('ireferenceindexcatalog-editor-title',
                  u"Editor"),
        description = _('ireferenceindexcatalog-editor-desc',
                  u"Search by editor."),
        required = False,
        default = u'',
        )

    publisher = TextLine(
        title = _('ireferenceindexcatalog-publisher-title',
                  u"Publisher"),
        description = _('ireferenceindexcatalog-publisher-desc',
                  u"Search by publisher."),
        required = False,
        default = u'',
        )

    location = TextLine(
        title = _('ireferenceindexcatalog-location-title',
                  u"Location"),
        description = _('ireferenceindexcatalog-location-desc',
                  u"Search by place of publication."),
        required = False,
        default = u'',
        )
