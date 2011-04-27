import zope.interface
import zope.component
from z3c.form import field
from z3c.formui import form
import z3c.form.interfaces
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import absoluteURL
from z3c.pagelet.browser import BrowserPagelet
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.browser import BrowserView
from zope.proxy import removeAllProxies
import zc.relation
from zope.viewlet import viewlet
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.viewlet.viewlet import ViewletBase
import zc.resourcelibrary
from zope.schema import getValidationErrors

from quotationtool.renderer.interfaces import IHTMLRenderer 
from quotationtool.skin.interfaces import ITabbedContentLayout

from quotationtool.figuresng import iexample
from quotationtool.figuresng.example import Example
from quotationtool.figuresng.i18n import _


class RenderQuotation(object):
    """A mixin class that provides a method for rendering the
    quotation text."""

    limit = None
    
    def renderQuotation(self):
        source = zope.component.createObject(
            self.context.source_type,
            self.context.quotation)
        renderer = zope.component.getMultiAdapter(
            (removeAllProxies(source), self.request),
            IHTMLRenderer, name = u'')
        return renderer.render(limit = self.limit)


class DetailsView(BrowserView, RenderQuotation):
    """The @@details view which can be called from within a zpt.
    """

    template = ViewPageTemplateFile('example_@@details.pt')

    def __call__(self):
        return self.template()


class ListView(BrowserView, RenderQuotation):
    """The @@list view which can be called from within a zpt."""

    limit = 200

    # TODO
    template = ViewPageTemplateFile('example_@@details.pt')

    def __call__(self):
        return self.template()


class SchemaErrorFlag(ViewletBase):
    """ Put flag on invalid examples."""

    def render(self):
        if getValidationErrors(iexample.IExample, self.context):
            return u'<abbr title="Schema validation error" class="error schema-validation-error">S</abbr>'
        else:
            return u''


class LabelView(BrowserView):
    """A view that informs about the object type."""

    def __call__(self):
        return _('example-labelview', u"Example #$ID", 
                 mapping = {'ID': self.context.__name__})


class AddExampleInReferenceContext(form.AddForm):
    """A form for adding a quotation object to the collectanea that
    takes a reference object as context."""

    zope.interface.implements(ITabbedContentLayout)

    label = _('add-example', u"Add a new Example")

    info = _('add-example-info', 
             u"The <span class=\"quotationtool-example-quid\">example</span> and its <span class=\"quotationtool-example-proquo\">denotation/meaning</span> have to be tagged in the quotation using the flags. If a marker is present, please tag the <span class=\"quotationtool-example-marker\">marker</span>, too.<br/>Then fill in the example, the denotation/meaning and--if present--the marker fields. The denotation/meaning field should not be used for repeating theorems most accurately, but for the term that is in question. The same with the example field. The input data should serve searching the database but not hermeneutics. If you would like to give more accurate information then please write a comment after submitting the form."
             )
    
    fields = field.Fields(iexample.IExample).omit(
        '__parent__', '__name__', 'reference', 'length')#, 'source_type')

    def __init__(self, context, request):
        super(AddExampleInReferenceContext, self).__init__(context, request)
        zc.resourcelibrary.need('quotationtool.tinymce.QuotationAndExample')

    def updateWidgets(self):
        super(AddExampleInReferenceContext, self).updateWidgets()
        self.widgets['source_type'].value = ('html',)
        self.widgets['source_type'].mode = HIDDEN_MODE # TODO: make more secure!

    def create(self, data):
        example = Example()
        form.applyChanges(self, example, data)
        example.source_type = 'html'
        
        # We want an object which is not security proxied as reference
        # attribute:
        #referatory = zope.component.getUtility(
        #    IReferatory, context = self.context)
        #reference = referatory.get(self.context.__name__)
        example.reference = removeAllProxies(self.context)

        # Grant the current user the Edit permission by assigning him
        # the quotationtool.Creator role, but only locally in the
        # context of the newly created object.
        manager = IPrincipalRoleManager(example)
        manager.assignRoleToPrincipal(
            'quotationtool.Creator',
            self.request.principal.id)

        return example

    def add(self, example):
        container = zope.component.getUtility(
            iexample.IExampleContainer, context = self.context)
        name = INameChooser(container).chooseName(example, None)
        self._obj = container[name] = example

    def nextURL(self):
        return absoluteURL(self._obj, self.request)


class ExampleEditForm(form.EditForm, RenderQuotation):
    """A form to edit the quotation."""

    zope.interface.implements(ITabbedContentLayout)

    info = AddExampleInReferenceContext.info

    fields = field.Fields(iexample.IExample).omit(
        '__parent__', '__name__', 'reference', 'length')

    def __init__(self, context, request):
        super(ExampleEditForm, self).__init__(context, request)
        if context.source_type == 'html':
            zc.resourcelibrary.need('quotationtool.tinymce.QuotationAndExample')

    def updateWidgets(self):
        super(ExampleEditForm, self).updateWidgets()
        self.widgets['source_type'].mode = DISPLAY_MODE


class ExampleFrontpage(form.DisplayForm, RenderQuotation):
    """The frontpage for quotation objects."""

    zope.interface.implements(ITabbedContentLayout)

    mode = z3c.form.interfaces.DISPLAY_MODE

    label = _('example-frontpage-label',
              u"Example")

    fields = field.Fields(iexample.IExample).omit(
        '__parent__', '__name__', 'reference', 'length', 'source_type')


class ExampleCountFlag(ViewletBase):

    template = ViewPageTemplateFile('examplecount.pt')

    def count(self):
        """Return the number of examples referencing to context"""
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        examples = list(cat.findRelations(
            cat.tokenizeQuery({'ifigure-reference': self.context})
            ))
        return len(examples)
    
    def render(self):
        return self.template()


class ExamplesInReferenceView(BrowserPagelet, RenderQuotation):
    """A list of the examples in a quotation.

    This view takes a reference object as context."""

    zope.interface.implements(ITabbedContentLayout)

    label1 = _('examples-in-reference-label1',
               u"Examples in Reference")

    def OFFdescription(self):
        return _('examples-in-reference-desc-OFF',
                 u"""This is a list of the examples from the edition
                 above that were collected so far. There might be
                 <a href='${href}' class='content'>more examples in
                 other editions, reprints or translations</a>.""",
                 mapping = {'href': absoluteURL(
            self.context.uniform_title, self.request) + u"/@@examples.html"})

    def description(self):
        return _('examples-in-reference-desc',
                 u"""This is a list of the examples from the edition
                 above that were collected so far.""")

    figurecontainerURL = None

    add_example_option = True

    def __init__(self, context, request):
        # get figurecontainer url only once for performance reasons:
        container = zope.component.getUtility(
            iexample.IExampleContainer, context = context)
        self.figurecontainerURL = absoluteURL(container, request)

        super(ExamplesInReferenceView, self).__init__(context, request)

    def examples(self):
        """Returns a list of examples that are related to the
        quotation object in the context."""
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        return sorted(cat.findRelations(
            cat.tokenizeQuery({'ifigure-reference': self.context})
            ),
                      cmp = lambda x,y: cmp(x.position, y.position))

    limit = 200

    def renderQuotation(self, example):
        source = zope.component.createObject(
            example.source_type,
            example.quotation)
        renderer = zope.component.getMultiAdapter(
            (removeAllProxies(source), self.request),
            IHTMLRenderer, name = u'')
        return renderer.render(limit = self.limit)
        

class ExamplesInUniformTitleView(ExamplesInReferenceView):
    """A list of the examples in a uniform title.

    This view takes a uniform title object as context."""

    zope.interface.implements(ITabbedContentLayout)

    add_example_option = False

    label1 = _('examples-in-uniformtitle-label1',
               u"Examples in Uniform Title")

    def description(self):
        return _('examples-in-uniformtitle-desc',
                 u"""This is a list of the examples from the uniform title above that were
                 collected so far. It is a set union of the examples
                 from all <a href='${href}' class='content'>editions
                 in use</a>.""",
                 mapping = {'href': absoluteURL(
            self.context, self.request) + u"/@@index.html"})
  
    def examples(self):
        """Returns a list of examples that are related to the
        reference object in the context."""
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        return sorted(cat.findRelations(
            {'ifigure-reference': zc.relation.catalog.any(
            *cat.findRelationTokens(
            cat.tokenizeQuery({'ireference-uniform_title': self.context})
            )
            )}
            ),
                      cmp = lambda x,y: cmp(x.position, y.position))
