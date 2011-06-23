import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import zc.relation
from zope.viewlet.viewlet import ViewletBase
from zope.schema import getValidationErrors

from quotationtool.figuresng.interfaces import _, IExample



class SchemaErrorFlag(ViewletBase):
    """ Put flag on invalid examples."""

    def render(self):
        if getValidationErrors(IExample, self.context):
            return u'<abbr title="Schema validation error" class="error schema-validation-error">S</abbr>'
        else:
            return u''


class ExampleCountFlag(ViewletBase):

    template = ViewPageTemplateFile('count.pt')

    def count(self):
        """Return the number of examples referencing to context"""
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        examples = list(cat.findRelations(
            cat.tokenizeQuery({'iquotation-reference': self.context})
            ))
        return len(examples)
    
    def render(self):
        return self.template()

