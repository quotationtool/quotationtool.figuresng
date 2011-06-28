import zope.interface
import zope.component
import zope.schema
from zope.traversing.browser.absoluteurl import absoluteURL
from z3c.form.form import Form as ViewletForm
from z3c.form import field, button
from zope.viewlet.interfaces import IViewlet
from zope.app.component.hooks import getSite
from zope.traversing.api import traverse

from quotationtool.figuresng.interfaces import _, IExampleContainer


example_id = zope.schema.TextLine(
    title = u"ID",
    required = False,
    )
example_id.__name__ = 'example_id'


class ExampleByIdForm(ViewletForm):
    """ Get example by ID."""

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
            IExampleContainer,
            context = getSite(),
            )
        self.request.response.redirect(
            absoluteURL(container, self.request) 
            + u"/" + data['example_id']
            )
