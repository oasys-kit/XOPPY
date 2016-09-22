import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from PyMca5.PyMcaIO import specfilewrapper as specfile
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui

from srxraylib.sources import srfunc

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

class OWxwiggler(XoppyWidget):
    name = "xwiggler"
    id = "orange.widgets.dataxwiggler"
    description = "xoppy application to compute XWIGGLER"
    icon = "icons/xoppy_xwiggler.png"
    priority = 6
    category = ""
    keywords = ["xoppy", "xwiggler"]

    FIELD = Setting(0)
    NPERIODS = Setting(12)
    ULAMBDA = Setting(0.125)
    K = Setting(14.0)
    ENERGY = Setting(6.04)
    PHOT_ENERGY_MIN = Setting(100.0)
    PHOT_ENERGY_MAX = Setting(100100.0)
    NPOINTS = Setting(100)
    LOGPLOT = Setting(1)
    NTRAJPOINTS = Setting(101)
    CURRENT = Setting(200.0)
    FILE = Setting("?")

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, "WIGGLER Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "FIELD",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Sinusoidal', 'B from file', 'B from harmonics'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ULAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOT_ENERGY_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOT_ENERGY_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "LOGPLOT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Lin', 'Log'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NTRAJPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['Magnetic field: ','Number of periods','Wiggler period [m]','K value','Beam energy [GeV]','Min Photon Energy [eV]','Max Photon Energy [eV]','Number of energy points','Energy points spacing','Number of traj points per period','Electron Beam Current [mA]','File with Magnetic Field']

    def unitFlags(self):
         return ['True','True','self.FIELD  !=  1','self.FIELD  ==  0','True','True','True','True','True','self.FIELD  !=  1','True','self.FIELD  !=  0']


    def get_help_name(self):
        return 'xwiggler'

    def check_fields(self):
        pass

    def do_xoppy_calculation(self):
        return xoppy_calc_xwiggler(FIELD=self.FIELD,NPERIODS=self.NPERIODS,ULAMBDA=self.ULAMBDA,K=self.K,ENERGY=self.ENERGY,PHOT_ENERGY_MIN=self.PHOT_ENERGY_MIN,PHOT_ENERGY_MAX=self.PHOT_ENERGY_MAX,NPOINTS=self.NPOINTS,LOGPLOT=self.LOGPLOT,NTRAJPOINTS=self.NTRAJPOINTS,CURRENT=self.CURRENT,FILE=self.FILE)

    def add_specific_content_to_calculated_data(self, calculated_data):
        calculated_data.add_content("is_log_plot", self.LOGPLOT)

    def get_data_exchange_widget_name(self):
        return "XWIGGLER"

    def getTitles(self):
        return ['Flux','Spectral Power']

    def getXTitles(self):
        return ["Energy [eV]","Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Phot/sec/0.1%bw]","Spectral Power [W/eV]"]

    def getLogPlot(self):
        return [(True, True),(True, True)]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2)]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def xoppy_calc_xwiggler(FIELD=0,NPERIODS=12,ULAMBDA=0.125,K=14.0,ENERGY=6.04,PHOT_ENERGY_MIN=100.0,\
                        PHOT_ENERGY_MAX=100100.0,NPOINTS=100,LOGPLOT=1,NTRAJPOINTS=101,CURRENT=200.0,FILE="?"):

    print("Inside xoppy_calc_xwiggler. ")

    outFileTraj = "xwiggler_traj.spec"
    outFile = "xwiggler.spec"

    if FIELD == 0:
        t0,p = srfunc.wiggler_trajectory(b_from=0, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS, \
                                         ener_gev=ENERGY, per=ULAMBDA, kValue=K, \
                                         trajFile=outFileTraj)
    if FIELD == 1:
        # magnetic field from B(s) map
        t0,p = srfunc.wiggler_trajectory(b_from=1, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS, \
                                         ener_gev=ENERGY, inData=FILE, trajFile=outFileTraj)
    if FIELD == 2:
        # magnetic field from harmonics
        # hh = srfunc.wiggler_harmonics(b_t,Nh=41,fileOutH="tmp.h")
        t0,p = srfunc.wiggler_trajectory(b_from=2, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS, \
                                         ener_gev=ENERGY, per=ULAMBDA, inData="", trajFile=outFileTraj)
    print(p)
    #
    # now spectra
    #
    e, f0 = srfunc.wiggler_spectrum(t0, enerMin=PHOT_ENERGY_MIN, enerMax=PHOT_ENERGY_MAX, nPoints=NPOINTS, \
                                    electronCurrent=CURRENT*1e-3, outFile=outFile, elliptical=False)
    return outFile



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxwiggler()
    w.show()
    app.exec()
    w.saveSettings()
