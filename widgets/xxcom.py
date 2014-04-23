import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import numpy as np

class OWxxcom(widget.OWWidget):
    name = "xxcom"
    id = "orange.widgets.dataxxcom"
    description = "xoppy application to compute..."
    icon = "icons/xoppy.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["list", "of", "keywords"]
    #outputs = [{"name": "xoppy_data",
    #            "type": np.ndarray,
    #            "doc": ""}]
    outputs = [{"name": "xoppy_data",
                "type": np.ndarray,
                "doc": ""},
               {"name": "xoppy_file",
                "type": str,
                "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    NAME = Setting("Pyrex Glass")
    SUBSTANCE = Setting(3)
    DESCRIPTION = Setting("SiO2:B2O3:Na2O:Al2O3:K2O")
    FRACTION = Setting("0.807:0.129:0.038:0.022:0.004")
    GRID = Setting(1)
    GRIDINPUT = Setting(0)
    GRIDDATA = Setting("0.0804:0.2790:0.6616:1.3685:2.7541")
    ELEMENTOUTPUT = Setting(0)


    def __init__(self):
        super().__init__()

        box0 = gui.widgetBox(self.controlArea, " ",orientation="horizontal") 
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Set defaults", callback=self.resetSettings)
        gui.button(box0, self, "Help", callback=self.help1)
        self.process_showers()
        box = gui.widgetBox(self.controlArea, " ",orientation="vertical") 
        
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SUBSTANCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Element (Atomic number)', 'Element (Symbol)', 'Compound (Formula)', 'Mixture (F1:F2:F3...)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTION",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FRACTION",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Standard', 'Standard+points', 'Points only'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRIDINPUT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['From Keyboard', 'From file'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDDATA",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ELEMENTOUTPUT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Cross section [b/atom]', 'Cross section [b/atom] & Attenuation coeff [cm2/g]', 'Partial interaction coeff & Attenuation coeff [cm2/g]'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Name','Substance:','Description:','fraction','grid','grid points','grid points [MeV]/file name','Output quantity']


    def unitFlags(self):
         return ['True','True','True','self.SUBSTANCE  ==  3','True','self.GRID  !=  0','(self.GRID  !=  0)','self.SUBSTANCE  <=  1']


    def unitNames(self):
         return ['NAME','SUBSTANCE','DESCRIPTION','FRACTION','GRID','GRIDINPUT','GRIDDATA','ELEMENTOUTPUT']


    def help1(self):
        try:
            from xoppy_calc import xoppy_doc
        except ImportError:
            print("help pressed.")
            print("Error importing: xoppy_doc")
            raise

        xoppy_doc('xxcom')


    def compute(self):
        try:
            from xoppy_calc import xoppy_calc_xxcom
        except ImportError:
            print("compute pressed.")
            print("Error importing: xoppy_calc_xxcom")
            raise
            
        fileName = xoppy_calc_xxcom(NAME=self.NAME,SUBSTANCE=self.SUBSTANCE,DESCRIPTION=self.DESCRIPTION,FRACTION=self.FRACTION,GRID=self.GRID,GRIDINPUT=self.GRIDINPUT,GRIDDATA=self.GRIDDATA,ELEMENTOUTPUT=self.ELEMENTOUTPUT)
        print("Loading file:  ",fileName)
        out = np.loadtxt(fileName)
        print("out.shape: ",out.shape)
        self.send("xoppy_data",out)

    def process_showers(self):

        from PyQt4.QtGui import QLayout
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        for shower in getattr(self, "showers", []):
            shower()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxxcom()
    w.show()
    app.exec()
    w.saveSettings()
