import sys
import numpy
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.sources.xoppy_calc_black_body import xoppy_calc_black_body

class OWblack_body(XoppyWidget):
    name = "Black Body"
    id = "orange.widgets.datablack_body"
    description = "Black Body Spectrum"
    icon = "icons/xoppy_black_body.png"
    priority = 19
    category = ""
    keywords = ["xoppy", "black_body"]

    TITLE = Setting("Thermal source: Planck distribution")
    TEMPERATURE = Setting(1200000.0)
    E_MIN = Setting(10.0)
    E_MAX = Setting(1000.0)
    NPOINTS = Setting(500)

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TEMPERATURE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "E_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "E_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['Title','Temperature [K]','Min energy [eV]','Max energy [eV]','Number of points ']

    def unitFlags(self):
         return ['True','True','True','True','True']

    def get_help_name(self):
        return 'black_body'

    def check_fields(self):
        self.TEMPERATURE = congruence.checkPositiveNumber(self.TEMPERATURE, "Temperature")
        self.E_MIN = congruence.checkPositiveNumber(self.E_MIN, "Min Energy")
        self.E_MAX = congruence.checkStrictlyPositiveNumber(self.E_MAX, "Max Energy")
        congruence.checkLessThan(self.E_MIN, self.E_MAX, "Min Energy", "Max Energy")
        self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.NPOINTS, "Number of Points")


    def do_xoppy_calculation(self):

        out_dict = xoppy_calc_black_body(
            TITLE       = self.TITLE,
            TEMPERATURE = self.TEMPERATURE,
            E_MIN       = self.E_MIN,
            E_MAX       = self.E_MAX,
            NPOINTS     = self.NPOINTS,
        )

        dict_parameters = {
            "TITLE"       : self.TITLE,
            "TEMPERATURE" : self.TEMPERATURE,
            "E_MIN"       : self.E_MIN,
            "E_MAX"       : self.E_MAX,
            "NPOINTS"     : self.NPOINTS,
        }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)

        return out_dict, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:black_body)
#
from xoppylib.sources.xoppy_calc_black_body import xoppy_calc_black_body

out_dict =  xoppy_calc_black_body(
        TITLE       = "{TITLE}",
        TEMPERATURE = {TEMPERATURE},
        E_MIN       = {E_MIN},
        E_MAX       = {E_MAX},
        NPOINTS     = {NPOINTS},
        )

#
# example plot
#
import numpy
from srxraylib.plot.gol import plot
        
energy = out_dict["data"][:,0]
brightness = out_dict["data"][:,2]
spectral_power = out_dict["data"][:,3]

plot(energy,brightness,
    xtitle="Photon energy [eV]",ytitle="Brightness [Photons/sec/0.1%bw/mm2/mrad2]",title="black_body brightness",
    xlog=False,ylog=False,show=False)
plot(energy,spectral_power,
    xtitle="Photon energy [eV]",ytitle="Spectral Power [W/eV/mrad2/mm2]",title="black_body Spectral Power",
    xlog=False,ylog=False,show=True)


#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):
        out_dict, script = calculation_output

        if "info" in out_dict.keys():
            print(out_dict["info"])

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", out_dict["data"])
        calculated_data.add_content("xoppy_script", script)

        return calculated_data

    def get_data_exchange_widget_name(self):
        return "BLACK_BODY"

    def getTitles(self):
        return ["Brightness", "Spectral Power"]

    def getXTitles(self):
        return ["Energy [eV]", "Energy [eV]"]

    def getYTitles(self):
        return ["Brightness [Photons/sec/0.1%bw/mm2/mrad2]", "Spectral Power [Watts/eV/mrad2/mm2]"]

    def getVariablesToPlot(self):
        return [(0, 2), (0, 3)]

    def getLogPlot(self):
        return[(False, False), (False, False)]



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWblack_body()
    w.show()
    app.exec()
    w.saveSettings()
