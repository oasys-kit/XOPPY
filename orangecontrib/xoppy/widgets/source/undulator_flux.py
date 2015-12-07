import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets.widget import OWWidget
from oasys.widgets.exchange import DataExchangeObject
from orangewidget.widget import OWAction

from collections import OrderedDict
from orangecontrib.xoppy.util import srundplug

try:
    from orangecontrib.xoppy.util.xoppy_util import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise

class OWundulator_flux(OWWidget):
    name = "undulator_flux"
    id = "orange.widgets.dataundulator_flux"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_undulator_flux.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 1
    category = ""
    keywords = ["xoppy", "undulator_flux"]
    outputs = [{"name": "xoppy_data",
               "type": numpy.ndarray,
               "doc": ""},
               {"name": "xoppy_specfile",
                "type": str,
                "doc": ""},
               {"name": "xoppy_exchange_data",
               "type": DataExchangeObject,
               "doc": ""},]

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
    GAPH = Setting(0.001)
    GAPV = Setting(0.001)
    PHOTONENERGYMIN = Setting(3000.0)
    PHOTONENERGYMAX = Setting(55000.0)
    PHOTONENERGYPOINTS = Setting(500)
    METHOD = Setting(0)


    def __init__(self):
        super().__init__()

        self.runaction = OWAction("Compute", self)
        self.runaction.triggered.connect(self.compute)
        self.addAction(self.runaction)

        box0 = gui.widgetBox(self.controlArea, "Input",orientation="horizontal")
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
        gui.lineEdit(box1, self, "PHOTONENERGYMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHOTONENERGYMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
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

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ["Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]", "Electron Beam Size H [m]", "Electron Beam Size V [m]", "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]", "Period ID [m]", "Number of periods", "Kv [undulator K value vertical field]", "Distance to slit [m]", "Slit gap H [m]", "Slit gap V [m]", "photon Energy Min [eV]", "photon Energy Max [eV]", "photon Energy Points", "calculation code"]


    def unitFlags(self):
         return ["True", "self.METHOD != 1", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True"]


    #def unitNames(self):
    #     return ["ELECTRONENERGY", "ELECTRONENERGYSPREAD", "ELECTRONCURRENT", "ELECTRONBEAMSIZEH", "ELECTRONBEAMSIZEV", "ELECTRONBEAMDIVERGENCEH", "ELECTRONBEAMDIVERGENCEV", "PERIODID", "NPERIODS", "KV", "DISTANCE", "GAPH", "GAPV", "PHOTONENERGYMIN", "PHOTONENERGYMAX", "PHOTONENERGYPOINTS", "METHOD"]


    def compute(self):
        fileName = xoppy_calc_undulator_flux(ELECTRONENERGY=self.ELECTRONENERGY,ELECTRONENERGYSPREAD=self.ELECTRONENERGYSPREAD,ELECTRONCURRENT=self.ELECTRONCURRENT,ELECTRONBEAMSIZEH=self.ELECTRONBEAMSIZEH,ELECTRONBEAMSIZEV=self.ELECTRONBEAMSIZEV,ELECTRONBEAMDIVERGENCEH=self.ELECTRONBEAMDIVERGENCEH,ELECTRONBEAMDIVERGENCEV=self.ELECTRONBEAMDIVERGENCEV,PERIODID=self.PERIODID,NPERIODS=self.NPERIODS,KV=self.KV,DISTANCE=self.DISTANCE,GAPH=self.GAPH,GAPV=self.GAPV,PHOTONENERGYMIN=self.PHOTONENERGYMIN,PHOTONENERGYMAX=self.PHOTONENERGYMAX,PHOTONENERGYPOINTS=self.PHOTONENERGYPOINTS,METHOD=self.METHOD)
        #send specfile
        self.send("xoppy_specfile",fileName)

        print("Loading file:  ",fileName)
        #load spec file with one scan, # is comment
        out = numpy.loadtxt(fileName)
        print("data shape: ",out.shape)
        #get labels
        txt = open(fileName).readlines()
        tmp = [ line.find("#L") for line in txt]
        itmp = numpy.where(numpy.array(tmp) != (-1))
        labels = txt[itmp[0]].replace("#L ","").split("  ")
        print("data labels: ",labels)
        self.send("xoppy_data",out)

        exchange_data = DataExchangeObject("XOPPY", "UNDULATOR_FLUX")

        exchange_data.add_content("xoppy_specfile", fileName)
        exchange_data.add_content("xoppy_data", out)

        self.send("xoppy_exchange_data", exchange_data)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('undulator_flux')


def xoppy_calc_undulator_flux(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                              ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                              ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                              PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                              PHOTONENERGYMIN=3000.0,PHOTONENERGYMAX=55000.0,PHOTONENERGYPOINTS=500,METHOD=0):
    print("Inside xoppy_calc_undulator_flux. ")

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

    outFile = "undulator_flux.spec"

    if METHOD == 0:
        print("Undulator flux calculation using US. Please wait...")
        e,f = srundplug.calc1dUs(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")
    if METHOD == 1:
        print("Undulator flux calculation using URGENT. Please wait...")
        e,f = srundplug.calc1dUrgent(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")
    if METHOD == 2:
        print("Undulator flux calculation using SRW. Please wait...")
        e,f = srundplug.calc1dSrw(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")

    return outFile



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_flux()
    w.show()
    app.exec()
    w.saveSettings()
