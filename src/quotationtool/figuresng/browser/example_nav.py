import zope.interface
import zope.component
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import ISiteMenu
from z3c.menu.ready2go.manager import MenuManager

from quotationtool.skin.interfaces import ISubNavManager
from quotationtool.skin.browser.nav import MainNavItem


class IExampleContainerMainNavItem(zope.interface.Interface): 
    """ A marker interface for the bibliography's item in the main navigation."""
    pass


class ExampleContainerMainNavItem(MainNavItem):
    """The bibliography navigation item in the main navigation."""

    zope.interface.implements(IExampleContainerMainNavItem)


class IExampleContainerSubNav(ISubNavManager):
    """A manager for the bibliography subnavigation."""

ExampleContainerSubNav = ViewletManager('examplecontainersubnav',
                                        ISiteMenu,
                                        bases = (MenuManager,))

IExampleContainerSubNav.implementedBy(ExampleContainerSubNav)
