import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from PyMca5.PyMcaIO import specfilewrapper as specfile
import PyMca5.PyMcaPhysics.xrf.Elements as Elements

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget
from srxraylib.sources import srfunc
import xraylib
from orangecontrib.xoppy.util import xoppy_util

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
    outputs = [{"name": "xoppy_data",
                "type": numpy.ndarray,
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
                out = numpy.loadtxt(fileName)
                print("data shape: ",out.shape)
                #get labels
                txt = open(fileName).readlines()
                tmp = [ line.find("#L") for line in txt]
                itmp = numpy.where(numpy.array(tmp) != (-1))
                labels = txt[itmp[0]].replace("#L ","").split("  ")
                print("data labels: ",labels)
                self.send("xoppy_data",out)
            else:
                print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xpower')


def xoppy_calc_xpower(F1F2=0,MU=0,SOURCE=1,DUMMY1="",DUMMY2="",DUMMY3="",ENER_MIN=1000.0,ENER_MAX=50000.0,ENER_N=100,\
                      SOURCE_FILE="?",NELEMENTS=1,\
                      EL1_FOR="Be",EL1_FLAG=0,EL1_THI=0.5,EL1_ANG=3.0,EL1_ROU=0.0,EL1_DEN="?",\
                      EL2_FOR="Rh",EL2_FLAG=1,EL2_THI=0.5,EL2_ANG=3.0,EL2_ROU=0.0,EL2_DEN="?",\
                      EL3_FOR="Al",EL3_FLAG=0,EL3_THI=0.5,EL3_ANG=3.0,EL3_ROU=0.0,EL3_DEN="?",\
                      EL4_FOR= "B",EL4_FLAG=0,EL4_THI=0.5,EL4_ANG=3.0,EL4_ROU=0.0,EL4_DEN="?",\
                      EL5_FOR="Pt",EL5_FLAG=1,EL5_THI=0.5,EL5_ANG=3.0,EL5_ROU=0.0,EL5_DEN="?"):
    print("Inside xoppy_calc_xpower. ")

    if ENER_MAX == ENER_MIN:
        ENER_N = 2

    #xpower_inp

    nelem = 1+NELEMENTS
    substance = [EL1_FOR,EL2_FOR,EL3_FOR,EL4_FOR,EL5_FOR]
    thick     = numpy.array( (EL1_THI,EL2_THI,EL3_THI,EL4_THI,EL5_THI))
    angle     = numpy.array( (EL1_ANG,EL2_ANG,EL3_ANG,EL4_ANG,EL5_ANG))
    dens      = [EL1_DEN,EL2_DEN,EL3_DEN,EL4_DEN,EL5_DEN]
    roughness = numpy.array( (EL1_ROU,EL2_ROU,EL3_ROU,EL4_ROU,EL5_ROU))
    flags     = numpy.array( (EL1_FLAG,EL2_FLAG,EL3_FLAG,EL4_FLAG,EL5_FLAG))

    for i in range(nelem):
        try:
            rho = float(dens[i])
        except:
            # rho = 1.0
            #is element? take density from PyMca
            rho = 0.0
            for item in Elements.ElementsInfo:
                if item[0] == substance[i]: rho = item[6]*1e-3
            if rho != 0:
                print("Found density for %s: %d g/cm3"%(substance[i],rho))
            else:
                print("Undefined density for %s => taking density = 1.0"%(substance[i]))
                rho = 1.0

        dens[i] = rho


    if SOURCE == 0:
        energies = numpy.linspace(1,100,495)
        source = numpy.ones(energies.size)
        tmp = numpy.vstack( (energies,source))
    if SOURCE == 1:
        energies = numpy.linspace(ENER_MIN,ENER_MAX,ENER_N)
        source = numpy.ones(energies.size)
        tmp = numpy.vstack( (energies,source))

    if SOURCE >= 2:
        if SOURCE == 2: source_file = SOURCE_FILE
        if SOURCE == 3: source_file = "SRCOMPE"
        if SOURCE == 4: source_file = "SRCOMPF"
        try:
            tmp = numpy.loadtxt(source_file)
            energies = tmp[:,0]
            source = tmp[:,1]
        except:
            print("Error loading file %s "%(source_file))
            raise


    outArray = numpy.hstack( energies )
    outColTitles = ["Photon Energy [eV]"]
    outArray = numpy.vstack((outArray,source))
    outColTitles.append("Source")

    txt = ""
    txt += "*************************** Xpower Results ******************\n"
    if energies[0] != energies[-1]:
        txt += "  Source energy: start=%f keV, end=%f keV, points=%d \n"%(energies[0],energies[-1],energies.size)
    else:
        txt += "  Source energy: %f keV\n"%(energies[0])
    txt += "  Number of optical elements: %d\n"%(nelem)

    if energies[0] != energies[-1]:
        # I0 = source[0:-1].sum()*(energies[1]-energies[0])
        I0 = numpy.trapz(source, x=energies, axis=-1)
        txt += "  Incoming power (integral of spectrum): %f \n"%(I0)

        I1 = I0
    else:
        txt += "  Incoming power: %f \n"%(source[0])
        I0  = source[0]
        I1 = I0

    outFile = "xpower.spec"

    cumulated = source

    for i in range(nelem):
        #info oe
        if flags[i] == 0:
            txt += '      *****   oe '+str(i+1)+'  [Filter] *************\n'
            txt += '      Material: %s\n'%(substance[i])
            txt += '      Density [g/cm^3]: %f \n'%(dens[i])
            txt += '      thickness [mm] : %f \n'%(thick[i])
        else:
            txt += '      *****   oe '+str(i+1)+'  [Mirror] *************\n'
            txt += '      Material: %s\n'%(substance[i])
            txt += '      Density [g/cm^3]: %f \n'%(dens[i])
            txt += '      grazing angle [mrad]: %f \n'%(angle[i])
            txt += '      roughness [A]: %f \n'%(roughness[i])


        if flags[i] == 0: # filter
            tmp = numpy.zeros(energies.size)
            for j,energy in enumerate(energies):

                tmp[j] = xraylib.CS_Total_CP(substance[i],energy/1000.0)

            trans = numpy.exp(-tmp*dens[i]*(thick[i]/10.0))
            outArray = numpy.vstack((outArray,tmp))
            outColTitles.append("[oe %i] Total CS cm2/g"%(1+i))
            print(outArray)

            outArray = numpy.vstack((outArray,tmp*dens[i]))
            outColTitles.append("[oe %i] Mu cm^-1"%(1+i))


            outArray = numpy.vstack((outArray,trans))
            outColTitles.append("[oe %i] Transmitivity "% (1+i))
            outArray = numpy.vstack((outArray,1.0-trans))
            outColTitles.append("[oe %i] Absorption "% (1+i))

            cumulated *= trans

        if flags[i] == 1: # mirror
            tmp = numpy.zeros(energies.size)
            for j,energy in enumerate(energies):
                tmp[j] = xraylib.Refractive_Index_Re(substance[i],energy/1000.0,dens[i])
            delta = 1.0 - tmp
            outArray = numpy.vstack((outArray,delta))
            outColTitles.append("[oe %i] 1-Re[n]=delta"%(1+i))

            beta = numpy.zeros(energies.size)
            for j,energy in enumerate(energies):
                beta[j] = xraylib.Refractive_Index_Im(substance[i],energy/1000.0,dens[i])
            outArray = numpy.vstack((outArray,beta))
            outColTitles.append("[oe %i] Im[n]=beta"%(1+i))

            outArray = numpy.vstack((outArray,delta/beta))
            outColTitles.append("[oe %i] delta/beta"%(1+i))

            (rs,rp,runp) = reflectivity_fresnel(refraction_index_beta=beta,refraction_index_delta=delta,\
                                        grazing_angle_mrad=angle[i],roughness_rms_A=roughness[i],\
                                        photon_energy_ev=energies)
            outArray = numpy.vstack((outArray,rs))
            outColTitles.append("[oe %i] Reflectivity-s"%(1+i))
            outArray = numpy.vstack((outArray,1.0-rs))
            outColTitles.append("[oe %i] Transmitivity"%(1+i))

            cumulated *= rs

        if energies[0] != energies[-1]:
            # I2 = cumulated[0:-1].sum()*(energies[1]-energies[0])
            #txt += "      Outcoming power [Sum]: %f\n"%(I2)
            #txt += "      Outcoming power [Trapez]: %f\n"%(I2b)
            I2 = numpy.trapz( cumulated, x=energies, axis=-1)
            txt += "      Outcoming power: %f\n"%(I2)
            txt += "      Absorbed power: %f\n"%(I1-I2)
            txt += "      Normalized Outcoming Power: %f\n"%(I2/I0)
            if flags[i] == 0:
                pass
                txt += "      Absorbed dose Gy.(mm^2 beam cross section)/s %f\n: "%((I1-I2)/(dens[i]*thick[i]*1e-6))
            I1 = I2
        else:
            I2 = cumulated[0]
            txt += "      Outcoming power: %f\n"%(cumulated[0])
            txt += "      Absorbed power: %f\n"%(I1-I2)
            txt += "      Normalized Outcoming Power: %f\n"%(I2/I0)
            I1 = I2

        outArray = numpy.vstack((outArray,cumulated))
        outColTitles.append("Intensity after oe #%i"%(1+i))

    ncol = len(outColTitles)
    npoints = energies.size

    f = open(outFile,"w")
    f.write("#F "+outFile+"\n")
    f.write("\n")
    f.write("#S 1 xpower: properties of optical elements\n")

    txt2 = txt.splitlines()
    for i in range(len(txt2)):
        f.write("#UINFO %s\n"%(txt2[i]))

    f.write("#N %d\n"%(ncol))
    f.write("#L")
    for i in range(ncol):
        f.write("  "+outColTitles[i])
    f.write("\n")

    for i in range(npoints):
            f.write((" %e "*ncol+"\n")%(tuple(outArray[:,i].tolist())))

    f.close()
    print("File written to disk: " + outFile)
    print(txt)

    return outFile


def reflectivity_fresnel(refraction_index_delta=1e-5,refraction_index_beta=0.0,\
                 grazing_angle_mrad=3.0,roughness_rms_A=0.0,photon_energy_ev=10000.0):
    """
    Calculates the reflectivity of an interface using Fresnel formulas.

    Code adapted from XOP and SHADOW

    :param refraction_index_delta: scalar or array with delta (n=1-delta+i beta)
    :param refraction_index_beta: scalar or array with beta (n=1-delta+i beta)
    :param grazing_angle_mrad: scalar with grazing angle in mrad
    :param roughness_rms_A: scalar with roughness rms in Angstroms
    :param photon_energy_ev: scalar or array with photon energies in eV
    :return: (rs,rp,runp) the s-polarized, p-pol and unpolarized reflectivities
    """
    # ;
    # ; calculation of reflectivity (piece of code adapted from shadow/abrefc)
    # ;
    #
    theta1 = grazing_angle_mrad*1e-3     # in rad
    rough1 = roughness_rms_A*1e-8 # in cm

    # ; epsi = 1 - alpha - i gamma
    # alpha = 2.0D0*k*f1
    # gamma = 2.0D0*k*f2
    alpha = 2*refraction_index_delta
    gamma = 2*refraction_index_beta

    rho = (numpy.sin(theta1))**2 - alpha
    rho += numpy.sqrt((numpy.sin(theta1)**2 - alpha)**2 + gamma**2)
    rho = numpy.sqrt(rho/2)

    rs1 = 4*(rho**2)*(numpy.sin(theta1) - rho)**2 + gamma**2
    rs2 = 4*(rho**2)*(numpy.sin(theta1) + rho)**2 + gamma**2
    rs = rs1/rs2

    ratio1 = 4*rho**2 * (rho*numpy.sin(theta1)-numpy.cos(theta1)**2)**2 + gamma**2*numpy.sin(theta1)**2
    ratio2 = 4*rho**2 * (rho*numpy.sin(theta1)+numpy.cos(theta1)**2)**2 + gamma**2*numpy.sin(theta1)**2
    ratio = ratio1/ratio2

    rp = rs*ratio
    runp = 0.5 * (rs + rp)
    wavelength_m = srfunc.m2ev / photon_energy_ev
    debyewaller = numpy.exp( -(4.0*numpy.pi*numpy.sin(theta1)*rough1/(wavelength_m*1e10))**2 )

    return rs*debyewaller, rp*debyewaller, runp*debyewaller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxpower()
    w.show()
    app.exec()
    w.saveSettings()
