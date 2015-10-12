#! /usr/bin/env python3

import imp
import os
import sys
import subprocess

from setuptools import find_packages, setup

NAME = 'XOPPY'
VERSION = '1.0.0'
ISRELEASED = False

DESCRIPTION = 'XOPPY: XOP (X-ray oriented programs) in Python'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Manuel Sanchez del Rio, Luca Rebuffi, and Bioinformatics Laboratory, FRI UL'
AUTHOR_EMAIL = 'srio@esrf.eu'
URL = 'https://github.com/srio/Orange-XOPPY'
DOWNLOAD_URL = 'https://github.com/srio/Orange-XOPPY'
LICENSE = 'GPLv3'

KEYWORDS = (
    'X-ray optics',
    'simulator',
    'oasys',
)

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
)

SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    'setuptools',
    'numpy',
    'scipy',
    'matplotlib',
    'orange-widget-core>=0.0.2',
    'oasys>=0.1',
)

PACKAGES = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests'))

PACKAGE_DATA = {
    "orangecontrib.xoppy.widgets.viewers":["icons/*.png", "icons/*.jpg"],
    "orangecontrib.xoppy.widgets.xoppy":["icons/*.png", "icons/*.jpg"],
}

NAMESPACE_PACAKGES = ["orangecontrib", "orangecontrib.xoppy", "orangecontrib.xoppy.widgets"]

ENTRY_POINTS = {
    'oasys.addons' : ("shadow = orangecontrib.xoppy", ),
    'oasys.widgets' : (
        "XOPPY viewers = orangecontrib.xoppy.widgets.viewers",
        "XOPPY components = orangecontrib.xoppy.widgets.xoppy",
    ),
    #'oasys.menus' : ("Menu = orangecontrib.shadow.menu",)
}

if __name__ == '__main__':
    setup(
          name = NAME,
          version = VERSION,
          description = DESCRIPTION,
          long_description = LONG_DESCRIPTION,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          url = URL,
          download_url = DOWNLOAD_URL,
          license = LICENSE,
          keywords = KEYWORDS,
          classifiers = CLASSIFIERS,
          packages = PACKAGES,
          package_data = PACKAGE_DATA,
          #          py_modules = PY_MODULES,
          setup_requires = SETUP_REQUIRES,
          install_requires = INSTALL_REQUIRES,
          #extras_require = EXTRAS_REQUIRE,
          #dependency_links = DEPENDENCY_LINKS,
          entry_points = ENTRY_POINTS,
          namespace_packages=NAMESPACE_PACAKGES,
          include_package_data = True,
          zip_safe = False,
          )
