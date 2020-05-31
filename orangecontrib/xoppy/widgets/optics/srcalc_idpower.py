import sys, os, platform
import numpy
from PyQt5.QtWidgets import QApplication, QSizePolicy
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtGui, QtWidgets

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
import orangecanvas.resources as resources


from oasys.util.oasys_util import EmittingStream, TTYGrabber

import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

from syned.widget.widget_decorator import WidgetDecorator

from syned.storage_ring.magnetic_structures.undulator import Undulator
from syned.storage_ring.electron_beam import ElectronBeam
import scipy.constants as codata

from silx.gui.plot import Plot2D

from orangecontrib.xoppy.util.messages import  showCriticalMessage
from orangecontrib.xoppy.util.srcalc.srcalc import  load_srcalc_output_file, ray_tracing
from orangecontrib.xoppy.util.srcalc.srcalc import  compute_power_density_footprint, compute_power_density_image
from orangecontrib.xoppy.util.srcalc.srcalc import  trapezoidal_rule_2d, trapezoidal_rule_2d_1darrays
from orangecontrib.xoppy.util.srcalc.srcalc import  write_ansys_files
from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.image_view_with_fwhm import ImageViewWithFWHM

#
# TODO: Recompile IDPower with higher dimensions
#                         with better format:                Pow. ref(W)    Pow. abs.(W)
#                                                            Mirror 1     ***********     ***********


class OWsrcalc_idpower(XoppyWidget, WidgetDecorator):

    IS_DEVELOP = False if not "OASYSDEVELOP" in os.environ.keys() else str(os.environ.get('OASYSDEVELOP')) == "1"

    name = "SRCALC-IDPOWER"
    id = "srcalc_idpower"
    description = "Power Absorbed and Transmitted by Optical Elements"
    icon = "icons/srcalc.png"
    priority = 1
    category = ""
    keywords = ["srcalc", "IDPower", "power", "Reininger", "OASYS"]


    RING_ENERGY = Setting(2.0)
    RING_CURRENT = Setting(0.5)
    KY = Setting(3.07)
    KX = Setting(0.0)
    NUMBER_OF_PERIODS = Setting(137)
    PERIOD_LENGTH = Setting(0.0288)
    NUMBER_OF_HARMONICS = Setting(-28)
    SOURCE_SCREEN_DISTANCE = Setting(15.00)
    HORIZONTAL_ACCEPTANCE = Setting(30.0)
    VERTICAL_ACCEPTANCE = Setting(15.0)
    NUMBER_OF_POINTS_H = Setting(31)
    NUMBER_OF_POINTS_V = Setting(21)
    ELECTRON_SIGMAS = Setting(4)
    SIGMAX = Setting(12.1e-3)
    SIGMAXP = Setting(5.7e-3)
    SIGMAY = Setting(14.7e-3)
    SIGMAYP = Setting(4.7e-3)
    NELEMENTS = Setting(1)

    EL0_SHAPE = Setting(5)
    EL0_P_POSITION = Setting(15.00)  # this is then copied from  SOURCE_SCREEN_DISTANCE
    EL0_Q_POSITION = Setting(5.0)
    EL0_P_FOCUS = Setting(15.0)
    EL0_Q_FOCUS = Setting(5.0)
    EL0_ANG = Setting(88.75)
    EL0_THICKNESS = Setting(1000)
    EL0_RELATIVE_TO_PREVIOUS = Setting(0)
    EL0_COATING = Setting(9)

    EL1_SHAPE = Setting(2)
    EL1_P_POSITION = Setting(1.0)
    EL1_Q_POSITION = Setting(16.0)
    EL1_P_FOCUS = Setting(16.0)
    EL1_Q_FOCUS = Setting(16.0)
    EL1_ANG = Setting(88.75)
    EL1_THICKNESS = Setting(1000)
    EL1_RELATIVE_TO_PREVIOUS = Setting(2)
    EL1_COATING = Setting(1)

    EL2_SHAPE = Setting(2)
    EL2_P_POSITION = Setting(10.0)
    EL2_Q_POSITION = Setting(0.0)
    EL2_P_FOCUS = Setting(10.0)
    EL2_Q_FOCUS = Setting(10.0)
    EL2_ANG = Setting(88.75)
    EL2_THICKNESS = Setting(1000)
    EL2_RELATIVE_TO_PREVIOUS = Setting(0)
    EL2_COATING = Setting(9)

    EL3_SHAPE = Setting(2)
    EL3_P_POSITION = Setting(10.0)
    EL3_Q_POSITION = Setting(0.0)
    EL3_P_FOCUS = Setting(10.0)
    EL3_Q_FOCUS = Setting(10.0)
    EL3_ANG = Setting(88.75)
    EL3_THICKNESS = Setting(1000)
    EL3_RELATIVE_TO_PREVIOUS = Setting(0)
    EL3_COATING = Setting(9)

    EL4_SHAPE = Setting(2)
    EL4_P_POSITION = Setting(10.0)
    EL4_Q_POSITION = Setting(0.0)
    EL4_P_FOCUS = Setting(10.0)
    EL4_Q_FOCUS = Setting(10.0)
    EL4_ANG = Setting(88.75)
    EL4_THICKNESS = Setting(1000)
    EL4_RELATIVE_TO_PREVIOUS = Setting(0)
    EL4_COATING = Setting(9)

    EL5_SHAPE = Setting(2)
    EL5_P_POSITION = Setting(10.0)
    EL5_Q_POSITION = Setting(0.0)
    EL5_P_FOCUS = Setting(10.0)
    EL5_Q_FOCUS = Setting(10.0)
    EL5_ANG = Setting(88.75)
    EL5_THICKNESS = Setting(1000)
    EL5_RELATIVE_TO_PREVIOUS = Setting(0)
    EL5_COATING = Setting(9)

    RAY_TRACING_IMAGE = Setting(1)
    RAY_TRACING_RUNS = Setting(5)
    RAY_TRACING_SEED = Setting(123456)

    PLOT_MODE = Setting(2)
    DO_PLOT_GRID = Setting(0)
    DUMP_ANSYS_FILES = Setting(0)
    SHOW_URGENT_PLOTS = Setting(0) # 0 only source, 1 all
    ORIENTATION_LOGIC = Setting(1) # 0=shadow, 1=Lab
    INTERPOLATION_OR_HISTOGRAMMING = Setting(0)  # 0 interpolation, 1 histogramming
    INTERPOLATION_METHOD = Setting(2) # 0 linear, 1 nearest, 2 cubic
    RATIO_PIXELS_0 = Setting(1.0)
    RATIO_PIXELS_1 = Setting(1.0)
    DEBUG_RUN_URGENT = Setting(0)

    inputs = WidgetDecorator.syned_input_data()

    def __init__(self):
        super().__init__()

        info_tab = oasysgui.createTabPage(self.main_tabs, "Info")
        self.info_output = QtWidgets.QTextEdit()
        self.info_output.setReadOnly(True)
        info_tab.layout().addWidget(self.info_output)


    def resetSettings(self):
        pass

    def build_gui(self):

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()

        self.controls_tabs = oasysgui.tabWidget(self.controlArea)
        box = oasysgui.createTabPage(self.controls_tabs, "Light Source")

        idx = -1 

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_RING_ENERGY = oasysgui.lineEdit(box1, self, "RING_ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_RING_CURRENT = oasysgui.lineEdit(box1, self, "RING_CURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KY = oasysgui.lineEdit(box1, self, "KY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KX = oasysgui.lineEdit(box1, self, "KX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_NUMBER_OF_PERIODS = oasysgui.lineEdit(box1, self, "NUMBER_OF_PERIODS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_PERIOD_LENGTH = oasysgui.lineEdit(box1, self, "PERIOD_LENGTH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_SIGMAX = oasysgui.lineEdit(box1, self, "SIGMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_SIGMAXP = oasysgui.lineEdit(box1, self, "SIGMAXP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_SIGMAY = oasysgui.lineEdit(box1, self, "SIGMAY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_SIGMAYP = oasysgui.lineEdit(box1, self, "SIGMAYP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        ##########################
        box = oasysgui.createTabPage(self.controls_tabs, "Calculation")
        ##########################



        ########
        idx += 1
        box1 = gui.widgetBox(box, orientation="horizontal")
        oasysgui.lineEdit(box1, self, "NUMBER_OF_HARMONICS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1)

        gui.button(box1 , self, "Guess", callback=self.guess_number_of_harmonics, height=25)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "SOURCE_SCREEN_DISTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250,
                          callback=self.setdistance)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "HORIZONTAL_ACCEPTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "VERTICAL_ACCEPTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        ########
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "NUMBER_OF_POINTS_H",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "NUMBER_OF_POINTS_V",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        ########
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ELECTRON_SIGMAS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)




        ##########################
        box = oasysgui.createTabPage(self.controls_tabs, "Beamline")
        ##########################


        #widget index 10
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "NELEMENTS",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['0', '1', '2', '3', '4', '5','6'],
                    valueType=int, orientation="horizontal", callback=self.set_NELEMENTS,
                    labelWidth=330)
        self.show_at(self.unitFlags()[idx], box1)



        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        self.shape_list = [
            "Toroidal mirror",
            "Spherical mirror",
            "Plane mirror",
            "MerCyl mirror",
            "SagCyl mirror",
            "Ellipsoidal mirror",
            "MerEll mirror",
            "SagEllip mirror",
            "Filter",
            "Crystal"]

        self.coating_list = ["Al","Au","Cr","Dia","Gra","InSb","MGF2","Ni","Pd","Rh","SiC","Test","Al2O3","Be","Cu","Fe","Ice","Ir","Mo","Os","Pt","Si","SiO2","WW"]


        tabs_elements = oasysgui.tabWidget(box)
        self.tab_el = []
        self.tab_el.append( oasysgui.createTabPage(tabs_elements, "o.e. 1") )
        self.tab_el.append( oasysgui.createTabPage(tabs_elements, "o.e. 2") )
        self.tab_el.append( oasysgui.createTabPage(tabs_elements, "o.e. 3") )
        self.tab_el.append( oasysgui.createTabPage(tabs_elements, "o.e. 4") )
        self.tab_el.append( oasysgui.createTabPage(tabs_elements, "o.e. 5") )
        self.tab_el.append( oasysgui.createTabPage(tabs_elements, "o.e. 6") )


        for element_index in range(6):

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            gui.comboBox(box1, self, "EL%d_SHAPE"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        items=self.shape_list,
                        valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            oasysgui.lineEdit(box1, self, "EL%d_P_POSITION"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=300)
            self.show_at(self.unitFlags()[idx], box1)


            # first element distance is the same as urgent screen position
            if element_index == 0:
                box1.setEnabled(False)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            oasysgui.lineEdit(box1, self, "EL%d_Q_POSITION"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=300)
            self.show_at(self.unitFlags()[idx], box1)


            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            oasysgui.lineEdit(box1, self, "EL%d_P_FOCUS"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            oasysgui.lineEdit(box1, self, "EL%d_Q_FOCUS"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            oasysgui.lineEdit(box1, self, "EL%d_ANG"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            oasysgui.lineEdit(box1, self, "EL%d_THICKNESS"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            gui.comboBox(box1, self, "EL%d_RELATIVE_TO_PREVIOUS"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        items=['Left (90)','Right (270)','Up (0)','Down (180)'],
                        valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index xx
            idx += 1
            box1 = gui.widgetBox(self.tab_el[element_index])
            gui.comboBox(box1, self, "EL%d_COATING"%element_index,
                         label=self.unitLabels()[idx], addSpace=False,
                        items=self.coating_list,
                        valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)



        #widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "RAY_TRACING_IMAGE",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes'],
                    valueType=int, orientation="horizontal", labelWidth=350)

        self.show_at(self.unitFlags()[idx], box1)

        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)
        oasysgui.lineEdit(box1, self, "RAY_TRACING_RUNS",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)
        oasysgui.lineEdit(box1, self, "RAY_TRACING_SEED",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #  Setting page
        #
        box0 = oasysgui.createTabPage(self.controls_tabs, "Settings")
        box = gui.widgetBox(box0,"Plots")

        #widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "PLOT_MODE",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['Basic image', 'Image and histograms', 'Image [default]'],
                    valueType=int, orientation="horizontal", labelWidth=350,
                    callback=self.set_ViewType)

        self.show_at(self.unitFlags()[idx], box1)

        #widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "DO_PLOT_GRID",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['No [default]', 'Yes (overplotted)', 'Yes (in a new tab)'],
                    valueType=int, orientation="horizontal", labelWidth=350,
                    callback=self.set_ViewType)

        self.show_at(self.unitFlags()[idx], box1)

        #widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "SHOW_URGENT_PLOTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Only source [default]', 'Source + elements'],
                    valueType=int, orientation="horizontal", labelWidth=350,)

        self.show_at(self.unitFlags()[idx], box1)



        box = gui.widgetBox(box0,"Files")

        #widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "DUMP_ANSYS_FILES",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No [default]', 'Yes (as plotted)', 'Yes (transposed)'],
                    valueType=int, orientation="horizontal", labelWidth=350)

        self.show_at(self.unitFlags()[idx], box1)


        box = gui.widgetBox(box0,"Processing")
        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "ORIENTATION_LOGIC",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['relative to previous o.e. [like SHADOW]',
                            'relative to lab frame [default]'],
                     valueType=int, orientation="horizontal", labelWidth=125)

        self.show_at(self.unitFlags()[idx], box1)

        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "INTERPOLATION_OR_HISTOGRAMMING",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Interpolation [default]', 'Histogramming'],
                     valueType=int, orientation="horizontal", labelWidth=350)

        self.show_at(self.unitFlags()[idx], box1)

        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "INTERPOLATION_METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['nearest', 'linear', 'cubic [default]'],
                     valueType=int, orientation="horizontal", labelWidth=350)

        self.show_at(self.unitFlags()[idx], box1)

        self.show_at(self.unitFlags()[idx], box1)

        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)
        oasysgui.lineEdit(box1, self, "RATIO_PIXELS_0",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)
        oasysgui.lineEdit(box1, self, "RATIO_PIXELS_1",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        box = gui.widgetBox(box0,"Debug")
        #
        # widget index xx
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "DEBUG_RUN_URGENT",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['No [default]', 'Yes [skip running URGENT]'],
                     valueType=int, orientation="horizontal", labelWidth=350)

        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #
        self.mirror_tabs_visibility()

    def guess_number_of_harmonics(self):

        syned_undulator = Undulator(
                 K_vertical = self.KY,
                 K_horizontal = self.KX,
                 period_length = self.PERIOD_LENGTH,
                 number_of_periods = self.NUMBER_OF_PERIODS)

        Bx = syned_undulator.magnetic_field_horizontal()
        By =  syned_undulator.magnetic_field_vertical()
        Ec = 665.0 * self.RING_ENERGY**2 * numpy.sqrt( Bx**2 + By**2)
        E1 = syned_undulator.resonance_energy(self.gamma(), harmonic=1)
        self.NUMBER_OF_HARMONICS = -(numpy.floor(numpy.abs(10*Ec/E1))+5)

        # UnNh = -(numpy.floor(numpy.abs(10 * Ec / E1)) + 5) # Number of harmonics in calculation

    def setdistance(self):
        self.EL0_P_POSITION = self.SOURCE_SCREEN_DISTANCE

    def set_NELEMENTS(self):
        self.initializeTabs()
        self.mirror_tabs_visibility()

    def mirror_tabs_visibility(self):

        for i in range(6):
            if (i+1) <= self.NELEMENTS:
                self.tab_el[i].setEnabled(True)
            else:
                self.tab_el[i].setEnabled(False)

    def set_EL_FLAG(self):
        self.initializeTabs()

    def unitLabels(self):
         labels =  ["Ring energy [GeV]","Ring current [A]","Ky","Kx",
                 "Number of Periods","Period Length [m]",
                 "Sigma H [mm]", "Sigma Prime H [mrad]", "Sigma V [mm]", "Sigma Prime V [mrad]",
                 "Number of harmonics",
                 "Source to screen distance [m]","Horizontal acceptance [mm]","Vertical acceptance [mm]",
                 "Number of intervals in half H screen","Number of intervals in half V screen","Electron sigmas",
                 'Number of optical elements:']

         for i in range(6):
            labels = labels + [
                'Type',
                'Distance from previous cont. plane [m]',
                'Distance to next continuation plane [m]',
                'Focus Entrance Arm [m]',
                'Focus Exit Arm [m]',
                'Inc. Angle to normal [deg]',
                'Thickness [microns]',
                'Orientation (see Settings tab)',
                'Coating',
                ]

         labels = labels + ["Calculate power on images","Number of ray-tracing runs","Random seed (int): ",
                            "Plot mode","Plot ray-traced grid","Show URGENT plots",
                            "Write FEA/ANSYS files",
                            "O.E. orientation","Calculation method for images","Interpolation",
                            "Ratio pixels axis 0 o.e./source","Ratio pixels axis 1 o.e./source",
                            "Debug mode (do not run URGENT)"]

         return labels


    def unitFlags(self):
         # labels =  ["Ring energy [GeV]","Ring current [A]","Ky","Kx",
         #         "Number of Periods","Period Length [m]",
         #         "Sigma H [mm]", "Sigma Prime H [mrad]", "Sigma V [mm]", "Sigma Prime V [mrad]",
         #         "Number of harmonics",
         #         "Source to screen distance [m]","Horizontal acceptance [mm]","Vertical acceptance [mm]",
         #         "Number of intervals in half H screen","Number of intervals in half V screen","Electron sigmas",
         #         'Number of optical elements:']
         return ["True", "True", "True", "True",
                 "True", "True",
                 "True", "True", "True", "True",
                 "True",
                 "True", "True", "True",
                 "True", "True","True",
                 'True', #
                 "True", "True", "True", "self.EL0_SHAPE not in (2,8,9)", "self.EL0_SHAPE not in (2,8,9)", "True", "self.EL0_SHAPE in (8,9)", "True", "True",  # shape, p, q, p_foc, q_foc, angle, thickness, orientation, coating
                 "True", "True", "True", "self.EL1_SHAPE not in (2,8,9)", "self.EL1_SHAPE not in (2,8,9)", "True", "self.EL1_SHAPE in (8,9)", "True", "True",  # OE fields
                 "True", "True", "True", "self.EL2_SHAPE not in (2,8,9)", "self.EL2_SHAPE not in (2,8,9)", "True", "self.EL2_SHAPE in (8,9)", "True", "True",  # OE fields
                 "True", "True", "True", "self.EL3_SHAPE not in (2,8,9)", "self.EL3_SHAPE not in (2,8,9)", "True", "self.EL3_SHAPE in (8,9)", "True", "True",  # OE fields
                 "True", "True", "True", "self.EL4_SHAPE not in (2,8,9)", "self.EL4_SHAPE not in (2,8,9)", "True", "self.EL4_SHAPE in (8,9)", "True", "True",  # OE fields
                 "True", "True", "True", "self.EL5_SHAPE not in (2,8,9)", "self.EL5_SHAPE not in (2,8,9)", "True", "self.EL5_SHAPE in (8,9)", "True", "True",  # OE fields
                 'True', 'self.RAY_TRACING_IMAGE == 1', 'self.RAY_TRACING_IMAGE == 1',
                 'True', 'True', 'True',
                 'True',
                 'True', 'True', 'True',
                 'True', 'True',
                 'True']

    # labels = labels + ["Calculate power on images", "Number of ray-tracing runs", "Random seed (int): ",
    #                    "Plot mode", "Plot ray-traced grid", "Show URGENT plots",
    #                    "Write SHADOW files", "Write FEA/ANSYS files",
    #                    "Calculation method for images", "Interpolation",
    #                    "Ratio pixels axis 0 o.e./source", "Ratio pixels axis 1 o.e./source",
    #                    "Debug mode (do not run URGENT)"]

    def get_help_name(self):
        return 'srcalc-idpower'

    def selectFile(self):
        self.le_source_file.setText(oasysgui.selectFileFromDialog(self, self.SOURCE_FILE, "Open Source File", file_extension_filter="*.*"))

    def check_fields(self):
        self.RING_ENERGY       = congruence.checkPositiveNumber(self.RING_ENERGY      , "RING_ENERGY      ")
        self.RING_CURRENT      = congruence.checkPositiveNumber(self.RING_CURRENT     , "RING_CURRENT     ")
        self.KY                = congruence.checkPositiveNumber(self.KY               , "KY               ")
        self.KX                = congruence.checkPositiveNumber(self.KX               , "KX               ")
        self.NUMBER_OF_PERIODS = congruence.checkPositiveNumber(self.NUMBER_OF_PERIODS, "NUMBER_OF_PERIODS")
        self.PERIOD_LENGTH     = congruence.checkPositiveNumber(self.PERIOD_LENGTH    , "PERIOD_LENGTH    ")

        self.NUMBER_OF_HARMONICS = congruence.checkNumber(self.NUMBER_OF_HARMONICS, "NUMBER_OF_HARMONICS")

        self.SOURCE_SCREEN_DISTANCE = congruence.checkPositiveNumber(self.SOURCE_SCREEN_DISTANCE, "SOURCE_SCREEN_DISTANCE")
        self.HORIZONTAL_ACCEPTANCE  = congruence.checkPositiveNumber(self.HORIZONTAL_ACCEPTANCE , "HORIZONTAL_ACCEPTANCE ")
        self.VERTICAL_ACCEPTANCE    = congruence.checkPositiveNumber(self.VERTICAL_ACCEPTANCE   , "VERTICAL_ACCEPTANCE   ")
        self.NUMBER_OF_POINTS_H     = congruence.checkPositiveNumber(self.NUMBER_OF_POINTS_H    , "NUMBER_OF_POINTS_H    ")
        self.NUMBER_OF_POINTS_V     = congruence.checkPositiveNumber(self.NUMBER_OF_POINTS_V    , "NUMBER_OF_POINTS_V    ")
        self.ELECTRON_SIGMAS        = congruence.checkPositiveNumber(self.ELECTRON_SIGMAS       , "ELECTRON_SIGMAS       ")
        self.SIGMAX                 = congruence.checkPositiveNumber(self.SIGMAX                , "SIGMAX                ")
        self.SIGMAXP                = congruence.checkPositiveNumber(self.SIGMAXP               , "SIGMAXP               ")
        self.SIGMAY                 = congruence.checkPositiveNumber(self.SIGMAY                , "SIGMAY                ")
        self.SIGMAYP                = congruence.checkPositiveNumber(self.SIGMAYP               , "SIGMAYP               ")

        if self.NELEMENTS >=6:
            self.EL5_P_POSITION  = congruence.checkPositiveNumber(self.EL5_P_POSITION,  "EL5_P_POSITION")
            self.EL5_Q_POSITION = congruence.checkPositiveNumber(self.EL5_Q_POSITION, "EL5_Q_POSITION")
            self.EL5_P_FOCUS   = congruence.checkPositiveNumber(self.EL5_P_FOCUS,         "EL5_P_FOCUS")
            self.EL5_Q_FOCUS   = congruence.checkPositiveNumber(self.EL5_Q_FOCUS,         "EL5_Q_FOCUS")
            self.EL5_ANG       = congruence.checkPositiveNumber(self.EL5_ANG,       "EL5_ANG")
            self.EL5_THICKNESS = congruence.checkPositiveNumber(self.EL5_THICKNESS, "EL5_THICKNESS")

        if self.NELEMENTS >=5:
            self.EL4_P_POSITION  = congruence.checkPositiveNumber(self.EL4_P_POSITION,  "EL4_P_POSITION")
            self.EL4_Q_POSITION  = congruence.checkPositiveNumber(self.EL4_Q_POSITION,  "EL4_Q_POSITION")
            self.EL4_P_FOCUS    = congruence.checkPositiveNumber(self.EL4_P_FOCUS,         "EL4_P_FOCUS")
            self.EL4_Q_FOCUS    = congruence.checkPositiveNumber(self.EL4_Q_FOCUS,         "EL4_Q_FOCUS")
            self.EL4_ANG       = congruence.checkPositiveNumber(self.EL4_ANG,       "EL4_ANG")
            self.EL4_THICKNESS = congruence.checkPositiveNumber(self.EL4_THICKNESS, "EL4_THICKNESS")

        if self.NELEMENTS >=4:
            self.EL3_P_POSITION  = congruence.checkPositiveNumber(self.EL3_P_POSITION,  "EL3_P_POSITION")
            self.EL3_Q_POSITION  = congruence.checkPositiveNumber(self.EL3_Q_POSITION,  "EL3_Q_POSITION")
            self.EL3_P_FOCUS         = congruence.checkPositiveNumber(self.EL3_P_FOCUS,         "EL3_P_FOCUS")
            self.EL3_Q_FOCUS         = congruence.checkPositiveNumber(self.EL3_Q_FOCUS,         "EL3_Q_FOCUS")
            self.EL3_ANG       = congruence.checkPositiveNumber(self.EL3_ANG,       "EL3_ANG")
            self.EL3_THICKNESS = congruence.checkPositiveNumber(self.EL3_THICKNESS, "EL3_THICKNESS")

        if self.NELEMENTS >=3:
            self.EL2_P_POSITION  = congruence.checkPositiveNumber(self.EL2_P_POSITION,  "EL2_P_POSITION")
            self.EL2_Q_POSITION  = congruence.checkPositiveNumber(self.EL2_Q_POSITION,  "EL2_Q_POSITION")
            self.EL2_P_FOCUS         = congruence.checkPositiveNumber(self.EL2_P_FOCUS,         "EL2_P_FOCUS")
            self.EL2_Q_FOCUS         = congruence.checkPositiveNumber(self.EL2_Q_FOCUS,         "EL2_Q_FOCUS")
            self.EL2_ANG       = congruence.checkPositiveNumber(self.EL2_ANG,       "EL2_ANG")
            self.EL2_THICKNESS = congruence.checkPositiveNumber(self.EL2_THICKNESS, "EL2_THICKNESS")

        if self.NELEMENTS >=2:
            self.EL1_P_POSITION  = congruence.checkPositiveNumber(self.EL1_P_POSITION,  "EL1_P_POSITION")
            self.EL1_Q_POSITION  = congruence.checkPositiveNumber(self.EL1_Q_POSITION,  "EL1_Q_POSITION")
            self.EL1_P_FOCUS         = congruence.checkPositiveNumber(self.EL1_P_FOCUS,         "EL1_P_FOCUS")
            self.EL1_Q_FOCUS         = congruence.checkPositiveNumber(self.EL1_Q_FOCUS,         "EL1_Q_FOCUS")
            self.EL1_ANG       = congruence.checkPositiveNumber(self.EL1_ANG,       "EL1_ANG")
            self.EL1_THICKNESS = congruence.checkPositiveNumber(self.EL1_THICKNESS, "EL1_THICKNESS")

        if self.NELEMENTS >=1:
            self.EL0_P_POSITION  = congruence.checkPositiveNumber(self.EL0_P_POSITION,  "EL0_P_POSITION")
            self.EL0_Q_POSITION  = congruence.checkPositiveNumber(self.EL0_Q_POSITION,  "EL0_Q_POSITION")
            self.EL0_P_FOCUS         = congruence.checkPositiveNumber(self.EL0_P_FOCUS,         "EL0_P_FOCUS")
            self.EL0_Q_FOCUS         = congruence.checkPositiveNumber(self.EL0_Q_FOCUS,         "EL0_Q_FOCUS")
            self.EL0_ANG       = congruence.checkPositiveNumber(self.EL0_ANG,       "EL0_ANG")
            self.EL0_THICKNESS = congruence.checkPositiveNumber(self.EL0_THICKNESS, "EL0_THICKNESS")

    def receive_syned_data(self, data):
        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data._light_source._magnetic_structure, synedid.InsertionDevice):
                light_source = data._light_source

                self.RING_ENERGY = light_source._electron_beam._energy_in_GeV
                self.RING_CURRENT = light_source._electron_beam._current

                x, xp, y, yp = light_source._electron_beam.get_sigmas_all()

                self.SIGMAX = x * 1e3
                self.SIGMAY = y * 1e3
                self.SIGMAXP = xp * 1e3
                self.SIGMAYP = yp * 1e3
                self.PERIOD_LENGTH = light_source._magnetic_structure._period_length
                self.NUMBER_OF_PERIODS = int(light_source._magnetic_structure._number_of_periods)
                self.KY = light_source._magnetic_structure._K_vertical
                self.KX = light_source._magnetic_structure._K_horizontal

                self.set_enabled(False)

            else:
                self.set_enabled(True)
                # raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)
            # raise ValueError("Syned data not correct")

    def set_enabled(self,value):
        if value == True:
                self.id_RING_ENERGY.setEnabled(True)
                self.id_SIGMAX.setEnabled(True)
                self.id_SIGMAY.setEnabled(True)
                self.id_SIGMAXP.setEnabled(True)
                self.id_SIGMAYP.setEnabled(True)
                self.id_RING_CURRENT.setEnabled(True)
                self.id_PERIOD_LENGTH.setEnabled(True)
                self.id_NUMBER_OF_PERIODS.setEnabled(True)
                self.id_KX.setEnabled(True)
                self.id_KY.setEnabled(True)
        else:
                self.id_RING_ENERGY.setEnabled(False)
                self.id_SIGMAX.setEnabled(False)
                self.id_SIGMAY.setEnabled(False)
                self.id_SIGMAXP.setEnabled(False)
                self.id_SIGMAYP.setEnabled(False)
                self.id_RING_CURRENT.setEnabled(False)
                self.id_PERIOD_LENGTH.setEnabled(False)
                self.id_NUMBER_OF_PERIODS.setEnabled(False)
                self.id_KX.setEnabled(False)
                self.id_KY.setEnabled(False)

    def do_xoppy_calculation(self):
        # odd way to clean output window during running
        view_type_old = self.view_type
        self.view_type = 0
        self.set_ViewType()

        out = self.xoppy_calc_srcalc()

        self.view_type = view_type_old
        self.set_ViewType()

        return out

    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def plot_results(self, calculated_data, progressBarValue=70):
        if not self.view_type == 0:
            if calculated_data is None:
                raise Exception("Empty Data")

            index = -1

            for oe_n in range(self.NELEMENTS+1):
                #
                # urgent results
                #
                if oe_n == 0 or self.SHOW_URGENT_PLOTS == 1:
                    totPower2 = trapezoidal_rule_2d_1darrays(calculated_data["Zlist"][oe_n])
                    if oe_n == 0:
                        title = 'Power density [W/mm2] at %4.1f m, Integrated Power: %6.1f W' % (
                        self.SOURCE_SCREEN_DISTANCE, totPower2)
                        xtitle = 'H (urgent) [mm] (%d pixels)' % (calculated_data["X"].size)
                        ytitle = 'V (urgent) [mm] (%d pixels)' % (calculated_data["Y"].size)
                        x = calculated_data["X"]
                        y = calculated_data["Y"]
                    else:
                        title = 'Power density [W/mm2] transmitted after element %d Integrated Power: %6.1f W' % (
                        oe_n, totPower2)
                        xtitle = 'H [pixels]'
                        ytitle = 'V [pixels]'
                        x = numpy.arange(calculated_data["X"].size)
                        y = numpy.arange(calculated_data["Y"].size)

                    index += 1
                    z = (calculated_data["Zlist"][oe_n]).copy()
                    z /= (calculated_data["X"][1] - calculated_data["X"][0]) * \
                         (calculated_data["Y"][1] - calculated_data["Y"][0])
                    self.plot_data2D(z, x, y,  index, 0, mode=self.PLOT_MODE,
                                     xtitle=xtitle, ytitle=ytitle, title=title)

                #
                # ray tracing results
                #
                if oe_n > 0:
                    overplot_data_footprint = None
                    overplot_data_image = None

                    if self.DO_PLOT_GRID == 0:
                        pass
                    elif self.DO_PLOT_GRID == 1:
                        overplot_data_footprint = [
                            1e3 * calculated_data["OE_FOOTPRINT"][oe_n - 1][0, :],
                            1e3 * calculated_data["OE_FOOTPRINT"][oe_n - 1][1, :],
                            ]
                        if self.RAY_TRACING_IMAGE:
                            overplot_data_image = [
                                1e3 * calculated_data["OE_IMAGE"][oe_n - 1][1, :],
                                1e3 * calculated_data["OE_IMAGE"][oe_n - 1][0, :],
                                ]
                    elif self.DO_PLOT_GRID == 2:

                        # mirror grid
                        index += 1
                        dataX = calculated_data["OE_FOOTPRINT"][oe_n-1][0, :]
                        dataY = calculated_data["OE_FOOTPRINT"][oe_n-1][1, :]
                        self.plot_data1D(1e3*dataY, 1e3*dataX, index, 0, title="footprint oe %d"%oe_n,
                                         ytitle="Y (shadow col 2) [mm]",
                                         xtitle="X (shadow col 1) [mm]")

                        if self.RAY_TRACING_IMAGE:
                            # image grid
                            index += 1
                            dataX = calculated_data["OE_IMAGE"][oe_n-1][0, :]
                            dataY = calculated_data["OE_IMAGE"][oe_n-1][1, :]
                            if self.ORIENTATION_LOGIC == 0:
                                xtitle = "X (shadow col 1) [mm]"
                                ytitle = "Z (shadow col 2) [mm]"
                            elif self.ORIENTATION_LOGIC == 1:
                                xtitle = "H [mm]"
                                ytitle = "V [mm]"

                            self.plot_data1D(1e3*dataX, 1e3*dataY, index, 0,
                                             title="image just after oe %d perp to beam"%oe_n,
                                             xtitle=xtitle, ytitle=ytitle)


                    # mirror power density
                    index += 1
                    H = 1e3 * calculated_data["POWER_DENSITY_FOOTPRINT_H"][oe_n - 1]
                    V = 1e3 * calculated_data["POWER_DENSITY_FOOTPRINT_V"][oe_n - 1]
                    stepx = numpy.abs(H[1,0] - H[0,0])
                    stepy = numpy.abs(V[0,1] - V[0,0])
                    data2D = (calculated_data["POWER_DENSITY_FOOTPRINT"][oe_n - 1])
                    totPower2 =   trapezoidal_rule_2d(data2D)
                    title = 'Power density [W/mm2] absorbed at element %d Integrated Power: %6.1f W' % (oe_n, totPower2)
                    if self.ORIENTATION_LOGIC == 0:
                        xtitle = 'X (shadow col 1) [mm] (%d pixels)' % (H.shape[0])
                        ytitle = 'Y (shadow col 2) [mm] (%d pixels)' % (H.shape[1])
                    elif self.ORIENTATION_LOGIC == 1:
                        xtitle = 'Width (perp to beam) [mm] (%d pixels)' % (H.shape[0])
                        ytitle = 'Length (along the beam) [mm] (%d pixels)' % (H.shape[1])

                    self.plot_data2D(data2D / (stepx * stepy) , H[:,0], V[0,:],
                                     index, 0, mode=self.PLOT_MODE,
                                     overplot=overplot_data_footprint,
                                     xtitle=xtitle,
                                     ytitle=ytitle,
                                     title=title)

                    if self.DUMP_ANSYS_FILES == 0:
                        pass
                    if self.DUMP_ANSYS_FILES == 1: # as plotted
                        write_ansys_files(data2D / (stepx * stepy), H[:,0], V[0,:], oe_number=oe_n)
                    elif self.DUMP_ANSYS_FILES == 2: # transposed
                        write_ansys_files(data2D.T / (stepx * stepy), V[0,:], H[:,0],  oe_number=oe_n)

                    if self.RAY_TRACING_IMAGE:
                        # image power density
                        index += 1
                        data2D = calculated_data["POWER_DENSITY_IMAGE"][oe_n - 1]
                        H = 1e3 * calculated_data["POWER_DENSITY_IMAGE_H"][oe_n - 1]
                        V = 1e3 * calculated_data["POWER_DENSITY_IMAGE_V"][oe_n - 1]
                        stepx = H[1,0] - H[0,0]
                        stepy = V[0,1] - V[0,0]
                        totPower2 = trapezoidal_rule_2d(data2D)
                        title = 'Power density [W/mm2] transmitted after element %d Integrated Power: %6.1f W' % (oe_n, totPower2)
                        if self.ORIENTATION_LOGIC == 0:
                            xtitle = 'X (shadow col 1) [mm] (%d pixels)' % (H.shape[0])
                            ytitle = 'Z (shadow col 3) [mm] (%d pixels)' % (H.shape[1])
                        elif self.ORIENTATION_LOGIC == 1:
                            xtitle = 'H [mm] (%d pixels)' % (H.shape[0])
                            ytitle = 'V [mm] (%d pixels)' % (H.shape[1])

                        self.plot_data2D(data2D / (stepx * stepy), H[:,0], V[0,:],
                                         index, 0, mode=self.PLOT_MODE,
                                         overplot=overplot_data_image,
                                         xtitle=xtitle,
                                         ytitle=ytitle,
                                         title=title)

                        if self.DUMP_ANSYS_FILES == 0:
                            pass
                        if self.DUMP_ANSYS_FILES == 1:  # as plotted
                            write_ansys_files(data2D / (stepx * stepy), H[:, 0], V[0, :], oe_number=oe_n,
                                              is_image=True)
                        elif self.DUMP_ANSYS_FILES == 2:  # transposed
                            write_ansys_files(data2D.T / (stepx * stepy), V[0, :], H[:, 0], oe_number=oe_n,
                                              is_image=True)


    def get_data_exchange_widget_name(self):
        return "SRCALC"

    def getTitles(self):
        titles = []
        for oe_n in range(self.NELEMENTS+1):
            if self.SHOW_URGENT_PLOTS == 0:
                if oe_n == 0: titles.append("[oe %d (urgent)]"%oe_n)
            else:
                titles.append("[oe %d (urgent)]" % oe_n)
            if oe_n > 0:
                if self.DO_PLOT_GRID == 2:
                    titles.append("[oe %d (ray-traced mirror grid)]" % oe_n)
                    if self.RAY_TRACING_IMAGE:
                        titles.append("[oe %d (ray-traced image grid)]" % oe_n)
                titles.append("[oe %d (ray tracing mirror power)]" % oe_n)
                if self.RAY_TRACING_IMAGE:
                    titles.append("[oe %d (ray tracing image power)]" % oe_n)
        return titles

    def run_urgent(self):
        polarization_list, polarization_inversion, polarization_info = self.get_polarization_list()

        if self.NUMBER_OF_POINTS_H > 50:
            showCriticalMessage("Max NUMBER_OF_POINTS_H is 50")
            raise Exception("Bad inputs")

        if self.NUMBER_OF_POINTS_V > 50:
            showCriticalMessage("Max NUMBER_OF_POINTS_V is 50")
            raise Exception("Bad inputs")

        if self.DEBUG_RUN_URGENT == 0:
            for file in ["IDPower.TXT","O_IDPower.TXT","D_IDPower.TXT"]:
                try:
                    os.remove(os.path.join(locations.home_bin_run(),file))
                except:
                    pass

            f = open("IDPower.TXT","w")

            f.write( "%s\n"% (os.path.join(locations.home_data(), "reflect" + os.sep))    )
            f.write("%f\n" % self.KY)               #   READ(1,*) ky
            f.write("%f\n" % self.RING_ENERGY)      # 	READ(1,*) energy
            f.write("%f\n" % self.RING_CURRENT)     # 	READ(1,*) cur
            f.write("%f\n" % self.SIGMAX)       # 	READ(1,*) sigmx
            f.write("%f\n" % self.SIGMAY)       # 	READ(1,*) sigy
            f.write("%f\n" % self.SIGMAXP)      # 	READ(1,*) sigx1
            f.write("%f\n" % self.SIGMAYP)      # 	READ(1,*) sigy1
            f.write("%d\n" % self.NUMBER_OF_PERIODS)     # 	READ(1,*) n
            f.write("%f\n" % self.PERIOD_LENGTH)         # 	READ(1,*) period

            f.write("%f\n" % self.SOURCE_SCREEN_DISTANCE)          # 	READ(1,*) d            p M1
            f.write("%d\n" % self.NELEMENTS)     # 	READ(1,*) nMir

            #
            # BEAMLINE
            #
            f.write("%f\n" % self.EL0_ANG)  # READ(1,*) anM(1)           # incidence angle
            f.write("%d\n" % self.EL0_SHAPE)  # READ(1,*) miType(1)        # type
            f.write("%d\n" % self.EL0_THICKNESS)  # READ(1,*) thic(1)
            f.write("'%s'\n" % self.coating_list[self.EL0_COATING])  # READ(1,*) com(1)           # coating
            f.write("'%s'\n" % polarization_list[0])

            f.write("%f\n" %                   self.EL1_ANG)        #  READ(1,*) anM(1)           # incidence angle
            f.write("%d\n" %                   self.EL1_SHAPE)      # 	READ(1,*) miType(1)        # type
            f.write("%d\n" %                   self.EL1_THICKNESS)  # 	READ(1,*) thic(1)
            f.write("'%s'\n" % self.coating_list[self.EL1_COATING])     # 	READ(1,*) com(1)           # coating
            f.write("'%s'\n" % polarization_list[1])                    # 	READ(1,*) iPom(1)          # ! Polarization or filter

            f.write("%f\n" %                   self.EL2_ANG)        #  READ(1,*) anM(1)           # incidence angle
            f.write("%d\n" %                   self.EL2_SHAPE)      # 	READ(1,*) miType(1)        # type
            f.write("%d\n" %                   self.EL2_THICKNESS)  # 	READ(1,*) thic(1)
            f.write("'%s'\n" % self.coating_list[self.EL2_COATING])     # 	READ(1,*) com(1)           # coating
            f.write("'%s'\n" % polarization_list[2])                                # 	READ(1,*) iPom(1)          # ! Polarization or filter

            f.write("%f\n" %                   self.EL3_ANG)        #  READ(1,*) anM(1)           # incidence angle
            f.write("%d\n" %                   self.EL3_SHAPE)      # 	READ(1,*) miType(1)        # type
            f.write("%d\n" %                   self.EL3_THICKNESS)  # 	READ(1,*) thic(1)
            f.write("'%s'\n" % self.coating_list[self.EL3_COATING])     # 	READ(1,*) com(1)           # coating
            f.write("'%s'\n" % polarization_list[3])                            # 	READ(1,*) iPom(1)          # ! Polarization or filter

            f.write("%f\n" %                   self.EL4_ANG)        #  READ(1,*) anM(1)           # incidence angle
            f.write("%d\n" %                   self.EL4_SHAPE)      # 	READ(1,*) miType(1)        # type
            f.write("%d\n" %                   self.EL4_THICKNESS)  # 	READ(1,*) thic(1)
            f.write("'%s'\n" % self.coating_list[self.EL4_COATING])     # 	READ(1,*) com(1)           # coating
            f.write("'%s'\n" % polarization_list[4])                         # 	READ(1,*) iPom(1)          # ! Polarization or filter

            f.write("%f\n" %                   self.EL5_ANG)        #  READ(1,*) anM(1)           # incidence angle
            f.write("%d\n" %                   self.EL5_SHAPE)      # 	READ(1,*) miType(1)        # type
            f.write("%d\n" %                   self.EL5_THICKNESS)  # 	READ(1,*) thic(1)
            f.write("'%s'\n" % self.coating_list[self.EL5_COATING])     # 	READ(1,*) com(1)           # coating
            f.write("'%s'\n" % polarization_list[5])                                # 	READ(1,*) iPom(1)          # ! Polarization or filter


            #
            # Calculation
            #
            f.write("%f\n" % self.HORIZONTAL_ACCEPTANCE)     # 	READ(1,*) xps
            f.write("%f\n" % self.VERTICAL_ACCEPTANCE)     # 	READ(1,*) yps

            f.write("%d\n" % self.NUMBER_OF_POINTS_H)     # 	READ(1,*) nxp
            f.write("%d\n" % self.NUMBER_OF_POINTS_V)     # 	READ(1,*) nyp
            f.write("%d\n" % -6)     # 	READ(1,*) mode
            f.write("%d\n" % self.NUMBER_OF_HARMONICS)   # 	READ(1,*) iharm
            f.write("%d\n" % 1)     # 	READ(1,*) icalc
            f.write("%d\n" % 1)     # 	READ(1,*) itype
            f.write("%d\n" % self.ELECTRON_SIGMAS)     # 	READ(1,*) nSig
            f.write("%d\n" % 20)     # 	READ(1,*) nPhi
            f.write("%d\n" % 20)     # 	READ(1,*) nAlpha
            f.write("%f\n" % 0.000000)     # 	READ(1,*) dAlpha
            f.write("%d\n" % 0)            # 	READ(1,*) nOmega
            f.write("%f\n" % 0.000000)     # 	READ(1,*) dOmega
            f.write("%f\n" % 0.000000)     # 	READ(1,*) xpc
            f.write("%f\n" % 0.000000)     # 	READ(1,*) ypc
            f.write("%d\n" % 0)            # 	READ(1,*) ne
            f.write("%f\n" % 0.000000)     # 	READ(1,*) emin
            f.write("%f\n" % 0.000000)     # 	READ(1,*) emax
            f.write("%f\n" % self.KX)      # 	READ(1,*) kx
            f.write("%f\n" % 0.000000)     # 	READ(1,*) phase

            f.close()

            if platform.system() == "Windows":
                command = os.path.join(locations.home_bin(),'srcalc')
            else:
                command = "'" + os.path.join(locations.home_bin(), 'srcalc') + "'"
            print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
            print("\n--------------------------------------------------------\n")
            os.system(command)
            print("\n--------------------------------------------------------\n")
        else:
            print("\n--------------------------------------------------------\n")
            print("\n    ************  WARNING  *****************************\n")
            print("\n   --- DEBUGGING: URGENT NOT RUN - REUSED LAST FILES ---\n")
            print("\n--------------------------------------------------------\n")


    def xoppy_calc_srcalc(self):

        self.progressBarSet(2)

        sys.stdout = EmittingStream(textWritten=self.writeStdOut)

        grabber = TTYGrabber()
        grabber.start()
        # run fortran code (urgent-based code)
        # self.progressBarSet(5)
        self.run_urgent()
        grabber.stop()

        for row in grabber.ttyData:
            self.writeStdOut(row)

        # self.progressBarSet(60)

        #
        # display some info
        #

        txt0 = "3\n# Info from IDPoser/Urgent\n#\n"
        f = open("O_IDPower.TXT",'r')
        txt = f.read()
        f.close()

        txt2 = self.info_undulator()

        txt3 = self.info_distances()

        polarization_list, polarization_inversion, polarization_info = self.get_polarization_list() # (TO BE DELETED??)
        self.info_output.setText("\n\n\n#\n# Info from IDPower/Urgent\n#\n" + txt + \
                                 "\n\n\n#\n# Additional Info from undulator source\n#\n" + txt2 + \
                                 "\n\n\n#\n# Additional Info o.e. distances\n#\n\n" + txt3 + \
                                 "\n\n\n#\n# Additional Info o.e. polarization\n#\n\n" + polarization_info)


        #
        # load results from file created by fortran
        #
        out_dictionary = load_srcalc_output_file(filename="D_IDPower.TXT")

        #
        # do additional calculations (ray-tracing and power density maps)
        # Note that the results of these two calculations are added to out_dictionary
        #

        #
        # do the ray tracing
        #
        oe_parameters = {
            "EL0_SHAPE":                self.EL0_SHAPE               ,
            "EL0_P_POSITION":           self.EL0_P_POSITION            ,
            "EL0_Q_POSITION":           self.EL0_Q_POSITION,
            "EL0_P_FOCUS":              self.EL0_P_FOCUS                   ,
            "EL0_Q_FOCUS":              self.EL0_Q_FOCUS                   ,
            "EL0_ANG":                  self.EL0_ANG                 ,
            "EL0_THICKNESS":            self.EL0_THICKNESS           ,
            "EL0_RELATIVE_TO_PREVIOUS": self.EL0_RELATIVE_TO_PREVIOUS,
            "EL1_SHAPE":                self.EL1_SHAPE               ,
            "EL1_P_POSITION":           self.EL1_P_POSITION            ,
            "EL1_Q_POSITION":           self.EL1_Q_POSITION,
            "EL1_P_FOCUS":              self.EL1_P_FOCUS             ,
            "EL1_Q_FOCUS":              self.EL1_Q_FOCUS             ,
            "EL1_ANG":                  self.EL1_ANG                 ,
            "EL1_THICKNESS":            self.EL1_THICKNESS           ,
            "EL1_RELATIVE_TO_PREVIOUS": self.EL1_RELATIVE_TO_PREVIOUS,
            "EL2_SHAPE":                self.EL2_SHAPE               ,
            "EL2_P_POSITION":           self.EL2_P_POSITION            ,
            "EL2_Q_POSITION":           self.EL2_Q_POSITION,
            "EL2_P_FOCUS":              self.EL2_P_FOCUS                   ,
            "EL2_Q_FOCUS":              self.EL2_Q_FOCUS                   ,
            "EL2_ANG":                  self.EL2_ANG                 ,
            "EL2_THICKNESS":            self.EL2_THICKNESS           ,
            "EL2_RELATIVE_TO_PREVIOUS": self.EL2_RELATIVE_TO_PREVIOUS,
            "EL3_SHAPE":                self.EL3_SHAPE               ,
            "EL3_P_POSITION":           self.EL3_P_POSITION            ,
            "EL3_Q_POSITION":           self.EL3_Q_POSITION,
            "EL3_P_FOCUS":              self.EL3_P_FOCUS                   ,
            "EL3_Q_FOCUS":              self.EL3_Q_FOCUS                   ,
            "EL3_ANG":                  self.EL3_ANG                 ,
            "EL3_THICKNESS":            self.EL3_THICKNESS           ,
            "EL3_RELATIVE_TO_PREVIOUS": self.EL3_RELATIVE_TO_PREVIOUS,
            "EL4_SHAPE":                self.EL4_SHAPE               ,
            "EL4_P_POSITION":           self.EL4_P_POSITION            ,
            "EL4_Q_POSITION":           self.EL4_Q_POSITION,
            "EL4_P_FOCUS":              self.EL4_P_FOCUS                   ,
            "EL4_Q_FOCUS":              self.EL4_Q_FOCUS                   ,
            "EL4_ANG":                  self.EL4_ANG                 ,
            "EL4_THICKNESS":            self.EL4_THICKNESS           ,
            "EL4_RELATIVE_TO_PREVIOUS": self.EL4_RELATIVE_TO_PREVIOUS,
            "EL5_SHAPE":                self.EL5_SHAPE               ,
            "EL5_P_POSITION":           self.EL5_P_POSITION            ,
            "EL5_Q_POSITION":           self.EL5_Q_POSITION,
            "EL5_P_FOCUS":              self.EL5_P_FOCUS                   ,
            "EL5_Q_FOCUS":              self.EL5_Q_FOCUS                   ,
            "EL5_ANG":                  self.EL5_ANG                 ,
            "EL5_THICKNESS":            self.EL5_THICKNESS           ,
            "EL5_RELATIVE_TO_PREVIOUS": self.EL5_RELATIVE_TO_PREVIOUS,

        }

        self.progressBarSet(45)
        # first run for mirror footprint
        out_dictionary = ray_tracing(out_dictionary,
                            SOURCE_SCREEN_DISTANCE=self.SOURCE_SCREEN_DISTANCE,
                            number_of_elements=self.NELEMENTS,
                            oe_parameters=oe_parameters,
                            real_space_shuffle=[0, 0, 0],
                            store_footprint=True,
                            store_image=False,
                            accumulate_results=False,
                            run_index=None,
                            undo_shadow_orientation_angle_rotation=self.ORIENTATION_LOGIC,
                            )

        tmp, flip_pixels_number, tmp = self.get_polarization_list()

        out_dictionary = compute_power_density_footprint(out_dictionary,
                                    interpolation_method=self.INTERPOLATION_METHOD,
                                    ratio_pixels_0=self.RATIO_PIXELS_0,
                                    ratio_pixels_1=self.RATIO_PIXELS_1,
                                    flip_pixels_number=flip_pixels_number)

        if self.RAY_TRACING_IMAGE == 1:

            numpy.random.seed(self.RAY_TRACING_SEED)

            if self.ORIENTATION_LOGIC == 1:
                flip_pixels_number = [0] * 6

            for i in range(self.RAY_TRACING_RUNS):

                depth = (numpy.random.random() - 0.5) * self.NUMBER_OF_PERIODS * self.PERIOD_LENGTH
                real_space_shuffle = [
                    1e-3 * self.SIGMAX * numpy.random.randn(),
                    depth,
                    1e-3 * self.SIGMAY * numpy.random.randn(),
                ]

                print("\n\n\n\n******************** STARTING RUN INDEX %d WITH INITIAL CONDITIONS [x,y,z]  ***********: "%i,real_space_shuffle)
                out_dictionary = ray_tracing(out_dictionary,
                                SOURCE_SCREEN_DISTANCE=self.SOURCE_SCREEN_DISTANCE,
                                number_of_elements=self.NELEMENTS,
                                oe_parameters=oe_parameters,
                                real_space_shuffle=real_space_shuffle,
                                store_footprint=False,
                                store_image=True,
                                accumulate_results=True,
                                run_index=i,
                                undo_shadow_orientation_angle_rotation=self.ORIENTATION_LOGIC,
                                )

            #
            # calculate power density maps and add results to the dictionaire
            #
            out_dictionary = compute_power_density_image(out_dictionary,
                                    interpolation_or_histogramming=self.INTERPOLATION_OR_HISTOGRAMMING,
                                    interpolation_method=self.INTERPOLATION_METHOD,
                                    ratio_pixels_0=self.RATIO_PIXELS_0,
                                    ratio_pixels_1=self.RATIO_PIXELS_1,
                                    flip_pixels_number=flip_pixels_number)

        return out_dictionary

    #
    # overwritten methods
    #
    def plot_data1D(self, dataX, dataY, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle=""):

        self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(0))

        self.plot_canvas[plot_canvas_index] = oasysgui.plotWindow()

        self.plot_canvas[plot_canvas_index].addCurve(dataX, dataY, symbol=',', linestyle=' ')

        self.plot_canvas[plot_canvas_index].resetZoom()
        self.plot_canvas[plot_canvas_index].setXAxisAutoScale(True)
        self.plot_canvas[plot_canvas_index].setYAxisAutoScale(True)
        self.plot_canvas[plot_canvas_index].setGraphGrid(False)

        self.plot_canvas[plot_canvas_index].setXAxisLogarithmic(False)
        self.plot_canvas[plot_canvas_index].setYAxisLogarithmic(False)
        self.plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
        self.plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
        self.plot_canvas[plot_canvas_index].setGraphTitle(title)

        self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])

    def plot_data2D(self, data2D, dataX, dataY, tabs_canvas_index, plot_canvas_index,
                    title="", xtitle="", ytitle="", mode=1, overplot = None):

        for i in range(1+self.tab[tabs_canvas_index].layout().count()):
            self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(i))

        origin = (dataX[0],dataY[0])
        scale = (dataX[1]-dataX[0],dataY[1]-dataY[0])


        colormap = {"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256}


        if mode == 0:
            data_to_plot = data2D
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from srxraylib.plot.gol import plot_image
            f = plot_image(data_to_plot,
                                                 dataX,
                                                 dataY,
                                                 xtitle=xtitle,
                                                 ytitle=ytitle,
                                                 title=title,
                                                 show=False,
                                                 aspect='auto')
            figure = FigureCanvas(f[0])
            self.plot_canvas[plot_canvas_index] = figure
        elif mode == 1:
            data_to_plot = data2D
            self.plot_canvas[plot_canvas_index] = ImageViewWithFWHM()  # Plot2D()
            self.plot_canvas[plot_canvas_index].plot_2D(data_to_plot,
                                dataX, dataY, factor1=1e0, factor2=1e0,
                                title=title, xtitle=xtitle, ytitle=ytitle, xum="[mm]", yum="[mm]",
                                colormap=colormap)
            self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])
        elif mode == 2:
            data_to_plot = data2D.T
            self.plot_canvas[plot_canvas_index] = Plot2D()
            self.plot_canvas[plot_canvas_index].resetZoom()
            self.plot_canvas[plot_canvas_index].setXAxisAutoScale(True)
            self.plot_canvas[plot_canvas_index].setYAxisAutoScale(True)
            self.plot_canvas[plot_canvas_index].setGraphGrid(False)
            self.plot_canvas[plot_canvas_index].setKeepDataAspectRatio(True)
            self.plot_canvas[plot_canvas_index].yAxisInvertedAction.setVisible(False)

            self.plot_canvas[plot_canvas_index].setXAxisLogarithmic(False)
            self.plot_canvas[plot_canvas_index].setYAxisLogarithmic(False)
            #silx 0.4.0
            self.plot_canvas[plot_canvas_index].getMaskAction().setVisible(False)
            self.plot_canvas[plot_canvas_index].getRoiAction().setVisible(False)
            self.plot_canvas[plot_canvas_index].getColormapAction().setVisible(True)
            self.plot_canvas[plot_canvas_index].setKeepDataAspectRatio(False)
            self.plot_canvas[plot_canvas_index].addImage(numpy.array(data_to_plot),
                                                         legend="zio billy",
                                                         scale=scale,
                                                         origin=origin,
                                                         colormap=colormap,
                                                         replace=True)
            self.plot_canvas[plot_canvas_index].setActiveImage("zio billy")

            if overplot is not None:
                self.plot_canvas[plot_canvas_index].addScatter(overplot[1],overplot[0],overplot[1]*0+data_to_plot.max()*2,
                                                             legend="tio pepe",
                                                             colormap={"name":"gray", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256},
                                                             symbol='.')

            self.plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
            self.plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
            self.plot_canvas[plot_canvas_index].setGraphTitle(title)

        self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])

    def gamma(self):
        return 1e9*self.RING_ENERGY / (codata.m_e *  codata.c**2 / codata.e)

    def info_undulator(self):
        syned_electron_beam = ElectronBeam(
                 energy_in_GeV = self.RING_ENERGY,
                 energy_spread = 0.0,
                 current = self.RING_CURRENT,
                 number_of_bunches = 400,
                 moment_xx=(1e-3*self.SIGMAX)**2,
                 moment_xxp=0.0,
                 moment_xpxp=(1e-3*self.SIGMAXP)**2,
                 moment_yy=(1e-3*self.SIGMAY)**2,
                 moment_yyp=0.0,
                 moment_ypyp=(1e-3*self.SIGMAYP)**2,)

        syned_undulator = Undulator(
                 K_vertical = self.KY,
                 K_horizontal = self.KX,
                 period_length = self.PERIOD_LENGTH,
                 number_of_periods = self.NUMBER_OF_PERIODS)

        gamma = self.gamma()

        Bx = syned_undulator.magnetic_field_horizontal()
        By =  syned_undulator.magnetic_field_vertical()
        Ec = 665.0 * self.RING_ENERGY**2 * numpy.sqrt( Bx**2 + By**2)

        # U_powerD = 10.84 * U_M_field_m * Energy ^ 4 * Current * U_Length * 100 / U_period
        # U_powerD = 10.84 * numpy.sqrt( Bx**2 + By**2) * self.RING_ENERGY ** 4 * self.RING_CURRENT * self.NUMBER_OF_PERIODS
        # Power Density[W / mrad2] = 116.18 * (Ee[GeV]) **4 * I[A] * N * K * G(K) / P[mm]

        U_powerD = 116.18 * self.RING_ENERGY **4 * self.RING_CURRENT * self.NUMBER_OF_PERIODS * self.KY * 1.0 / (1e3 * self.PERIOD_LENGTH)

        info_parameters = {
            "electron_energy_in_GeV": self.RING_ENERGY,
            "gamma": "%8.3f" % gamma,
            "ring_current": "%4.3f " % syned_electron_beam.current(),
            "K_horizontal": syned_undulator.K_horizontal(),
            "K_vertical": syned_undulator.K_vertical(),
            "period_length": syned_undulator.period_length(),
            "number_of_periods": syned_undulator.number_of_periods(),
            "undulator_length": syned_undulator.length(),
            "critical_energy": "%6.3f" % Ec,
            "resonance_energy": "%6.3f" % syned_undulator.resonance_energy(gamma, harmonic=1),
            "resonance_energy3": "%6.3f" % syned_undulator.resonance_energy(gamma, harmonic=3),
            "resonance_energy5": "%6.3f" % syned_undulator.resonance_energy(gamma, harmonic=5),
            "B_horizontal": "%4.2F" % syned_undulator.magnetic_field_horizontal(),
            "B_vertical": "%4.2F" % syned_undulator.magnetic_field_vertical(),
            "cc_1": "%4.2f" % (1e6 * syned_undulator.gaussian_central_cone_aperture(gamma, 1)),
            "cc_3": "%4.2f" % (1e6 * syned_undulator.gaussian_central_cone_aperture(gamma, 3)),
            "cc_5": "%4.2f" % (1e6 * syned_undulator.gaussian_central_cone_aperture(gamma, 5)),
            # "cc_7": "%4.2f" % (self.gaussian_central_cone_aperture(7)*1e6),
            "sigma_rad": "%5.2f" % (1e6 * syned_undulator.get_sigmas_radiation(gamma, harmonic=1)[0]),
            "sigma_rad_prime": "%5.2f" % (1e6 * syned_undulator.get_sigmas_radiation(gamma, harmonic=1)[1]),
            "sigma_rad3": "%5.2f" % (1e6 * syned_undulator.get_sigmas_radiation(gamma, harmonic=3)[0]),
            "sigma_rad_prime3": "%5.2f" % (1e6 * syned_undulator.get_sigmas_radiation(gamma, harmonic=3)[1]),
            "sigma_rad5": "%5.2f" % (1e6 * syned_undulator.get_sigmas_radiation(gamma, harmonic=5)[0]),
            "sigma_rad_prime5": "%5.2f" % (1e6 * syned_undulator.get_sigmas_radiation(gamma, harmonic=5)[1]),
            "first_ring_1": "%5.2f" % (1e6 * syned_undulator.get_resonance_ring(gamma, harmonic=1, ring_order=1)),
            "first_ring_3": "%5.2f" % (1e6 * syned_undulator.get_resonance_ring(gamma, harmonic=3, ring_order=1)),
            "first_ring_5": "%5.2f" % (1e6 * syned_undulator.get_resonance_ring(gamma, harmonic=5, ring_order=1)),
            "Sx": "%5.2f" % (1e6 * syned_undulator.get_photon_sizes_and_divergences(syned_electron_beam)[0]),
            "Sy": "%5.2f" % (1e6 * syned_undulator.get_photon_sizes_and_divergences(syned_electron_beam)[1]),
            "Sxp": "%5.2f" % (1e6 * syned_undulator.get_photon_sizes_and_divergences(syned_electron_beam)[2]),
            "Syp": "%5.2f" % (1e6 * syned_undulator.get_photon_sizes_and_divergences(syned_electron_beam)[3]),
            "und_power": "%5.2f" % syned_undulator.undulator_full_emitted_power(gamma, syned_electron_beam.current()),
            "und_power_density": "%5.2f" % U_powerD ,
            "CF_h": "%4.3f" % syned_undulator.approximated_coherent_fraction_horizontal(syned_electron_beam,
                                                                                        harmonic=1),
            "CF_v": "%4.3f" % syned_undulator.approximated_coherent_fraction_vertical(syned_electron_beam, harmonic=1),
            "CF": "%4.3f" % syned_undulator.approximated_coherent_fraction(syned_electron_beam, harmonic=1),
        }
        return self.info_template().format_map(info_parameters)

    def info_distances(self):
        txt  = '  ********  SUMMARY OF DISTANCES ********\n'
        txt += '   ** DISTANCES FOR ALL O.E. [m] **           \n\n'
        txt += "%4s %20s %8s %8s %8s %8s \n" % ('OE#', 'TYPE', 'p [m]', 'q [m]', 'src-oe', 'src-screen')
        txt += '----------------------------------------------------------------------\n'

        txt_2 = '\n\n  ********  ELLIPTICAL ELEMENTS  ********\n'
        txt_2 += "%4s %8s %8s %8s %1s\n" % ('OE#', 'p(ell)', 'q(ell)', 'p+q(ell)', 'M')
        txt_2 += '----------------------------------------------------------------------\n'

        P = [self.EL0_P_POSITION, self.EL1_P_POSITION, self.EL2_P_POSITION, self.EL3_P_POSITION, self.EL4_P_POSITION,
             self.EL5_P_POSITION,]
        Q = [self.EL0_Q_POSITION, self.EL1_Q_POSITION, self.EL2_Q_POSITION, self.EL3_Q_POSITION, self.EL4_Q_POSITION,
             self.EL5_Q_POSITION, ]
        SHAPE_INDEX = [self.EL0_SHAPE, self.EL1_SHAPE, self.EL2_SHAPE, self.EL3_SHAPE, self.EL4_SHAPE, self.EL5_SHAPE,]
        oe = 0
        final_screen_to_source = 0.0
        for i in range(self.NELEMENTS):
            oe += 1
            p = P[i]
            q = Q[i]
            shape_index = SHAPE_INDEX[i]

            final_screen_to_source = final_screen_to_source + p + q
            oe_to_source = final_screen_to_source - q

            txt += "%4d %20s %8.4f %8.4f %8.4f %8.4f \n" % (oe, self.shape_list[shape_index], p, q, oe_to_source, final_screen_to_source)
        return txt

    def info_template(self):
        return \
            """
            
            ================ input parameters ===========
            Electron beam energy [GeV]: {electron_energy_in_GeV}
            Electron current:           {ring_current}
            Period Length [m]:          {period_length}
            Number of Periods:          {number_of_periods}
            
            Horizontal K:               {K_horizontal}
            Vertical K:                 {K_vertical}
            ==============================================
            
            Electron beam gamma:                {gamma}
            Undulator Length [m]:               {undulator_length}
            Horizontal Peak Magnetic field [T]: {B_horizontal}
            Vertical Peak Magnetic field [T]:   {B_vertical}
            
            Total power radiated by the undulator [W]: {und_power}
            Power density at center of beam (if Kx=0) [W/mrad2]: {und_power_density}
            
            Resonances:
            
            Photon energy [eV]: 
                   for harmonic 1 : {resonance_energy}
                   for harmonic 3 : {resonance_energy3}
                   for harmonic 3 : {resonance_energy5}
                   Critical energy: {critical_energy}
            
            Central cone (RMS urad):
                   for harmonic 1 : {cc_1}
                   for harmonic 3 : {cc_3}
                   for harmonic 5 : {cc_5}
            
            First ring at (urad):
                   for harmonic 1 : {first_ring_1}
                   for harmonic 3 : {first_ring_3}
                   for harmonic 5 : {first_ring_5}
            
            Sizes and divergences of radiation :
                at 1st harmonic: sigma: {sigma_rad} um, sigma': {sigma_rad_prime} urad
                at 3rd harmonic: sigma: {sigma_rad3} um, sigma': {sigma_rad_prime3} urad
                at 5th harmonic: sigma: {sigma_rad5} um, sigma': {sigma_rad_prime5} urad
            
            Sizes and divergences of photon source (convolution) at resonance (1st harmonic): :
                Sx: {Sx} um
                Sy: {Sy} um,
                Sx': {Sxp} urad
                Sy': {Syp} urad
            
            Approximated coherent fraction at 1st harmonic: 
                Horizontal: {CF_h}  Vertical: {CF_v} 
                Coherent fraction 2D (HxV): {CF} 
            
            """

    def get_polarization_list(self):
        if self.ORIENTATION_LOGIC == 0:
            return self.get_polarization_list_shadow()
        else:
            return self.get_polarization_list_lab()

    def get_polarization_list_shadow(self):
        KY = self.KY
        KX = self.KX

        EL0_RELATIVE_TO_PREVIOUS = self.EL0_RELATIVE_TO_PREVIOUS
        EL1_RELATIVE_TO_PREVIOUS = self.EL1_RELATIVE_TO_PREVIOUS
        EL2_RELATIVE_TO_PREVIOUS = self.EL2_RELATIVE_TO_PREVIOUS
        EL3_RELATIVE_TO_PREVIOUS = self.EL3_RELATIVE_TO_PREVIOUS
        EL4_RELATIVE_TO_PREVIOUS = self.EL4_RELATIVE_TO_PREVIOUS
        EL5_RELATIVE_TO_PREVIOUS = self.EL5_RELATIVE_TO_PREVIOUS

        #
        #
        #
        SP = ['s', 'p']

        if KX != 0 and KY != 0:
            source_pol = 0
            txt = "Polarization at the source: f"
        else:
            if KX == 0:
                source_pol = 0  # s
            else:
                source_pol = 1  # p
            txt = "Polarization at the source: %s" % (SP[source_pol])

        txt += "\nNumber of optical elements: %d" % self.NELEMENTS
        RR = ['Left (90)', 'Right (270)', 'Up (0)', 'Down (180)']
        RELATIVE_TO_PREVIOUS = [
            RR[EL0_RELATIVE_TO_PREVIOUS],
            RR[EL1_RELATIVE_TO_PREVIOUS],
            RR[EL2_RELATIVE_TO_PREVIOUS],
            RR[EL3_RELATIVE_TO_PREVIOUS],
            RR[EL4_RELATIVE_TO_PREVIOUS],
            RR[EL5_RELATIVE_TO_PREVIOUS], ]

        # items = ['Left', 'Right', 'Up', 'Down'],
        FLAG_PERPENDICULAR_TO_PREVIOUS = [
            EL0_RELATIVE_TO_PREVIOUS < 2,
            EL1_RELATIVE_TO_PREVIOUS < 2,
            EL2_RELATIVE_TO_PREVIOUS < 2,
            EL3_RELATIVE_TO_PREVIOUS < 2,
            EL4_RELATIVE_TO_PREVIOUS < 2,
            EL5_RELATIVE_TO_PREVIOUS < 2, ]

        # s=0, p=1

        txt += "\nRELATIVE_TO_PREVIOUS: " + str(RELATIVE_TO_PREVIOUS[0:self.NELEMENTS])[1:-1]
        txt += "\nFLAG_PERPENDICULAR_TO_PREVIOUS: " + str(FLAG_PERPENDICULAR_TO_PREVIOUS[0:self.NELEMENTS])[1:-1]

        NUMBER_OF_INVERSIONS = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            if i == 0:
                if FLAG_PERPENDICULAR_TO_PREVIOUS[0]:
                    NUMBER_OF_INVERSIONS[0] += 1
            else:
                if FLAG_PERPENDICULAR_TO_PREVIOUS[i]:
                    NUMBER_OF_INVERSIONS[i] += 1
                NUMBER_OF_INVERSIONS[i] += NUMBER_OF_INVERSIONS[i - 1]

        txt += "\nNUMBER_OF_INVERSIONS: " + str(NUMBER_OF_INVERSIONS[0:self.NELEMENTS])[1:-1]

        NUMBER_OF_INVERSIONS_MODULO_2 = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            NUMBER_OF_INVERSIONS_MODULO_2[i] = numpy.mod(NUMBER_OF_INVERSIONS[i], 2)

        txt += "\nNUMBER_OF_INVERSIONS_MODULO_2: " + str(NUMBER_OF_INVERSIONS_MODULO_2[0:self.NELEMENTS])[1:-1]

        OUTPUT_LIST = []
        for i in range(6):
            OUTPUT_LIST.append(SP[numpy.mod(NUMBER_OF_INVERSIONS_MODULO_2[i] + source_pol, 2)])

        if (KX != 0 and KY != 0):
            OUTPUT_LIST = ['f'] * 6

        txt += "\nOUTPUT_LIST: " + str(OUTPUT_LIST[0:self.NELEMENTS])[1:-1]

        txt += "\n"

        return OUTPUT_LIST, NUMBER_OF_INVERSIONS_MODULO_2, txt

    def get_polarization_list_lab(self):
        KY = self.KY
        KX = self.KX

        EL0_RELATIVE_TO_PREVIOUS = self.EL0_RELATIVE_TO_PREVIOUS
        EL1_RELATIVE_TO_PREVIOUS = self.EL1_RELATIVE_TO_PREVIOUS
        EL2_RELATIVE_TO_PREVIOUS = self.EL2_RELATIVE_TO_PREVIOUS
        EL3_RELATIVE_TO_PREVIOUS = self.EL3_RELATIVE_TO_PREVIOUS
        EL4_RELATIVE_TO_PREVIOUS = self.EL4_RELATIVE_TO_PREVIOUS
        EL5_RELATIVE_TO_PREVIOUS = self.EL5_RELATIVE_TO_PREVIOUS

        #
        #
        #
        SP = ['s', 'p']


        if KX != 0 and KY != 0:
            source_pol = 0
            txt = "Polarization at the source: f"
        else:
            if KX == 0:
                source_pol = 0  # s
            else:
                source_pol = 1  # p
            txt = "Polarization at the source: %s" % (SP[source_pol])

        txt += "\nNumber of optical elements: %d" % self.NELEMENTS
        RR = ['Left (90)', 'Right (270)', 'Up (0)', 'Down (180)']
        RELATIVE_TO_PREVIOUS = [
            RR[EL0_RELATIVE_TO_PREVIOUS],
            RR[EL1_RELATIVE_TO_PREVIOUS],
            RR[EL2_RELATIVE_TO_PREVIOUS],
            RR[EL3_RELATIVE_TO_PREVIOUS],
            RR[EL4_RELATIVE_TO_PREVIOUS],
            RR[EL5_RELATIVE_TO_PREVIOUS], ]

        # items = ['Left', 'Right', 'Up', 'Down'],
        FLAG_PERPENDICULAR_TO_PREVIOUS = [
            EL0_RELATIVE_TO_PREVIOUS < 2,
            EL1_RELATIVE_TO_PREVIOUS < 2,
            EL2_RELATIVE_TO_PREVIOUS < 2,
            EL3_RELATIVE_TO_PREVIOUS < 2,
            EL4_RELATIVE_TO_PREVIOUS < 2,
            EL5_RELATIVE_TO_PREVIOUS < 2, ]

        # s=0, p=1

        txt += "\nORIENTATION: " + str(RELATIVE_TO_PREVIOUS[0:self.NELEMENTS])[1:-1]
        txt += "\nFLAG_PERPENDICULAR: " + str(FLAG_PERPENDICULAR_TO_PREVIOUS[0:self.NELEMENTS])[1:-1]

        NUMBER_OF_INVERSIONS = [
            int(FLAG_PERPENDICULAR_TO_PREVIOUS[0]),
            int(FLAG_PERPENDICULAR_TO_PREVIOUS[1]),
            int(FLAG_PERPENDICULAR_TO_PREVIOUS[2]),
            int(FLAG_PERPENDICULAR_TO_PREVIOUS[3]),
            int(FLAG_PERPENDICULAR_TO_PREVIOUS[4]),
            int(FLAG_PERPENDICULAR_TO_PREVIOUS[5]) ]

        txt += "\nNUMBER_OF_INVERSIONS: " + str(NUMBER_OF_INVERSIONS[0:self.NELEMENTS])[1:-1]

        NUMBER_OF_INVERSIONS_MODULO_2 = NUMBER_OF_INVERSIONS

        txt += "\nNUMBER_OF_INVERSIONS_MODULO_2: " + str(NUMBER_OF_INVERSIONS_MODULO_2[0:self.NELEMENTS])[1:-1]

        OUTPUT_LIST = []
        for i in range(6):
            OUTPUT_LIST.append(SP[numpy.mod(NUMBER_OF_INVERSIONS_MODULO_2[i] + source_pol, 2)] )

        if (KX != 0 and KY != 0):
            OUTPUT_LIST = ['f'] * 6

        txt += "\nOUTPUT_LIST: " + str(OUTPUT_LIST[0:self.NELEMENTS])[1:-1]

        txt += "\n"

        return OUTPUT_LIST, NUMBER_OF_INVERSIONS_MODULO_2, txt

    def help1(self):

        import os
        from orangecontrib.xoppy.util.text_window import TextWindow
        # from orangecontrib.xoppy.util.xoppy_util import locations

        home_doc = locations.home_doc()

        filename1 = os.path.join(home_doc, self.get_help_name() + '.txt')

        TextWindow(file=filename1,parent=self)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = OWsrcalc_idpower()
    w.DEBUG_RUN_URGENT = 1
    w.show()
    app.exec()
    w.saveSettings()


    # import Shadow
    # beam = Shadow.Beam()
    # beam.load("star_srcalc_000.01")
    # x, z, w = beam.getshcol([1,3,23])
    # for i in range(5):
    #     print(x[i], z[i], w[i])