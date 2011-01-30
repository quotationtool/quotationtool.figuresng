from zope.publisher.browser import BrowserView


class YearView(BrowserView):
    
    def __call__(self):
        return u"View 'year' not implemented for %s." % unicode(self.context.__class__)


class AuthorView(BrowserView):
    
    def __call__(self):
        return u"View 'author' not implemented for %s." % unicode(self.context.__class__)


class TitleView(BrowserView):
    
    def __call__(self):
        return u"View 'title' not implemented for %s." % unicode(self.context.__class__)
