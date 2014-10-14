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
#    from ..tools.xoppy_calc import xoppy_calc_BC_PerfectCrystal
#except ImportError:
#    print("compute pressed.")
#    print("Error importing: xoppy_calc_BC_PerfectCrystal")
#    raise

class OWBC_PerfectCrystal(widget.OWWidget):
    name = "BC_PerfectCrystal"
    id = "orange.widgets.dataBC_PerfectCrystal"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_BC_PerfectCrystal.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "BC_PerfectCrystal"]
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

    material = Setting("Si")
    thickness = Setting(0.0001)
    cell = Setting("[5.430700,5.430700,5.430700,90,90,90]")
    Natoms = Setting(8)
    Zatoms = Setting("[14,14,14,14,14,14,14,14]")
    XYZ = Setting("[ [0.000000,0.000000,0.000000],                       [0.000000,0.500000,0.500000],                       [0.500000,0.000000,0.500000],                       [0.500000,0.500000,0.000000],                       [0.250000,0.250000,0.250000],                       [0.250000,0.750000,0.750000],                       [0.750000,0.250000,0.750000],                       [0.750000,0.750000,0.250000] ]")
    occupancy = Setting("[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]")
    Temperature0 = Setting(300.0)
    Temperature = Setting(330.0)
    Miller = Setting("[1,1,1]")
    AsymmetryAngle = Setting(0.0)


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
        gui.lineEdit(box1, self, "material",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "thickness",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "cell",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "Natoms",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "Zatoms",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XYZ",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "occupancy",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "Temperature0",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "Temperature",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "Miller",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "AsymmetryAngle",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        self.process_showers()
        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material', 'thickness', 'crystallographic cell parameters', 'number of atoms in unit cell', 'atomic number of atoms in unic cell', 'coordinates of atoms in crystallographic cell', 'occupancy', 'temperature at which unit cell is given [K]', 'Crystal temperature [K]', 'Miller indices', 'Asymmetry angle [deg]']

    def unitFlags(self):
         return ['True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True']


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
        #xoppy_doc('BC_PerfectCrystal')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWBC_PerfectCrystal()
    w.show()
    app.exec()
    w.saveSettings()
