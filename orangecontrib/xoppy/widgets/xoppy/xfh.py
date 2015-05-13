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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xfh
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xfh")
    raise

class OWxfh(widget.OWWidget):
    name = "xfh"
    id = "orange.widgets.dataxfh"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xfh.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xfh"]
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

    FILEF0 = Setting(0)
    FILEF1F2 = Setting(0)
    FILECROSSSEC = Setting(0)
    ILATTICE = Setting(0)
    HMILLER = Setting(1)
    KMILLER = Setting(1)
    LMILLER = Setting(1)
    I_ABSORP = Setting(2)
    TEMPER = Setting("1.0")
    ENERGY = Setting(8000.0)
    ENERGY_END = Setting(18000.0)
    NPOINTS = Setting(20)


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
        gui.comboBox(box1, self, "FILEF0",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['f0_xop.dat'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "FILEF1F2",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['f1f2_Windt.dat', 'f1f2_EPDL97.dat'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "FILECROSSSEC",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['CrossSec_XCOM.dat'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ILATTICE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Si', 'Si_NIST', 'Si2', 'Ge', 'Diamond', 'GaAs', 'GaSb', 'GaP', 'InAs', 'InP', 'InSb', 'SiC', 'NaCl', 'CsF', 'LiF', 'KCl', 'CsCl', 'Be', 'Graphite', 'PET', 'Beryl', 'KAP', 'RbAP', 'TlAP', 'Muscovite', 'AlphaQuartz', 'Copper', 'LiNbO3', 'Platinum', 'Gold', 'Sapphire', 'LaB6', 'LaB6_NIST', 'KTP', 'AlphaAlumina', 'Aluminum', 'Iron', 'Titanium'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HMILLER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KMILLER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LMILLER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "I_ABSORP",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['No', 'Yes (photoelectric)', 'Yes(ph.el+compton)', 'Yes(ph.el+compton+rayleigh)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEMPER",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY_END",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['DABAX f0 file:','DABAX f1f2 file:','DABAX CrossSec file:','Crystal:','h miller index','k miller index','l miller index','Include absorption:','Temperature factor [see help]:','From Energy [eV]','To energy [eV]','Number of points']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','True']


    #def unitNames(self):
    #     return ['FILEF0','FILEF1F2','FILECROSSSEC','ILATTICE','HMILLER','KMILLER','LMILLER','I_ABSORP','TEMPER','ENERGY','ENERGY_END','NPOINTS']


    def compute(self):
        fileName = xoppy_calc_xfh(FILEF0=self.FILEF0,FILEF1F2=self.FILEF1F2,FILECROSSSEC=self.FILECROSSSEC,ILATTICE=self.ILATTICE,HMILLER=self.HMILLER,KMILLER=self.KMILLER,LMILLER=self.LMILLER,I_ABSORP=self.I_ABSORP,TEMPER=self.TEMPER,ENERGY=self.ENERGY,ENERGY_END=self.ENERGY_END,NPOINTS=self.NPOINTS)
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
        xoppy_doc('xfh')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxfh()
    w.show()
    app.exec()
    w.saveSettings()
