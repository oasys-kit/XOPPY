import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np


try:
    from orangecontrib.xoppy.util.xsh_calc import calc_xshwig
except ImportError:
    print("compute pressed.")
    print("Error importing: xsh_calc_xshwig")
    raise

class OWxshwig(widget.OWWidget):
    name = "xshwig"
    id = "orange.widgets.dataxshwig"
    description = "xoppy application to compute..."
    icon = "icons/xshwig.jpg"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xshwig"]
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

    BENER = Setting(2.01)
    USERUNIT = Setting(1)
    FLAG_EMITTANCE = Setting(1)
    SIGMAX = Setting(0.0056)
    SIGMAZ = Setting(0.0005)
    EPSI_X = Setting(2.88e-07)
    EPSI_Z = Setting(2.88e-09)
    EPSI_DX = Setting(0.0)
    EPSI_DZ = Setting(0.0)
    WIGGLER_TYPE = Setting(0)
    PERIODS = Setting(50)
    K = Setting(7.85)
    WAVLEN = Setting(0.04)
    FILE_B = Setting("wiggler.b")
    FILE_H = Setting("wiggler.h")
    NPOINT = Setting(5000)
    ISTAR1 = Setting(5676561)
    PH1 = Setting(10000.0)
    PH2 = Setting(10010.0)
    F_BOUND_SOUR = Setting(0)
    FILE_BOUND = Setting("NONESPECIFIED")
    NTOTALPOINT = Setting(10000000)
    SLIT_DISTANCE = Setting(1000.0)
    SLIT_XMIN = Setting(-1.0)
    SLIT_XMAX = Setting(1.0)
    SLIT_ZMIN = Setting(-1.0)
    SLIT_ZMAX = Setting(1.0)


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
        gui.lineEdit(box1, self, "BENER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box)

        gui.comboBox(box1, self, "USERUNIT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['mm', 'cm', 'm'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 1b (added by hand)
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "FLAG_EMITTANCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['No', 'Yes'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGMAZ",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EPSI_X",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EPSI_Z",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EPSI_DX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EPSI_DZ",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "WIGGLER_TYPE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['conventional/sinusoidal', 'B from file', 'B from harmonics'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PERIODS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "WAVLEN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE_B",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE_H",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ISTAR1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PH1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PH2",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "F_BOUND_SOUR",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['No', 'Using file with phase space volume', 'Using slit/acceptance'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE_BOUND",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NTOTALPOINT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SLIT_DISTANCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SLIT_XMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SLIT_XMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SLIT_ZMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SLIT_ZMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Electron Energy [GeV]','User unit (length)','Use emittances','Sigma X [user unit]','Sigma Z [user unit]','Emittance X [rad.user unit]','Emittance Z [rad.user unit]','Distance from X waist [user unit]','Distance from Z waist [user unit]', 'Type','Number of periods','K value','ID period [m]','file with B vs Y','file with harmonics', 'Number of rays','Seed (0=clock)','Photon energy from [eV]','Photon energy to [eV]','Optimize source (reject rays)','File with phase space volume','Max number of rejected rays (set 0 for infinity)','Slit distance [user unit] (set 0 for angular acceptance)','Min X [user unit] (or min Xp if distance=0)','Max X [user unit] (or max Xp if distance=0)','Min Z [user unit] (or min Zp if distance=0)','Max Z [user unit] (or max Zp if distance=0)']


    def unitFlags(self):
         return ['True','True','True','self.FLAG_EMITTANCE == 1','self.FLAG_EMITTANCE == 1','self.FLAG_EMITTANCE == 1','self.FLAG_EMITTANCE == 1','self.FLAG_EMITTANCE == 1','self.FLAG_EMITTANCE == 1', 'True','True','self.WIGGLER_TYPE == 0','self.WIGGLER_TYPE != 1','self.WIGGLER_TYPE == 1','self.WIGGLER_TYPE == 2', 'True','True','True','True', 'True','self.F_BOUND_SOUR == 1','self.F_BOUND_SOUR != 0','self.F_BOUND_SOUR == 2','self.F_BOUND_SOUR == 2','self.F_BOUND_SOUR == 2','self.F_BOUND_SOUR == 2','self.F_BOUND_SOUR == 2']


    #def unitNames(self):
    #     return ["BENER", "FLAG_EMITTANCE", "SIGMAX", "SIGMAZ", "EPSI_X", "EPSI_Z", "EPSI_DX", "EPSI_DZ", "WIGGLER_TYPE", "PERIODS", "K", "WAVLEN", "FILE_B", "FILE_H", "NPOINT", "ISTAR1", "PH1", "PH2", "F_BOUND_SOUR", "FILE_BOUND", "NTOTALPOINT", "SLIT_DISTANCE", "SLIT_XMIN", "SLIT_XMAX", "SLIT_ZMIN", "SLIT_ZMAX"]


    def compute(self):
        tmp = calc_xshwig(BENER=self.BENER,USERUNIT=self.USERUNIT,FLAG_EMITTANCE=self.FLAG_EMITTANCE,SIGMAX=self.SIGMAX,SIGMAZ=self.SIGMAZ,EPSI_X=self.EPSI_X,EPSI_Z=self.EPSI_Z,EPSI_DX=self.EPSI_DX,EPSI_DZ=self.EPSI_DZ,WIGGLER_TYPE=self.WIGGLER_TYPE,PERIODS=self.PERIODS,K=self.K,WAVLEN=self.WAVLEN,FILE_B=self.FILE_B,FILE_H=self.FILE_H,NPOINT=self.NPOINT,ISTAR1=self.ISTAR1,PH1=self.PH1,PH2=self.PH2,F_BOUND_SOUR=self.F_BOUND_SOUR,FILE_BOUND=self.FILE_BOUND,NTOTALPOINT=self.NTOTALPOINT,SLIT_DISTANCE=self.SLIT_DISTANCE,SLIT_XMIN=self.SLIT_XMIN,SLIT_XMAX=self.SLIT_XMAX,SLIT_ZMIN=self.SLIT_ZMIN,SLIT_ZMAX=self.SLIT_ZMAX)
        #send specfile
        #self.send("xsh__specfile",fileName)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        #xoppy_doc('xshwig')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxshwig()
    w.show()
    app.exec()
    w.saveSettings()
