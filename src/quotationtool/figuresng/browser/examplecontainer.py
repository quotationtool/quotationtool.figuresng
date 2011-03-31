import zope.component
import zope.interface
import zope.schema
from z3c.pagelet.browser import BrowserPagelet
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.form.form import Form as ViewletForm
from z3c.form import field, button
from zope.viewlet.interfaces import IViewlet
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.component.hooks import getSite
from zope.traversing.api import traverse

from quotationtool.search.browser import search

from quotationtool.figuresng import iexample
from quotationtool.figuresng.i18n import _


class LabelView(BrowserView):

    def __call__(self):
        return _('examplecontainer-labelview',
                 u"Examples")


class FrontPage(BrowserPagelet):
    """The front page for the figure container."""


class Container(BrowserPagelet):
    """List of examples in the container."""

    def getExamples(self):
        """Returns the examples in the container. Called by the
        template."""
        return self.context.values()



class ExampleSearchTargetViewlet(search.SearchTargetViewlet):
    """A viewlet with the option to search the referatory."""

    label = _('example-search-target-label',
              u"Examples")

    description = _('example-search-target-desc',
                    u"Search for an example by example term, by denotation or meaning, by name of its author, by title, by year etc.")


class SearchForm(search.SearchFormBase):
    """A form for searching the example container."""

    catalog_name = 'examples'

    query = ('quid_pro_quo', 'quid', 'pro_quo', 'marker', 'quotation', 'author', 'title')

    label = _('search-form-label', u"Search for Examples")


class SearchResultPage(search.SearchResultPageBase):
    """Display search results of the example catalog in a 'page'
    manner."""

    catalog_name = 'examples'

    def getExamples(self):
        return self.getResultPage()


example_id = zope.schema.TextLine(
    title = u"ID",
    required = False,
    )
example_id.__name__ = 'example_id'


class ExampleByIdForm(ViewletForm):

    label = _('example-by-id-label',
              u"Example by ID (unique Number)")

    zope.interface.implements(IViewlet)

    ignoreContext = True

    prefix = "examplebyid."

    fields = field.Fields(example_id)

    def __init__(self, context, request, view, manager):
        """ See zope.viewlet.viewlet.ViewletBase"""
        self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    @button.buttonAndHandler(_(u"Show!"), name = 'show')
    def handleShow(self, action):
        data, errors = self.extractData()
        if not data['example_id'] in self.context:
            self.status = _('example-by-id-failure',
                            u"Example #$ID does not exist",
                            mapping = {'ID': data['example_id']})
            return
        container = zope.component.getUtility(
            iexample.IExampleContainer,
            context = getSite(),
            )
        self.request.response.redirect(
            absoluteURL(container, self.request) 
            + u"/" + data['example_id']
            )
