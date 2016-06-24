import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets.widget import OWWidget
from oasys.widgets.exchange import DataExchangeObject

from collections import OrderedDict

from orangecontrib.xoppy.util import srundplug
from orangecontrib.xoppy.util import xoppy_util
from orangecontrib.xoppy.util import xoppy_pymca_tools

class OWundulator_power_density(OWWidget):
    name = "undulator_power_density"
    id = "orange.widgets.dataundulator_power_density"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_undulator_power_density.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 2
    category = ""
    keywords = ["xoppy", "undulator_power_density"]
    outputs = [{"name": "xoppy_data",
               "type": numpy.ndarray,
               "doc": ""},
               {"name": "xoppy_specfile",
                "type": str,
                "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

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
    GAPH = Setting(0.003)
    GAPV = Setting(0.003)
    HSLITPOINTS = Setting(41)
    VSLITPOINTS = Setting(41)
    METHOD = Setting(0)


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
        gui.lineEdit(box1, self, "ELECTRONENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELECTRONENERGYSPREAD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELECTRONCURRENT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELECTRONBEAMSIZEH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELECTRONBEAMSIZEV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PERIODID",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
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
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GAPH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GAPV",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HSLITPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "VSLITPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['US', 'URGENT', 'SRW'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ["Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]", "Electron Beam Size H [m]", "Electron Beam Size V [m]", "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]", "Period ID [m]", "Number of periods", "Kv [undulator K value vertical field]", "Distance to slit [m]", "Slit gap H [m]", "Slit gap V [m]", "Number of slit mesh points in H", "Number of slit mesh points in V", "calculation code"]


    def unitFlags(self):
         return ["True", "self.METHOD != 1", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True"]


    #def unitNames(self):
    #     return ["ELECTRONENERGY", "ELECTRONENERGYSPREAD", "ELECTRONCURRENT", "ELECTRONBEAMSIZEH", "ELECTRONBEAMSIZEV", "ELECTRONBEAMDIVERGENCEH", "ELECTRONBEAMDIVERGENCEV", "PERIODID", "NPERIODS", "KV", "DISTANCE", "GAPH", "GAPV", "HSLITPOINTS", "VSLITPOINTS", "METHOD"]


    def compute(self):
        fileName = xoppy_calc_undulator_power_density(ELECTRONENERGY=self.ELECTRONENERGY,ELECTRONENERGYSPREAD=self.ELECTRONENERGYSPREAD,ELECTRONCURRENT=self.ELECTRONCURRENT,ELECTRONBEAMSIZEH=self.ELECTRONBEAMSIZEH,ELECTRONBEAMSIZEV=self.ELECTRONBEAMSIZEV,ELECTRONBEAMDIVERGENCEH=self.ELECTRONBEAMDIVERGENCEH,ELECTRONBEAMDIVERGENCEV=self.ELECTRONBEAMDIVERGENCEV,PERIODID=self.PERIODID,NPERIODS=self.NPERIODS,KV=self.KV,DISTANCE=self.DISTANCE,GAPH=self.GAPH,GAPV=self.GAPV,HSLITPOINTS=self.HSLITPOINTS,VSLITPOINTS=self.VSLITPOINTS,METHOD=self.METHOD)
        #send specfile
        self.send("xoppy_specfile",fileName)

        print("Loading file:  ",fileName)
        #load spec file with one scan, # is comment

        out = xoppy_pymca_tools.xoppy_loadspec(fileName)


        print("data shape: ",out.shape)
        #get labels
        # txt = open(fileName).readlines()
        # tmp = [ line.find("#L") for line in txt]
        # itmp = numpy.where(numpy.array(tmp) != (-1))
        # labels = txt[itmp[0]].replace("#L ","").split("  ")
        # print("data labels: ",labels)
        self.send("xoppy_data",out.T)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('undulator_power_density')

def xoppy_calc_undulator_power_density(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                       ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                       ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                       PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                                       HSLITPOINTS=101,VSLITPOINTS=51,METHOD=0):
    print("Inside xoppy_calc_undulator_power_density. ")

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

    outFile = "undulator_power_density.spec"

    if METHOD == 0:
        print("Undulator power_density calculation using US. Please wait...")
        h,v,p = srundplug.calc2dUs(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS)
        print("Done")
    if METHOD == 1:
        print("Undulator power_density calculation using URGENT. Please wait...")
        h,v,p = srundplug.calc2dUrgent(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS)
        print("Done")
    if METHOD == 2:
        print("Undulator power_density calculation using SRW. Please wait...")
        h,v,p = srundplug.calc2dSrw(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS)
        print("Done")

    return outFile



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_power_density()
    w.show()
    app.exec()
    w.saveSettings()
