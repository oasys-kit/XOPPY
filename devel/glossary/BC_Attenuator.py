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
#    from ..tools.xoppy_calc import xoppy_calc_BC_Attenuator
#except ImportError:
#    print("compute pressed.")
#    print("Error importing: xoppy_calc_BC_Attenuator")
#    raise

class OWBC_Attenuator(widget.OWWidget):
    name = "BC_Attenuator"
    id = "orange.widgets.dataBC_Attenuator"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_BC_Attenuator.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "BC_Attenuator"]
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
    thickness = Setting(0.001)
    density = Setting(1.0)


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
        gui.lineEdit(box1, self, "density",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        self.process_showers()
        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material', 'thickness [m]', 'material density [g/cm^3]']

    def unitFlags(self):
         return ['True', 'True', 'True']


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
        #xoppy_doc('BC_Attenuator')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWBC_Attenuator()
    w.show()
    app.exec()
    w.saveSettings()
