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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xcrystal
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xcrystal")
    raise

class OWxcrystal(widget.OWWidget):
    name = "xcrystal"
    id = "orange.widgets.dataxcrystal"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xcrystal.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xcrystal"]
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
    CRYSTAL_MATERIAL = Setting(0)
    MILLER_INDEX_H = Setting(1)
    MILLER_INDEX_K = Setting(1)
    MILLER_INDEX_L = Setting(1)
    I_ABSORP = Setting(2)
    TEMPER = Setting("1.0")
    MOSAIC = Setting(0)
    GEOMETRY = Setting(0)
    SCAN = Setting(2)
    UNIT = Setting(1)
    SCANFROM = Setting(-100.0)
    SCANTO = Setting(100.0)
    SCANPOINTS = Setting(200)
    ENERGY = Setting(8000.0)
    ASYMMETRY_ANGLE = Setting(0.0)
    THICKNESS = Setting(0.7)
    MOSAIC_FWHM = Setting(0.1)
    RSAG = Setting(125.0)
    RMER = Setting(1290.0)
    ANISOTROPY = Setting(0)
    POISSON = Setting(0.22)
    CUT = Setting("2 -1 -1 ; 1 1 1 ; 0 0 0")
    FILECOMPLIANCE = Setting("mycompliance.dat")


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
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Si', 'Si_NIST', 'Si2', 'Ge', 'Diamond', 'GaAs', 'GaSb', 'GaP', 'InAs', 'InP', 'InSb', 'SiC', 'NaCl', 'CsF', 'LiF', 'KCl', 'CsCl', 'Be', 'Graphite', 'PET', 'Beryl', 'KAP', 'RbAP', 'TlAP', 'Muscovite', 'AlphaQuartz', 'Copper', 'LiNbO3', 'Platinum', 'Gold', 'Sapphire', 'LaB6', 'LaB6_NIST', 'KTP', 'AlphaAlumina', 'Aluminum', 'Iron', 'Titanium'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_INDEX_H",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_INDEX_K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_INDEX_L",
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
        gui.comboBox(box1, self, "MOSAIC",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Perfect crystal', 'Mosaic', 'Bent Crystal ML', 'Bent Crystal PP'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GEOMETRY",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['BRAGG: diffr beam', 'LAUE: diffr beam', 'BRAGG: transm beam', 'LAUE: transm beam'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCAN",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Theta (absolute)', 'Th - ThBragg(corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "UNIT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Radians', 'micro rads', 'Degrees', 'ArcSec'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SCANFROM",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SCANTO",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SCANPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ASYMMETRY_ANGLE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THICKNESS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MOSAIC_FWHM",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "RSAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "RMER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ANISOTROPY",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['None (isotropic)', 'Default cut', 'Cut directions', 'From file'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "POISSON",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CUT",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILECOMPLIANCE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['DABAX f0 file:','DABAX f1f2 file:','DABAX CrossSec file:','Crystal:','h Miller index','k Miller index','l Miller index','Include absorption:','Temperature factor [see help]:','Crystal Model:','Geometry:','Scan:','Scan Units:','Min Scan value:','Max Scan value:','Scan Points:','Fix value (E[eV] or Theta[deg])','Asymmetry angle [deg] (to surf.)','Crystal Thickness [cm]:','Mosaicity [deg, fwhm]: ','R sagittal [cm]: ','R meridional [cm]: ','Anisotropy: ','Poisson ratio','Valong ; Vnorm ; Vperp','File (compliance tensor)']


    def unitFlags(self):
         return ['True','self.I_ABSORP  >  0','self.I_ABSORP  >  1','True','True','True','True','True','True','True','True','True','self.SCAN  <=  2','True','True','True','True','(self.MOSAIC  ==  0) OR (self.MOSAIC  >  1)','True','self.MOSAIC  ==  1','self.MOSAIC  >  1','self.MOSAIC  >  1','self.MOSAIC  >  1','self.MOSAIC  >  1  &  self.ANISOTROPY  ==  0','self.MOSAIC  >  1  &  self.ANISOTROPY  ==  2','self.MOSAIC  >  1  &  self.ANISOTROPY  ==  3']


    #def unitNames(self):
    #     return ['FILEF0','FILEF1F2','FILECROSSSEC','CRYSTAL_MATERIAL','MILLER_INDEX_H','MILLER_INDEX_K','MILLER_INDEX_L','I_ABSORP','TEMPER','MOSAIC','GEOMETRY','SCAN','UNIT','SCANFROM','SCANTO','SCANPOINTS','ENERGY','ASYMMETRY_ANGLE','THICKNESS','MOSAIC_FWHM','RSAG','RMER','ANISOTROPY','POISSON','CUT','FILECOMPLIANCE']


    def compute(self):
        fileName = xoppy_calc_xcrystal(FILEF0=self.FILEF0,FILEF1F2=self.FILEF1F2,FILECROSSSEC=self.FILECROSSSEC,CRYSTAL_MATERIAL=self.CRYSTAL_MATERIAL,MILLER_INDEX_H=self.MILLER_INDEX_H,MILLER_INDEX_K=self.MILLER_INDEX_K,MILLER_INDEX_L=self.MILLER_INDEX_L,I_ABSORP=self.I_ABSORP,TEMPER=self.TEMPER,MOSAIC=self.MOSAIC,GEOMETRY=self.GEOMETRY,SCAN=self.SCAN,UNIT=self.UNIT,SCANFROM=self.SCANFROM,SCANTO=self.SCANTO,SCANPOINTS=self.SCANPOINTS,ENERGY=self.ENERGY,ASYMMETRY_ANGLE=self.ASYMMETRY_ANGLE,THICKNESS=self.THICKNESS,MOSAIC_FWHM=self.MOSAIC_FWHM,RSAG=self.RSAG,RMER=self.RMER,ANISOTROPY=self.ANISOTROPY,POISSON=self.POISSON,CUT=self.CUT,FILECOMPLIANCE=self.FILECOMPLIANCE)
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
        xoppy_doc('xcrystal')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxcrystal()
    w.show()
    app.exec()
    w.saveSettings()
