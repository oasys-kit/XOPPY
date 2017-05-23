import sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import numpy
import scipy.constants as codata

class OWws(XoppyWidget):
    name = "WS"
    id = "orange.widgets.dataws"
    description = "Wiggler Spectrum on a Screen"
    icon = "icons/xoppy_ws.png"
    priority = 11
    category = ""
    keywords = ["xoppy", "ws"]

    ENERGY = Setting(7.0)
    CUR = Setting(100.0)
    PERIOD = Setting(8.5)
    N = Setting(28.0)
    KX = Setting(0.0)
    KY = Setting(8.74)
    EMIN = Setting(1000.0)
    EMAX = Setting(200000.0)
    NEE = Setting(500)
    D = Setting(30.0)
    XPC = Setting(0.0)
    YPC = Setting(0.0)
    XPS = Setting(2.0)
    YPS = Setting(2.0)
    NXP = Setting(10)
    NYP = Setting(10)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 


        #widget index 1
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "CUR",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "KX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "KY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NEE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "D",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NXP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NYP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['Beam energy (GeV)','Beam current (mA)','Period (cm)','Number of periods','Kx','Ky','Min energy (eV)','Max energy (eV)','Number of energy steps','Distance (m)','X-pos. (mm)','Y-pos. (mm)','X slit [mm or mrad]','Y slit [mm or mrad]','Integration points X','Integration points Y']

    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True']

    def get_help_name(self):
        return 'ws'

    def check_fields(self):
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Beam Energy")
        self.CUR = congruence.checkStrictlyPositiveNumber(self.CUR, "Beam Current")
        self.PERIOD = congruence.checkStrictlyPositiveNumber(self.PERIOD, "Period")
        self.N = congruence.checkStrictlyPositiveNumber(self.N, "Number of Periods")
        self.KX = congruence.checkNumber(self.KX, "Kx")
        self.KY = congruence.checkNumber(self.KY, "Ky")
        self.EMIN = congruence.checkPositiveNumber(self.EMIN, "Min Energy")
        self.EMAX = congruence.checkStrictlyPositiveNumber(self.EMAX, "Max Energy")
        congruence.checkLessThan(self.EMIN, self.EMAX, "Min Energy", "Max Energy")
        self.NEE = congruence.checkStrictlyPositiveNumber(self.NEE, "Number of energy steps")
        self.D = congruence.checkPositiveNumber(self.D, "Distance")
        self.XPC = congruence.checkNumber(self.XPC, "X-pos")
        self.YPC = congruence.checkNumber(self.YPC, "Y-pos")
        self.XPS = congruence.checkNumber(self.XPS, "X slit")
        self.YPS = congruence.checkNumber(self.YPS, "Y Slit")
        self.NXP = congruence.checkStrictlyPositiveNumber(self.NXP, "Integration points X")
        self.NYP = congruence.checkStrictlyPositiveNumber(self.NYP, "Integration points Y")

    def do_xoppy_calculation(self):
        return xoppy_calc_ws(ENERGY=self.ENERGY,CUR=self.CUR,PERIOD=self.PERIOD,N=self.N,KX=self.KX,KY=self.KY,EMIN=self.EMIN,EMAX=self.EMAX,NEE=self.NEE,D=self.D,XPC=self.XPC,YPC=self.YPC,XPS=self.XPS,YPS=self.YPS,NXP=self.NXP,NYP=self.NYP)

    def get_data_exchange_widget_name(self):
        return "WS"

    def getTitles(self):
        return ['Flux','Spectral power']

    def getXTitles(self):
        return ["Energy [eV]","Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Photons/sec/0.1%bw]","Spectral Power [W/eV]"]

    def getVariablesToPlot(self):
        return [(0, 1),(0, 2)]

    def getLogPlot(self):
        return [(True, True),(True, True)]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


def xoppy_calc_ws(ENERGY=7.0,CUR=100.0,PERIOD=8.5,N=28.0,KX=0.0,KY=8.739999771118164,\
                  EMIN=1000.0,EMAX=100000.0,NEE=2000,D=30.0,XPC=0.0,YPC=0.0,XPS=2.0,YPS=2.0,NXP=10,NYP=10):
    print("Inside xoppy_calc_ws. ")

    try:
        with open("ws.inp","wt") as f:
            f.write("inputs from xoppy \n")
            f.write("%f     %f\n"%(ENERGY,CUR))
            f.write("%f  %d  %f  %f\n"%(PERIOD,N,KX,KY))
            f.write("%f  %f   %d\n"%(EMIN,EMAX,NEE))
            f.write("%f  %f  %f  %f  %f  %d  %d\n"%(D,XPC,YPC,XPS,YPS,NXP,NYP))
            f.write("%d  \n"%(4))

        command = "'" + os.path.join(locations.home_bin(),'ws') + "'"
        print("Running command '%s' in directory: %s \n"%(command, locations.home_bin_run()))
        # TODO try to capture the text output of the external code
        os.system(command)

        # write spec file
        txt = open("ws.out").readlines()
        outFile = os.path.join(locations.home_bin_run(), "ws.spec")
        f = open(outFile,"w")

        f.write("#F ws.spec\n")
        f.write("\n")
        f.write("#S 1 ws results\n")
        f.write("#N 3\n")
        f.write("#L  Energy(eV)  Flux(photons/s/0.1%bw)  Spectral power(W/eV)\n")
        for i in txt:
            tmp = i.strip(" ")
            if tmp[0].isdigit():
                tmp1 = numpy.fromstring(tmp, dtype=float, sep=' ')
                f.write("%f %f %f \n"%(tmp1[0],tmp1[1],tmp1[1]*codata.e*1e3))
            else:
               f.write("#UD "+tmp)
        f.close()
        print("File written to disk: ws.spec")

        # print output file
        # for line in txt:
        #     print(line, end="")
        print("Results written to file: %s"%os.path.join(locations.home_bin_run(),'ws.out'))

        return outFile
    except Exception as e:
        raise e



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWws()
    w.show()
    app.exec()
    w.saveSettings()
