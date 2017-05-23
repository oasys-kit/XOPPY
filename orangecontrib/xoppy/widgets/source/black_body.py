import sys
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

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
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "E_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "E_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
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
        return self.xoppy_calc_black_body()

    def extract_data_from_xoppy_output(self, calculation_output):
        out_dict = calculation_output

        if "info" in out_dict.keys():
            print(out_dict["info"])

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", out_dict["data"])

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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

    def xoppy_calc_black_body(self):

        TITLE = self.TITLE
        TEMPERATURE = self.TEMPERATURE
        E_MIN = self.E_MIN
        E_MAX = self.E_MAX
        NPOINTS = self.NPOINTS
        try:

            import scipy.constants as codata

            #
            # text info
            #
            kb = codata.Boltzmann / codata.e # eV/K
            txt = ' \n'
            txt += 'Results of Black Body Radiation: Planck distribution\n'
            txt += 'TITLE: %s'%TITLE
            txt += ' \n'
            txt += '-------------------------------------------------------------\n'
            txt += 'Temperature           = %g K\n'%(TEMPERATURE)
            txt += 'Minimum photon energy = %g eV\n'%(E_MIN)
            txt += 'Maximum photon energy = %g eV\n'%(E_MAX)
            txt += '-------------------------------------------------------------\n'
            txt += 'Kb*T                = %g eV\n'%(TEMPERATURE*kb)
            txt += 'Peak at 2.822*Kb*T  = %g eV\n'%(2.822*TEMPERATURE*kb)
            txt += '-------------------------------------------------------------\n'

            # print(txt)

            #
            # calculation data
            #
            e_ev = numpy.linspace(E_MIN,E_MAX,NPOINTS)
            e_kt = e_ev/(TEMPERATURE*kb)
            brightness=3.146e11*(TEMPERATURE*kb)**3*e_kt**3/(numpy.exp(e_kt)-1)
            a3 = numpy.zeros((4,NPOINTS))
            a3[0,:] = e_ev
            a3[1,:] = e_kt
            a3[2,:] = brightness
            a3[3,:] = brightness*1e3*codata.e

            labels = ["Photon energy [eV]","Photon energy/(Kb*T)", "Brightness [Photons/sec/mm2/mrad2/0.1%bw]", "Spectral Power [Watts/eV/mrad2/mm2]"]

            return {"application":"xoppy","name":"black_body","data":a3.T,"labels":labels,"info":txt}


        except Exception as e:
            raise e

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWblack_body()
    w.show()
    app.exec()
    w.saveSettings()
