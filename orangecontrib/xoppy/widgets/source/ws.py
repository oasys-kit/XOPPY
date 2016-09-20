import sys, os
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui

from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import numpy
import scipy.constants as codata

class OWws(XoppyWidget):
    name = "ws"
    id = "orange.widgets.dataws"
    description = "xoppy application to compute the wigggler spectrum over a screen"
    icon = "icons/xoppy_ws.png"
    priority = 5
    category = ""
    keywords = ["xoppy", "ws"]

    TITLE = Setting("Wiggler A at APS")
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

        box = oasysgui.widgetBox(self.controlArea, "WIGGLER Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=True, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CUR",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NEE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "D",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NXP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NYP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['Title','Beam energy (GeV)','Beam current (mA)','Period (cm)','Number of periods','Kx','Ky','Min energy (eV)','Max energy (eV)','Number of energy steps','Distance (m)','X-pos. (mm)','Y-pos. (mm)','X slit [mm or mrad]','Y slit [mm or mrad]','Integration points X','Integration points Y']

    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True']

    def get_help_name(self):
        return 'ws'

    def check_fields(self):
        pass

    def do_xoppy_calculation(self):
        return xoppy_calc_ws(TITLE=self.TITLE,ENERGY=self.ENERGY,CUR=self.CUR,PERIOD=self.PERIOD,N=self.N,KX=self.KX,KY=self.KY,EMIN=self.EMIN,EMAX=self.EMAX,NEE=self.NEE,D=self.D,XPC=self.XPC,YPC=self.YPC,XPS=self.XPS,YPS=self.YPS,NXP=self.NXP,NYP=self.NYP)

    def get_data_exchange_widget_name(self):
        return "WS"

    def getTitles(self):
        return ['Flux']

    def getXTitles(self):
        return ["Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Photons/sec/0.1%bw]"]

    def getVariablesToPlot(self):
        return [(0, 1)]

    def getLogPlot(self):
        return [(True, True)]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


def xoppy_calc_ws(TITLE="Wiggler A at APS",ENERGY=7.0,CUR=100.0,PERIOD=8.5,N=28.0,KX=0.0,KY=8.739999771118164,\
                  EMIN=1000.0,EMAX=100000.0,NEE=2000,D=30.0,XPC=0.0,YPC=0.0,XPS=2.0,YPS=2.0,NXP=10,NYP=10):
    print("Inside xoppy_calc_ws. ")

    try:
        with open("ws.inp","wt") as f:
            f.write("%s\n"%(TITLE))
            f.write("%f     %f\n"%(ENERGY,CUR))
            f.write("%f  %d  %f  %f\n"%(PERIOD,N,KX,KY))
            f.write("%f  %f   %d\n"%(EMIN,EMAX,NEE))
            f.write("%f  %f  %f  %f  %f  %d  %d\n"%(D,XPC,YPC,XPS,YPS,NXP,NYP))
            f.write("%d  \n"%(4))

        command = os.path.join(locations.home_bin(),'ws')
        print("Running command '%s' in directory: %s \n"%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

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

        return outFile
    except Exception as e:
        raise e



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWws()
    w.show()
    app.exec()
    w.saveSettings()
