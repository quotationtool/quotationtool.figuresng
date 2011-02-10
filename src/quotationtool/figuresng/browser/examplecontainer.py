import zope.component
from z3c.pagelet.browser import BrowserPagelet
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

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

    query = ('any', 'quid_pro_quo', 'quid', 'pro_quo', 'marker', 'quotation', 'author', 'title')

    label = _('search-form-label', u"Search for Examples")


class SearchResultPage(search.SearchResultPageBase):
    """Display search results of the example catalog in a 'page'
    manner."""

    catalog_name = 'examples'

    def getExamples(self):
        return self.getResultPage()
