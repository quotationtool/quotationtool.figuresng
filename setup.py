# -*- coding: utf-8 -*-
"""Setup for quotationtool.figuresng package

$Id$
"""
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name='quotationtool.figuresng'

setup(
    name = name,
    version='0.1.0',
    description="Figures Next Generation, e.g. examples, content types for the quotationtool application",
    long_description=(
        read('README')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'quotationtool', 'figuresng', 'README.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    keywords='quotationtool',
    author=u"Christian Lueck",
    author_email='cluecksbox@googlemail.com',
    url='',
    license='ZPL 2.1',
    # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: BlueBream',
                 ],
    packages = find_packages('src'),
    namespace_packages = ['quotationtool',],
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'setuptools',
        'ZODB3',
        'zope.interface',
        'zope.schema',
        'zope.component',
        'zope.container',
        'zope.exceptions',
        'zope.i18nmessageid',
        'zope.intid',
        'zope.keyreference',
        'zope.catalog',
        'zc.catalog >= 1.5',
        'zc.relation',
        'zope.app.content',
        'zope.annotation',
        'zope.dublincore',
        'zope.security',
        'zope.securitypolicy',
        'zope.app.schema',
        'zope.app.appsetup',
        'zope.processlifetime',
        'z3c.indexer',
        'z3c.searcher',

        'quotationtool.quotation',
        'quotationtool.site',
        'quotationtool.security',
        'quotationtool.renderer',
        'quotationtool.relation',
        'quotationtool.skin',
        'quotationtool.tinymce',
        'quotationtool.editorial',
        'quotationtool.search',

        'z3c.template',
        'z3c.macro',
        'z3c.pagelet',
        'z3c.layer.pagelet',
        'zope.app.publication',
        'zope.browserpage',
        'zope.publisher',
        'z3c.formui',
        'z3c.form',
        'zc.resourcelibrary',
        'z3c.menu.ready2go',
        'z3c.table',
        'zope.contentprovider',

        'zope.app.pagetemplate',
        'zope.viewlet',
        'zope.app.component',

        # BBB required by packages but not configured there
        'zope.app.generations', # required by z3c.searcher
        ],
    extras_require = dict(
        test = [
            'zope.testing',
            'zope.configuration',
            ],
        ),
    )
