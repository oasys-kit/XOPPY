import sys
import numpy

from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.util.xoppy_xraylib_util import parse_formula
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import xraylib


class OWxf0(XoppyWidget):
    name = "F0"
    id = "orange.widgets.dataxf0"
    description = "xoppy application to compute XF0"
    icon = "icons/xoppy_xf0.png"
    priority = 11
    category = ""
    keywords = ["xoppy", "xf0"]

    MAT_FLAG = Setting(0)
    DESCRIPTOR = Setting("Si")
    GRIDSTART = Setting(0.0)
    GRIDEND = Setting(8.0)
    GRIDN = Setting(100)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
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


    def unitLabels(self):
         return ['material','formula','From q [sin(theta)/lambda]: ','To q [sin(theta)/lambda]: ','Number of q points']

    def unitFlags(self):
         return ['True','self.MAT_FLAG  !=  2','True','True','True']

    def get_help_name(self):
        return 'xf0'

    def check_fields(self):
        pass

    def do_xoppy_calculation(self):
        out_dict = self.xoppy_calc_xf0()

        if "info" in out_dict.keys():
            print(out_dict["info"])

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", out_dict["data"].T)
            calculated_data.add_content("plot_x_col",0)
            calculated_data.add_content("plot_y_col",-1)
        except:
            pass
        try:
            calculated_data.add_content("labels",out_dict["labels"])
        except:
            pass
        try:
            calculated_data.add_content("info",out_dict["info"])
        except:
            pass

        return calculated_data

    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def get_data_exchange_widget_name(self):
        return "XF0"

    def getTitles(self):
        return ["f0"]

    def getXTitles(self):
        return ["q=sin(theta)/lambda [A^-1]"]

    def getYTitles(self):
        return ["f0 [electron units]"]

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
