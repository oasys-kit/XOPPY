import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np

try:
    from orangecontrib.xoppy.util.xsh_calc import *
except ImportError:
    print("Error importing: calc")
    raise



class OWxsh_und_gauss(widget.OWWidget):
    name = "xsh_und_gauss"
    id = "orange.widgets.dataxsh_und_gauss"
    description = "xoppy application to compute..."
    icon = "icons/xsh_und_gauss.jpg"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xsh_und_gauss"]
    outputs = [#{"name": "xoppy_data",
               # "type": np.ndarray,
               # "doc": ""},
               {"name": "xoppy_table",
                "type": Table,
                "doc": ""},
               {"name": "xoppy_specfile",
                "type": str,
                "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    UND_LENGTH = Setting(4.0)
    UND_E0 = Setting(15000.0)
    UND_DE = Setting(1500.0)
    USERUNIT = Setting(1)
    SIGMAX = Setting(0.04131)
    SIGMAZ = Setting(0.00034)
    SIGDIX = Setting(10.3e-06)
    SIGDIZ = Setting(1.2e-06)
    NPOINT = Setting(25000)
    ISTAR1 = Setting(0)


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
        gui.lineEdit(box1, self, "UND_LENGTH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "UND_E0",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "UND_DE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "USERUNIT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['mm', 'cm', 'm'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGMAZ",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGDIX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGDIZ",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ISTAR1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Undulator length [m]','Set undulator to energy [eV]','Delta Energy [eV]','User unit (length)','Size RMS H [user units]','Size RMS V [user units]','Divergence RMS H [rad]','Divergence RMS V [rad]','Number of points','Seed']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True']


    #def unitNames(self):
    #     return [ "UND_LENGTH", "UND_E0", "UND_DE", "USERUNIT", "SIGMAX", "SIGMAZ", "SIGDIX", "SIGDIZ", "NPOINT", "ISTAR1"]




    def compute(self):
        tmp = calc_xsh_und_gauss(UND_LENGTH=self.UND_LENGTH,UND_E0=self.UND_E0,UND_DE=self.UND_DE,USERUNIT=self.USERUNIT,SIGMAX=self.SIGMAX,SIGMAZ=self.SIGMAZ,SIGDIX=self.SIGDIX,SIGDIZ=self.SIGDIZ,NPOINT=self.NPOINT,ISTAR1=self.ISTAR1)



    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        #xoppy_doc('xsh_und_gauss')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxsh_und_gauss()
    w.show()
    app.exec()
    w.saveSettings()
