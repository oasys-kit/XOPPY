import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util import xoppy_util

from oasys.widgets.exchange import DataExchangeObject
import xraylib


class OWxf0(widget.OWWidget):
    name = "xf0"
    id = "orange.widgets.dataxf0"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xf0.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xf0"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    MAT_FLAG = Setting(0)
    DESCRIPTOR = Setting("Si")
    GRIDSTART = Setting(0.0)
    GRIDEND = Setting(4.0)
    GRIDN = Setting(100)


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
        

        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Element(formula)', 'Mixture(formula)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material','formula','From q [sin(theta)/lambda]: ','To q [sin(theta)/lambda]: ','Number of q points']


    def unitFlags(self):
         return ['True','self.MAT_FLAG  !=  2','True','True','True']


    def compute(self):
        out_dict = self.xoppy_calc_xf0()

        if "info" in out_dict.keys():
            print(out_dict["info"])

        #send exchange
        tmp = DataExchangeObject("xoppy_calc_xf0","xf0")
        try:
            tmp.add_content("data",out_dict["data"])
            tmp.add_content("plot_x_col",0)
            tmp.add_content("plot_y_col",-1)
        except:
            pass
        try:
            tmp.add_content("labels",out_dict["labels"])
        except:
            pass
        try:
            tmp.add_content("info",out_dict["info"])
        except:
            pass


        self.send("ExchangeData",tmp)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xf0')


    def xoppy_calc_xf0(self):
        MAT_FLAG = self.MAT_FLAG
        DESCRIPTOR = self.DESCRIPTOR
        GRIDSTART = self.GRIDSTART
        GRIDEND = self.GRIDEND
        GRIDN = self.GRIDN


        qscale = numpy.linspace(GRIDSTART,GRIDEND,GRIDN)

        f0 = numpy.zeros_like(qscale)

        if MAT_FLAG == 0: # element
            descriptor = DESCRIPTOR
            for i,iqscale in enumerate(qscale):
                f0[i] = xraylib.FF_Rayl(xraylib.SymbolToAtomicNumber(descriptor),iqscale)
        elif MAT_FLAG == 1: # formula
            tmp = parse_formula(DESCRIPTOR)
            zetas = tmp["Elements"]
            multiplicity = tmp["n"]
            for j,jz in enumerate(zetas):
                for i,iqscale in enumerate(qscale):
                    f0[i] += multiplicity[j] * xraylib.FF_Rayl(jz,iqscale)
        elif MAT_FLAG == 2:
            raise Exception("Not implemented")

        #
        # return
        #
        return {"application":"xoppy","name":"xf0","data":numpy.vstack((qscale,f0)),"labels":["q=sin(theta)/lambda [A^-1]","f0 [electron units]"]}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxf0()
    w.show()
    app.exec()
    w.saveSettings()
