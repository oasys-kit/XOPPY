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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xpower
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xpower")
    raise

class OWxpower(widget.OWWidget):
    name = "xpower"
    id = "orange.widgets.dataxpower"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xpower.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xpower"]
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

    F1F2 = Setting(0)
    MU = Setting(0)
    SOURCE = Setting(1)
    DUMMY1 = Setting("")
    DUMMY2 = Setting("")
    DUMMY3 = Setting("")
    ENER_MIN = Setting(1000.0)
    ENER_MAX = Setting(50000.0)
    ENER_N = Setting(100)
    SOURCE_FILE = Setting("?")
    NELEMENTS = Setting(1)
    EL1_FOR = Setting("Be")
    EL1_FLAG = Setting(0)
    EL1_THI = Setting(0.5)
    EL1_ANG = Setting(3.0)
    EL1_ROU = Setting(0.0)
    EL1_DEN = Setting("?")
    EL2_FOR = Setting("Rh")
    EL2_FLAG = Setting(1)
    EL2_THI = Setting(0.5)
    EL2_ANG = Setting(3.0)
    EL2_ROU = Setting(0.0)
    EL2_DEN = Setting("?")
    EL3_FOR = Setting("Al")
    EL3_FLAG = Setting(0)
    EL3_THI = Setting(0.5)
    EL3_ANG = Setting(3.0)
    EL3_ROU = Setting(0.0)
    EL3_DEN = Setting("?")
    EL4_FOR = Setting("B")
    EL4_FLAG = Setting(0)
    EL4_THI = Setting(0.5)
    EL4_ANG = Setting(3.0)
    EL4_ROU = Setting(0.0)
    EL4_DEN = Setting("?")
    EL5_FOR = Setting("Pt")
    EL5_FLAG = Setting(1)
    EL5_THI = Setting(0.5)
    EL5_ANG = Setting(3.0)
    EL5_ROU = Setting(0.0)
    EL5_DEN = Setting("?")


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
        gui.comboBox(box1, self, "F1F2",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['f1f2_Windt.dat', 'f1f2_EPDL97.dat'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MU",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['CrossSec_XCOM.dat'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SOURCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Normalized to 1 (Standard E grid)  ', 'Normalized to 1 (E from keyboard)  ', 'From external file.                ', 'xop/source Flux (file: SRCOMPE)    ', 'xop/source Power (file: SRCOMPW)   '],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DUMMY1",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DUMMY2",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DUMMY3",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENER_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENER_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENER_N",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SOURCE_FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "NELEMENTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['1', '2', '3', '4', '5'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_FOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL1_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_ANG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_ROU",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_DEN",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_FOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL2_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_ANG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_ROU",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_DEN",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_FOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL3_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 26 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_ANG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 27 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_ROU",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 28 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_DEN",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 29 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_FOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 30 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL4_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 31 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 32 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_ANG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 33 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_ROU",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 34 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_DEN",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 35 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_FOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 36 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL5_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 37 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 38 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_ANG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 39 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_ROU",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 40 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_DEN",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['    f1f2 dataset:     ','Mu dataset:','Source:','DUMMY1','DUMMY2','DUMMY3','From energy [eV]:      ','To energy [eV]:','Energy points:  ','File with source:','Number of elements:','1st oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]','2nd oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]','3rd oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]','4th oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]','5th oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]']


    def unitFlags(self):
         return ['True','True','True','False','False','False','self.SOURCE  ==  1','self.SOURCE  ==  1','self.SOURCE  ==  1','self.SOURCE  ==  2','True',' self.NELEMENTS  >=  0',' self.NELEMENTS  >=  0','self.EL1_FLAG  ==  0  &  self.NELEMENTS  >=  0','self.EL1_FLAG  !=  0  &  self.NELEMENTS  >=  0','self.EL1_FLAG  !=  0  &  self.NELEMENTS  >=  0',' self.NELEMENTS  >=  0',' self.NELEMENTS  >=  1',' self.NELEMENTS  >=  1','self.EL2_FLAG  ==  0  &  self.NELEMENTS  >=  1','self.EL2_FLAG  !=  0  &  self.NELEMENTS  >=  1','self.EL2_FLAG  !=  0  &  self.NELEMENTS  >=  1',' self.NELEMENTS  >=  1',' self.NELEMENTS  >=  2',' self.NELEMENTS  >=  2','self.EL3_FLAG  ==  0  &  self.NELEMENTS  >=  2','self.EL3_FLAG  !=  0  &  self.NELEMENTS  >=  2','self.EL3_FLAG  !=  0  &  self.NELEMENTS  >=  2',' self.NELEMENTS  >=  2',' self.NELEMENTS  >=  3',' self.NELEMENTS  >=  3','self.EL4_FLAG  ==  0  &  self.NELEMENTS  >=  3','self.EL4_FLAG  !=  0  &  self.NELEMENTS  >=  3','self.EL4_FLAG  !=  0  &  self.NELEMENTS  >=  3',' self.NELEMENTS  >=  3',' self.NELEMENTS  >=  4',' self.NELEMENTS  >=  4','self.EL5_FLAG  ==  0  &  self.NELEMENTS  >=  4','self.EL5_FLAG  !=  0  &  self.NELEMENTS  >=  4','self.EL5_FLAG  !=  0  &  self.NELEMENTS  >=  4',' self.NELEMENTS  >=  4']


    #def unitNames(self):
    #     return ['F1F2','MU','SOURCE','DUMMY1','DUMMY2','DUMMY3','ENER_MIN','ENER_MAX','ENER_N','SOURCE_FILE','NELEMENTS','EL1_FOR','EL1_FLAG','EL1_THI','EL1_ANG','EL1_ROU','EL1_DEN','EL2_FOR','EL2_FLAG','EL2_THI','EL2_ANG','EL2_ROU','EL2_DEN','EL3_FOR','EL3_FLAG','EL3_THI','EL3_ANG','EL3_ROU','EL3_DEN','EL4_FOR','EL4_FLAG','EL4_THI','EL4_ANG','EL4_ROU','EL4_DEN','EL5_FOR','EL5_FLAG','EL5_THI','EL5_ANG','EL5_ROU','EL5_DEN']


    def compute(self):
        fileName = xoppy_calc_xpower(F1F2=self.F1F2,MU=self.MU,SOURCE=self.SOURCE,DUMMY1=self.DUMMY1,DUMMY2=self.DUMMY2,DUMMY3=self.DUMMY3,ENER_MIN=self.ENER_MIN,ENER_MAX=self.ENER_MAX,ENER_N=self.ENER_N,SOURCE_FILE=self.SOURCE_FILE,NELEMENTS=self.NELEMENTS,EL1_FOR=self.EL1_FOR,EL1_FLAG=self.EL1_FLAG,EL1_THI=self.EL1_THI,EL1_ANG=self.EL1_ANG,EL1_ROU=self.EL1_ROU,EL1_DEN=self.EL1_DEN,EL2_FOR=self.EL2_FOR,EL2_FLAG=self.EL2_FLAG,EL2_THI=self.EL2_THI,EL2_ANG=self.EL2_ANG,EL2_ROU=self.EL2_ROU,EL2_DEN=self.EL2_DEN,EL3_FOR=self.EL3_FOR,EL3_FLAG=self.EL3_FLAG,EL3_THI=self.EL3_THI,EL3_ANG=self.EL3_ANG,EL3_ROU=self.EL3_ROU,EL3_DEN=self.EL3_DEN,EL4_FOR=self.EL4_FOR,EL4_FLAG=self.EL4_FLAG,EL4_THI=self.EL4_THI,EL4_ANG=self.EL4_ANG,EL4_ROU=self.EL4_ROU,EL4_DEN=self.EL4_DEN,EL5_FOR=self.EL5_FOR,EL5_FLAG=self.EL5_FLAG,EL5_THI=self.EL5_THI,EL5_ANG=self.EL5_ANG,EL5_ROU=self.EL5_ROU,EL5_DEN=self.EL5_DEN)
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
        xoppy_doc('xpower')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxpower()
    w.show()
    app.exec()
    w.saveSettings()
