# namespace declaration.
__import__("pkg_resources").declare_namespace(__name__)
import os,sys
xoppy_home = os.path.dirname(__file__)
home_bin = os.path.join(xoppy_home,'bin.'+sys.platform)
home_doc = os.path.join(xoppy_home,'doc_txt')
home_data = os.path.join(xoppy_home,'data')
#home_wd = os.path.join(xoppy_home,'tmp')