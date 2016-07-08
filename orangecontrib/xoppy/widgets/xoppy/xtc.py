import sys,os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util.xoppy_util import locations, xoppy_doc
from oasys.widgets.exchange import DataExchangeObject

class OWxtc(widget.OWWidget):
    name = "xtc"
    id = "orange.widgets.dataxtc"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xtc.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xtc"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    #19 variables
    TITLE = Setting("APS Undulator A, Beam Parameters for regular lattice nux36nuy39.twi, 1.5% cpl.")
    ENERGY = Setting(7.0)
    CURRENT = Setting(100.0)
    ENERGY_SPREAD = Setting(0.00096)
    SIGX = Setting(0.274)
    SIGY = Setting(0.011)
    SIGX1 = Setting(0.0113)
    SIGY1 = Setting(0.0036)
    PERIOD = Setting(3.23)
    NP = Setting(70)
    EMIN = Setting(2950.0)
    EMAX = Setting(13500.0)
    N = Setting(40)
    HARMONIC_FROM = Setting(1)
    HARMONIC_TO = Setting(15)
    HARMONIC_STEP = Setting(2)
    HELICAL = Setting(0)
    METHOD = Setting(1)
    NEKS = Setting(100)


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
        gui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY_SPREAD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HARMONIC_FROM",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HARMONIC_TO",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HARMONIC_STEP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HELICAL",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NEKS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1)


        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Title','Electron energy (GeV)','Current (mA)','Energy Spread (DE/E)',
                 'SigmaX (mm)','Sigma Y (mm)',"Sigma X' (mrad)","Sigma Z' (mrad)",
                 'Period length (cm)','Number of periods',
                 'E1 minimum energy (eV)','E1 maximum energy (eV)',
                 'Number of energy-points','Minimum harmonic number','Maximum harmonic number','Harmonic step size',
                 'Mode','Method','Intrinsic NEKS']


    def unitFlags(self):
         return ['True' for i in range(19)]

    def compute(self):

        with open("tc.inp", "wt") as f:
            f.write("%s\n"%self.TITLE)
            f.write("%10.3f %10.2f %10.6f %s\n"%(self.ENERGY,self.CURRENT,self.ENERGY_SPREAD,self.TITLE))
            f.write("%10.4f %10.4f %10.4f %10.4f beam\n"%(self.SIGX,self.SIGY,self.SIGX1,self.SIGY1))
            f.write("%10.3f %d undelator\n"%(self.PERIOD,self.NP))
            f.write("%10.1f %10.1f %d energy\n"%(self.EMIN,self.EMAX,self.N))
            f.write("%d %d %d harmonics\n"%(self.HARMONIC_FROM,self.HARMONIC_TO,self.HARMONIC_STEP))
            f.write("%d %d %d %d parameters\n"%(self.HELICAL,self.METHOD,1,self.NEKS))
            f.write("foreground\n")

        command = os.path.join(locations.home_bin(), 'tc')
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("Output file: %s"%("tc.out"))
        print("\n--------------------------------------------------------\n")

        #
        # parse result files to exchange object
        #


        with open("tc.out","r") as f:
            lines = f.readlines()

        # remove returns
        lines = [line[:-1] for line in lines]

        # separate numerical data from text
        floatlist = []
        txtlist = []
        for line in lines:
            try:
                tmp = float(line.strip()[0])
                floatlist.append(line)
            except:
                txtlist.append(line)

        data = numpy.loadtxt(floatlist).T

        #TODO: compute envelopes (as in XOP)

        #send exchange
        tmp = DataExchangeObject("xoppy_xtc","xtc")

        try:
            tmp.add_content("data",data)
            tmp.add_content("plot_x_col",1)
            tmp.add_content("plot_y_col",2)
        except:
            pass
        try:
            tmp.add_content("labels",["Energy (eV) without emittance", "Energy (eV) with emittance",
                                      "Brilliance (ph/s/mrad^2/mm^2/0.1%bw)","Ky","Total Power (W)","Power density (W/mr^2)"])
        except:
            pass
        try:
            tmp.add_content("info",txtlist)
        except:
            pass

        self.send("ExchangeData",tmp)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('xtc')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtc()
    w.show()
    app.exec()
    w.saveSettings()
