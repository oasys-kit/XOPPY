import numpy
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.xoppy_run_binaries import xoppy_calc_xtube_w
from oasys.widgets.exchange import DataExchangeObject

class OWxtube_w(XoppyWidget):
    name = "Tube_W"
    id = "orange.widgets.dataxtube_w"
    description = "X-ray tube Spectrum (W)"
    icon = "icons/xoppy_xtube_w.png"
    priority = 17
    category = ""
    keywords = ["xoppy", "xtube_w"]

    VOLTAGE = Setting(100.0)
    RIPPLE = Setting(0.0)
    AL_FILTER = Setting(0.0)

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters",orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "VOLTAGE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "RIPPLE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "AL_FILTER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['Voltage 30<V<140 (kV)','Voltage ripple (%)','Al filter [mm]']


    def unitFlags(self):
         return ['True','True','True']

    def get_help_name(self):
        return 'xtube_w'

    def check_fields(self):
        self.VOLTAGE = congruence.checkStrictlyPositiveNumber(self.VOLTAGE, "Voltage")
        if self.VOLTAGE < 30 or self.VOLTAGE > 140: raise Exception("Voltage out of range")
        self.RIPPLE = congruence.checkPositiveNumber(self.RIPPLE, "Voltage ripple")
        self.AL_FILTER = congruence.checkPositiveNumber(self.AL_FILTER, "Al filter")

    def do_xoppy_calculation(self):
        out_file = xoppy_calc_xtube_w(VOLTAGE=self.VOLTAGE,RIPPLE=self.RIPPLE,AL_FILTER=self.AL_FILTER)
        dict_parameters = {
                        "VOLTAGE"   : self.VOLTAGE,
                        "RIPPLE"    : self.RIPPLE,
                        "AL_FILTER" : self.AL_FILTER,
                        }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)
        return out_file, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:xtube_w)
#
import numpy
import scipy.constants as codata
from xoppylib.xoppy_run_binaries import xoppy_calc_xtube_w

out_file =  xoppy_calc_xtube_w(
        VOLTAGE = {VOLTAGE},
        RIPPLE    = {RIPPLE},
        AL_FILTER = {AL_FILTER},
        )

# data to pass to power
data = numpy.loadtxt(out_file)
energy = data[:,0]
flux = data[:,1] # photons/1keV(bw)/mA/mm^2(@1m)/s
spectral_power = flux * 1e3 * energy * codata.e # W/eV/mA/mm^2(@1m)
cumulated_power = spectral_power.cumsum() * numpy.abs(energy[1]-energy[0]) # W/mA/mm^2(@1m)

#
# example plot
#
from srxraylib.plot.gol import plot
plot(energy,flux,
    xtitle="Photon energy [eV]",ytitle="Flux [photons/1keV(bw)/mA/mm^2(@1m)/s]",title="xtube_w Flux",
    xlog=False,ylog=False,show=False)
plot(energy,spectral_power,
    xtitle="Photon energy [eV]",ytitle="Spectral Power [W/eV/mA/mm^2(@1m)]",title="xtube_w Spectral Power",
    xlog=False,ylog=False,show=False)
plot(energy,cumulated_power,
    xtitle="Photon energy [eV]",ytitle="Cumulated Power [W/mA/mm^2(@1m)]",title="xtube_w Cumulated Power",
    xlog=False,ylog=False,show=True)
    
#
# end script
#
"""


    def extract_data_from_xoppy_output(self, calculation_output):

        spec_file_name, script = calculation_output
        out = numpy.loadtxt(spec_file_name)
        if len(out) == 0 : raise Exception("Calculation gave no results (empty data)")

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_specfile", spec_file_name)
        calculated_data.add_content("xoppy_data", out)
        calculated_data.add_content("xoppy_script", script)

        return calculated_data

    def get_data_exchange_widget_name(self):
        return "XTUBE_W"

    def getTitles(self):
        return ['W X-Ray Tube Spectrum']

    def getXTitles(self):
        return ["Energy [eV]"]

    def getYTitles(self):
        return ["Flux [photons/1keV(bw)/mA/mm^2(@1m)/s])"]




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = OWxtube_w()
    w.show()
    app.exec()
    w.saveSettings()
