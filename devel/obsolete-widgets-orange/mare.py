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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_mare
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_mare")
    raise

class OWmare(widget.OWWidget):
    name = "mare"
    id = "orange.widgets.datamare"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_mare.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "mare"]
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

    CRYSTAL = Setting(2)
    H = Setting(2)
    K = Setting(2)
    L = Setting(2)
    HMAX = Setting(3)
    KMAX = Setting(3)
    LMAX = Setting(3)
    FHEDGE = Setting(1e-08)
    DISPLAY = Setting(0)
    LAMBDA = Setting(1.54)
    DELTALAMBDA = Setting(0.009999999776483)
    PHI = Setting(-20.0)
    DELTAPHI = Setting(0.1)


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
        gui.comboBox(box1, self, "CRYSTAL",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Si', 'Si_NIST', 'Si2', 'Ge', 'Diamond', 'GaAs', 'GaSb', 'GaP', 'InAs', 'InP', 'InSb', 'SiC', 'NaCl', 'CsF', 'LiF', 'KCl', 'CsCl', 'Be', 'Graphite', 'PET', 'Beryl', 'KAP', 'RbAP', 'TlAP', 'Muscovite', 'AlphaQuartz', 'Copper', 'LiNbO3', 'Platinum', 'Gold', 'Sapphire', 'LaB6', 'LaB6_NIST', 'KTP', 'AlphaAlumina', 'Aluminum', 'Iron', 'Titanium'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "H",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "L",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FHEDGE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "DISPLAY",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Spaghetti', 'Spaghetti+Umweg', 'Spaghetti+Glitches', 'All'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DELTALAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DELTAPHI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal:','h main','k main','l main','h max','k max','l max','Eliminate reflection with fh less than ','Display','Wavelength [A] (for Unweg)','Delta Wavelength [A]','Phi [deg] (for Glitches)','Delta Phi [deg]']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','self.DISPLAY  ==  1 OR self.DISPLAY  ==  3','self.DISPLAY  ==  1 OR self.DISPLAY  ==  3','self.DISPLAY  ==  2 OR self.DISPLAY  ==  3','self.DISPLAY  ==  2 OR self.DISPLAY  ==  3']


    #def unitNames(self):
    #     return ['CRYSTAL','H','K','L','HMAX','KMAX','LMAX','FHEDGE','DISPLAY','LAMBDA','DELTALAMBDA','PHI','DELTAPHI']


    def compute(self):
        fileName = xoppy_calc_mare(CRYSTAL=self.CRYSTAL,H=self.H,K=self.K,L=self.L,HMAX=self.HMAX,KMAX=self.KMAX,LMAX=self.LMAX,FHEDGE=self.FHEDGE,DISPLAY=self.DISPLAY,LAMBDA=self.LAMBDA,DELTALAMBDA=self.DELTALAMBDA,PHI=self.PHI,DELTAPHI=self.DELTAPHI)
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
        xoppy_doc('mare')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWmare()
    w.show()
    app.exec()
    w.saveSettings()
