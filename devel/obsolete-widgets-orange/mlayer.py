import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np
from PyMca5.PyMcaIO import specfilewrapper as specfile

try:
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise

try:
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_mlayer
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_mlayer")
    raise

class OWmlayer(widget.OWWidget):
    name = "mlayer"
    id = "orange.widgets.datamlayer"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_mlayer.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "mlayer"]
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

    MODE = Setting(0)
    SCAN = Setting(0)
    F12_FLAG = Setting(0)
    SUBSTRATE = Setting("Si")
    ODD_MATERIAL = Setting("Si")
    EVEN_MATERIAL = Setting("W")
    ENERGY = Setting(8050.0)
    THETA = Setting(0.0)
    SCAN_STEP = Setting(0.009999999776483)
    NPOINTS = Setting(600)
    ODD_THICKNESS = Setting(25.0)
    EVEN_THICKNESS = Setting(25.0)
    NLAYERS = Setting(50)
    FILE = Setting("layers.dat")


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
        gui.comboBox(box1, self, "MODE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Periodic Layers', 'Individual Layers'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCAN",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Grazing Angle', 'Photon Energy'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "F12_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Create on the fly', 'Use existing file: mlayers.f12'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SUBSTRATE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ODD_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EVEN_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THETA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SCAN_STEP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ODD_THICKNESS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EVEN_THICKNESS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NLAYERS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Layer periodicity: ','Scanning variable: ','Material parameters:','Substrate: ','Odd layer material (closer to vacuum): ','Even layer material (closer to substrate): ','Photon energy [eV]:','Grazing angle [degrees]:','Scanning variable step: ','Number of scanning points','Thickness [A] for odd material:','Thickness [A] for even material:','Number of layer pairs:','File with layer thicknesses:']


    def unitFlags(self):
         return ['True','True','True','self.F12_FLAG  ==  0','self.F12_FLAG  ==  0','self.F12_FLAG  ==  0','True','True','True','True','self.MODE  ==  0  &  self.F12_FLAG  ==  0','self.MODE  ==  0  &  self.F12_FLAG  ==  0','self.MODE  ==  0  &  self.F12_FLAG  ==  0','self.MODE  ==  1']


    #def unitNames(self):
    #     return ['MODE','SCAN','F12_FLAG','SUBSTRATE','ODD_MATERIAL','EVEN_MATERIAL','ENERGY','THETA','SCAN_STEP','NPOINTS','ODD_THICKNESS','EVEN_THICKNESS','NLAYERS','FILE']


    def compute(self):
        fileName = xoppy_calc_mlayer(MODE=self.MODE,SCAN=self.SCAN,F12_FLAG=self.F12_FLAG,SUBSTRATE=self.SUBSTRATE,ODD_MATERIAL=self.ODD_MATERIAL,EVEN_MATERIAL=self.EVEN_MATERIAL,ENERGY=self.ENERGY,THETA=self.THETA,SCAN_STEP=self.SCAN_STEP,NPOINTS=self.NPOINTS,ODD_THICKNESS=self.ODD_THICKNESS,EVEN_THICKNESS=self.EVEN_THICKNESS,NLAYERS=self.NLAYERS,FILE=self.FILE)
        #send specfile

        if fileName == None:
            print("Nothing to send")
        else:
            self.send("xoppy_specfile",fileName)
            sf = specfile.Specfile(fileName)
            if sf.scanno() == 1:
                #load spec file with one scan, # is comment
                print("Loading file:  ",fileName)
                out = np.loadtxt(fileName)
                print("data shape: ",out.shape)
                #get labels
                txt = open(fileName).readlines()
                tmp = [ line.find("#L") for line in txt]
                itmp = np.where(np.array(tmp) != (-1))
                labels = txt[itmp[0]].replace("#L ","").split("  ")
                print("data labels: ",labels)
                #
                # build and send orange table
                #
                domain = Domain([ ContinuousVariable(i) for i in labels ])
                table = Table.from_numpy(domain, out)
                self.send("xoppy_table",table)
            else:
                print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('mlayer')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWmlayer()
    w.show()
    app.exec()
    w.saveSettings()
