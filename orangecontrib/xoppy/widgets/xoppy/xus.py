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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xus
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xus")
    raise

class OWxus(widget.OWWidget):
    name = "xus"
    id = "orange.widgets.dataxus"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xus.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xus"]
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

    TITLE = Setting("APS Undulator A, Beam Parameters for regular lattice nux36nuy39.twi, 1.5% cpl.")
    ENERGY = Setting(7.0)
    CUR = Setting(100.0)
    SIGE = Setting(0.000959999975748)
    TEXT_MACHINE = Setting("")
    SIGX = Setting(0.273999989032745)
    SIGY = Setting(0.010999999940395)
    SIGX1 = Setting(0.011300000362098)
    SIGY1 = Setting(0.00359999993816)
    TEXT_BEAM = Setting("")
    PERIOD = Setting(3.299999952316284)
    NP = Setting(70)
    KX = Setting(0.0)
    KY = Setting(2.75)
    TEXT_UNDULATOR = Setting("")
    EMIN = Setting(1000.0)
    EMAX = Setting(50000.0)
    N = Setting(5000)
    TEXT_ENERGY = Setting("")
    D = Setting(30.0)
    XPC = Setting(0.0)
    YPC = Setting(0.0)
    XPS = Setting(2.5)
    YPS = Setting(1.0)
    NXP = Setting(25)
    NYP = Setting(10)
    TEXT_PINHOLE = Setting("")
    MODE = Setting(2)
    METHOD = Setting(4)
    IHARM = Setting(0)
    TEXT_MODE = Setting("")
    NPHI = Setting(0)
    NALPHA = Setting(0)
    CALPHA2 = Setting(0.0)
    NOMEGA = Setting(64)
    COMEGA = Setting(8.0)
    NSIGMA = Setting(0)
    TEXT_CALC = Setting("")
    RUN_MODE_NAME = Setting("foreground")


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
        gui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CUR",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_MACHINE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_BEAM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_UNDULATOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_ENERGY",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "D",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NXP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NYP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 26 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_PINHOLE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 27 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MODE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 28 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 29 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "IHARM",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 30 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_MODE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 31 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPHI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 32 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NALPHA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 33 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CALPHA2",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 34 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NOMEGA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 35 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "COMEGA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 36 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NSIGMA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 37 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEXT_CALC",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 38 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "RUN_MODE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True']


    #def unitNames(self):
    #     return ['TITLE','ENERGY','CUR','SIGE','TEXT_MACHINE','SIGX','SIGY','SIGX1','SIGY1','TEXT_BEAM','PERIOD','NP','KX','KY','TEXT_UNDULATOR','EMIN','EMAX','N','TEXT_ENERGY','D','XPC','YPC','XPS','YPS','NXP','NYP','TEXT_PINHOLE','MODE','METHOD','IHARM','TEXT_MODE','NPHI','NALPHA','CALPHA2','NOMEGA','COMEGA','NSIGMA','TEXT_CALC','RUN_MODE_NAME']


    def compute(self):
        fileName = xoppy_calc_xus(TITLE=self.TITLE,ENERGY=self.ENERGY,CUR=self.CUR,SIGE=self.SIGE,TEXT_MACHINE=self.TEXT_MACHINE,SIGX=self.SIGX,SIGY=self.SIGY,SIGX1=self.SIGX1,SIGY1=self.SIGY1,TEXT_BEAM=self.TEXT_BEAM,PERIOD=self.PERIOD,NP=self.NP,KX=self.KX,KY=self.KY,TEXT_UNDULATOR=self.TEXT_UNDULATOR,EMIN=self.EMIN,EMAX=self.EMAX,N=self.N,TEXT_ENERGY=self.TEXT_ENERGY,D=self.D,XPC=self.XPC,YPC=self.YPC,XPS=self.XPS,YPS=self.YPS,NXP=self.NXP,NYP=self.NYP,TEXT_PINHOLE=self.TEXT_PINHOLE,MODE=self.MODE,METHOD=self.METHOD,IHARM=self.IHARM,TEXT_MODE=self.TEXT_MODE,NPHI=self.NPHI,NALPHA=self.NALPHA,CALPHA2=self.CALPHA2,NOMEGA=self.NOMEGA,COMEGA=self.COMEGA,NSIGMA=self.NSIGMA,TEXT_CALC=self.TEXT_CALC,RUN_MODE_NAME=self.RUN_MODE_NAME)
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
        xoppy_doc('xus')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxus()
    w.show()
    app.exec()
    w.saveSettings()
