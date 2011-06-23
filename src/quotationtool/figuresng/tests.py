import unittest
import doctest
import zope.component
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig

import quotationtool.figuresng

_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS


def setUpZCML(test):
    setUp(test)
    XMLConfig('configure.zcml', quotationtool.figuresng)()


class SiteCreationTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(SiteCreationTests, self).setUp()
        setUpZCML(self)
        import quotationtool.site
        XMLConfig('configure.zcml', quotationtool.site)

    def test_ExampleContainer(self):
        """ Test if container is created on a new site event."""
        from quotationtool.site.site import QuotationtoolSite
        from zope.container.btree import BTreeContainer
        root = BTreeContainer()
        root['quotationtool'] = site = QuotationtoolSite()
        self.assertTrue('examples' in site.keys())
        from quotationtool.figuresng.examplecontainer import ExampleContainer
        self.assertTrue(isinstance(site['examples'], ExampleContainer))
        from quotationtool.figuresng.iexample import IExampleContainer
        ut = zope.component.getUtility(
            IExampleContainer, 
            context = site)
        self.assertTrue(ut is site['examples'])



def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite('README.txt',
                                 setUp = setUpZCML,
                                 tearDown = tearDown,
                                 optionflags=_flags),
            unittest.makeSuite(SiteCreationTests),
            ))
