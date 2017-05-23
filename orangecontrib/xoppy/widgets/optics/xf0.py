import sys
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.util.xoppy_xraylib_util import parse_formula
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import xraylib


class OWxf0(XoppyWidget):
    name = "F0"
    id = "orange.widgets.dataxf0"
    description = "Elastic Scattering Function"
    icon = "icons/xoppy_xf0.png"
    priority = 13
    category = ""
    keywords = ["xoppy", "xf0"]

    MAT_FLAG = Setting(0)
    DESCRIPTOR = Setting("Si")
    GRIDSTART = Setting(0.0)
    GRIDEND = Setting(8.0)
    GRIDN = Setting(100)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME = Setting("f0.dat")

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 

        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Element(formula)', 'Mixture(formula)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], orientation="horizontal", addSpace=False)
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        # widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["No", "Yes"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material','formula','From q [sin(theta)/lambda]: ','To q [sin(theta)/lambda]: ','Number of q points',
                 'Dump to file','File name']

    def unitFlags(self):
         return ['True','self.MAT_FLAG  !=  2','True','True','True',
                 'True','self.DUMP_TO_FILE == 1']

    def get_help_name(self):
        return 'f0'

    def check_fields(self):
        self.DESCRIPTOR = congruence.checkEmptyString(self.DESCRIPTOR, "formula")
        self.GRIDSTART = congruence.checkPositiveNumber(self.GRIDSTART, "Q from")
        self.GRIDEND = congruence.checkStrictlyPositiveNumber(self.GRIDEND, "Q to")
        congruence.checkLessThan(self.GRIDSTART, self.GRIDEND, "Q from", "Q to")
        self.GRIDN = congruence.checkStrictlyPositiveNumber(self.GRIDN, "Number of q Points")

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

        if self.DUMP_TO_FILE:
            with open(self.FILE_NAME, "w") as file:
                try:
                    file.write("#F %s\n"%self.FILE_NAME)
                    file.write("\n#S 1 xoppy f0 results\n")
                    file.write("#N 2\n")
                    file.write("#L  q=sin(theta)/lambda [A^-1]  f0 [electron units]\n")
                    for j in range(qscale.size):
                        # file.write("%19.12e  "%energy[j])
                        file.write("%19.12e  %19.12e\n"%(qscale[j],f0[j]))
                    file.close()
                    print("File written to disk: %s \n"%self.FILE_NAME)
                except:
                    raise Exception("f0: The data could not be dumped onto the specified file!\n")


        #
        # return
        #
        return {"application":"xoppy","name":"f0","data":numpy.vstack((qscale,f0)),"labels":["q=sin(theta)/lambda [A^-1]","f0 [electron units]"]}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxf0()
    w.show()
    app.exec()
    w.saveSettings()
