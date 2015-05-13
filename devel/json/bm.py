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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_bm
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_bm")
    raise

class OWbm(widget.OWWidget):
    name = "bm"
    id = "orange.widgets.databm"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_bm.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "bm"]
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

    TYPE_CALC = Setting(0)
    MACHINE_NAME = Setting("ESRF bending magnet")
    RB_CHOICE = Setting(0)
    MACHINE_R_M = Setting(25.0)
    BFIELD_T = Setting(0.8)
    BEAM_ENERGY_GEV = Setting(6.0)
    CURRENT_A = Setting(0.1)
    HOR_DIV_MRAD = Setting(1.0)
    VER_DIV = Setting(0)
    PHOT_ENERGY_MIN = Setting(100.0)
    PHOT_ENERGY_MAX = Setting(100000.0)
    NPOINTS = Setting(500)
    LOG_CHOICE = Setting(1)
    PSI_MRAD_PLOT = Setting(1.0)
    PSI_MIN = Setting(-1.0)
    PSI_MAX = Setting(1.0)
    PSI_NPOINTS = Setting(500)


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
        gui.comboBox(box1, self, "TYPE_CALC",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Energy or Power spectra', 'Angular distribution (all wavelengths)', 'Angular distribution (one wavelength)', '2D flux and power (angular,energy) distribution'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MACHINE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "RB_CHOICE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Magnetic Radius', 'Magnetic Field'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MACHINE_R_M",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BFIELD_T",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BEAM_ENERGY_GEV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CURRENT_A",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HOR_DIV_MRAD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "VER_DIV",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Full (integrated in Psi)', 'At Psi=0', 'In [PsiMin,PsiMax]', 'At Psi=Psi_Min'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOT_ENERGY_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOT_ENERGY_MAX",
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
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "LOG_CHOICE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Lin', 'Log'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_MRAD_PLOT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PSI_NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Type of calculation','Machine name','B from:','Machine Radius [m]','Magnetic Field [T]','Beam energy [GeV]','Beam Current [A]','Horizontal div Theta [mrad]','Psi (vertical div) for energy spectra','Min Photon Energy [eV]','Max Photon Energy [eV]','Number of energy points','Separation between energy points','Max Psi[mrad] for angular plots','Psi min [mrad]','Psi max [mrad]','Number of Psi points']


    def unitFlags(self):
         return ['True','True','True','self.RB_CHOICE  ==  0','self.RB_CHOICE  ==  1','True','True','True','True','True','True','True','True','True','self.VER_DIV  >=  2','self.VER_DIV  ==  2','self.VER_DIV  ==  2']


    #def unitNames(self):
    #     return ['TYPE_CALC','MACHINE_NAME','RB_CHOICE','MACHINE_R_M','BFIELD_T','BEAM_ENERGY_GEV','CURRENT_A','HOR_DIV_MRAD','VER_DIV','PHOT_ENERGY_MIN','PHOT_ENERGY_MAX','NPOINTS','LOG_CHOICE','PSI_MRAD_PLOT','PSI_MIN','PSI_MAX','PSI_NPOINTS']


    def compute(self):
        fileName = xoppy_calc_bm(TYPE_CALC=self.TYPE_CALC,MACHINE_NAME=self.MACHINE_NAME,RB_CHOICE=self.RB_CHOICE,MACHINE_R_M=self.MACHINE_R_M,BFIELD_T=self.BFIELD_T,BEAM_ENERGY_GEV=self.BEAM_ENERGY_GEV,CURRENT_A=self.CURRENT_A,HOR_DIV_MRAD=self.HOR_DIV_MRAD,VER_DIV=self.VER_DIV,PHOT_ENERGY_MIN=self.PHOT_ENERGY_MIN,PHOT_ENERGY_MAX=self.PHOT_ENERGY_MAX,NPOINTS=self.NPOINTS,LOG_CHOICE=self.LOG_CHOICE,PSI_MRAD_PLOT=self.PSI_MRAD_PLOT,PSI_MIN=self.PSI_MIN,PSI_MAX=self.PSI_MAX,PSI_NPOINTS=self.PSI_NPOINTS)
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
        xoppy_doc('bm')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWbm()
    w.show()
    app.exec()
    w.saveSettings()
