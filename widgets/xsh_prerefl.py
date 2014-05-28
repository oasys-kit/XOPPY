import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np
from Shadow.ShadowPreprocessorsXraylib import prerefl

try:
    from ..tools.xoppy_calc import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise

try:
    from ..tools.xoppy_calc import xoppy_calc_xsh_prerefl
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xsh_prerefl")
    raise

class OWxsh_prerefl(widget.OWWidget):
    name = "xsh_prerefl"
    id = "orange.widgets.dataxsh_prerefl"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xsh_prerefl.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xsh_prerefl"]
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

    SYMBOL = Setting("SiC")
    DENSITY = Setting(3.217)
    FILE = Setting("reflec.dat")
    E_MIN = Setting(100.0)
    E_MAX = Setting(20000.0)
    E_STEP = Setting(100.0)


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
        gui.lineEdit(box1, self, "SYMBOL",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DENSITY",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_STEP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Element/Compound formula','Density [ g/cm3 ]','File for SHADOW (trace):','Minimum energy [eV]','Maximum energy [eV]','Energy step [eV]']


    def unitFlags(self):
         return ['True','True','True','True','True','True']


    #def unitNames(self):
    #     return ['SYMBOL','DENSITY','FILE','E_MIN','E_MAX','E_STEP']


    def compute(self):
        tmp = prerefl(interactive=False,SYMBOL=self.SYMBOL,DENSITY=self.DENSITY,FILE=self.FILE,E_MIN=self.E_MIN,E_MAX=self.E_MAX,E_STEP=self.E_STEP)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('xsh_prerefl')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxsh_prerefl()
    w.show()
    app.exec()
    w.saveSettings()
