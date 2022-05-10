import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.scattering_functions.xoppy_calc_crosssec import xoppy_calc_crosssec
from dabax.dabax_files import dabax_crosssec_files

import xraylib
from dabax.dabax_xraylib import DabaxXraylib


class OWxcrosssec(XoppyWidget):
    name = "CrossSec"
    id = "orange.widgets.dataxcrosssec"
    description = "X-ray Matter Cross Sections"
    icon = "icons/xoppy_xcrosssec.png"
    priority = 19
    category = ""
    keywords = ["xoppy", "xcrosssec"]


    DESCRIPTOR   = Setting("Si")
    DENSITY      = Setting("?")
    MAT_FLAG     = Setting(2)
    MAT_LIST     = Setting(177)
    CALCULATE    = Setting(1)
    GRID         = Setting(0)
    GRIDSTART    = Setting(100.0)
    GRIDEND      = Setting(10000.0)
    GRIDN        = Setting(200)
    UNIT         = Setting(0)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME    = Setting("CrossSec.dat")

    MATERIAL_CONSTANT_LIBRARY_FLAG = Setting(0)
    DABAX_CROSSSEC_FILE_INDEX = Setting(0)

    xtitle = None
    ytitle = None

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Element(formula)', 'Compound(formula)', 'Compound(table)'],
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
                    valueType=str, orientation="horizontal", labelWidth=250)
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
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

        #
        #
        #

        box = oasysgui.widgetBox(self.controlArea, self.name + " Material Library", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)


        # widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "MATERIAL_CONSTANT_LIBRARY_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["xraylib [default]", "dabax"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DABAX_CROSSSEC_FILE_INDEX",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=dabax_crosssec_files(),
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)


        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material','table','formula','density',
                 'Cross section','Energy [eV] grid:',
                 'Starting Energy [eV]: ','To: ','Number of points','Units',
                 'Dump to file','File name',
                 'Material Library','dabax crosssec file',
                 ]

    def unitFlags(self):
         return ['True','self.MAT_FLAG  ==  2','self.MAT_FLAG  <=  1 ','True',
                 'True','True',
                 'self.GRID  !=  0','self.GRID  ==  1','self.GRID  ==  1','True',
                 'True','self.DUMP_TO_FILE == 1',
                 'True',
                 'self.MATERIAL_CONSTANT_LIBRARY_FLAG == 1',
                 ]

    def get_help_name(self):
        return 'crosssec'

    def check_fields(self):
        self.DESCRIPTOR = congruence.checkEmptyString(self.DESCRIPTOR, "formula")

        if self.GRID > 0:
            self.GRIDSTART = congruence.checkPositiveNumber(self.GRIDSTART, "Starting Energy")

            if self.GRID == 1:
                self.GRIDEND = congruence.checkStrictlyPositiveNumber(self.GRIDEND, "Energy to")
                congruence.checkLessThan(self.GRIDSTART, self.GRIDEND, "Starting Energy", "Energy to")
                self.GRIDN = congruence.checkStrictlyPositiveNumber(self.GRIDN, "Number of points")


    def do_xoppy_calculation(self):

        if self.MATERIAL_CONSTANT_LIBRARY_FLAG == 0:
            material_constants_library = xraylib
            material_constants_library_str = "xraylib"
        else:
            material_constants_library = DabaxXraylib(file_CrossSec=dabax_crosssec_files()[self.DABAX_CROSSSEC_FILE_INDEX])
            material_constants_library_str = 'DabaxXraylib(file_CrossSec="%s")' % (dabax_crosssec_files()[self.DABAX_CROSSSEC_FILE_INDEX])
            print(material_constants_library.info())


        if self.MAT_FLAG == 0: # element
            descriptor = self.DESCRIPTOR
            try:
                density = float(self.DENSITY)
            except:
                Z = material_constants_library.SymbolToAtomicNumber(self.DESCRIPTOR)
                density = material_constants_library.ElementDensity(Z)

        elif self.MAT_FLAG == 1: # compund
            descriptor = self.DESCRIPTOR
            try:
                density = float(self.DENSITY)
            except:
                raise Exception("Density must be entered.")
        elif self.MAT_FLAG == 2: # nist list
            descriptor = xraylib.GetCompoundDataNISTList()[self.MAT_LIST]
            try:
                density = float(self.DENSITY)
            except:
                cp = xraylib.GetCompoundDataNISTByIndex(self.MAT_LIST)
                density = cp["density"]

        print("using descriptor = %s" % descriptor)
        print("using density = %g g/cm3" % density)



        out_dict = xoppy_calc_crosssec(
                descriptor                 = descriptor  ,
                density                    = density     ,
                MAT_FLAG                   = self.MAT_FLAG ,
                CALCULATE                  = self.CALCULATE,
                GRID                       = self.GRID     ,
                GRIDSTART                  = self.GRIDSTART,
                GRIDEND                    = self.GRIDEND  ,
                GRIDN                      = self.GRIDN    ,
                UNIT                       = self.UNIT     ,
                DUMP_TO_FILE               = self.DUMP_TO_FILE,
                FILE_NAME                  = self.FILE_NAME   ,
                material_constants_library = material_constants_library,
        )

        if "info" in out_dict.keys():
            print(out_dict["info"])

        dict_parameters = {
                "descriptor"                 : descriptor  ,
                "density"                    : density     ,
                "MAT_FLAG"                   : self.MAT_FLAG ,
                "CALCULATE"                  : self.CALCULATE,
                "GRID"                       : self.GRID     ,
                "GRIDSTART"                  : self.GRIDSTART,
                "GRIDEND"                    : self.GRIDEND  ,
                "GRIDN"                      : self.GRIDN    ,
                "UNIT"                       : self.UNIT     ,
                "DUMP_TO_FILE"               : self.DUMP_TO_FILE,
                "FILE_NAME"                  : self.FILE_NAME   ,
                "material_constants_library" : material_constants_library_str,
            }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)
        return out_dict

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:crosssec)
#
from xoppylib.scattering_functions.xoppy_calc_crosssec import xoppy_calc_crosssec
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

out_dict =  xoppy_calc_crosssec(
    descriptor   = "{descriptor}",
    density      = {density},
    MAT_FLAG     = {MAT_FLAG},
    CALCULATE    = {CALCULATE},
    GRID         = {GRID},
    GRIDSTART    = {GRIDSTART},
    GRIDEND      = {GRIDEND},
    GRIDN        = {GRIDN},
    UNIT         = {UNIT},
    DUMP_TO_FILE = {DUMP_TO_FILE},
    FILE_NAME    = "{FILE_NAME}",
    material_constants_library = {material_constants_library},
    )

#
# example plot
#
from srxraylib.plot.gol import plot

plot(out_dict["data"][0,:],out_dict["data"][-1,:],
    xtitle=out_dict["labels"][0],ytitle=out_dict["labels"][1],title="xcrosssec",
    xlog=True,ylog=True,show=True)

#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):

        out_dict = calculation_output
        # send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", out_dict["data"].T)
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", -1)
        except:
            pass
        try:
            calculated_data.add_content("labels", out_dict["labels"])
        except:
            pass
        try:
            calculated_data.add_content("info", out_dict["info"])
        except:
            pass


        #
        # display single point calculation
        #
        try:
            tmp = calculated_data.get_content("xoppy_data")
            try:
                labels = calculated_data.get_content("labels")
                self.xtitle = labels[0]
                self.ytitle = labels[1]
            except:
                self.xtitle = None
                self.ytitle = None

            if tmp.shape == (1, 2):  # single value calculation

                QMessageBox.information(self,
                                        "Calculation Result",
                                        "Calculation Result:\n"+calculated_data.get_content("info"),
                                        QMessageBox.Ok)
        except:
            pass

        return calculated_data

    def plot_results(self, calculated_data, progressBarValue=80):
        self.initializeTabs()

        try:
            calculated_data.get_content("xoppy_data")
            super().plot_results(calculated_data, progressBarValue)
        except:
            pass


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxcrosssec()
    w.show()
    app.exec()
    w.saveSettings()
