import numpy
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.xoppy_run_binaries import xoppy_calc_xtubes
from oasys.widgets.exchange import DataExchangeObject

class OWxtubes(XoppyWidget):
    name = "Tubes"
    id = "orange.widgets.dataxtubes"
    description = "X-ray tube Spectrum (Mo,Rh,W)"
    icon = "icons/xoppy_xtubes.png"
    priority = 15
    category = ""
    keywords = ["xoppy", "xtubes"]

    ITUBE = Setting(0)
    VOLTAGE = Setting(30.0)

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters",orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ITUBE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Mo', 'Rh', 'W'],
                    valueType=int, orientation="horizontal", labelWidth=330)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "VOLTAGE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['Target element ','Voltage  [kV] (18<V<42)']

    def unitFlags(self):
         return ['True','True']

    def get_help_name(self):
        return 'xtubes'

    def check_fields(self):
        if self.VOLTAGE <= 18 or self.VOLTAGE >= 42: raise Exception("Voltage out of range")

    def do_xoppy_calculation(self):
        out_file = xoppy_calc_xtubes(ITUBE=self.ITUBE,VOLTAGE=self.VOLTAGE)

        dict_parameters = {
                        "ITUBE": self.ITUBE,
                        "VOLTAGE"   : self.VOLTAGE,
                        }
        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)
        return out_file, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:xtubes)
#
import numpy
import scipy.constants as codata
from xoppylib.xoppy_run_binaries import xoppy_calc_xtubes

out_file =  xoppy_calc_xtubes(
        ITUBE    = {ITUBE},
        VOLTAGE = {VOLTAGE},
        )

# data to pass to power
data = numpy.loadtxt(out_file)
energy = data[:,0]
flux = data[:,1] # for units, see discussion in 'help'
spectral_power = flux / 0.5e-3 * energy * codata.e # W/eV/mA/mm^2(@?m) 
cumulated_power = spectral_power.cumsum() * numpy.abs(energy[1]-energy[0]) # W/mA/mm^2(@1m)

#
# example plot
#
from srxraylib.plot.gol import plot

plot(energy,flux,
    xtitle="Photon energy [eV]",ytitle="Fluence [photons/s/mm^2/0.5keV(bw)/mA]",title="xtubes Fluence",
    xlog=False,ylog=False,show=True)
plot(energy,spectral_power,
    xtitle="Photon energy [eV]",ytitle="Spectral Power [W/eV/mA/mm^2(@?m) ]",title="xtube_w Spectral Power",
    xlog=False,ylog=False,show=False)
plot(energy,cumulated_power,
    xtitle="Photon energy [eV]",ytitle="Cumulated Power [W/mA/mm^2(@?m) ]",title="xtube_w Cumulated Power",
    xlog=False,ylog=False,show=True)
    
#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):

        spec_file_name, script = calculation_output
        out = numpy.loadtxt(spec_file_name)
        if len(out) == 0: raise Exception("Calculation gave no results (empty data)")

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_specfile", spec_file_name)
        calculated_data.add_content("xoppy_data", out)
        calculated_data.add_content("xoppy_script", script)

        return calculated_data



    def get_data_exchange_widget_name(self):
        return "XTUBES"

    def getTitles(self):
        return ['X-Ray Tube Spectrum']

    def getXTitles(self):
        return ["Energy [eV]"]

    def getYTitles(self):
        return ["Fluence [photons/s/mm^2/0.5keV(bw)/mA]"]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = OWxtubes()
    w.show()
    app.exec()
    w.saveSettings()
