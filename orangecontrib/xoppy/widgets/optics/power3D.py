import sys
import numpy
from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence


from oasys.widgets.exchange import DataExchangeObject
# from orangecontrib.xoppy.util.xoppy_exchange import RadiationDataExchangeObject #as DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util.xoppy_xraylib_util import reflectivity_fresnel

import scipy.constants as codata
import xraylib


class OWpower3D(XoppyWidget):
    name = "POWER3D"
    id = "orange.widgets.datapower3D"
    description = "Power (vs Energy and spatial coordinates) Absorbed and Transmitted by Optical Elements"
    icon = "icons/xoppy_power3d.png"
    priority = 3
    category = ""
    keywords = ["xoppy", "power3D"]

    inputs = [{"name": "ExchangeData",
               "type": DataExchangeObject,
               "handler": "acceptExchangeData" } ]
    # [("ExchangeData", DataExchangeObject, "acceptExchangeData")]
    # inputs = [("xoppy_data", DataExchangeObject, "acceptExchangeData")]


    NELEMENTS = Setting(1)
    EL1_FOR = Setting("Be")
    EL1_FLAG = Setting(0)
    EL1_THI = Setting(0.5)
    EL1_ANG = Setting(3.0)
    EL1_ROU = Setting(0.0)
    EL1_DEN = Setting("?")
    EL2_FOR = Setting("Rh")
    EL2_FLAG = Setting(1)
    EL2_THI = Setting(0.5)
    EL2_ANG = Setting(3.0)
    EL2_ROU = Setting(0.0)
    EL2_DEN = Setting("?")
    EL3_FOR = Setting("Al")
    EL3_FLAG = Setting(0)
    EL3_THI = Setting(0.5)
    EL3_ANG = Setting(3.0)
    EL3_ROU = Setting(0.0)
    EL3_DEN = Setting("?")
    EL4_FOR = Setting("B")
    EL4_FLAG = Setting(0)
    EL4_THI = Setting(0.5)
    EL4_ANG = Setting(3.0)
    EL4_ROU = Setting(0.0)
    EL4_DEN = Setting("?")
    EL5_FOR = Setting("Pt")
    EL5_FLAG = Setting(1)
    EL5_THI = Setting(0.5)
    EL5_ANG = Setting(3.0)
    EL5_ROU = Setting(0.0)
    EL5_DEN = Setting("?")
    PLOT_SETS = Setting(1)
    FILE_DUMP = 0

    def build_gui(self):

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        idx = -1 


        #widget index 10
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "NELEMENTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['0','1', '2', '3', '4', '5'],
                    valueType=int, orientation="horizontal", callback=self.set_NELEMENTS, labelWidth=330)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.separator(box1, height=7)

        oasysgui.lineEdit(box1, self, "EL1_FOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL1_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL1_THI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL1_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL1_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL1_DEN",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 17
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.separator(box1, height=7)

        oasysgui.lineEdit(box1, self, "EL2_FOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL2_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL2_THI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL2_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL2_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL2_DEN",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.separator(box1, height=7)

        oasysgui.lineEdit(box1, self, "EL3_FOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL3_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL3_THI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 26 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL3_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 27 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL3_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 28 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL3_DEN",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 29 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.separator(box1, height=7)

        oasysgui.lineEdit(box1, self, "EL4_FOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 30 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL4_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 31 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL4_THI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 32 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL4_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 33 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL4_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 34 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL4_DEN",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 35 
        idx += 1 
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        oasysgui.lineEdit(box1, self, "EL5_FOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 36 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "EL5_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Filter', 'Mirror'],
                    valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 37 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL5_THI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 38 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL5_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 39 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL5_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 40 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL5_DEN",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 41
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "PLOT_SETS",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Input beam',
                           'Beam transmitted after last element',
                           'Absorption by ALL elements',
                           'Absorption by LAST element'],
                    valueType=int, orientation="horizontal", labelWidth=250, callback=self.replot_results)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 42
        # idx += 1
        # box1 = gui.widgetBox(box)
        # gui.separator(box1, height=7)
        #
        # gui.comboBox(box1, self, "FILE_DUMP",
        #              label=self.unitLabels()[idx], addSpace=False,
        #             items=['No', 'Yes (power.spec)'],
        #             valueType=int, orientation="horizontal", labelWidth=250)
        # self.show_at(self.unitFlags()[idx], box1)

    def set_NELEMENTS(self):
        self.initializeTabs()

    def set_EL_FLAG(self):
        self.initializeTabs()

    def unitLabels(self):
         return ['Number of elements:',
                 '1st oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '2nd oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '3rd oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '4th oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '5th oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 "Plot","Dump file"]


    def unitFlags(self):
         return ['True',
                 'self.NELEMENTS  >=  1+0',' self.NELEMENTS  >=  1+0','self.EL1_FLAG  ==  0  and  self.NELEMENTS  >=  1+0','self.EL1_FLAG  !=  0  and  self.NELEMENTS  >=  1+0','self.EL1_FLAG  !=  0  and  self.NELEMENTS  >=  1+0',' self.NELEMENTS  >=  1+0',
                 'self.NELEMENTS  >=  1+1',' self.NELEMENTS  >=  1+1','self.EL2_FLAG  ==  0  and  self.NELEMENTS  >=  1+1','self.EL2_FLAG  !=  0  and  self.NELEMENTS  >=  1+1','self.EL2_FLAG  !=  0  and  self.NELEMENTS  >=  1+1',' self.NELEMENTS  >=  1+1',
                 'self.NELEMENTS  >=  1+2',' self.NELEMENTS  >=  1+2','self.EL3_FLAG  ==  0  and  self.NELEMENTS  >=  1+2','self.EL3_FLAG  !=  0  and  self.NELEMENTS  >=  1+2','self.EL3_FLAG  !=  0  and  self.NELEMENTS  >=  1+2',' self.NELEMENTS  >=  1+2',
                 'self.NELEMENTS  >=  1+3',' self.NELEMENTS  >=  1+3','self.EL4_FLAG  ==  0  and  self.NELEMENTS  >=  1+3','self.EL4_FLAG  !=  0  and  self.NELEMENTS  >=  1+3','self.EL4_FLAG  !=  0  and  self.NELEMENTS  >=  1+3',' self.NELEMENTS  >=  1+3',
                 'self.NELEMENTS  >=  1+4',' self.NELEMENTS  >=  1+4','self.EL5_FLAG  ==  0  and  self.NELEMENTS  >=  1+4','self.EL5_FLAG  !=  0  and  self.NELEMENTS  >=  1+4','self.EL5_FLAG  !=  0  and  self.NELEMENTS  >=  1+4',' self.NELEMENTS  >=  1+4',
                 'True','True']

    def get_help_name(self):
        return 'power3d'

    def acceptExchangeData(self, exchangeData):
        try:
            if not exchangeData is None:
                if exchangeData.get_program_name() == "XOPPY":
                    if exchangeData.get_widget_name() =="UNDULATOR_RADIATION" :
                        pass
                    elif exchangeData.get_widget_name() =="POWER3D" :
                        pass
                    else:
                        raise Exception("Xoppy Input beam not recognized")

                    self.input_beam = exchangeData
                    self.output_beam = None
                    self.process_showers()


                    self.compute()


        except Exception as exception:
            QMessageBox.critical(self, "Error",
                                       str(exception),
                QMessageBox.Ok)




    def check_fields(self):


        if self.NELEMENTS >= 1:
            self.EL1_FOR = congruence.checkEmptyString(self.EL1_FOR, "1st oe formula")

            if self.EL1_FLAG == 0: # filter
                self.EL1_THI = congruence.checkStrictlyPositiveNumber(self.EL1_THI, "1st oe filter thickness")
            elif self.EL1_FLAG == 1: # mirror
                self.EL1_ANG = congruence.checkStrictlyPositiveNumber(self.EL1_ANG, "1st oe mirror angle")
                self.EL1_ROU = congruence.checkPositiveNumber(self.EL1_ROU, "1st oe mirror roughness")

            if not self.EL1_DEN.strip() == "?":
                self.EL1_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL1_DEN, "1st oe density")), "1st oe density"))

        if self.NELEMENTS >= 2:
            self.EL2_FOR = congruence.checkEmptyString(self.EL2_FOR, "2nd oe formula")

            if self.EL2_FLAG == 0: # filter
                self.EL2_THI = congruence.checkStrictlyPositiveNumber(self.EL2_THI, "2nd oe filter thickness")
            elif self.EL2_FLAG == 1: # mirror
                self.EL2_ANG = congruence.checkStrictlyPositiveNumber(self.EL2_ANG, "2nd oe mirror angle")
                self.EL2_ROU = congruence.checkPositiveNumber(self.EL2_ROU, "2nd oe mirror roughness")

            if not self.EL2_DEN.strip() == "?":
                self.EL2_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL2_DEN, "2nd oe density")), "2nd oe density"))

        if self.NELEMENTS >= 3:
            self.EL3_FOR = congruence.checkEmptyString(self.EL3_FOR, "3rd oe formula")

            if self.EL3_FLAG == 0: # filter
                self.EL3_THI = congruence.checkStrictlyPositiveNumber(self.EL3_THI, "3rd oe filter thickness")
            elif self.EL3_FLAG == 1: # mirror
                self.EL3_ANG = congruence.checkStrictlyPositiveNumber(self.EL3_ANG, "3rd oe mirror angle")
                self.EL3_ROU = congruence.checkPositiveNumber(self.EL3_ROU, "3rd oe mirror roughness")

            if not self.EL3_DEN.strip() == "?":
                self.EL3_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL3_DEN, "3rd oe density")), "3rd oe density"))

        if self.NELEMENTS >= 4:
            self.EL4_FOR = congruence.checkEmptyString(self.EL4_FOR, "4th oe formula")

            if self.EL4_FLAG == 0: # filter
                self.EL4_THI = congruence.checkStrictlyPositiveNumber(self.EL4_THI, "4th oe filter thickness")
            elif self.EL4_FLAG == 1: # mirror
                self.EL4_ANG = congruence.checkStrictlyPositiveNumber(self.EL4_ANG, "4th oe mirror angle")
                self.EL4_ROU = congruence.checkPositiveNumber(self.EL4_ROU, "4th oe mirror roughness")

            if not self.EL4_DEN.strip() == "?":

                self.EL4_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL4_DEN, "4th oe density")), "4th oe density"))

        if self.NELEMENTS >= 5:
            self.EL5_FOR = congruence.checkEmptyString(self.EL5_FOR, "5th oe formula")

            if self.EL5_FLAG == 0: # filter
                self.EL5_THI = congruence.checkStrictlyPositiveNumber(self.EL5_THI, "5th oe filter thickness")
            elif self.EL5_FLAG == 1: # mirror
                self.EL5_ANG = congruence.checkStrictlyPositiveNumber(self.EL5_ANG, "5th oe mirror angle")
                self.EL5_ROU = congruence.checkPositiveNumber(self.EL5_ROU, "5th oe mirror roughness")

            if not self.EL5_DEN.strip() == "?":
                self.EL5_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL5_DEN, "5th oe density")), "5th oe density"))

    def do_xoppy_calculation(self):

        return self.xoppy_calc_power3D()


    # TODO THIS TO SEND DATA

    def extract_data_from_xoppy_output(self, calculation_output):

        [p, e, h, v] = self.input_beam.get_content("xoppy_data")

        data_to_send = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        data_to_send.add_content("xoppy_data", [p*calculation_output.prod(axis=0), e, h, v])
        data_to_send.add_content("xoppy_transmittivity", calculation_output)
        data_to_send.add_content("xoppy_code", "power3")

        self.output_beam = data_to_send

        return data_to_send


    # def extract_data_from_xoppy_output(self, calculation_output):
    #     return calculation_output

    def get_data_exchange_widget_name(self):
        return "POWER3D"

    def getKind(self, oe_n):
        if oe_n == 1:
            return self.EL1_FLAG
        elif oe_n == 2:
            return self.EL2_FLAG
        elif oe_n == 3:
            return self.EL3_FLAG
        elif oe_n == 4:
            return self.EL4_FLAG
        elif oe_n == 5:
            return self.EL5_FLAG

    def getTitles(self):
        return ['Transmittance vs X,Y,E','Transmittance vs E',
                'Spectral Power Density vs E,X,Y','Power Density vs X,Y','Spectral Power vs E']


    def replot_results(self):
        if self.output_beam is None:
            pass
        else:
            self.plot_results(self.output_beam, progressBarValue=80)

    def plot_results(self, calculated_data, progressBarValue=80):
        current_index = self.tabs.currentIndex()
        if not self.view_type == 0:
            if not calculated_data is None:

                self.initializeTabs() # added by srio to avoid overlapping graphs

                self.view_type_combo.setEnabled(False)

                p,e,h,v = self.input_beam.get_content("xoppy_data")
                code = self.input_beam.get_content("xoppy_code")

                p_spectral_power = p * codata.e * 1e3
                p_to_plot = p_spectral_power

                transmittivity = calculated_data.get_content("xoppy_transmittivity")


                transmittivity_total = transmittivity.prod(axis=0)

                if self.PLOT_SETS == 0: # source
                    p_to_plot = p_spectral_power
                    pre_title = "Input beam"
                elif self.PLOT_SETS == 1:
                    p_to_plot = p_spectral_power * transmittivity_total
                    pre_title = "Beam transmitted after LAST element"
                elif self.PLOT_SETS == 2:
                    p_to_plot = p_spectral_power * ( numpy.ones_like(transmittivity_total) - transmittivity_total)
                    pre_title = "Absorption by ALL elements"
                elif self.PLOT_SETS == 3:
                    transmittivity_before_last_element = transmittivity_total / transmittivity[-1,:,:,:]
                    p_to_plot = p_spectral_power * (transmittivity_before_last_element - transmittivity_total)
                    pre_title = "Absorption by the LAST element"




                # plot transmittance stack
                try:
                    self.plot_data3D(transmittivity_total, e, h, v, 0, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Code '+code+'; Flux [photons/s/0.1%bw/mm^2]',)

                    self.tabs.setCurrentIndex(0)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))


                # plot transmittance spectrum
                try:
                    self.plot_data1D(e,transmittivity_total.sum(axis=2).sum(axis=1)/h.size/v.size, 1, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Tramsmittance',
                                     title='Transmittance',)

                    # self.tabs.setCurrentIndex(2)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))



                # plot result s E,X,Y
                try:
                    self.plot_data3D(p_to_plot, e, h, v, 2, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title=pre_title+' Spectral power density[W/eV/mm^2]',)

                    self.tabs.setCurrentIndex(0)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))

                # plot result vs X,Y
                try:
                    if len(e) > 1:
                        energy_step = e[1]-e[0]
                    else:
                        energy_step = 1.0

                    self.plot_data2D(p_to_plot.sum(axis=0)*energy_step, h, v, 3, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title=pre_title+' Power density [W/mm^2]',)

                    # self.tabs.setCurrentIndex(1)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))

                # plot result vs E
                try:
                    self.plot_data1D(e,p_to_plot.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0]), 4, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Spectral power [W/eV]',
                                     title=pre_title+' Spectral power',)

                    # self.tabs.setCurrentIndex(2)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)

                try:
                    self.tabs.setCurrentIndex(current_index)
                except:
                    pass

            else:
                raise Exception("Empty Data")


    def xoppy_calc_power3D(self):

        #
        # prepare input for xpower_calc
        # Note that the input for xpower_calc accepts any number of elements.
        #

        substance = [self.EL1_FOR,self.EL2_FOR,self.EL3_FOR,self.EL4_FOR,self.EL5_FOR]
        thick     = numpy.array( (self.EL1_THI,self.EL2_THI,self.EL3_THI,self.EL4_THI,self.EL5_THI))
        angle     = numpy.array( (self.EL1_ANG,self.EL2_ANG,self.EL3_ANG,self.EL4_ANG,self.EL5_ANG))
        dens      = [self.EL1_DEN,self.EL2_DEN,self.EL3_DEN,self.EL4_DEN,self.EL5_DEN]
        roughness = numpy.array( (self.EL1_ROU,self.EL2_ROU,self.EL3_ROU,self.EL4_ROU,self.EL5_ROU))
        flags     = numpy.array( (self.EL1_FLAG,self.EL2_FLAG,self.EL3_FLAG,self.EL4_FLAG,self.EL5_FLAG))

        substance = substance[0:self.NELEMENTS+1]
        thick = thick[0:self.NELEMENTS+1]
        angle = angle[0:self.NELEMENTS+1]
        dens = dens[0:self.NELEMENTS+1]
        roughness = roughness[0:self.NELEMENTS+1]
        flags = flags[0:self.NELEMENTS+1]

        p,e,h,v = self.input_beam.get_content("xoppy_data")

        nelem_including_source = self.NELEMENTS + 1
        energies = e



        # initialize results


        # note that element of zero index corresponds to source!!!
        transmittance = numpy.zeros((nelem_including_source,p.shape[0],p.shape[1],p.shape[2]))
        for i in range(nelem_including_source):
            transmittance[i] = numpy.ones_like(p)

        #
        # get undefined densities
        #
        for i in range(nelem_including_source):
            try:
                rho = float(dens[i])
            except:
                rho = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(substance[i]))
                print("Density for %s: %g g/cm3"%(substance[i],rho))

            dens[i] = rho


        #info oe
        txt = ""
        for i in range(self.NELEMENTS):
            if flags[i] == 0:
                txt += '      *****   oe '+str(i+1)+'  [Filter] *************\n'
                txt += '      Material: %s\n'%(substance[i])
                txt += '      Density [g/cm^3]: %f \n'%(dens[i])
                txt += '      thickness [mm] : %f \n'%(thick[i])
            else:
                txt += '      *****   oe '+str(i+1)+'  [Mirror] *************\n'
                txt += '      Material: %s\n'%(substance[i])
                txt += '      Density [g/cm^3]: %f \n'%(dens[i])
                txt += '      grazing angle [mrad]: %f \n'%(angle[i])
                txt += '      roughness [A]: %f \n'%(roughness[i])


        for i in range(self.NELEMENTS):
            if flags[i] == 0: # filter

                for j,energy in enumerate(energies):

                    tmp = xraylib.CS_Total_CP(substance[i],energy/1000.0)

                    # pay attention to the element index...
                    transmittance[i+1,j,:,:] = numpy.exp(-tmp*dens[i]*(thick[i]/10.0))


            if flags[i] == 1: # mirror
                tmp = numpy.zeros(energies.size)
                for j,energy in enumerate(energies):
                    tmp[j] = xraylib.Refractive_Index_Re(substance[i],energy/1000.0,dens[i])
                delta = 1.0 - tmp

                beta = numpy.zeros(energies.size)
                for j,energy in enumerate(energies):
                    beta[j] = xraylib.Refractive_Index_Im(substance[i],energy/1000.0,dens[i])

                (rs,rp,runp) = reflectivity_fresnel(refraction_index_beta=beta,refraction_index_delta=delta,\
                                            grazing_angle_mrad=angle[i],roughness_rms_A=roughness[i],\
                                            photon_energy_ev=energies)

                for j,energy in enumerate(energies):
                    transmittance[i+1,j,:,:] = rs[j]


        txt += "\n\n\n"
        integration_constante = (e[1] - e[0]) * (h[1] - h[0]) * (v[1] - v[0]) * codata.e * 1e3
        p_cumulated = p.copy()
        power_cumulated = p_cumulated.sum()*integration_constante
        txt += '      Input beam power: %f W\n'%(power_cumulated)
        for i in range(self.NELEMENTS):
            p_cumulated *= transmittance[i+1]
            power_transmitted = (p_cumulated).sum()*integration_constante
            txt += '      Beam power after optical element %d: %6.3f W (absorbed: %6.3f W)\n'%\
                   (i+1,power_transmitted,power_cumulated-power_transmitted)
            power_cumulated = power_transmitted
        print(txt)

        return transmittance





if __name__ == "__main__":

    # create unulator_radiation xoppy exchange data
    from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_radiation
    from oasys.widgets.exchange import DataExchangeObject

    e, h, v, p, code = xoppy_calc_undulator_radiation(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                       ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                       ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                       PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,
                                       SETRESONANCE=0,HARMONICNUMBER=1,
                                       GAPH=0.001,GAPV=0.001,\
                                       HSLITPOINTS=41,VSLITPOINTS=41,METHOD=2,
                                       PHOTONENERGYMIN=7000,PHOTONENERGYMAX=8100,PHOTONENERGYPOINTS=20,
                                       USEEMITTANCES=1)
    # received_data = DataExchangeObject("XOPPY", "UNDULATOR_RADIATION")
    received_data = DataExchangeObject("XOPPY", "POWER3D")
    received_data.add_content("xoppy_data", [p, e, h, v])
    received_data.add_content("xoppy_code", code)


    #
    app = QApplication(sys.argv)
    w = OWpower3D()

    w.acceptExchangeData(received_data)

    w.show()
    app.exec()

    w.saveSettings()
