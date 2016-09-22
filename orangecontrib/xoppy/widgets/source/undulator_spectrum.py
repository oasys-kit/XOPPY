import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui

from collections import OrderedDict
from orangecontrib.xoppy.util import srundplug

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

class OWundulator_spectrum(XoppyWidget):
    name = "undulator_spectrum"
    id = "orange.widgets.dataundulator_spectrum"
    description = "xoppy application to compute UNDULATOR_SPECTRUM"
    icon = "icons/xoppy_undulator_spectrum.png"
    priority = 1
    category = ""
    keywords = ["xoppy", "undulator_spectrum"]

    ELECTRONENERGY = Setting(6.04)
    ELECTRONENERGYSPREAD = Setting(0.001)
    ELECTRONCURRENT = Setting(0.2)
    ELECTRONBEAMSIZEH = Setting(0.000395)
    ELECTRONBEAMSIZEV = Setting(9.9e-06)
    ELECTRONBEAMDIVERGENCEH = Setting(1.05e-05)
    ELECTRONBEAMDIVERGENCEV = Setting(3.9e-06)
    PERIODID = Setting(0.018)
    NPERIODS = Setting(222)
    KV = Setting(1.68)
    DISTANCE = Setting(30.0)
    GAPH = Setting(0.001)
    GAPV = Setting(0.001)
    PHOTONENERGYMIN = Setting(3000.0)
    PHOTONENERGYMAX = Setting(55000.0)
    PHOTONENERGYPOINTS = Setting(500)
    METHOD = Setting(0)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, "UNDULATOR Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1

        #widget index 0
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 1
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONENERGYSPREAD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 2
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONCURRENT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONBEAMSIZEH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONBEAMSIZEV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "PERIODID",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "KV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "GAPH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "GAPV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "PHOTONENERGYMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "PHOTONENERGYMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "PHOTONENERGYPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['US', 'URGENT', 'SRW'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

    def unitLabels(self):
         return ["Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]", "Electron Beam Size H [m]", "Electron Beam Size V [m]", "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]", "Period ID [m]", "Number of periods", "Kv [undulator K value vertical field]", "Distance to slit [m]", "Slit gap H [m]", "Slit gap V [m]", "photon Energy Min [eV]", "photon Energy Max [eV]", "photon Energy Points", "calculation code"]

    def unitFlags(self):
         return ["True", "self.METHOD != 1", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True"]

    def get_help_name(self):
        return 'undulator_spectrum'

    def check_fields(self):
        pass

    def do_xoppy_calculation(self):
        return xoppy_calc_undulator_spectrum(ELECTRONENERGY=self.ELECTRONENERGY,ELECTRONENERGYSPREAD=self.ELECTRONENERGYSPREAD,ELECTRONCURRENT=self.ELECTRONCURRENT,ELECTRONBEAMSIZEH=self.ELECTRONBEAMSIZEH,ELECTRONBEAMSIZEV=self.ELECTRONBEAMSIZEV,ELECTRONBEAMDIVERGENCEH=self.ELECTRONBEAMDIVERGENCEH,ELECTRONBEAMDIVERGENCEV=self.ELECTRONBEAMDIVERGENCEV,PERIODID=self.PERIODID,NPERIODS=self.NPERIODS,KV=self.KV,DISTANCE=self.DISTANCE,GAPH=self.GAPH,GAPV=self.GAPV,PHOTONENERGYMIN=self.PHOTONENERGYMIN,PHOTONENERGYMAX=self.PHOTONENERGYMAX,PHOTONENERGYPOINTS=self.PHOTONENERGYPOINTS,METHOD=self.METHOD)

    def get_data_exchange_widget_name(self):
        return "UNDULATOR_SPECTRUM"

    def getTitles(self):
        return ['Flux','Spectral Power']

    def getXTitles(self):
        return ["Energy [eV]","Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Phot/sec/0.1%bw]","Spectral Power [W/eV]"]

    def getVariablesToPlot(self):
        return [(0, 2),(0,3)]

    def getLogPlot(self):
        return [(False, False),(False, False)]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def xoppy_calc_undulator_spectrum(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                              ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                              ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                              PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                              PHOTONENERGYMIN=3000.0,PHOTONENERGYMAX=55000.0,PHOTONENERGYPOINTS=500,METHOD=0):
    print("Inside xoppy_calc_undulator_spectrum. ")

    bl = OrderedDict()
    bl['ElectronBeamDivergenceH'] = ELECTRONBEAMDIVERGENCEH
    bl['ElectronBeamDivergenceV'] = ELECTRONBEAMDIVERGENCEV
    bl['ElectronBeamSizeH'] = ELECTRONBEAMSIZEH
    bl['ElectronBeamSizeV'] = ELECTRONBEAMSIZEV
    bl['ElectronCurrent'] = ELECTRONCURRENT
    bl['ElectronEnergy'] = ELECTRONENERGY
    bl['ElectronEnergySpread'] = ELECTRONENERGYSPREAD
    bl['Kv'] = KV
    bl['NPeriods'] = NPERIODS
    bl['PeriodID'] = PERIODID
    bl['distance'] = DISTANCE
    bl['gapH'] = GAPH
    bl['gapV'] = GAPV

    #TODO remove file and export e,f arrays
    outFile = "undulator_spectrum.spec"

    if METHOD == 0:
        print("Undulator flux calculation using US. Please wait...")
        e,f = srundplug.calc1d_us(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")
    if METHOD == 1:
        print("Undulator flux calculation using URGENT. Please wait...")
        e,f = srundplug.calc1d_urgent(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")
    if METHOD == 2:
        print("Undulator flux calculation using SRW. Please wait...")
        e,f = srundplug.calc1d_srw(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")


    return outFile



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_spectrum()
    w.show()
    app.exec()
    w.saveSettings()
