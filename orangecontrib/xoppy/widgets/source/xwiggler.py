import sys
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject
from srxraylib.sources import srfunc
import scipy.constants as codata

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

class OWxwiggler(XoppyWidget):
    name = "WIGGLER"
    id = "orange.widgets.dataxwiggler"
    description = "Wiggler Spectrum (Full Emission)"
    icon = "icons/xoppy_xwiggler.png"
    priority = 9
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
    NTRAJPOINTS = Setting(101)
    CURRENT = Setting(200.0)
    FILE = Setting("?")

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "FIELD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Sinusoidal', 'B from file', 'B from harmonics'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ULAMBDA",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHOT_ENERGY_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHOT_ENERGY_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NTRAJPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 

        box1 = gui.widgetBox(box)

        file_box = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file = oasysgui.lineEdit(file_box, self, "FILE",
                                         label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.button(file_box, self, "...", callback=self.selectFile)

    def unitLabels(self):
         return ['Magnetic field: ','Number of periods','Wiggler period [m]','K value','Beam energy [GeV]',
                 'Min Photon Energy [eV]','Max Photon Energy [eV]','Number of energy points',
                 'Number of traj points per period','Electron Beam Current [mA]','File with Magnetic Field']

    def unitFlags(self):
         return ['True','True','self.FIELD  !=  1','self.FIELD  ==  0','True',
                 'True','True','True',
                 'self.FIELD  !=  1','True','self.FIELD  !=  0']

    def selectFile(self):
        self.le_file.setText(oasysgui.selectFileFromDialog(self, self.FILE, "Open B File"))

    def get_help_name(self):
        return 'wiggler'

    def check_fields(self):
        self.NPERIODS = congruence.checkStrictlyPositiveNumber(self.NPERIODS, "Number of Periods")
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Beam Energy")
        self.PHOT_ENERGY_MIN = congruence.checkPositiveNumber(self.PHOT_ENERGY_MIN, "Min Photon Energy")
        self.PHOT_ENERGY_MAX = congruence.checkStrictlyPositiveNumber(self.PHOT_ENERGY_MAX, "Max Photon Energy")
        congruence.checkLessThan(self.PHOT_ENERGY_MIN, self.PHOT_ENERGY_MAX, "Min Photon Energy", "Max Photon Energy")
        self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.NPOINTS, "Number of Energy Points")
        self.CURRENT = congruence.checkStrictlyPositiveNumber(self.CURRENT, "Electron Beam Current")

        if self.FIELD == 0:
            self.ULAMBDA = congruence.checkStrictlyPositiveNumber(self.ULAMBDA, "Wiggler period")
            self.K = congruence.checkStrictlyPositiveNumber(self.K, "K")
            self.NTRAJPOINTS = congruence.checkStrictlyPositiveNumber(self.NTRAJPOINTS, "Number of traj points per period")
        elif self.FIELD == 1:
            self.ULAMBDA = congruence.checkStrictlyPositiveNumber(self.ULAMBDA, "Wiggler period")
            self.NTRAJPOINTS = congruence.checkStrictlyPositiveNumber(self.NTRAJPOINTS, "Number of traj points per period")
            congruence.checkFile(self.FILE)
        elif self.FIELD == 2:
            congruence.checkFile(self.FILE)

    def do_xoppy_calculation(self):
        return xoppy_calc_xwiggler(FIELD=self.FIELD,NPERIODS=self.NPERIODS,ULAMBDA=self.ULAMBDA,K=self.K,ENERGY=self.ENERGY,
                                   PHOT_ENERGY_MIN=self.PHOT_ENERGY_MIN,PHOT_ENERGY_MAX=self.PHOT_ENERGY_MAX,
                                   NPOINTS=self.NPOINTS,NTRAJPOINTS=self.NTRAJPOINTS,CURRENT=self.CURRENT,FILE=self.FILE)

    def extract_data_from_xoppy_output(self, calculation_output):
        e, f, sp = calculation_output

        data = numpy.zeros((len(e), 3))
        data[:, 0] = numpy.array(e)
        data[:, 1] = numpy.array(f)
        data[:, 2] = numpy.array(sp)

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", data)

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "XWIGGLER"

    def getTitles(self):
        return ['Flux','Spectral Power']

    def getXTitles(self):
        return ["Energy [eV]","Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Phot/sec/0.1%bw]", "Spectral Power [W/eV]"]

    def getLogPlot(self):
        return [(True, True), (True, True)]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2)]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def xoppy_calc_xwiggler(FIELD=0,NPERIODS=12,ULAMBDA=0.125,K=14.0,ENERGY=6.04,PHOT_ENERGY_MIN=100.0,\
                        PHOT_ENERGY_MAX=100100.0,NPOINTS=100,NTRAJPOINTS=101,CURRENT=200.0,FILE="?"):

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
    e, f0, p0 = srfunc.wiggler_spectrum(t0, enerMin=PHOT_ENERGY_MIN, enerMax=PHOT_ENERGY_MAX, nPoints=NPOINTS, \
                                    electronCurrent=CURRENT*1e-3, outFile=outFile, elliptical=False)

    print("\nPower from integral of spectrum: %8.3f W"%(f0.sum()*1e3*codata.e*(e[1]-e[0])))
    return e, f0, p0



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxwiggler()
    w.show()
    app.exec()
    w.saveSettings()
