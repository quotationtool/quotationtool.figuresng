Examples
========

(Note that we have registered some utilities in test setup so that we
can use the vocabulary for the source_type field of an example
object.)

The example class is destined to store the rhetorical figure of
example.

Let's first examine the schema:

    >>> from quotationtool.figuresng.interfaces import IExample
    >>> IExample.names()
    ['pro_quo', 'quid', 'marker', '__parent__']

    >>> import zope.schema
    >>> zope.schema.getFields(IExample).keys()
    ['reference', 'quid', 'pro_quo', 'volume', 'source_type', 'length', 'position', 'marker', '__name__', 'page', '__parent__', 'quotation']


    >>> from quotationtool.figuresng.example import Example
    >>> tulip = Example()


There are constraints regarding containment. Example objects live in
IExampleContainerContainer objects only, and
IExamplecontainerContainer objects hold Example objects only:

    >>> from quotationtool.figuresng.examplecontainer import ExampleContainer
    >>> from zope.container.constraints import checkObject
    >>> examples = ExampleContainer()
    >>> bad = object()
    >>> checkObject(examples, 'bad', bad)
    Traceback (most recent call last):
    ...
    InvalidItemType: (<quotationtool.figuresng.examplecontainer.ExampleContainer object at ...>, <object object at ...>, [<InterfaceClass quotationtool.figuresng.interfaces.IExample>])

    >>> checkObject(bad, 'tulip', tulip)
    Traceback (most recent call last):
    ...
    InvalidContainerType: (<object object at ...>, (<InterfaceClass quotationtool.figuresng.interfaces.IExampleContainerContainer>,))

    >>> checkObject(examples, 'tulip', tulip)


Now let's check the schema of example objects. The reference attribute
asserts the precondition of IEntry objects. That means, that an
object must implement IEntry. (See
quotationtool.relation.schema.Relation.)


    >>> tulip.reference = bad
    Traceback (most recent call last):
    ...
    RelationPreconditionError


    >>> from quotationtool.quotation.interfaces import IReference
    >>> from zope.interface import implements
    >>> class Reference(object):
    ...     implements(IReference)

    >>> kant_kdu = Reference()
    >>> tulip.reference = kant_kdu


Setting the quotation attribute sets the lenght attribute
automaticly. This is for performance reasons, since that way we have
to calculate the length only once. It is calculated at write time,
but not at read time any more.

    >>> quote = u"Eine Blume aber, zum Beispiel eine Tulpe, wird usw."
    >>> tulip.quotation = quote
    >>> tulip.length == len(quote)
    True

    >>> tulip.position = 123
    Traceback (most recent call last):
    ...
    WrongType: (123, <type 'unicode'>, 'position')

    >>> tulip.source_type = 'plaintext'
    >>> tulip.position = u"123"
    >>> tulip.quid = u"Tulpe"
    >>> tulip.pro_quo = u"Blume, gewisse Zweckmaessigkeit usw."
    >>> tulip.marker = u"zum Beispiel"


Container for Examples
----------------------

    >>> from quotationtool.figuresng.examplecontainer import ExampleContainer
    >>> c = ExampleContainer()
    >>> c._count
    0
    
    >>> c[unicode(c._count+1)] = tulip
    >>> c._count
    1

There is also a name chooser.


Indexing
--------
