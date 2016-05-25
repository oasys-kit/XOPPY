__author__ = 'labx'

import sys, os
import orangecanvas.resources as resources
import xraylib
from PyQt4 import QtGui

class locations:
    @classmethod
    def home_bin(cls):
        return resources.package_dirname("orangecontrib.xoppy.util") + "/bin/" + str(sys.platform) + "/"

    @classmethod
    def home_doc(cls):
        return resources.package_dirname("orangecontrib.xoppy.util") + "/doc_txt/"

    @classmethod
    def home_data(cls):
        return resources.package_dirname("orangecontrib.xoppy.util") + "/data/"

    @classmethod
    def home_bin_run(cls):
        #return resources.package_dirname("orangecontrib.xoppy.util") + "/bin_run/"
        return os.getcwd()


import urllib

XRAY_SERVER_URL = "http://x-server.gmca.aps.anl.gov/"

class HttpManager():

    @classmethod
    def send_xray_server_request(cls, application, parameters):

        data = urllib.parse.urlencode(parameters)
        data = data.encode('utf-8') # data should be bytes
        req = urllib.request.Request(XRAY_SERVER_URL + application, data)
        resp = urllib.request.urlopen(req)

        return resp.read()

class ShowTextDialog(QtGui.QDialog):

    def __init__(self, title, text, width=650, height=400, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(title)
        layout = QtGui.QVBoxLayout(self)

        text_edit = QtGui.QTextEdit(text, self)
        text_edit.setReadOnly(True)

        text_area = QtGui.QScrollArea(self)
        text_area.setWidget(text_edit)
        text_area.setWidgetResizable(True)
        text_area.setFixedHeight(height)
        text_area.setFixedWidth(width)

        bbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)

        bbox.accepted.connect(self.accept)
        layout.addWidget(text_area)
        layout.addWidget(bbox)

    @classmethod
    def show_text(cls, title, text, width=650, height=400, parent=None):
        dialog = ShowTextDialog(title, text, width, height, parent)
        dialog.show()

def xoppy_doc(app):
    home_doc = locations.home_doc()

    filename1 = os.path.join(home_doc,app+'.txt')
    filename2 = os.path.join(home_doc,app+'_par.txt')
    command = "gedit "+filename1+" "+filename2+" &"
    print("Running command '%s' "%(command))
    os.system(command)

class XoppyPhysics:
    @classmethod
    def getMaterialDensity(cls, material_formula):
        if material_formula is None: return 0.0
        if str(material_formula.strip()) == "": return 0.0

        try:
            compoundData = xraylib.CompoundParser(material_formula)

            if compoundData["nElements"] == 1:
                return xraylib.ElementDensity(compoundData["Elements"][0])
            else:
                return 0.0
        except:
            return 0.0
