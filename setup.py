#! /usr/bin/env python3

import os

try:
    from setuptools import find_packages, setup
except AttributeError:
    from setuptools import find_packages, setup

NAME = 'OASYS1-XOPPY'
VERSION = '1.0.40'
ISRELEASED = False

DESCRIPTION = 'XOPPY: XOP (X-ray oriented programs) in Python'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Manuel Sanchez del Rio, Luca Rebuffi, and Bioinformatics Laboratory, FRI UL'
AUTHOR_EMAIL = 'srio@esrf.eu, lrebuffi@anl.gov'
URL = 'https://github.com/oasys-kit/XOPPY'
DOWNLOAD_URL = 'https://github.com/oasys-kit/XOPPY'
LICENSE = 'GPLv3'

KEYWORDS = (
    'X-ray optics',
    'simulator',
    'oasys1',
)

CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
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
    'oasys1>=1.1.42',
    'oasys1-srwlib',
    'pySRU',
)

PACKAGES = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests'))

PACKAGE_DATA = {
    "orangecontrib.xoppy.widgets.source":["icons/*.png", "icons/*.jpg"],
    "orangecontrib.xoppy.widgets.optics":["icons/*.png", "icons/*.jpg", "misc/*.*"],
}

NAMESPACE_PACAKGES = ["orangecontrib", "orangecontrib.xoppy", "orangecontrib.xoppy.widgets"]

ENTRY_POINTS = {
    'oasys.addons' : ("xoppy = orangecontrib.xoppy", ),
    'oasys.widgets' : (
        "XOPPY Sources = orangecontrib.xoppy.widgets.source",
        "XOPPY Optics = orangecontrib.xoppy.widgets.optics",
    ),
    #'oasys.menus' : ("xoppymenu = orangecontrib.xoppy.menu",)
}

import site, shutil, sys


if __name__ == '__main__':
    is_beta = False

    try:
        import PyMca5, PyQt4

        is_beta = True
    except:
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

        if is_beta: raise NotImplementedError("This version of XOPPY doesn't work with Oasys1 beta.\nPlease install OASYS1 final release: http://www.elettra.eu/oasys.html")
