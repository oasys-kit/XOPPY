import sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

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
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
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
        return xoppy_calc_xtubes(ITUBE=self.ITUBE,VOLTAGE=self.VOLTAGE)

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

def xoppy_calc_xtubes(ITUBE=0,VOLTAGE=30.0):
    print("Inside xoppy_calc_xtubes. ")

    for file in ["xtubes_tmp.dat"]:
        try:
            os.remove(os.path.join(locations.home_bin_run(),file))
        except:
            pass

    try:
        with open("xoppy.inp","wt") as f:
            f.write("%d\n%f\n"%(ITUBE+1,VOLTAGE))
    
        command = "'" + os.path.join(locations.home_bin(), "xtubes") + "' < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

        return os.path.join(locations.home_bin_run(), "xtubes_tmp.dat")
    except Exception as e:
        raise e



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtubes()
    w.show()
    app.exec()
    w.saveSettings()
