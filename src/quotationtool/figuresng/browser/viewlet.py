import zope.interface
import zope.component
import zope.schema
from zope.traversing.browser.absoluteurl import absoluteURL
from z3c.form.form import Form as ViewletForm
from z3c.form import field, button
from zope.viewlet.interfaces import IViewlet, IViewletManager
from zope.app.component.hooks import getSite
from zope.traversing.api import traverse
from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager
from zope.contentprovider.interfaces import IContentProvider

from quotationtool.figuresng.interfaces import _, IExampleContainer


class IExampleContainerAdds(IViewletManager):
    """ A viewlet manager for adds on the container view."""


ExampleContainerAdds = ViewletManager('examplecontainer-adds',
                                      IExampleContainerAdds,
                                      bases = (WeightOrderedViewletManager,))


example_id = zope.schema.TextLine(
    title = _('exampleid-field-title',
              u"ID"),
    required = False,
    )
example_id.__name__ = 'example_id'


class ExampleByIdForm(ViewletForm):
    """ Get example by ID."""

    label = _('examplebyidform-label', u"Display example by ID-number") 

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

    @button.buttonAndHandler(_(u"Display"), name = 'show')
    def handleShow(self, action):
        data, errors = self.extractData()
        if data['example_id'] in self.context:
            container = zope.component.getUtility(
                IExampleContainer,
                context = getSite(),
                )
            self.request.response.redirect(
                absoluteURL(container, self.request) 
                + u"/" + data['example_id']
                )
        else:
            self.status = _('example-by-id-failure',
                            u"Example #$ID does not exist",
                            mapping = {'ID': data['example_id']})

