from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject


from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from dabax.dabax_files import dabax_f0_files

from xoppylib.scattering_functions.xoppy_calc_f0 import xoppy_calc_f0

import xraylib
from dabax.dabax_xraylib import DabaxXraylib


class OWxf0(XoppyWidget):
    name = "F0"
    id = "orange.widgets.dataxf0"
    description = "Elastic Scattering Function"
    icon = "icons/xoppy_xf0.png"
    priority = 13
    category = ""
    keywords = ["xoppy", "xf0"]

    DESCRIPTOR   = Setting("Si")
    MAT_FLAG     = Setting(0)
    GRIDSTART    = Setting(0.0)
    GRIDEND      = Setting(8.0)
    GRIDN        = Setting(100)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME    = Setting("f0.dat")
    CHARGE       = Setting(0.0)
    MATERIAL_CONSTANT_LIBRARY_FLAG = Setting(0)

    NIST_NAME    = Setting(177)
    DABAX_F0_FILE_INDEX = Setting(0)

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

        #widget index 2
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], orientation="horizontal", addSpace=False)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        self.nist_list = xraylib.GetCompoundDataNISTList()
        gui.comboBox(box1, self, "NIST_NAME",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=self.nist_list,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
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


        box = oasysgui.widgetBox(self.controlArea, self.name + " Material Library", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        # widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "MATERIAL_CONSTANT_LIBRARY_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["xraylib [default]", "dabax"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DABAX_F0_FILE_INDEX",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=dabax_f0_files(),
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material','formula','name','From q [sin(theta)/lambda]: ','To q [sin(theta)/lambda]: ','Number of q points',
                 'Dump to file','File name','Material Library','dabax f0 file']

    def unitFlags(self):
         return ['True','self.MAT_FLAG  !=  2','self.MAT_FLAG  ==  2','True','True','True',
                 'True','self.DUMP_TO_FILE == 1','True', 'self.MATERIAL_CONSTANT_LIBRARY_FLAG == 1']

    def get_help_name(self):
        return 'f0'

    def check_fields(self):
        self.DESCRIPTOR = congruence.checkEmptyString(self.DESCRIPTOR, "formula")
        self.GRIDSTART = congruence.checkPositiveNumber(self.GRIDSTART, "Q from")
        self.GRIDEND = congruence.checkStrictlyPositiveNumber(self.GRIDEND, "Q to")
        congruence.checkLessThan(self.GRIDSTART, self.GRIDEND, "Q from", "Q to")
        self.GRIDN = congruence.checkStrictlyPositiveNumber(self.GRIDN, "Number of q Points")

    def do_xoppy_calculation(self):


        if self.MAT_FLAG == 2:
            descriptor = self.nist_list[self.NIST_NAME]
        else:
            descriptor = self.DESCRIPTOR

        if self.MATERIAL_CONSTANT_LIBRARY_FLAG == 0:
            material_constants_library = xraylib
            material_constants_library_str = "xraylib"
        else:
            material_constants_library = DabaxXraylib(file_f0=dabax_f0_files()[self.DABAX_F0_FILE_INDEX])
            material_constants_library_str = 'DabaxXraylib(file_f0="%s")' % (dabax_f0_files()[self.DABAX_F0_FILE_INDEX])
            print(material_constants_library.info())

        out_dict = xoppy_calc_f0(
                descriptor                  = descriptor,
                MAT_FLAG                    = self.MAT_FLAG,
                GRIDSTART                   = self.GRIDSTART,
                GRIDEND                     = self.GRIDEND,
                GRIDN                       = self.GRIDN,
                DUMP_TO_FILE                = self.DUMP_TO_FILE,
                FILE_NAME                   = self.FILE_NAME,
                CHARGE                      = 0.0,
                material_constants_library  = material_constants_library,
                )

        if "info" in out_dict.keys():
            print(out_dict["info"])

        dict_parameters = {
                "descriptor"                      : descriptor,
                "MAT_FLAG"                        : self.MAT_FLAG,
                "GRIDSTART"                       : self.GRIDSTART,
                "GRIDEND"                         : self.GRIDEND,
                "GRIDN"                           : self.GRIDN,
                "DUMP_TO_FILE"                    : self.DUMP_TO_FILE,
                "FILE_NAME"                       : self.FILE_NAME,
                "CHARGE"                          : 0.0,
                "material_constants_library_str"  : material_constants_library_str,
            }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)

        return out_dict

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:xf0)
#
from xoppylib.scattering_functions.xoppy_calc_f0 import xoppy_calc_f0
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

out_dict =  xoppy_calc_f0(
        descriptor                  = "{descriptor}",
        MAT_FLAG                    = {MAT_FLAG},
        GRIDSTART                   = {GRIDSTART},
        GRIDEND                     = {GRIDEND},
        GRIDN                       = {GRIDN},
        DUMP_TO_FILE                = {DUMP_TO_FILE},
        FILE_NAME                   = "{FILE_NAME}",
        CHARGE                      = 0.0,
        material_constants_library  = {material_constants_library_str},
        )

#
# example plot
#
from srxraylib.plot.gol import plot
plot(out_dict["data"][0,:],out_dict["data"][-1,:],
    xtitle=out_dict["labels"][0],ytitle=out_dict["labels"][1],title="f0",
    xlog=False,ylog=False,show=True)
#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):
        out_dict = calculation_output

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

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "XF0"

    def getTitles(self):
        return ["f0"]

    def getXTitles(self):
        return ["q=sin(theta)/lambda [A^-1]"]

    def getYTitles(self):
        return ["f0 [electron units]"]

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = OWxf0()
    w.show()
    app.exec()
    w.saveSettings()
