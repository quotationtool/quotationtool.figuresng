import zope.interface
import zope.component
from z3c.form import field
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import absoluteURL
import zc.resourcelibrary

from quotationtool.quotation.browser.form import AddQuotationInReferenceContext, QuotationEditForm

from quotationtool.figuresng.interfaces import _, IExample, IExampleContainer


class AddExampleInReferenceContext(AddQuotationInReferenceContext):
    """A form for adding a quotation object to the collectanea that
    takes a reference object as context."""

    factory_name = 'quotationtool.figuresng.Example'

    label = _('add-example', u"Add a new Example")

    info = _('add-example-info', 
             u"The <span class=\"quotationtool-example-quid\">example</span> and its <span class=\"quotationtool-example-proquo\">denotation/meaning</span> have to be tagged in the quotation using the flags. If a marker is present, please tag the <span class=\"quotationtool-example-marker\">marker</span>, too.<br/>Then fill in the example, the denotation/meaning and--if present--the marker fields. The denotation/meaning field should not be used for repeating theorems most accurately, but for the term that is in question. The same with the example field. The input data should serve searching the database but not hermeneutics. If you would like to give more accurate information then please write a comment after submitting the form."
             )
    
    fields = field.Fields(IExample).omit(
        '__parent__', '__name__', 'reference', 'length')#, 'source_type')

    def __init__(self, context, request):
        super(AddQuotationInReferenceContext, self).__init__(context, request)
        zc.resourcelibrary.need('quotationtool.tinymce.QuotationAndExample')

    def add(self, example):
        container = zope.component.getUtility(
            IExampleContainer, context=self.context)
        name = INameChooser(container).chooseName(example, None)
        self._obj = container[name] = example


class ExampleEditForm(QuotationEditForm):
    """A form to edit the example."""

    info = AddExampleInReferenceContext.info

    label = _('edit-example-label', u"Edit Example") 

    fields = field.Fields(IExample).omit(
        '__parent__', '__name__', 'reference', 'length')

    def __init__(self, context, request):
        super(QuotationEditForm, self).__init__(context, request)
        if context.source_type == 'html':
            zc.resourcelibrary.need('quotationtool.tinymce.QuotationAndExample')
