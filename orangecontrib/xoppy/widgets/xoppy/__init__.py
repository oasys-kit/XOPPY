# namespace declaration.
__import__("pkg_resources").declare_namespace(__name__)
import os,sys
import orangecanvas.resources as resources

xoppy_home = resources.package_dirname("orangecontrib.xoppy")

def home_bin():
    return os.path.join(xoppy_home, 'bin.' + str(sys.platform) + '/')

def home_doc():
    return os.path.join(xoppy_home, 'doc_txt/')

def home_data():
    return os.path.join(xoppy_home, 'data/')

def home_testrun():
    return os.path.join(xoppy_home, 'testrun/')