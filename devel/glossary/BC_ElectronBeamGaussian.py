import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np

#try:
#    from ..tools.xoppy_calc import xoppy_doc
#except ImportError:
#    print("Error importing: xoppy_doc")
#    raise

#try:
#    from ..tools.xoppy_calc import xoppy_calc_BC_ElectronBeamGaussian
#except ImportError:
#    print("compute pressed.")
#    print("Error importing: xoppy_calc_BC_ElectronBeamGaussian")
#    raise

class OWBC_ElectronBeamGaussian(widget.OWWidget):
    name = "BC_ElectronBeamGaussian"
    id = "orange.widgets.dataBC_ElectronBeamGaussian"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_BC_ElectronBeamGaussian.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "BC_ElectronBeamGaussian"]
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

    ElectronEnergy = Setting(1.0)
    ElectronCurrent = Setting(0.1)
    OrbitOffset = Setting("[0.0,0.0,0.0,0.0,0.0,0.0]")
    InputType = Setting(0)
    ElectronEnergySpread = Setting(0.0)
    EmittanceH = Setting(0.0)
    EmittanceV = Setting(0.0)
    BetaH = Setting(0.0)
    BetaV = Setting(0.0)
    AlphaH = Setting(0.0)
    AlphaV = Setting(0.0)
    BunchLength = Setting(0.0)
    DispersionH = Setting(0.0)
    DispersionV = Setting(0.0)
    DispersionDerivH = Setting(0.0)
    DispersionDerivV = Setting(0.0)
    SigmaMatrix = Setting("[ [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0] ]")
    Mmatrix = Setting("[ [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0],                            [0.0,0.0,0.0,0.0,0.0,0.0] ]")


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
        gui.lineEdit(box1, self, "ElectronEnergy",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ElectronCurrent",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "OrbitOffset",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "InputType",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Twiss description', 'Full description'],
                    valueType=list, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ElectronEnergySpread",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EmittanceH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EmittanceV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BetaH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BetaV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "AlphaH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "AlphaV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BunchLength",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DispersionH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DispersionV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DispersionDerivH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DispersionDerivV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SigmaMatrix",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "Mmatrix",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        self.process_showers()
        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Electron Energy in the storage ring', 'Electron current intensity [A]', "Orbit offset (x,x',y,y',s,delta) from where initial conditions are defined", 'Type of description', 'Spread RMS of the energy of the electrons', 'Horizontal emittance', 'Vertical emittance', 'Beta function (Horizontal)', 'Beta function (Vertical)', 'Alpha function (Horizontal)', 'Alpha function (Vertical)', 'Bunch length', 'Dispersion (Horizontal)', 'Dispersion (Vertical)', 'Dispersion Derivative (Horizontal)', 'Dispersion Derivative (Vertical)', 'Sigma matrix', 'M matrix']

    def unitFlags(self):
         return ['True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True']


    def compute(self):
        print("compute executed.")
        #table = Table.from_numpy(domain, out)
        #self.send("xoppy_table",table)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        #xoppy_doc('BC_ElectronBeamGaussian')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWBC_ElectronBeamGaussian()
    w.show()
    app.exec()
    w.saveSettings()
