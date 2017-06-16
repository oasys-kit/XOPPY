#! /usr/bin/env python3

import os

try:
    from setuptools import find_packages, setup
except AttributeError:
    from setuptools import find_packages, setup

NAME = 'OASYS1-XOPPY'
VERSION = '1.0.22'
ISRELEASED = False

DESCRIPTION = 'XOPPY: XOP (X-ray oriented programs) in Python'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Manuel Sanchez del Rio, Luca Rebuffi, and Bioinformatics Laboratory, FRI UL'
AUTHOR_EMAIL = 'srio@esrf.eu, luca.rebuffi@elettra.eu'
URL = 'https://github.com/srio/Orange-XOPPY'
DOWNLOAD_URL = 'https://github.com/srio/Orange-XOPPY'
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
    'oasys1>=1.0.12',
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

    try:
        is_install = False
        for arg in sys.argv:
            if arg == 'install': is_install = True

        if is_install:
            site_packages_dir = None

            for directory in site.getsitepackages():
                if os.path.exists(directory + "/oasys"):
                    site_packages_dir = directory
                    break

            if not site_packages_dir is None:
                if sys.platform == 'darwin':
                    shutil.copyfile("libraries/" + str(sys.platform) + "/srwl_bl.py", site_packages_dir + "/srwl_bl.py")
                    shutil.copyfile("libraries/" + str(sys.platform) + "/srwl_uti_cryst.py", site_packages_dir + "/srwl_uti_cryst.py")
                    shutil.copyfile("libraries/" + str(sys.platform) + "/srwl_uti_src.py", site_packages_dir + "/srwl_uti_src.py")
                    shutil.copyfile("libraries/" + str(sys.platform) + "/srwl_util_und.py", site_packages_dir + "/srwl_util_und.py")
                    shutil.copyfile("libraries/" + str(sys.platform) + "/srwlib.py", site_packages_dir + "/srwlib.py")
                    shutil.copyfile("libraries/" + str(sys.platform) + "/uti_math.py", site_packages_dir + "/uti_math.py")
                    shutil.copyfile("libraries/" + str(sys.platform) + "/srwlpy.so", site_packages_dir + "/srwlpy.so")
                elif sys.platform == 'linux':
                    pass

                # TODO: to be removed
                #if sys.platform == 'linux':
                #    os.remove(site_packages_dir + "/orangecontrib/xoppy/widgets/optics/xpower.py")

    except Exception as exception:
        print(str(exception))
