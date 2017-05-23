import sys
import numpy
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.util.xoppy_xraylib_util import cross_calc, cross_calc_mix
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import xraylib


class OWxcrosssec(XoppyWidget):
    name = "CrossSec"
    id = "orange.widgets.dataxcrosssec"
    description = "X-ray Matter Cross Sections"
    icon = "icons/xoppy_xcrosssec.png"
    priority = 19
    category = ""
    keywords = ["xoppy", "xcrosssec"]

    MAT_FLAG = Setting(0)
    MAT_LIST = Setting(0)
    DESCRIPTOR = Setting("Si")
    DENSITY = Setting(1.0)
    CALCULATE = Setting(1)
    GRID = Setting(0)
    GRIDSTART = Setting(100.0)
    GRIDEND = Setting(10000.0)
    GRIDN = Setting(200)
    UNIT = Setting(0)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME = Setting("CrossSec.dat")

    xtitle = None
    ytitle = None

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Element(formula)', 'Mixture(formula)', 'Mixture(table)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box)
        items = xraylib.GetCompoundDataNISTList()
        gui.comboBox(box1, self, "MAT_LIST",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=items,
                     valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DENSITY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CALCULATE",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Total','PhotoElectric','Rayleigh','Compton','Total-Rayleigh'],
                     valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Standard', 'User defined', 'Single Value'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "UNIT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['barn/atom [Cross Section] *see help*', 'cm^2 [Cross Section] *see help*', 'cm^2/g [Mass abs coef]', 'cm^-1 [Linear abs coef]'],
                    valueType=int, orientation="horizontal", labelWidth=130)
        self.show_at(self.unitFlags()[idx], box1) 

        # widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["No", "Yes"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)




        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material','table','formula','density','Cross section','Energy [eV] grid:',
                 'Starting Energy [eV]: ','To: ','Number of points','Units',
                 'Dump to file','File name']

    def unitFlags(self):
         return ['True','self.MAT_FLAG  ==  2','self.MAT_FLAG  <=  1 ','self.MAT_FLAG  ==  1  &  self.UNIT  ==  3',
                 'True','True','self.GRID  !=  0','self.GRID  ==  1','self.GRID  ==  1','True',
                 'True','self.DUMP_TO_FILE == 1']

    def get_help_name(self):
        return 'crosssec'

    def check_fields(self):
        self.DESCRIPTOR = congruence.checkEmptyString(self.DESCRIPTOR, "formula")
        if self.MAT_FLAG == 1:
            self.DENSITY = congruence.checkStrictlyPositiveNumber(self.DENSITY, "density")

        if self.GRID > 0:
            self.GRIDSTART = congruence.checkPositiveNumber(self.GRIDSTART, "Starting Energy")

            if self.GRID == 1:
                self.GRIDEND = congruence.checkStrictlyPositiveNumber(self.GRIDEND, "Energy to")
                congruence.checkLessThan(self.GRIDSTART, self.GRIDEND, "Starting Energy", "Energy to")
                self.GRIDN = congruence.checkStrictlyPositiveNumber(self.GRIDN, "Number of points")


    def do_xoppy_calculation(self):
        out_dict = self.xoppy_calc_xcrosssec()

        if "info" in out_dict.keys():
            print(out_dict["info"])

        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        
        try:
            calculated_data.add_content("xoppy_data", out_dict["data"].T)
            calculated_data.add_content("plot_x_col",0)
            calculated_data.add_content("plot_y_col",-1)
        except:
            pass
        try:
            calculated_data.add_content("labels", out_dict["labels"])
        except:
            pass
        try:
            calculated_data.add_content("info",out_dict["info"])
        except:
            pass

        return calculated_data

    def extract_data_from_xoppy_output(self, calculation_output):
        try:
            calculation_output.get_content("xoppy_data")

            labels = calculation_output.get_content("labels")

            self.xtitle = labels[0]
            self.ytitle = labels[1]
        except:
            QMessageBox.information(self,
                                    "Calculation Result",
                                    "Calculation Result:\n"+calculation_output.get_content("info"),
                                    QMessageBox.Ok)

            self.xtitle = None
            self.ytitle = None

        return calculation_output

    def plot_results(self, calculated_data, progressBarValue=80):
        self.initializeTabs()

        try:
            calculated_data.get_content("xoppy_data")

            super().plot_results(calculated_data, progressBarValue)
        except:
            self.plot_info(calculated_data.get_content("info") + "\n", progressBarValue, 0, 0)


    def get_data_exchange_widget_name(self):
        return "XCROSSSEC"

    def getTitles(self):
        return ["Calculation Result"]

    def getXTitles(self):
        if self.xtitle is None:
            return [""]
        else:
            return [self.xtitle]

    def getYTitles(self):
        if self.ytitle is None:
            return [""]
        else:
            return [self.ytitle]

    def getLogPlot(self):
        return [(True, True)]

    def getVariablesToPlot(self):
        return [(0, 1)]

    def getLogPlot(self):
        return[(True, True)]


    def xoppy_calc_xcrosssec(self):

        MAT_FLAG = self.MAT_FLAG
        MAT_LIST = self.MAT_LIST
        DESCRIPTOR = self.DESCRIPTOR
        density = self.DENSITY
        CALCULATE = self.CALCULATE
        GRID = self.GRID
        GRIDSTART = self.GRIDSTART
        GRIDEND = self.GRIDEND
        GRIDN = self.GRIDN
        UNIT = self.UNIT


        if MAT_FLAG == 0: # element
            descriptor = DESCRIPTOR
            density = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(DESCRIPTOR))
        elif MAT_FLAG == 1: # formula
            descriptor = DESCRIPTOR
        elif MAT_FLAG == 2:
            tmp = xraylib.GetCompoundDataNISTByIndex(MAT_LIST)
            descriptor = tmp["name"]
            density = tmp["density"]

        print("xoppy_calc_xcrosssec: using density = %g g/cm3"%density)
        if GRID == 0:
            energy = numpy.arange(0,500)
            elefactor = numpy.log10(10000.0 / 30.0) / 300.0
            energy = 10.0 * 10**(energy * elefactor)
        elif GRID == 1:
            if GRIDN == 1:
                energy = numpy.array([GRIDSTART])
            else:
                energy = numpy.linspace(GRIDSTART,GRIDEND,GRIDN)
        elif GRID == 2:
            energy = numpy.array([GRIDSTART])

        if MAT_FLAG == 0: # element
            out =  cross_calc(descriptor,energy,calculate=CALCULATE,density=density)
        elif MAT_FLAG == 1: # compound parse
            out =  cross_calc_mix(descriptor,energy,calculate=CALCULATE,density=density,parse_or_nist=0)
        elif MAT_FLAG == 2: # NIST compound
            out =  cross_calc_mix(descriptor,energy,calculate=CALCULATE,density=density,parse_or_nist=1)

        calculate_items = ['Total','PhotoElectric','Rayleigh','Compton','Total minus Rayleigh']
        unit_items = ['barn/atom','cm^2','cm^2/g','cm^-1']
        if energy.size > 1:
            tmp_x = out[0,:].copy()
            tmp_y = out[UNIT+1,:].copy()
            tmp = numpy.vstack((tmp_x,tmp_y))
            labels = ["Photon energy [eV]","%s cross section [%s]"%(calculate_items[CALCULATE],unit_items[UNIT])]
            to_return = {"application":"xoppy","name":"xcrosssec","data":tmp,"labels":labels}
        else:
            tmp = None
            txt = "xoppy_calc_xcrosssec: Calculated %s cross section: %g %s"%(calculate_items[CALCULATE],out[UNIT+1,0],unit_items[UNIT])
            print(txt)
            to_return  = {"application":"xoppy","name":"xcrosssec","info":txt}

        if self.DUMP_TO_FILE:
            with open(self.FILE_NAME, "w") as file:
                try:
                    file.write("#F %s\n"%self.FILE_NAME)
                    file.write("\n#S 1 xoppy CrossSec results\n")
                    file.write("#N 5\n")
                    tmp = "#L  Photon energy [eV]"
                    for unit_item in unit_items:
                        tmp += "  %s [%s]"%(calculate_items[CALCULATE],unit_item)
                    tmp += "\n"
                    file.write(tmp)
                    for j in range(out.shape[1]):
                        # file.write("%19.12e  "%energy[j])
                        file.write(("%19.12e  "*out.shape[0]+"\n")%tuple(out[i,j] for i in range(out.shape[0])))
                    file.close()
                    print("File written to disk: %s \n"%self.FILE_NAME)
                except:
                    raise Exception("CrossSec: The data could not be dumped onto the specified file!\n")

        return to_return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxcrosssec()
    w.show()
    app.exec()
    w.saveSettings()
