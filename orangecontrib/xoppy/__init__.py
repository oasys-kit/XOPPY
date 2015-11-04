# namespace declaration.
__import__("pkg_resources").declare_namespace(__name__)
import os,sys
import orangecanvas.resources as resources

def home_bin():
    return resources.package_dirname("orangecontrib.xoppy.bin_" + str(sys.platform)) + "/"

def home_doc():
    return resources.package_dirname("orangecontrib.xoppy.doc_txt") + "/"

def home_data():
    return resources.package_dirname("orangecontrib.xoppy.data") + "/"

def home_testrun():
    return resources.package_dirname("orangecontrib.xoppy.testrun") + "/"

