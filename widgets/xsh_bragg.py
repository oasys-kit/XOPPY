import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np
from Shadow.ShadowPreprocessorsXraylib import bragg

try:
    from ..tools.xoppy_calc import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise


class OWxsh_bragg(widget.OWWidget):
    name = "xsh_bragg"
    id = "orange.widgets.dataxsh_bragg"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xsh_bragg.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xsh_bragg"]
    #outputs = [#{"name": "xoppy_data",
    #           # "type": np.ndarray,
    #           # "doc": ""},
    #           {"name": "xoppy_table",
    #            "type": Table,
    #            "doc": ""},
    #           {"name": "xoppy_specfile",
    #            "type": str,
    #            "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    DESCRIPTOR = Setting("Si")
    H_MILLER_INDEX = Setting(1)
    K_MILLER_INDEX = Setting(1)
    L_MILLER_INDEX = Setting(1)
    TEMPERATURE_FACTOR = Setting(1.0)
    E_MIN = Setting(5000.0)
    E_MAX = Setting(15000.0)
    E_STEP = Setting(100.0)
    SHADOW_FILE = Setting("bragg.dat")


    def __init__(self):
        super().__init__()

        box0 = gui.widgetBox(self.controlArea, " ",orientation="horizontal") 
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Defaults", callback=self.defaults)
        gui.button(box0, self, "Help", callback=self.help1)
        self.process_showers()
        box = gui.widgetBox(self.controlArea, " ",orientation="vertical") 
        
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "H_MILLER_INDEX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "K_MILLER_INDEX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "L_MILLER_INDEX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEMPERATURE_FACTOR",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_STEP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SHADOW_FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal descriptor','H miller index','K miller index','L miller index','Temperature factor','From Energy [eV]','To Energy to [eV]','Energy step [eV]','File name (for SHADOW)']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True']


    #def unitNames(self):
    #     return ['DESCRIPTOR','H_MILLER_INDEX','K_MILLER_INDEX','L_MILLER_INDEX','TEMPERATURE_FACTOR','E_MIN','E_MAX','E_STEP','SHADOW_FILE']


    def compute(self):
        tmp = bragg(interactive=False,DESCRIPTOR=self.DESCRIPTOR,H_MILLER_INDEX=self.H_MILLER_INDEX,K_MILLER_INDEX=self.K_MILLER_INDEX,L_MILLER_INDEX=self.L_MILLER_INDEX,TEMPERATURE_FACTOR=self.TEMPERATURE_FACTOR,E_MIN=self.E_MIN,E_MAX=self.E_MAX,E_STEP=self.E_STEP,SHADOW_FILE=self.SHADOW_FILE)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('xsh_bragg')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxsh_bragg()
    w.show()
    app.exec()
    w.saveSettings()
