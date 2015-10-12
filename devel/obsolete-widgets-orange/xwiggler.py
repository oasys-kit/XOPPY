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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xwiggler
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xwiggler")
    raise

class OWxwiggler(widget.OWWidget):
    name = "xwiggler"
    id = "orange.widgets.dataxwiggler"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xwiggler.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xwiggler"]
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

    FIELD = Setting(0)
    NPERIODS = Setting(12)
    ULAMBDA = Setting(0.125)
    K = Setting(14.0)
    ENERGY = Setting(6.04)
    PHOT_ENERGY_MIN = Setting(100.0)
    PHOT_ENERGY_MAX = Setting(100100.0)
    NPOINTS = Setting(100)
    LOGPLOT = Setting(1)
    NTRAJPOINTS = Setting(101)
    CURRENT = Setting(200.0)
    FILE = Setting("?")


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
        gui.comboBox(box1, self, "FIELD",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Sinusoidal', 'B from file', 'B from harmonics'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ULAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOT_ENERGY_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOT_ENERGY_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "LOGPLOT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Lin', 'Log'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NTRAJPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Magnetic field: ','Number of periods','Wiggler period [m]','K value','Beam energy [GeV]','Min Photon Energy [eV]','Max Photon Energy [eV]','Number of energy points','Energy points spacing','Number of traj points per period','Electron Beam Current [mA]','File with Magnetic Field']


    def unitFlags(self):
         return ['True','True','self.FIELD  !=  1','self.FIELD  ==  0','True','True','True','True','True','self.FIELD  !=  1','True','self.FIELD  !=  0']


    #def unitNames(self):
    #     return ['FIELD','NPERIODS','ULAMBDA','K','ENERGY','PHOT_ENERGY_MIN','PHOT_ENERGY_MAX','NPOINTS','LOGPLOT','NTRAJPOINTS','CURRENT','FILE']


    def compute(self):
        fileName = xoppy_calc_xwiggler(FIELD=self.FIELD,NPERIODS=self.NPERIODS,ULAMBDA=self.ULAMBDA,K=self.K,ENERGY=self.ENERGY,PHOT_ENERGY_MIN=self.PHOT_ENERGY_MIN,PHOT_ENERGY_MAX=self.PHOT_ENERGY_MAX,NPOINTS=self.NPOINTS,LOGPLOT=self.LOGPLOT,NTRAJPOINTS=self.NTRAJPOINTS,CURRENT=self.CURRENT,FILE=self.FILE)
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
        xoppy_doc('xwiggler')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxwiggler()
    w.show()
    app.exec()
    w.saveSettings()
