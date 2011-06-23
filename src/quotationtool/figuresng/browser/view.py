import zope.interface
import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.browser import BrowserView
from zope.proxy import removeAllProxies
import zc.relation
from zope.viewlet import viewlet
from zope.viewlet.viewlet import ViewletBase
from zope.schema import getValidationErrors

from quotationtool.renderer.interfaces import IHTMLRenderer 

from quotationtool.figuresng import interfaces

from quotationtool.figuresng.interfaces import _


class ExampleLabelView(BrowserView):
    """A view that informs about the object type."""

    def __call__(self):
        return _('example-labelview', u"Example #$ID", 
                 mapping = {'ID': self.context.__name__})


class ExampleContainerLabelView(BrowserView):

    def __call__(self):
        return _('examplecontainer-labelview',
                 u"Examples")


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

    template = ViewPageTemplateFile('details.pt')

    def __call__(self):
        return self.template()


class ListView(BrowserView, RenderQuotation):
    """The @@list view which can be called from within a zpt."""

    limit = 200

    # TODO
    template = ViewPageTemplateFile('details.pt')

    def __call__(self):
        return self.template()
