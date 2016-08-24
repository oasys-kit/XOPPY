import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util import xoppy_util
from orangecontrib.xoppy.widgets.xoppy.xoppy_xraylib_util import crystal_fh, bragg_calc
from oasys.widgets.exchange import DataExchangeObject
from xraylib import Crystal_GetCrystalsList

class OWxfh(widget.OWWidget):
    name = "xfh"
    id = "orange.widgets.dataxfh"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xfh.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 5
    category = ""
    keywords = ["xoppy", "xfh"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False


    ILATTICE = Setting(0)
    HMILLER = Setting(1)
    KMILLER = Setting(1)
    LMILLER = Setting(1)
    I_PLOT = Setting(2)
    TEMPER = Setting(1.0)
    ENERGY = Setting(8000.0)
    ENERGY_END = Setting(18000.0)
    NPOINTS = Setting(20)


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
        

        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ILATTICE",
                    label=self.unitLabels()[idx], addSpace=True,
                    items=Crystal_GetCrystalsList(),
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HMILLER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KMILLER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LMILLER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "I_PLOT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=self.plotOptionList(),
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEMPER",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY_END",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal:','h miller index','k miller index','l miller index','Plot:','Temperature factor [see help]:','From Energy [eV]','To energy [eV]','Number of points']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True']\

    def plotOptionList(self):
        return ["Photon energy [eV]",
                  "Wavelength [A]",
                  "Bragg angle [deg]",
                  "Re(f_0)",
                  "Im(f_0)  ",
                  "Re(FH)",
                  "Im(FH)",
                  "Re(FH_BAR)",
                  "Im(FH_BAR)",
                  "Re(psi_0)",
                  "Im(psi_0)  ",
                  "Re(psi_H)",
                  "Im(psi_H)",
                  "Re(psi_BAR)",
                  "Im(psi_BAR)",
                  "Re(F(h,k,l))",
                  "Im(F(h,k,l))",
                  "delta (1-Re(refrac))",
                  "Re(refrac index)",
                  "Im(refrac index)",
                  "absorption coeff",
                  "s-pol Darwin width [microrad]",
                  "p-pol Darwin width [microrad]",
                  "Sin(Bragg angle)/Lambda",
                  "psi_over_f"]

    def compute(self):
        #TODO: remove I_ABSORP
        ILATTICE = self.ILATTICE
        HMILLER = self.HMILLER
        KMILLER = self.KMILLER
        LMILLER = self.LMILLER
        I_PLOT = self.I_PLOT
        TEMPER = self.TEMPER
        ENERGY = self.ENERGY
        ENERGY_END = self.ENERGY_END
        NPOINTS = self.NPOINTS

        descriptor = Crystal_GetCrystalsList()[ILATTICE]
        print("Using crystal descriptor: ",descriptor)
        bragg_dictionary = bragg_calc(descriptor=descriptor,hh=HMILLER,kk=KMILLER,ll=LMILLER,temper=TEMPER,
                                                emin=ENERGY,emax=ENERGY_END,estep=50.0,fileout="/dev/null")

        energy = numpy.linspace(ENERGY,ENERGY_END,NPOINTS)

        out = numpy.zeros((25,NPOINTS))

        info = ""
        for i,ienergy in enumerate(energy):
            dic2 = crystal_fh(bragg_dictionary,ienergy)
            print("Energy=%g eV FH=(%g,%g)"%(ienergy,dic2["STRUCT"].real,dic2["STRUCT"].imag))

            out[0,i]  = ienergy
            out[1,i]  = dic2["WAVELENGTH"]*1e10
            out[2,i]  = dic2["THETA"]*180/numpy.pi
            out[3,i]  = dic2["F_0"].real
            out[4,i]  = dic2["F_0"].imag
            out[5,i]  = dic2["FH"].real
            out[6,i]  = dic2["FH"].imag
            out[7,i]  = dic2["FH_BAR"].real
            out[8,i]  = dic2["FH_BAR"].imag
            out[9,i]  = dic2["psi_0"].real
            out[10,i] = dic2["psi_0"].imag
            out[11,i] = dic2["psi_h"].real
            out[12,i] = dic2["psi_h"].imag
            out[13,i] = dic2["psi_hbar"].real
            out[14,i] = dic2["psi_hbar"].imag
            out[15,i] = dic2["STRUCT"].real
            out[16,i] = dic2["STRUCT"].imag
            out[17,i] = dic2["DELTA_REF"]
            out[18,i] = dic2["REFRAC"].real
            out[19,i] = dic2["REFRAC"].imag
            out[20,i] = dic2["ABSORP"]
            out[21,i] = dic2["ssr"]
            out[22,i] = dic2["spr"]
            out[23,i] = dic2["RATIO"]
            out[24,i] = dic2["psi_over_f"]
            info += "#\n#\n#\n"
            info += dic2["info"]

        #send exchange
        tmp = DataExchangeObject("xoppy_calc_xfh","xfh")

        try:
            tmp.add_content("data",out)
            tmp.add_content("plot_x_col",0)
            tmp.add_content("plot_y_col",I_PLOT)
        except:
            pass
        try:
            tmp.add_content("labels",self.plotOptionList())
        except:
            pass
        try:
            tmp.add_content("info",info)
        except:
            pass

        self.send("ExchangeData",tmp)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xfh')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxfh()
    w.show()
    app.exec()
    w.saveSettings()
