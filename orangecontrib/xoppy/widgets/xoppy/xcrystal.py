import sys
import os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util import xoppy_util
from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.xoppy.xoppy_xraylib_util import bragg_calc

from oasys.widgets.exchange import DataExchangeObject
from xraylib import Crystal_GetCrystalsList

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
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    CRYSTAL_MATERIAL = Setting(0)
    MILLER_INDEX_H = Setting(1)
    MILLER_INDEX_K = Setting(1)
    MILLER_INDEX_L = Setting(1)
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

        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=Crystal_GetCrystalsList(),
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
         return ['Crystal:','h Miller index','k Miller index','l Miller index','Temperature factor [see help]:', # 0-5
                 'Crystal Model:','Geometry:','Scan:','Scan Units:','Min Scan value:','Max Scan value:','Scan Points:', # 6-12
                 'Fix value (E[eV] or Theta[deg])','Asymmetry angle [deg] (to surf.)','Crystal Thickness [cm]:', # 13-15
                 'Mosaicity [deg, fwhm]: ', #16
                 'R sagittal [cm]: ','R meridional [cm]: ','Anisotropy: ','Poisson ratio','Valong ; Vnorm ; Vperp','File (compliance tensor)']


    def unitFlags(self):
         return ['True','True','True','True','True',
                 'True','True','True','self.SCAN  <=  2','True','True','True',
                 'True','(self.MOSAIC  ==  0) or (self.MOSAIC  >  1)','True',
                 'self.MOSAIC  ==  1',
                 'self.MOSAIC  >  1','self.MOSAIC  >  1','self.MOSAIC  >  1','self.MOSAIC  >  1  and  self.ANISOTROPY  ==  0','self.MOSAIC  >  1  and  self.ANISOTROPY  ==  2','self.MOSAIC  >  1  and  self.ANISOTROPY  ==  3']

    def compute(self):

        CRYSTAL_MATERIAL = self.CRYSTAL_MATERIAL
        MILLER_INDEX_H = self.MILLER_INDEX_H
        MILLER_INDEX_K = self.MILLER_INDEX_K
        MILLER_INDEX_L = self.MILLER_INDEX_L
        TEMPER = self.TEMPER
        MOSAIC = self.MOSAIC
        GEOMETRY = self.GEOMETRY
        SCAN = self.SCAN
        UNIT = self.UNIT
        SCANFROM = self.SCANFROM
        SCANTO = self.SCANTO
        SCANPOINTS = self.SCANPOINTS
        ENERGY = self.ENERGY
        ASYMMETRY_ANGLE = self.ASYMMETRY_ANGLE
        THICKNESS = self.THICKNESS
        MOSAIC_FWHM = self.MOSAIC_FWHM
        RSAG = self.RSAG
        RMER = self.RMER
        ANISOTROPY = self.ANISOTROPY
        POISSON = self.POISSON
        CUT = self.CUT
        FILECOMPLIANCE = self.FILECOMPLIANCE

        if (GEOMETRY == 1) or (GEOMETRY == 3):
            if ASYMMETRY_ANGLE == 0.0:
                print("xoppy_calc_xcrystal: WARNING: In xcrystal the asymmetry angle is the angle between Bragg planes and crystal surface,"+
                      "in BOTH Bragg and Laue geometries.")


        descriptor = Crystal_GetCrystalsList()[CRYSTAL_MATERIAL]
        if SCAN == 3: # energy scan
            emin = SCANFROM - 1
            emax = SCANTO + 1
        else:
            emin = ENERGY - 100.0
            emax = ENERGY + 100.0

        print("Using crystal descriptor: ",descriptor)
        bragg_dictionary = bragg_calc(descriptor=descriptor,
                                                hh=MILLER_INDEX_H,kk=MILLER_INDEX_K,ll=MILLER_INDEX_L,
                                                temper=float(TEMPER),
                                                emin=emin,emax=emax,estep=5.0,fileout="xcrystal.bra")

        with open("xoppy.inp", "wt") as f:
            f.write("xcrystal.bra\n")
            f.write("%d\n"%MOSAIC)
            f.write("%d\n"%GEOMETRY)

            if MOSAIC == 1:
                f.write("%g\n"%MOSAIC_FWHM)
                f.write("%g\n"%THICKNESS)
            else:
                f.write("%g\n"%THICKNESS)
                f.write("%g\n"%ASYMMETRY_ANGLE)

            scan_flag = 1 + SCAN

            f.write("%d\n"%scan_flag)

            f.write("%19.9f\n"%ENERGY)

            if scan_flag <= 3:
                f.write("%d\n"%UNIT)

            f.write("%g\n"%SCANFROM)
            f.write("%g\n"%SCANTO)
            f.write("%d\n"%SCANPOINTS)

            if MOSAIC > 1: # bent
                f.write("%g\n"%RSAG)
                f.write("%g\n"%RMER)
                f.write("%0\n")

                if CRYSTAL_MATERIAL >=  5: # not Si,Ge,Diamond
                    if ((ANISOTROPY == 1) or (ANISOTROPY == 2)):
                        raise Exception("Anisotropy data not available for this crystal. Either use isotropic or use external compliance file. Please change and run again'")

                f.write("%d\n"%ANISOTROPY)

                if ANISOTROPY == 0:
                    f.write("%g\n"%POISSON)
                elif ANISOTROPY == 1:
                    f.write("%d\n"%CRYSTAL_MATERIAL)
                    f.write("%g\n"%ASYMMETRY_ANGLE)
                    f.write("%d\n"%MILLER_INDEX_H)
                    f.write("%d\n"%MILLER_INDEX_K)
                    f.write("%d\n"%MILLER_INDEX_L)
                elif ANISOTROPY == 2:
                    f.write("%d\n"%CRYSTAL_MATERIAL)
                    f.write("%g\n"%ASYMMETRY_ANGLE)
                    # TODO: check syntax for CUT: Cut syntax is: valong_X valong_Y valong_Z ; vnorm_X vnorm_Y vnorm_Z ; vperp_x vperp_Y vperp_Z
                    f.write("%s\n"%CUT.split(";")[0])
                    f.write("%s\n"%CUT.split(";")[1])
                    f.write("%s\n"%CUT.split(";")[2])
                elif ANISOTROPY == 3:
                    f.write("%s\n"%FILECOMPLIANCE)


        command = os.path.join(locations.home_bin(), 'diff_pat') + " < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")


        #send exchange
        tmp = DataExchangeObject("xoppy_xcrystal","xcrystal")

        try:
            tmp.add_content("data",numpy.loadtxt("diff_pat.dat",skiprows=5).T)
            tmp.add_content("plot_x_col",0)
            tmp.add_content("plot_y_col",-1)
        except:
            pass
        try:
            tmp.add_content("labels",["Th-ThB{in} [microrad]","Th-ThB{out} [microrad]","phase_p[rad]","phase_s[rad]","Circ Polariz","p-polarized reflectivity","s-polarized reflectivity"
])

        except:
            pass
        try:
            with open("diff_pat.par") as f:
                info = f.readlines()
            tmp.add_content("info",info)
        except:
            pass

        self.send("ExchangeData",tmp)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xcrystal')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxcrystal()
    w.show()
    app.exec()
    w.saveSettings()
