__author__ = 'labx'

import sys
import Orange.widgets.__init__
import Orange.canvas.__main__
import pkg_resources

def widget_discovery(discovery):
    dist = pkg_resources.get_distribution("Orange")
    pkgs = ["orangecontrib.xoppy.widgets"]
    for pkg in pkgs:
        discovery.process_category_package(pkg, distribution=dist)

Orange.widgets.__dict__['widget_discovery'] = widget_discovery

def main(argv=None):
    Orange.canvas.__main__.main(argv)


if __name__ == "__main__":
    sys.exit(main())