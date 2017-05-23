import sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

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


    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters",orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "VOLTAGE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "RIPPLE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "AL_FILTER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
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
        return xoppy_calc_xtube_w(VOLTAGE=self.VOLTAGE,RIPPLE=self.RIPPLE,AL_FILTER=self.AL_FILTER)

    def get_data_exchange_widget_name(self):
        return "XTUBE_W"

    def getTitles(self):
        return ['W X-Ray Tube Spectrum']

    def getXTitles(self):
        return ["Energy [eV]"]

    def getYTitles(self):
        return ["Flux [photons/1keV(bw)/mA/mm^2(@1m)/s])"]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def xoppy_calc_xtube_w(VOLTAGE=100.0,RIPPLE=0.0,AL_FILTER=0.0):
    print("Inside xoppy_calc_xtube_w. ")

    for file in ["tasmip_tmp.dat"]:
        try:
            os.remove(os.path.join(locations.home_bin_run(),file))
        except:
            pass

    try:
        with open("xoppy.inp","wt") as f:
            f.write("%f\n%f\n%f\n"%(VOLTAGE,RIPPLE,AL_FILTER))
    
        command = "'" + os.path.join(locations.home_bin(), 'tasmip') + "' < xoppy.inp"
        print("Running command '%s' in directory: %s \n"%(command,locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

        return "tasmip_tmp.dat"
    except Exception as e:
        raise e


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtube_w()
    w.show()
    app.exec()
    w.saveSettings()
