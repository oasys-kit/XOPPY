import sys
import os
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.util.xoppy_xraylib_util import bragg_calc

from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xraylib import Crystal_GetCrystalsList

class OWxcrystal(XoppyWidget):
    name = "CRYSTAL"
    id = "orange.widgets.dataxcrystal"
    description = "Crystal Reflectivity (perfect, bent, mosaic)"
    icon = "icons/xoppy_xcrystal.png"
    priority = 5
    category = ""
    keywords = ["xoppy", "xcrystal"]
 
    CRYSTAL_MATERIAL = Setting(32)
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

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=Crystal_GetCrystalsList(),
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_H",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_L",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TEMPER",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MOSAIC",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Perfect crystal', 'Mosaic', 'Bent Crystal ML', 'Bent Crystal PP'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GEOMETRY",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['BRAGG: diffr beam', 'LAUE: diffr beam', 'BRAGG: transm beam', 'LAUE: transm beam'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCAN",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.unit_combo = gui.comboBox(box1, self, "UNIT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Radians', 'micro rads', 'Degrees', 'ArcSec'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANFROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANTO",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ASYMMETRY_ANGLE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THICKNESS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MOSAIC_FWHM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "RSAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "RMER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ANISOTROPY",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['None (isotropic)', 'Default cut', 'Cut directions', 'From file'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "POISSON",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "CUT",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box)

        file_box = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file_compliance = oasysgui.lineEdit(file_box, self, "FILECOMPLIANCE",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        gui.button(file_box, self, "...", callback=self.selectFile)

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

    def get_help_name(self):
        return 'crystal'

    def selectFile(self):
        self.le_file_compliance.setText(oasysgui.selectFileFromDialog(self, self.FILECOMPLIANCE, "Open File (compliance tensor)", file_extension_filter="*.dat *.txt"))


    def check_fields(self):
        self.MILLER_INDEX_H = congruence.checkNumber(self.MILLER_INDEX_H, "Miller index H")
        self.MILLER_INDEX_K = congruence.checkNumber(self.MILLER_INDEX_K, "Miller index K")
        self.MILLER_INDEX_L = congruence.checkNumber(self.MILLER_INDEX_L, "Miller index L")
        self.TEMPER = congruence.checkNumber(self.TEMPER, "Temperature factor")

        if self.SCAN == 0 or self.SCAN == 3:
            self.SCANFROM = congruence.checkPositiveNumber(self.SCANFROM, "Min Scan value")
            self.SCANTO = congruence.checkStrictlyPositiveNumber(self.SCANTO, "Max Scan value")
        else:
            self.SCANFROM = congruence.checkNumber(self.SCANFROM, "Min Scan value")
            self.SCANTO = congruence.checkNumber(self.SCANTO, "Max Scan value")

        congruence.checkLessThan(self.SCANFROM, self.SCANTO, "Min Scan value", "Max Scan value")
        self.SCANPOINTS = congruence.checkStrictlyPositiveNumber(self.SCANPOINTS, "Scan points")

        if self.SCAN < 4:
            self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY , "Fix value")
        else:
            self.ENERGY = congruence.checkNumber(self.ENERGY , "Fix value")

        if self.MOSAIC == 0: #perfect
            self.ASYMMETRY_ANGLE = congruence.checkNumber(self.ASYMMETRY_ANGLE, "Asymmetry angle")
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
        elif self.MOSAIC == 1: #mosaic
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
            self.MOSAIC_FWHM = congruence.checkNumber(self.MOSAIC_FWHM, "Mosaicity")
        elif self.MOSAIC == 2 or self.MOSAIC == 3: #bent ML/PP
            self.ASYMMETRY_ANGLE = congruence.checkNumber(self.ASYMMETRY_ANGLE, "Asymmetry angle")
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
            self.RSAG = congruence.checkStrictlyPositiveNumber(self.RSAG, "R Sagittal")
            self.RMER = congruence.checkStrictlyPositiveNumber(self.RMER, "R meridional")

            if self.ANISOTROPY == 0:
                self.POISSON = congruence.checkStrictlyPositiveNumber(self.POISSON, "Poisson Ratio")
            elif self.ANISOTROPY == 2:
                congruence.checkEmptyString(self.CUT, "Valong; Vnorm; Vperp")
            elif self.ANISOTROPY == 3:
                congruence.checkFile(self.FILECOMPLIANCE)


    def do_xoppy_calculation(self):
        return self.xoppy_calc_xcrystal()

    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def get_data_exchange_widget_name(self):
        return "XCRYSTAL"

    def getTitles(self):
        return ["Phase_p","Phase_s","Circ. Polariz.","p-polarized reflectivity","s-polarized reflectivity"]

    def getXTitles(self):
        if self.SCAN < 4:
            return ["Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]"]
        elif self.SCAN ==4:
            return ["Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]"]
        else:
            return ["y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)"]


    def getYTitles(self):
        return ["phase_p [rad]","phase_s [rad]","Circ. Polariz.","p-polarized reflectivity","s-polarized reflectivity"]

    def getVariablesToPlot(self):
        return [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]

    def getLogPlot(self):
        return[(False, False), (False, False), (False, False), (False, False), (False, False)]

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):
        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        # ALLOW FIT BUTTON HERE
        self.plot_canvas[plot_canvas_index].fitAction.setVisible(True)

        # overwrite FWHM and peak values
        if title == "s-polarized reflectivity" or title == "p-polarized reflectivity":
            t = numpy.where(y>=max(y)*0.5)
            x_left,x_right =  x[t[0][0]], x[t[0][-1]]


            self.plot_canvas[plot_canvas_index].addMarker(x_left, 0.5, legend="G1", text="FWHM=%5.2f"%(x_right-x_left),
                                                          color="pink",selectable=False, draggable=False,
                                                          symbol="+", constraint=None)
            self.plot_canvas[plot_canvas_index].addMarker(x_right, 0.5, legend="G2", text=None, color="pink",
                                                          selectable=False, draggable=False, symbol="+", constraint=None)

            index_ymax = numpy.argmax(y)
            self.plot_canvas[plot_canvas_index].addMarker(x[index_ymax], y[index_ymax], legend="G3",
                                                          text=None, color="pink",
                                                          selectable=False, draggable=False, symbol="+", constraint=None)
            self.plot_canvas[plot_canvas_index].addMarker(x[index_ymax], y[index_ymax]-0.05, legend="G4",
                                                          text="Peak=%5.2f"%(y[index_ymax]), color="pink",
                                                          selectable=False, draggable=False, symbol=None, constraint=None)

    def xoppy_calc_xcrystal(self):
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


        for file in ["diff_pat.dat","diff_pat.gle","diff_pat.par","diff_pat.xop","xcrystal.bra"]:
            try:
                os.remove(os.path.join(locations.home_bin_run(),file))
            except:
                pass


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
                f.write("0\n")

                if ( (descriptor == "Si") or (descriptor == "Si2") or (descriptor == "Si_NIST") or (descriptor == "Ge") or descriptor == "Diamond"):
                    pass
                else:  # not Si,Ge,Diamond
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



        command = "'" + os.path.join(locations.home_bin(), 'diff_pat') + "' < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")
        
        #show calculated parameters in standard output
        txt_info = open("diff_pat.par").read()
        for line in txt_info:
            print(line,end="")


        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", numpy.loadtxt("diff_pat.dat", skiprows=5))
            calculated_data.add_content("plot_x_col",0)
            calculated_data.add_content("plot_y_col",-1)
            calculated_data.add_content("units_to_degrees", self.get_units_to_degrees())
        except Exception as e:
            raise Exception("Error loading diff_pat.dat :" + str(e))

        try:
            calculated_data.add_content("labels",
                                        ["Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                                         "Th-ThB{out} [" + self.unit_combo.itemText(self.UNIT) + "]",
                                         "phase_p[rad]",
                                         "phase_s[rad]","Circ Polariz",
                                         "p-polarized reflectivity",
                                         "s-polarized reflectivity"])

        except:
            pass

        try:
            with open("diff_pat.par") as f:
                info = f.readlines()
            calculated_data.add_content("info",info)
        except:
            pass

        return calculated_data


    def get_units_to_degrees(self):
        if self.UNIT == 0: # RADIANS
            return 57.2957795
        elif self.UNIT == 1: #MICRORADIANS
            return 57.2957795e-6
        elif self.UNIT == 2: # DEGREES
            return 1.0
        elif self.UNIT == 3: # ARCSEC
            return 0.000277777805






if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxcrystal()
    w.show()
    app.exec()
    w.saveSettings()
