Examples
========

(Note that we have registered some utilities in test setup so that we
can use the vocabulary for the source_type field of an example
object.)

The example class is destined to store the rhetorical figure of
example.

Let's first examine the schema:

    >>> from quotationtool.figuresng.iexample import IExample
    >>> IExample.names()
    ['pro_quo', 'quid', 'marker', '__parent__']

    >>> import zope.schema
    >>> zope.schema.getFields(IExample).keys()
    ['reference', 'quid', 'pro_quo', 'source_type', 'length', 'position', 'marker', '__name__', '__parent__', 'quotation']


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
    InvalidItemType: (<quotationtool.figuresng.examplecontainer.ExampleContainer object at ...>, <object object at ...>, [<InterfaceClass quotationtool.figuresng.iexample.IExample>])

    >>> checkObject(bad, 'tulip', tulip)
    Traceback (most recent call last):
    ...
    InvalidContainerType: (<object object at ...>, (<InterfaceClass quotationtool.figuresng.iexample.IExampleContainerContainer>,))

    >>> checkObject(examples, 'tulip', tulip)


Now let's check the schema of example objects. The reference attribute
asserts the precondition of IEntry objects. That means, that an
object must implement IEntry. (See
quotationtool.relation.schema.Relation.)


    >>> tulip.reference = bad
    Traceback (most recent call last):
    ...
    RelationPreconditionError


    >>> from quotationtool.bibliography.interfaces import IEntry
    >>> from zope.interface import implements
    >>> class Reference(object):
    ...     implements(IEntry)

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

    >>> c[u'1'] = tulip
    Traceback (most recent call last):
    ...
    UserError: You want to use ... as key for the example, but it should be ...!

There is also a name chooser.


Indexing
--------

In order to get the values out of an example object an its reference we
make use of adapters. There are allready some there, which we only
need to register:

    >>> from quotationtool.figuresng.exampleindexing import ReferenceIndexer

Then we need an adapter that adapts IEntry objects to
IBibliographyCatalog. We have to implement and register this adapter
for each type of reference i.e. classes marked with or implementing
the IEntry interface. Otherwise we get a component lookup error:

    >>> from quotationtool.bibliography.interfaces import IBibliographyCatalog, IEntry
    >>> zope.component.provideAdapter(ReferenceIndexer)
    >>> IBibliographyCatalog(tulip)
    Traceback (most recent call last):
    ...
    TypeError: ('Could not adapt', <Reference object at ...>, <InterfaceClass quotationtool.bibliography.interfaces.IBibliographyCatalog>)

    >>> from zope.interface import implements
    >>> from zope.component import adapts
    >>> class DummyReferenceIndexer(object):
    ...     implements(IBibliographyCatalog)
    ...     adapts(IEntry)
    ...	    def __init__(self, context):
    ...         self.context = context
    ...     def __getattr__(self, name):
    ...	        return getattr(self.context, name, u'no real value')
    >>> zope.component.provideAdapter(DummyReferenceIndexer)
    >>> isinstance(IBibliographyCatalog(kant_kdu), DummyReferenceIndexer)
    True

Now we can adapt example objects to IBibliographyCatalog:

    >>> IBibliographyCatalog(tulip)
    <quotationtool.figuresng.exampleindexing.ReferenceIndexer object at 0x...>


There is an adapter in exampleindexing.py which adapts IExample
objects to example catalog indices.
    
    >>> from quotationtool.figuresng.iexample import IExampleIndexCatalog
    >>> from quotationtool.figuresng.exampleindexing import ExampleIndexer
    >>> import zope.component
    >>> list(zope.component.adaptedBy(ExampleIndexer)) == [IExample]
    True

    >>> zope.component.provideAdapter(ExampleIndexer,
    ...     provides = IExampleIndexCatalog)

    >>> indexer = IExampleIndexCatalog(tulip)
    >>> indexer.quotation
    u'Eine Blume aber, zum Beispiel eine Tulpe, wird usw.'

    >>> indexer.quid
    u'Tulpe'

    >>> indexer.pro_quo
    u'Blume, gewisse Zweckmaessigkeit usw.'

    >>> indexer.quid_pro_quo
    u'Tulpe Blume, gewisse Zweckmaessigkeit usw.'

    >>> indexer.marker
    u'zum Beispiel'

    >>> from quotationtool.figuresng.exampleindexing import ReferenceIndexer
    >>> list(zope.component.adaptedBy(ReferenceIndexer)) == [IExample]
    True

    >>> zope.component.provideAdapter(ReferenceIndexer)
    >>> from quotationtool.bibliography.interfaces import IBibliographyCatalog

    >>> IEntry.providedBy(tulip.reference)
    True
    
Create the catalog:

    >>> from quotationtool.figuresng.exampleindexing import createExampleIndices, filter
    >>> from quotationtool.bibliography.indexing import createBibliographyCatalogIndices
    >>> from zc.catalog.extentcatalog import FilterExtent, Catalog
    >>> extent = FilterExtent(filter)
    >>> cat = Catalog(extent)
    >>> createExampleIndices(cat)
    >>> createBibliographyCatalogIndices(cat)
    >>> list(cat.keys())
    [u'ante', u'author', u'language', u'marker', u'post', u'pro_quo', u'quid', u'quid_pro_quo', u'quotation', u'title', u'year']

    >>> cat.index_doc(1, tulip)
    >>> list(cat.apply({'quotation': u"Tulpe"}))
    [1]

    >>> list(cat.apply({'quid_pro_quo': u"Blume"}))
    [1]

    >>> list(cat.apply({'pro_quo': u"Blume"}))
    [1]

    >>> list(cat.apply({'quid': u"Blume"}))
    []

    >>> list(cat.apply({'quid': u"tulpe"}))
    [1]

    >>> list(cat.apply({'marker': u"Beispiel"}))
    [1]

    >>> len(extent) == 1
    True

    >>> list(cat.apply({'author': u"kant"}))
    []

    >>> kant_kdu.author = u"Kant, Immanuel"
    >>> list(cat.apply({'author': u"kant"}))
    []

    >>> tulip.reference.author
    u'Kant, Immanuel'

    >>> IBibliographyCatalog(tulip).author
    u'Kant, Immanuel'

    >>> cat.index_doc(1, tulip)
    >>> list(cat.apply({'author': u"kant"}))
    [1]


Further
-------

It is required for indexing relations that an example object is
adaptable (implements) both, IFigure and IExample

    >>> IExample(tulip).reference == kant_kdu
    True

    >>> from quotationtool.figuresng.interfaces import IFigure
    >>> IFigure(tulip).reference == kant_kdu
    True
