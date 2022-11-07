import numpy
from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from xoppylib.power.xoppy_calc_power import xoppy_calc_power

from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import scipy.constants as codata

import xraylib
from dabax.dabax_xraylib import DabaxXraylib

class OWxpower(XoppyWidget):
    name = "POWER"
    id = "orange.widgets.dataxpower"
    description = "Power Absorbed and Transmitted by Optical Elements"
    icon = "icons/xoppy_xpower.png"
    priority = 2
    category = ""
    keywords = ["xoppy", "power"]

    inputs = [("ExchangeData", DataExchangeObject, "acceptExchangeData")]

    SOURCE = Setting(2)
    ENER_MIN = Setting(1000.0)
    ENER_MAX = Setting(50000.0)
    ENER_N = Setting(100)
    SOURCE_FILE = Setting("?")
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
    PLOT_SETS = Setting(2)
    FILE_DUMP = 0

    MATERIAL_CONSTANT_LIBRARY_FLAG = Setting(0) # not yet interfaced, to be done

    input_spectrum = None
    input_script = None

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        idx = -1 

        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.box_source = gui.comboBox(box1, self, "SOURCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['From Oasys wire', 'Normalized to 1 W/eV', 'From external file (eV, W/eV)', 'From external file (eV, phot/s/.1%bw)'],
                    valueType=int, orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENER_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENER_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENER_N",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9 ***********   File Browser ******************
        idx += 1
        box1 = gui.widgetBox(box)
        file_box_id = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal")
        self.file_id = oasysgui.lineEdit(file_box_id, self, "SOURCE_FILE", self.unitLabels()[idx],
                                    labelWidth=100, valueType=str, orientation="horizontal")
        gui.button(file_box_id, self, "...", callback=self.select_input_file, width=25)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 10
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "NELEMENTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['1', '2', '3', '4', '5'],
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL1_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL1_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL2_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL2_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 26 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL3_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 27 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL3_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 32 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL4_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 33 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL4_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 38 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL5_ANG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 39 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EL5_ROU",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
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
                    items=['Local properties', 'Cumulated intensities', 'All'],
                    valueType=int, orientation="horizontal", labelWidth=250, callback=self.set_NELEMENTS)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 42
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "FILE_DUMP",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes (power.spec)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # self.input_spectrum = None

    def select_input_file(self):
        self.file_id.setText(oasysgui.selectFileFromDialog(self, self.SOURCE_FILE,
                                    "Open 2-columns file with spectral power",
                                    file_extension_filter="ascii dat (*.dat *.txt *spec)"))

    def set_NELEMENTS(self):
        self.initializeTabs()

    def set_EL_FLAG(self):
        self.initializeTabs()

    def unitLabels(self):
         return ['Input beam:',
                 'From energy [eV]:      ',
                 'To energy [eV]:',
                 'Energy points:  ',
                 'File with input beam spectral power:',
                 'Number of elements:',
                 '1st oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '2nd oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '3rd oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '4th oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 '5th oe formula','kind:','Filter thick[mm]','Mirror angle[mrad]','Roughness[A]','Density [g/cm^3]',
                 "Plot","Dump file"]


    def unitFlags(self):
         return ['True',
                 'self.SOURCE  ==  1',
                 'self.SOURCE  ==  1',
                 'self.SOURCE  ==  1',
                 'self.SOURCE  >  1',
                 'True',
                 'self.NELEMENTS  >=  0',' self.NELEMENTS  >=  0','self.EL1_FLAG  ==  0  and  self.NELEMENTS  >=  0','self.EL1_FLAG  !=  0  and  self.NELEMENTS  >=  0','self.EL1_FLAG  !=  0  and  self.NELEMENTS  >=  0',' self.NELEMENTS  >=  0',
                 'self.NELEMENTS  >=  1',' self.NELEMENTS  >=  1','self.EL2_FLAG  ==  0  and  self.NELEMENTS  >=  1','self.EL2_FLAG  !=  0  and  self.NELEMENTS  >=  1','self.EL2_FLAG  !=  0  and  self.NELEMENTS  >=  1',' self.NELEMENTS  >=  1',
                 'self.NELEMENTS  >=  2',' self.NELEMENTS  >=  2','self.EL3_FLAG  ==  0  and  self.NELEMENTS  >=  2','self.EL3_FLAG  !=  0  and  self.NELEMENTS  >=  2','self.EL3_FLAG  !=  0  and  self.NELEMENTS  >=  2',' self.NELEMENTS  >=  2',
                 'self.NELEMENTS  >=  3',' self.NELEMENTS  >=  3','self.EL4_FLAG  ==  0  and  self.NELEMENTS  >=  3','self.EL4_FLAG  !=  0  and  self.NELEMENTS  >=  3','self.EL4_FLAG  !=  0  and  self.NELEMENTS  >=  3',' self.NELEMENTS  >=  3',
                 'self.NELEMENTS  >=  4',' self.NELEMENTS  >=  4','self.EL5_FLAG  ==  0  and  self.NELEMENTS  >=  4','self.EL5_FLAG  !=  0  and  self.NELEMENTS  >=  4','self.EL5_FLAG  !=  0  and  self.NELEMENTS  >=  4',' self.NELEMENTS  >=  4',
                 'True','True']

    def get_help_name(self):
        return 'power'

    def selectFile(self):
        self.le_source_file.setText(oasysgui.selectFileFromDialog(self, self.SOURCE_FILE, "Open Source File", file_extension_filter="*.*"))

    def acceptExchangeData(self, exchangeData):

        self.input_spectrum = None
        self.input_script = None
        self.SOURCE = 0

        try:
            if not exchangeData is None:
                if exchangeData.get_program_name() == "XOPPY":
                    no_bandwidth = False
                    if exchangeData.get_widget_name() =="UNDULATOR_FLUX" :
                        # self.SOURCE_FILE = "xoppy_undulator_flux"
                        no_bandwidth = True
                        index_flux = 2
                    elif exchangeData.get_widget_name() == "BM" :
                        if exchangeData.get_content("is_log_plot") == 1:
                            raise Exception("Logaritmic X scale of Xoppy Energy distribution not supported")
                        if exchangeData.get_content("calculation_type") == 0 and exchangeData.get_content("psi") in [0,2]:
                            # self.SOURCE_FILE = "xoppy_bm_flux"
                            no_bandwidth = True
                            index_flux = 6
                        else:
                            raise Exception("Xoppy result is not a Flux vs Energy distribution integrated in Psi")
                    elif exchangeData.get_widget_name() =="XWIGGLER" :
                        # self.SOURCE_FILE = "xoppy_xwiggler_flux"
                        no_bandwidth = True
                        index_flux = 2
                    elif exchangeData.get_widget_name() =="WS" :
                        # self.SOURCE_FILE = "xoppy_xwiggler_flux"
                        no_bandwidth = True
                        index_flux = 2
                    elif exchangeData.get_widget_name() =="XTUBES" :
                        # self.SOURCE_FILE = "xoppy_xtubes_flux"
                        index_flux = 1
                        no_bandwidth = True
                    elif exchangeData.get_widget_name() =="XTUBE_W" :
                        # self.SOURCE_FILE = "xoppy_xtube_w_flux"
                        index_flux = 1
                        no_bandwidth = True
                    elif exchangeData.get_widget_name() =="BLACK_BODY" :
                        # self.SOURCE_FILE = "xoppy_black_body_flux"
                        no_bandwidth = True
                        index_flux = 2

                    elif exchangeData.get_widget_name() =="UNDULATOR_RADIATION" :
                        # self.SOURCE_FILE = "xoppy_undulator_radiation"
                        no_bandwidth = True
                        index_flux = 1
                    elif exchangeData.get_widget_name() =="POWER" :
                        # self.SOURCE_FILE = "xoppy_undulator_power"
                        no_bandwidth = True
                        index_flux = -1
                    elif exchangeData.get_widget_name() =="POWER3D" :
                        # self.SOURCE_FILE = "xoppy_power3d"
                        no_bandwidth = True
                        index_flux = 1

                    else:
                        raise Exception("Xoppy Source not recognized")

                    # self.SOURCE_FILE += "_" + str(id(self)) + ".dat"


                    spectrum = exchangeData.get_content("xoppy_data")

                    if exchangeData.get_widget_name() =="UNDULATOR_RADIATION" or \
                        exchangeData.get_widget_name() =="POWER3D":
                        [p, e, h, v ] = spectrum
                        tmp = p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*codata.e*1e3
                        spectrum = numpy.vstack((e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*
                                                 codata.e*1e3))
                        self.input_spectrum = spectrum
                    else:

                        if not no_bandwidth:
                            spectrum[:,index_flux] /= 0.001*spectrum[:,0]

                        self.input_spectrum = numpy.vstack((spectrum[:,0],spectrum[:,index_flux]))

                    try:
                        self.input_script = exchangeData.get_content("xoppy_script")
                    except:
                        self.input_script = None

                    self.process_showers()
                    self.compute()

        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

    def check_fields(self):

        if self.SOURCE == 1:
            self.ENER_MIN = congruence.checkPositiveNumber(self.ENER_MIN, "Energy from")
            self.ENER_MAX = congruence.checkStrictlyPositiveNumber(self.ENER_MAX, "Energy to")
            congruence.checkLessThan(self.ENER_MIN, self.ENER_MAX, "Energy from", "Energy to")
            self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.ENER_N, "Energy Points")
        elif self.SOURCE == 2:
            congruence.checkFile(self.SOURCE_FILE)

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

        if self.SOURCE == 0:
            if self.input_spectrum is None:
                raise Exception("No input beam")
            else:
                energies = self.input_spectrum[0,:].copy()
                source = self.input_spectrum[1,:].copy()
            if self.input_script is None:
                script_previous = '#\n# >> MISSING SCRIPT TO CREATE (energy, spectral_power) <<\n#\n'
            else:
                script_previous = self.input_script
        elif self.SOURCE == 1:
            energies = numpy.linspace(self.ENER_MIN,self.ENER_MAX,self.ENER_N)
            source = numpy.ones(energies.size)
            tmp = numpy.vstack( (energies,source))
            self.input_spectrum = source
            script_previous = "import numpy\nenergy = numpy.linspace(%g,%g,%d)\nspectral_power = numpy.ones(%d)\n" % \
                        (self.ENER_MIN,self.ENER_MAX,self.ENER_N,self.ENER_N)
        elif self.SOURCE == 2:  # file contains energy_eV and spectral power (W/eV)
            source_file = self.SOURCE_FILE
            try:
                tmp = numpy.loadtxt(source_file)
                energies = tmp[:,0]
                source = tmp[:,1]
                self.input_spectrum = source
                script_previous = "import numpy\ntmp = numpy.loadtxt(%s)\nenergy = tmp[:,0]\nspectral_power = tmp[:,1]\n" % \
                                (source_file)
            except:
                print("Error loading file %s "%(source_file))
                raise
        elif self.SOURCE == 3:  # file contains energy_eV and flux (ph/s/0.1%bw
            source_file = self.SOURCE_FILE
            try:
                tmp = numpy.loadtxt(source_file)
                energies = tmp[:,0]
                source = tmp[:,1] * (codata.e * 1e3)
                self.input_spectrum = source
                script_previous = "import numpy\nimport scipy.constants as codata\ntmp = numpy.loadtxt(%s)\nenergy = tmp[:,0]\nspectral_power = tmp[:,1] / (codata.e * 1e3)\n" % \
                                (source_file)
            except:
                print("Error loading file %s "%(source_file))
                raise

        # substance = [self.EL1_FOR,self.EL2_FOR,self.EL3_FOR,self.EL4_FOR,self.EL5_FOR]
        # thick     = numpy.array( (self.EL1_THI,self.EL2_THI,self.EL3_THI,self.EL4_THI,self.EL5_THI))
        # angle     = numpy.array( (self.EL1_ANG,self.EL2_ANG,self.EL3_ANG,self.EL4_ANG,self.EL5_ANG))
        # dens      = [self.EL1_DEN,self.EL2_DEN,self.EL3_DEN,self.EL4_DEN,self.EL5_DEN]
        # roughness = numpy.array( (self.EL1_ROU,self.EL2_ROU,self.EL3_ROU,self.EL4_ROU,self.EL5_ROU))
        # flags     = numpy.array( (self.EL1_FLAG,self.EL2_FLAG,self.EL3_FLAG,self.EL4_FLAG,self.EL5_FLAG))

        substance = [self.EL1_FOR,  self.EL2_FOR,  self.EL3_FOR,  self.EL4_FOR,  self.EL5_FOR]  # str
        thick     = [self.EL1_THI,  self.EL2_THI,  self.EL3_THI,  self.EL4_THI,  self.EL5_THI]  # float
        angle     = [self.EL1_ANG,  self.EL2_ANG,  self.EL3_ANG,  self.EL4_ANG,  self.EL5_ANG]  # float
        dens      = [self.EL1_DEN,  self.EL2_DEN,  self.EL3_DEN,  self.EL4_DEN,  self.EL5_DEN]  # str
        roughness = [self.EL1_ROU,  self.EL2_ROU,  self.EL3_ROU,  self.EL4_ROU,  self.EL5_ROU]  # float
        flags     = [self.EL1_FLAG, self.EL2_FLAG, self.EL3_FLAG, self.EL4_FLAG, self.EL5_FLAG] # int

        # this is for creating script
        substance_str = "["
        thick_str = "["
        angle_str = "["
        dens_str = "["
        roughness_str = "["
        flags_str = "["
        for i in range(self.NELEMENTS+1):
            substance_str += "'%s'," % (substance[i])
            thick_str     += "%g," % (thick[i])
            angle_str     += "%g," % (angle[i])
            dens_str      += "'%s'," % (dens[i])
            roughness_str += "%g," % (roughness[i])
            flags_str     += "%d," % (flags[i])
        substance_str += "]"
        thick_str += "]"
        angle_str += "]"
        dens_str += "]"
        roughness_str += "]"
        flags_str += "]"

        if self.MATERIAL_CONSTANT_LIBRARY_FLAG == 0:
            material_constants_library = xraylib
            material_constants_library_str = "xraylib"
        else:
            material_constants_library = DabaxXraylib()
            material_constants_library_str = 'DabaxXraylib()'
            print(material_constants_library.info())

        out_dictionary = xoppy_calc_power(
            energies,
            source,
            substance                  = substance,
            thick                      = thick    ,
            angle                      = angle    ,
            dens                       = dens     ,
            roughness                  = roughness,
            flags                      = flags    ,
            nelements                  = self.NELEMENTS + 1,
            FILE_DUMP                  = self.FILE_DUMP,
            material_constants_library = material_constants_library,
                                                )

        print(out_dictionary["info"])

        dict_parameters = {
            "substance"                 : substance_str,
            "thick"                     : thick_str,
            "angle"                     : angle_str,
            "dens"                      : dens_str,
            "roughness"                 : roughness_str,
            "flags"                     : flags_str,
            "nelements"                 : self.NELEMENTS + 1,
            "FILE_DUMP"                 : self.FILE_DUMP,
            "material_constants_library": material_constants_library_str,
        }

        script_element = self.script_template().format_map(dict_parameters)

        script = script_previous + script_element

        self.xoppy_script.set_code(script)

        return  out_dictionary, script

    def script_template(self):
        return """

#
# script to make the calculations (created by XOPPY:xpower)
#

import numpy
from xoppylib.power.xoppy_calc_power import xoppy_calc_power
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

out_dictionary = xoppy_calc_power(
        energy,
        spectral_power,
        substance = {substance},
        thick     = {thick}, # in mm (for filters)
        angle     = {angle}, # in mrad (for mirrors)
        dens      = {dens},
        roughness = {roughness}, # in A (for mirrors)
        flags     = {flags}, # 0=Filter, 1=Mirror
        nelements = {nelements},
        FILE_DUMP = {FILE_DUMP},
        material_constants_library = {material_constants_library},
        )


# data to pass
energy = out_dictionary["data"][0,:]
spectral_power = out_dictionary["data"][-1,:]

#                       
# example plots
#
from srxraylib.plot.gol import plot
plot(out_dictionary["data"][0,:], out_dictionary["data"][1,:],
    out_dictionary["data"][0,:], out_dictionary["data"][-1,:],
    xtitle=out_dictionary["labels"][0],
    legend=[out_dictionary["labels"][1],out_dictionary["labels"][-1]],
    title='Spectral Power [W/eV]')
 
#
# end script
#
"""



    def extract_data_from_xoppy_output(self, calculation_output):

        out_dictionary, script = calculation_output

        # send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", out_dictionary["data"].T)
        except:
            pass
        try:
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", -1)
        except:
            pass
        try:
            calculated_data.add_content("xoppy_script", script)
        except:
            pass
        try:
            calculated_data.add_content("labels", out_dictionary["labels"])
        except:
            pass
        try:
            calculated_data.add_content("info", out_dictionary["info"])
        except:
            pass

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "POWER"

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

    def do_plot_local(self):
        out = False
        if self.PLOT_SETS == 0: out = True
        if self.PLOT_SETS == 2: out = True
        return out

    def do_plot_intensity(self):
        out = False
        if self.PLOT_SETS == 1: out = True
        if self.PLOT_SETS == 2: out = True
        return out


    def getTitles(self):
        titles = []

        if self.do_plot_intensity(): titles.append("Input beam")

        for oe_n in range(1, self.NELEMENTS+2):
            kind = self.getKind(oe_n)

            if kind == 0: # FILTER
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Total CS")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Mu")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Transmitivity")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Absorption")
                if self.do_plot_intensity(): titles.append("Spectral power absorbed in oe " + str(oe_n))
                if self.do_plot_intensity(): titles.append("Spectral power after oe " + str(oe_n))


            else: # MIRROR
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] 1-Re[n]=delta")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Im[n]=beta")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] delta/beta")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Reflectivity-s")
                if self.do_plot_local(): titles.append("[oe " + str(oe_n) + "] Absorption")
                if self.do_plot_intensity(): titles.append("Spectral power absorbed in oe " + str(oe_n))
                if self.do_plot_intensity(): titles.append("Spectral power after oe " + str(oe_n))


        return titles

    def getXTitles(self):

        xtitles = []

        if self.do_plot_intensity(): xtitles.append("Photon Energy [eV]")

        for oe_n in range(1, self.NELEMENTS+2):
            kind = self.getKind(oe_n)

            if kind == 0: # FILTER
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_intensity(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_intensity(): xtitles.append("Photon Energy [eV]")
            else: # MIRROR
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_local(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_intensity(): xtitles.append("Photon Energy [eV]")
                if self.do_plot_intensity(): xtitles.append("Photon Energy [eV]")

        return xtitles

    def getYTitles(self):
        ytitles = []


        if self.SOURCE == 1:
            unit_str = '[a.u]'
        else:
            unit_str = '[W/eV]'

        if self.do_plot_intensity(): ytitles.append("Spectral Power %s" % unit_str )


        for oe_n in range(1, self.NELEMENTS+2):
            kind = self.getKind(oe_n)

            if kind == 0: # FILTER
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Total CS cm2/g")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Mu cm^-1")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Transmitivity")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Absorption")

                if self.do_plot_intensity(): ytitles.append("Absorbed Spectral power %s" % unit_str)
                if self.do_plot_intensity(): ytitles.append(         "Spectral power %s" % unit_str)

            else: # MIRROR
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] 1-Re[n]=delta")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Im[n]=beta")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] delta/beta")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Reflectivity-s")
                if self.do_plot_local(): ytitles.append("[oe " + str(oe_n) + "] Transmitivity")

                if self.do_plot_intensity(): ytitles.append("Absorbed Spectral power %s" % unit_str)
                if self.do_plot_intensity(): ytitles.append(         "Spectral power %s" % unit_str)

        return ytitles

    def getVariablesToPlot(self):
        variables = []

        if self.do_plot_intensity(): variables.append((0, 1)) # start plotting the source
        shift = 0

        for oe_n in range(1, self.NELEMENTS+2):
            kind = self.getKind(oe_n)

            if oe_n == 1:
                shift = 0
            else:
                kind_previous = self.getKind(oe_n-1)

                if kind_previous == 0: # FILTER
                    shift += 6
                else:
                    shift += 7

            if kind == 0: # FILTER
                if self.do_plot_local(): variables.append((0, 2+shift))
                if self.do_plot_local(): variables.append((0, 3+shift))
                if self.do_plot_local(): variables.append((0, 4+shift))
                if self.do_plot_local(): variables.append((0, 5+shift))
                if self.do_plot_intensity(): variables.append((0, 6+shift))
                if self.do_plot_intensity(): variables.append((0, 7+shift))
            else:
                if self.do_plot_local(): variables.append((0, 2+shift))
                if self.do_plot_local(): variables.append((0, 3+shift))
                if self.do_plot_local(): variables.append((0, 4+shift))
                if self.do_plot_local(): variables.append((0, 5+shift))
                if self.do_plot_local(): variables.append((0, 6+shift))
                if self.do_plot_intensity(): variables.append((0, 7+shift))
                if self.do_plot_intensity(): variables.append((0, 8+shift))

        return variables

    def getLogPlot(self):


        logplot = []

        if self.do_plot_intensity(): logplot.append((False,False))

        for oe_n in range(1, self.NELEMENTS+2):
            kind = self.getKind(oe_n)

            if kind == 0: # FILTER
                if self.do_plot_local(): logplot.append((False, True))
                if self.do_plot_local(): logplot.append((False, True))
                if self.do_plot_local(): logplot.append((False, False))
                if self.do_plot_local(): logplot.append((False, False))
                if self.do_plot_intensity(): logplot.append((False, False))
                if self.do_plot_intensity(): logplot.append((False, False))
            else: # MIRROR
                if self.do_plot_local(): logplot.append((False, True))
                if self.do_plot_local(): logplot.append((False, True))
                if self.do_plot_local(): logplot.append((False, False))
                if self.do_plot_local(): logplot.append((False, False))
                if self.do_plot_local(): logplot.append((False, False))
                if self.do_plot_intensity(): logplot.append((False, False))
                if self.do_plot_intensity(): logplot.append((False, False))

        return logplot

if __name__ == "__main__":
    import sys
    input_type = 0

    if input_type == 1:
        from oasys.widgets.exchange import DataExchangeObject
        input_data_type = "POWER"

        if input_data_type == "POWER":
            # create fake UNDULATOR_FLUX xoppy exchange data
            e = numpy.linspace(1000.0, 10000.0, 100)
            source = e/10
            received_data = DataExchangeObject("XOPPY", "POWER")
            received_data.add_content("xoppy_data", numpy.vstack((e,e,source)).T)
            received_data.add_content("xoppy_code", "US")

        elif input_data_type == "POWER3D":
            # create unulator_radiation xoppy exchange data
            from xoppylib.sources.xoppy_undulators import xoppy_calc_undulator_radiation

            e, h, v, p, code = xoppy_calc_undulator_radiation(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                               ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                               ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                               PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,
                                               SETRESONANCE=0,HARMONICNUMBER=1,
                                               GAPH=0.001,GAPV=0.001,\
                                               HSLITPOINTS=41,VSLITPOINTS=41,METHOD=0,
                                               PHOTONENERGYMIN=7000,PHOTONENERGYMAX=8100,PHOTONENERGYPOINTS=20,
                                               USEEMITTANCES=1)
            received_data = DataExchangeObject("XOPPY", "POWER3D")
            received_data = DataExchangeObject("XOPPY", "UNDULATOR_RADIATION")
            received_data.add_content("xoppy_data", [p, e, h, v])
            received_data.add_content("xoppy_code", code)




        app = QApplication(sys.argv)
        w = OWxpower()
        w.acceptExchangeData(received_data)
        w.show()
        app.exec()
        w.saveSettings()

    else:
        app = QApplication(sys.argv)
        w = OWxpower()
        w.SOURCE = 1
        w.show()
        app.exec()
        w.saveSettings()

