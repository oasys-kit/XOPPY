import sys, os
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

class OWxinpro(XoppyWidget):
    name = "INPRO"
    id = "orange.widgets.dataxinpro"
    description = "Crystal Reflectivity (perfect)"
    icon = "icons/xoppy_xinpro.png"
    priority = 7
    category = ""
    keywords = ["xoppy", "xinpro"]

    CRYSTAL_MATERIAL = Setting(0)
    MODE = Setting(0)
    ENERGY = Setting(8000.0)
    MILLER_INDEX_H = Setting(1)
    MILLER_INDEX_K = Setting(1)
    MILLER_INDEX_L = Setting(1)
    ASYMMETRY_ANGLE = Setting(0.0)
    THICKNESS = Setting(500.0)
    TEMPERATURE = Setting(300.0)
    NPOINTS = Setting(100)
    SCALE = Setting(0)
    XFROM = Setting(-50.0)
    XTO = Setting(50.0)


    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Silicon', 'Germanium', 'Diamond', 'GaAs', 'GaP', 'InAs', 'InP', 'InSb', 'SiC', 'CsF', 'KCl', 'LiF', 'NaCl', 'Graphite', 'Beryllium'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MODE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Reflectivity in Bragg case', 'Transmission in Bragg case', 'Reflectivity in Laue case', 'Transmission in Laue case'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_H",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_L",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ASYMMETRY_ANGLE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THICKNESS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TEMPERATURE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCALE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Automatic', 'External'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "XFROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "XTO",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal material: ','Calculation mode:','Energy [eV]:','Miller index H:','Miller index K:','Miller index L:','Asymmetry angle:','Crystal thickness [microns]:','Crystal temperature [K]:','Number of points: ','Angular limits: ','Theta min [arcsec]:','Theta max [arcsec]:']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','self.SCALE  ==  1','self.SCALE  ==  1']


    def get_help_name(self):
        return 'inpro'

    def check_fields(self):
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Energy")
        self.MILLER_INDEX_H = congruence.checkNumber(self.MILLER_INDEX_H, "Miller index H")
        self.MILLER_INDEX_K = congruence.checkNumber(self.MILLER_INDEX_K, "Miller index K")
        self.MILLER_INDEX_L = congruence.checkNumber(self.MILLER_INDEX_L, "Miller index L")
        self.ASYMMETRY_ANGLE = congruence.checkNumber(self.ASYMMETRY_ANGLE, "Asymmetry angle")
        self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
        self.TEMPERATURE = congruence.checkNumber(self.TEMPERATURE, "Crystal temperature")
        self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.NPOINTS, "Number of points")
        
        if self.SCALE == 1:
            self.XFROM = congruence.checkNumber(self.XFROM, "Theta min")
            self.XTO = congruence.checkNumber(self.XTO, "Theta max")
            congruence.checkLessThan(self.XFROM, self.XTO, "Theta min", "Theta max")


    def do_xoppy_calculation(self):
        return xoppy_calc_xinpro(CRYSTAL_MATERIAL=self.CRYSTAL_MATERIAL,MODE=self.MODE,ENERGY=self.ENERGY,MILLER_INDEX_H=self.MILLER_INDEX_H,MILLER_INDEX_K=self.MILLER_INDEX_K,MILLER_INDEX_L=self.MILLER_INDEX_L,ASYMMETRY_ANGLE=self.ASYMMETRY_ANGLE,THICKNESS=self.THICKNESS,TEMPERATURE=self.TEMPERATURE,NPOINTS=self.NPOINTS,SCALE=self.SCALE,XFROM=self.XFROM,XTO=self.XTO)

    def get_data_exchange_widget_name(self):
        return "XINPRO"

    def add_specific_content_to_calculated_data(self, calculated_data):
        calculated_data.add_content("units_to_degrees",  0.000277777805)

    def getTitles(self):
        return ['s-polarized reflectivity', 'p-polarized reflectivity']

    def getXTitles(self):
        return ["Theta-ThetaB [arcsec]", "Theta-ThetaB [arcsec]"]

    def getYTitles(self):
        return ['s-polarized reflectivity', 'p-polarized reflectivity']

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2)]

    def getLogPlot(self):
        return [(False, False), (False, False)]

def xoppy_calc_xinpro(CRYSTAL_MATERIAL=0,MODE=0,ENERGY=8000.0,MILLER_INDEX_H=1,MILLER_INDEX_K=1,MILLER_INDEX_L=1,\
                      ASYMMETRY_ANGLE=0.0,THICKNESS=500.0,TEMPERATURE=300.0,NPOINTS=100,SCALE=0,XFROM=-50.0,XTO=50.0):
    print("Inside xoppy_calc_xinpro. ")

    try:
        with open("xoppy.inp", "wt") as f:
            f.write("%s\n"% (os.path.join(locations.home_data(), "inpro" + os.sep)))
            if MODE == 0:
                f.write("+1\n")
            elif MODE == 1:
                f.write("-1\n")
            elif MODE == 2:
                f.write("+2\n")
            elif MODE == 3:
                f.write("-1\n")
            else:
                f.write("ERROR!!\n")

            f.write("%f\n%d\n"%(THICKNESS,CRYSTAL_MATERIAL+1))
            f.write("%s\n%f\n"%("EV",ENERGY))
            f.write("%d\n%d\n%d\n"%(MILLER_INDEX_H,MILLER_INDEX_K,MILLER_INDEX_L))
            f.write("%f\n%f\n%s\n"%(ASYMMETRY_ANGLE,TEMPERATURE, "inpro.dat"))
            if SCALE == 0:
                f.write("1\n")
            else:
                f.write("%d\n%f\n%f\n"%(2,XFROM,XTO))
            f.write("%d\n"%(NPOINTS))


        for file in ["inpro.par","inpro.dat","inpro.spec"]:
            try:
                os.remove(os.path.join(locations.home_bin_run(),file))
            except:
                pass


        command = "'" + os.path.join(locations.home_bin(), 'inpro') + "' < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

        #add SPEC header
        txt = open("inpro.dat").read()
        outFile = "inpro.spec"

        f = open(outFile,"w")
        f.write("#F inpro.spec\n")
        f.write("\n")
        f.write("#S 1 inpro results\n")
        f.write("#N 3\n")
        f.write("#L Theta-TetaB  s-polarized reflectivity  p-polarized reflectivity\n")
        f.write(txt)
        f.close()
        print("File written to disk: inpro.dat, inpro.par, inpro.spec")

        #show calculated parameters in standard output
        txt_info = open("inpro.par").read()
        for line in txt_info:
            print(line,end="")


        return outFile
    except Exception as e:
        raise e




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxinpro()
    w.show()
    app.exec()
    w.saveSettings()
