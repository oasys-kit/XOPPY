import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import numpy as np

class OWxtubes(widget.OWWidget):
    name = "xtubes"
    id = "orange.widgets.dataxtubes"
    description = "xoppy application to compute..."
    icon = "icons/Unknown.svg"
    author = ""
    maintainer_email = ""
    priority = 10
    category = ""
    keywords = ["list", "of", "keywords"]
    outputs = [{"name": "flux",
                "type": np.ndarray,
                "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    ITUBE = Setting(0)
    VOLTAGE = Setting(30.0)


    def __init__(self):
        super().__init__()

        box0 = gui.widgetBox(self.controlArea, " ",orientation="horizontal") 
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Set defaults", callback=self.resetSettings)
        gui.button(box0, self, "Help", callback=self.help)
        self.process_showers()
        box = gui.widgetBox(self.controlArea, " ",orientation="vertical") 
        
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ITUBE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Mo', 'Rh', 'W'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "VOLTAGE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Target element ','Voltage  [kV] (18<V<42)']


    def unitFlags(self):
         return ['True','True']


    def unitNames(self):
         return ['ITUBE','VOLTAGE']


    def help(self):
        try:
            from xoppy_calc import xoppy_doc
        except ImportError:
            print("help pressed.")
            print("Error importing: xoppy_doc")
            raise

        xoppy_doc('xtubes')


    def compute(self):
        try:
            from xoppy_calc import xoppy_calc_xtubes
        except ImportError:
            print("compute pressed.")
            print("Error importing: xoppy_calc_xtubes")
            raise
            
        fileName = xoppy_calc_xtubes(ITUBE=self.ITUBE,VOLTAGE=self.VOLTAGE)
        print("Loading file:  ",fileName)
        out = np.loadtxt(fileName)
        print("out.shape: ",out.shape)
        self.send("flux",out)

    def process_showers(self):

        from PyQt4.QtGui import QLayout
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        for shower in getattr(self, "showers", []):
            shower()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtubes()
    w.show()
    app.exec()
    w.saveSettings()
