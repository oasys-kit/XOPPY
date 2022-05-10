import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.scattering_functions.xoppy_calc_f1f2 import xoppy_calc_f1f2
from dabax.dabax_files import dabax_f1f2_files

import xraylib
from dabax.dabax_xraylib import DabaxXraylib


class OWxf1f2(XoppyWidget):
    name = "F1F2"
    id = "orange.widgets.dataxf1f2"
    description = "X-ray Matter Scattering Functions and Reflectivity"
    icon = "icons/xoppy_xf1f2.png"
    priority = 15
    category = ""
    keywords = ["xoppy", "xf1f2"]


    DESCRIPTOR   = Setting("Si")
    DENSITY      = Setting("?")
    MAT_FLAG     = Setting(0)
    NIST_NAME    = Setting(177)
    CALCULATE    = Setting(1)
    GRID         = Setting(0)
    GRIDSTART    = Setting(5000.0)
    GRIDEND      = Setting(25000.0)
    GRIDN        = Setting(100)
    THETAGRID    = Setting(0)
    ROUGH        = Setting(0.0)
    THETA1       = Setting(2.0)
    THETA2       = Setting(5.0)
    THETAN       = Setting(50)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME    = Setting("f1f2.dat")

    MATERIAL_CONSTANT_LIBRARY_FLAG = Setting(0)
    DABAX_F1F2_FILE_INDEX = Setting(0)

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
                    items=['Element(formula)', 'Compound(formula)','Compound(NIST list)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 


        #widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        self.nist_list = xraylib.GetCompoundDataNISTList()
        gui.comboBox(box1, self, "NIST_NAME",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=self.nist_list,
                    valueType=int, orientation="horizontal", labelWidth=150)
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
                    items=['f1', 'f2', 'delta', 'beta [includes all cross sections]', \
                           'mu [cm^-1] [only photoelectric CS]', \
                           'mu [cm^2/g] [only photoelectric CS]', 'Cross Section [barn] [only photoelectric CS]', \
                           'reflectivity-s', 'reflectivity-p', 'reflectivity-unpol', 'delta/beta'],
                    valueType=int, orientation="horizontal", labelWidth=150)
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
        gui.comboBox(box1, self, "THETAGRID",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Single value', 'User Defined'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ROUGH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THETA1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETA2",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETAN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        # widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["No", "Yes"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #

        box = oasysgui.widgetBox(self.controlArea, self.name + " Material Library", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)


        # widget index 17
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "MATERIAL_CONSTANT_LIBRARY_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["xraylib [default]", "dabax"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 18
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DABAX_F1F2_FILE_INDEX",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=dabax_f1f2_files(),
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        gui.rubber(self.controlArea)



    def unitLabels(self):
         return ['material',  #   True',
                 'formula',  #   self.MAT_FLAG  <=  1',
                 'name',
                 'density',  #   self.MAT_FLAG  ==  1  &  (s
                 'Calculate',  #   True',
                 'Energy [eV] grid:',  #   True',
                 'Starting Energy [eV]: ',  #   self.GRID  !=  0',
                 'To: ',  #   self.GRID  ==  1',
                 'Number of points',  #   self.GRID  ==  1',
                 'Grazing angle',  #   self.CALCULATE  ==  0 or (s
                 'Roughness rms [A]',  #   self.CALCULATE  ==  0 or (s
                 'Starting Graz angle [mrad]',  #   self.CALCULATE  ==  0 or (s
                 'To [mrad]',  #   (self.CALCULATE  ==  0 or (
                 'Number of angular points',  #   (self.CALCULATE  ==  0 or (
                 'Dump to file',
                 'File name',
                 'Material Library',
                 'dabax f1f2 file']


    def unitFlags(self):
         return ['True',
                 'self.MAT_FLAG  in [0,1]',
                 'self.MAT_FLAG  ==  2',
                 'True', #'self.MAT_FLAG  ==  1  or (self.MAT_FLAG  ==  1 and  (self.CALCULATE  ==  2 or self.CALCULATE  ==  3 or self.CALCULATE  ==  4 or self.CALCULATE  ==  7 or self.CALCULATE  ==  8 or self.CALCULATE  ==  9 or self.CALCULATE  ==  10 ))  ',
                 'True',
                 'True',
                 'self.GRID  !=  0',
                 'self.GRID  ==  1',
                 'self.GRID  ==  1',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 '(self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9)  &  self.THETAGRID  ==  1',
                 '(self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9)  &  self.THETAGRID  ==  1',
                 'True',
                 'self.DUMP_TO_FILE == 1',
                 'True',
                 'self.MATERIAL_CONSTANT_LIBRARY_FLAG == 1']

    def get_help_name(self):
        return 'f1f2'

    def check_fields(self):
        self.DESCRIPTOR = congruence.checkEmptyString(self.DESCRIPTOR, "formula")
        # if self.MAT_FLAG == 1:
        #     self.DENSITY = congruence.checkStrictlyPositiveNumber(self.DENSITY, "density")

        if self.GRID > 0:
            self.GRIDSTART = congruence.checkPositiveNumber(self.GRIDSTART, "Starting Energy")

            if self.GRID == 1:
                self.GRIDEND = congruence.checkStrictlyPositiveNumber(self.GRIDEND, "Energy to")
                congruence.checkLessThan(self.GRIDSTART, self.GRIDEND, "Starting Energy", "Energy to")
                self.GRIDN = congruence.checkStrictlyPositiveNumber(self.GRIDN, "Number of points")

        if self.CALCULATE >= 7 and self.CALCULATE <= 9:
            self.ROUGH = congruence.checkPositiveNumber(self.ROUGH, "Roughness")
            self.THETA1 = congruence.checkPositiveNumber(self.THETA1, "Starting Graz angle")

            if self.THETAGRID == 1:
                self.THETA2 = congruence.checkStrictlyPositiveNumber(self.THETA2, "Graz angle to")
                congruence.checkLessThan(self.THETA1, self.THETA2, "Starting Graz angle", "Graz angle to")
                self.THETAN = congruence.checkStrictlyPositiveNumber(self.THETAN, "Number of angular points")
        else:
            self.THETAGRID = 0

    def do_xoppy_calculation(self):

        if self.MATERIAL_CONSTANT_LIBRARY_FLAG == 0:
            material_constants_library = xraylib
            material_constants_library_str = "xraylib"
        else:
            material_constants_library = DabaxXraylib(file_f1f2=dabax_f1f2_files()[self.DABAX_F1F2_FILE_INDEX])
            material_constants_library_str = 'DabaxXraylib(file_f1f2="%s")' % (dabax_f1f2_files()[self.DABAX_F1F2_FILE_INDEX])
            print(material_constants_library.info())


        if self.MAT_FLAG == 0: # element
            descriptor = self.DESCRIPTOR
            # density = element_density(DESCRIPTOR)
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
            descriptor = self.nist_list[self.NIST_NAME]
            try:
                density = float(self.DENSITY)
            except:
                cp = xraylib.GetCompoundDataNISTByIndex(self.NIST_NAME)
                density = cp["density"]

        print("Using descriptor: %s" % descriptor)
        print("Using density: %6.3f" % density)

        out_dict = xoppy_calc_f1f2(
            descriptor                 = descriptor  ,
            density                    = density     ,
            MAT_FLAG                   = self.MAT_FLAG    ,
            CALCULATE                  = self.CALCULATE   ,
            GRID                       = self.GRID        ,
            GRIDSTART                  = self.GRIDSTART   ,
            GRIDEND                    = self.GRIDEND     ,
            GRIDN                      = self.GRIDN       ,
            THETAGRID                  = self.THETAGRID   ,
            ROUGH                      = self.ROUGH       ,
            THETA1                     = self.THETA1      ,
            THETA2                     = self.THETA2      ,
            THETAN                     = self.THETAN      ,
            DUMP_TO_FILE               = self.DUMP_TO_FILE,
            FILE_NAME                  = self.FILE_NAME   ,
            material_constants_library = material_constants_library,
        )

        if "info" in out_dict.keys():
            print(out_dict["info"])

        dict_parameters = {
            "descriptor"                 : descriptor  ,
            "density"                    : density     ,
            "MAT_FLAG"                   : self.MAT_FLAG    ,
            "CALCULATE"                  : self.CALCULATE   ,
            "GRID"                       : self.GRID        ,
            "GRIDSTART"                  : self.GRIDSTART   ,
            "GRIDEND"                    : self.GRIDEND     ,
            "GRIDN"                      : self.GRIDN       ,
            "THETAGRID"                  : self.THETAGRID   ,
            "ROUGH"                      : self.ROUGH       ,
            "THETA1"                     : self.THETA1      ,
            "THETA2"                     : self.THETA2      ,
            "THETAN"                     : self.THETAN      ,
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
# script to make the calculations (created by XOPPY:xf1f2)
#
from xoppylib.scattering_functions.xoppy_calc_f1f2 import xoppy_calc_f1f2
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

out_dict =  xoppy_calc_f1f2(
        descriptor   = "{descriptor}",
        density      = {density},
        MAT_FLAG     = {MAT_FLAG},
        CALCULATE    = {CALCULATE},
        GRID         = {GRID},
        GRIDSTART    = {GRIDSTART},
        GRIDEND      = {GRIDEND},
        GRIDN        = {GRIDN},
        THETAGRID    = {THETAGRID},
        ROUGH        = {ROUGH},
        THETA1       = {THETA1},
        THETA2       = {THETA2},
        THETAN       = {THETAN},
        DUMP_TO_FILE = {DUMP_TO_FILE},
        FILE_NAME    = "{FILE_NAME}",
        material_constants_library = {material_constants_library},
    )

#
# example plot
#
from srxraylib.plot.gol import plot, plot_image
try:
    plot(out_dict["data"][0,:],out_dict["data"][-1,:],
        xtitle=out_dict["labels"][0],ytitle=out_dict["labels"][1],title="xf1f2",
        xlog=True,ylog=True,show=True)
except:
    plot_image(out_dict["data2D"],out_dict["dataX"],out_dict["dataY"],
        xtitle='Energy [eV]',ytitle='Theta [mrad]',title='Reflectivity',
        aspect='auto',show=True)
#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):

        out_dict = calculation_output

        #send exchange
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

        try:
            calculated_data.add_content("data2D", out_dict["data2D"])
            calculated_data.add_content("dataX", out_dict["dataX"])
            calculated_data.add_content("dataY", out_dict["dataY"])
        except:
            pass

        #
        # display single point results
        #
        try:
            calculated_data.get_content("data2D")
        except:
            try:
                tmp = calculated_data.get_content("xoppy_data")
                labels = calculated_data.get_content("labels")

                self.xtitle = labels[0]
                self.ytitle = labels[1]

                if tmp.shape == (1, 2): # single value calculation
                    message = calculated_data.get_content("info")
                    QMessageBox.information(self,
                                            "Calculation Result",
                                            "Calculation Result:\n %s"%message,
                                            QMessageBox.Ok)

            except:
                QMessageBox.information(self,
                                        "Calculation Result",
                                        "Calculation Result:\n"+calculated_data.get_content("info"),
                                        QMessageBox.Ok)

                self.xtitle = None
                self.ytitle = None

        return calculated_data


    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:
                try:
                    calculated_data.get_content("xoppy_data")

                    self.tab[0].layout().removeItem(self.tab[0].layout().itemAt(0))
                    self.plot_canvas[0] = None

                    super().plot_results(calculated_data, progressBarValue)
                except:
                    try:
                        data2D = calculated_data.get_content("data2D")
                        dataX = calculated_data.get_content("dataX")
                        dataY = calculated_data.get_content("dataY")

                        self.plot_data2D(data2D, dataX, dataY, 0, 0,
                                         xtitle='Energy [eV]',
                                         ytitle='Theta [mrad]',
                                         title='Reflectivity')
                    except:
                        pass

            else:
                raise Exception("Empty Data")

    def get_data_exchange_widget_name(self):
        return "XF1F2"

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

    def getVariablesToPlot(self):
        return [(0, 1)]

    def getLogPlot(self):
        return[(True, True)]

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):
        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        # place a big dot if there is only a single value
        if ((x.size == 1) and (y.size == 1)):
            self.plot_canvas[plot_canvas_index].setDefaultPlotLines(False)
            self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxf1f2()
    w.show()
    app.exec()
    w.saveSettings()
