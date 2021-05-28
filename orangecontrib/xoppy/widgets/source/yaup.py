import sys,os
import numpy
import platform
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice as synedid

import os
from orangecontrib.xoppy.util.text_window import TextWindow

class OWyaup(XoppyWidget):
    name = "yaup"
    id = "orange.widgets.datayaup"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_yaup.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "yaup"]

    # want_main_area = False

    TITLE = Setting("YAUP EXAMPLE (ESRF BL-8)")
    PERIOD = Setting(4.0)
    NPER = Setting(42)
    NPTS = Setting(40)
    EMIN = Setting(3000.0)
    EMAX = Setting(30000.0)
    NENERGY = Setting(100)
    ENERGY = Setting(6.039999961853027)
    CUR = Setting(0.100000001490116)
    SIGX = Setting(0.425999999046326)
    SIGY = Setting(0.08500000089407)
    SIGX1 = Setting(0.017000000923872)
    SIGY1 = Setting(0.008500000461936)
    D = Setting(30.0)
    XPC = Setting(0.0)
    YPC = Setting(0.0)
    XPS = Setting(2.0)
    YPS = Setting(2.0)
    NXP = Setting(0)
    NYP = Setting(0)
    MODE = Setting(4)
    NSIG = Setting(2)
    TRAJECTORY = Setting("new+keep")
    XSYM = Setting("yes")
    HANNING = Setting(0)
    BFILE = Setting("undul.bf")
    TFILE = Setting("undul.traj")

    # B field

    BFIELD_FLAG = Setting(1)

    BFIELD_ASCIIFILE = Setting("")

    PERIOD_BFIELD = Setting(4.0)
    NPER_BFIELD = Setting(42)
    NPTS_BFIELD = Setting(40)

    IMAGNET = Setting(0)
    ITYPE = Setting(0)
    K = Setting(1.379999995231628)
    GAP = Setting(2.0)
    GAPTAP = Setting(10.0)
    FILE = Setting("undul.bf")

    I2TYPE = Setting(0)
    A1 = Setting(0.5)
    A2 = Setting(1.0)

    inputs = WidgetDecorator.syned_input_data()


    def build_gui(self):

        self.IMAGE_WIDTH = 850

        # box = oasysgui.widgetBox(self.controlArea, "Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        ##########################
        self.controls_tabs = oasysgui.tabWidget(self.controlArea)
        box = oasysgui.createTabPage(self.controls_tabs, "Input Parameters")
        ##########################


        idx = -1

        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CUR",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "D",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NXP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NYP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MODE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NSIG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TRAJECTORY",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XSYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HANNING",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BFILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 26 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TFILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 


        ##########################
        box = oasysgui.createTabPage(self.controls_tabs, "B field")
        ##########################

        # widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "BFIELD_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['from ASCII file', 'from BFIELD preprocessor', 'linear B field'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)


        # widget index XX
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "BFIELD_ASCIIFILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)


        # widget index 0
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "PERIOD_BFIELD",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 1
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "NPER_BFIELD",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=int)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 2
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "NPTS_BFIELD",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=int)
        self.show_at(self.unitFlags()[idx], box1)



        # widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "IMAGNET",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['Nd-Fe-B', 'Sm-Co'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "ITYPE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['planar undulator', 'tapered undulator'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "GAP",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "GAPTAP",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)

        # linear B field
        # NPTS: yaupstr.npts, $
        # ITYPE: ['0', 'Magnetic field B [Tesla]', 'Deflection parameter K'], $
        # a1: 0.5, a2: 1.0, FILE: yaupstr.bfile}

        # widget index XX
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "I2TYPE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['Magnetic field B [Tesla]', 'Deflection parameter K'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "A1",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "A2",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)



        gui.rubber(self.controlArea)

    def unitLabels(self):
         # return ['Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title']

        return [
            # 'TITLE', 'PERIOD', 'NPER', 'NPTS',
            #     'EMIN', 'EMAX', 'NENERGY',
            #     'ENERGY', 'CUR',
            #     'SIGX', 'SIGY', 'SIGX1', 'SIGY1',
            #     'D', 'XPC', 'YPC', 'XPS', 'YPS', 'NXP', 'NYP',
            #     'MODE', 'NSIG', 'TRAJECTORY', 'XSYM', 'HANNING', 'BFILE', 'TFILE',
            ' Title:  ',
            'PERIOD - magnet period (cm)',
            'NPER - number of periods',
            'NPTS - number of point/period',
            'EMIN - minimum energy (eV)',
            'EMAX - maximum energy (eV)',
            'NE - number of energy points',
            'ENERGY - e energy (GeV)',
            'CUR - e current (A)',
            'SIGX - H rms e beam (mm)',
            'SIGY - V rms e beam (mm)',
            'SIGX1 - rms H e div (mrad)',
            'SIGY1 - rms V e div (mrad)',
            'D - dist und-observator (m)',
            'XPC - H obs position (mm)',
            'YPC - V obs position (mm)',
            'XPS - H acceptance (mm\mrad)',
            'YPS - V acceptance (mm\mrad)',
            'NXP - no acceptance pts (H)',
            'NYP - no acceptance pts (V)',
            'MODE - (see help)',
            'NSIG - (see help)',
            'TRAJECTORY - calculation flag',
            'XSYM - horizontal symmetry',
            'HANNING - (see help)',
            'BFILE - B filename',
            'TFILE - Traj filename',
            'BFIELD_FLAG',
            'BFIELD_ASCIIFILE - Filename: ',
         # 'PERIOD', 'NPER', 'NPTS',
            'PERIOD_BFIELD - magnet period (cm)',
            'N_BFIELD - number of periods'      ,
            'NPTS_BFIELD - nb of point / period',
        # 'IMAGNET', 'ITYPE', 'K', 'GAP', 'GAPTAP', 'FILE',
            'IMAGNET - Undulator Magnet: '         ,
            'ITYPE - Undulator type: '           ,
            'K - K field parameter'      ,
            'GAP - initial gap (cm)'     ,
            'GAPTAP - Gap taper (%)'     ,
            'FILE - Output file name'    ,
         #    aa       =  {PERIOD: yaupstr.period, NPER: yaupstr.nper, $
         # NPTS: yaupstr.npts, $
         # ITYPE: ['0', 'Magnetic field B [Tesla]', 'Deflection parameter K'], $
         # a1: 0.5, a2: 1.0, FILE: yaupstr.bfile}
         #
         # titles = ['PERIOD - magnet period (cm)', 'N - number of periods'  $
         # , 'NPTS - nb of point / period', 'Input parameter: '                 $
         # , 'From:', 'To:', 'FILE - Output (binary) file name'
            'Input parameter: ',
            'From:',
            'To:'
         ]

    def unitFlags(self):
         return ['True','True','True','True',
                 'True','True','True',
                 'True','True',
                 'True','True','True','True',
                 'True','True','True','True','True','True','True',
                 'True','True','True','True','True','True','True',
                 'True',
                 'self.BFIELD_FLAG == 0',
                 'self.BFIELD_FLAG > 0','self.BFIELD_FLAG > 0','self.BFIELD_FLAG > 0',
                 'self.BFIELD_FLAG == 1','self.BFIELD_FLAG == 1','self.BFIELD_FLAG == 1 and self.ITYPE == 0','self.BFIELD_FLAG == 1 and self.ITYPE == 1','self.BFIELD_FLAG == 1 and self.ITYPE == 1','self.BFIELD_FLAG > 0',
                 'self.BFIELD_FLAG == 2','self.BFIELD_FLAG == 2','self.BFIELD_FLAG == 2',]


    #def unitNames(self):
    #     return ['TITLE','PERIOD','NPER','NPTS','EMIN','EMAX','NENERGY','ENERGY','CUR','SIGX','SIGY','SIGX1','SIGY1','D','XPC','YPC','XPS','YPS','NXP','NYP','MODE','NSIG','TRAJECTORY','XSYM','HANNING','BFILE','TFILE']

    def check_fields(self):
        pass
        # self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Electron Energy")
        # self.CURRENT = congruence.checkStrictlyPositiveNumber(self.CURRENT, "Current")
        # self.ENERGY_SPREAD = congruence.checkStrictlyPositiveNumber(self.ENERGY_SPREAD, "Energy Spread")
        # self.SIGX  = congruence.checkPositiveNumber(self.SIGX , "Sigma X")
        # self.SIGY  = congruence.checkPositiveNumber(self.SIGY , "Sigma Y")
        # self.SIGX1 = congruence.checkPositiveNumber(self.SIGX1, "Sigma X'")
        # self.SIGY1 = congruence.checkPositiveNumber(self.SIGY1, "Sigma Y'")
        # self.PERIOD = congruence.checkStrictlyPositiveNumber(self.PERIOD, "Period length")
        # self.NP = congruence.checkStrictlyPositiveNumber(self.NP, "Number of periods")
        # self.EMIN = congruence.checkPositiveNumber(self.EMIN, "E1 minimum energy")
        # self.EMAX = congruence.checkStrictlyPositiveNumber(self.EMAX, "E1 maximum energy")
        # congruence.checkLessThan(self.EMIN, self.EMAX, "E1 minimum energy", "E1 maximum energy")
        # self.N = congruence.checkStrictlyPositiveNumber(self.N, "Number of Energy Points")
        # self.HARMONIC_FROM = congruence.checkStrictlyPositiveNumber(self.HARMONIC_FROM, "Minimum harmonic number")
        # self.HARMONIC_TO = congruence.checkStrictlyPositiveNumber(self.HARMONIC_TO, "Maximum harmonic number")
        # congruence.checkLessThan(self.HARMONIC_FROM, self.HARMONIC_TO, "Minimum harmonic number", "Maximum harmonic number")
        # self.HARMONIC_STEP = congruence.checkStrictlyPositiveNumber(self.HARMONIC_STEP, "Harmonic step size")
        # self.NEKS  = congruence.checkPositiveNumber(self.NEKS , "Neks OR % Helicity")

    def do_xoppy_calculation(self):
        return self.xoppy_calc_yaup()

    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def plot_results(self, calculated_data, progressBarValue=80):
        pass
        # if not self.view_type == 0:
        #     if not calculated_data is None:
        #         self.view_type_combo.setEnabled(False)
        #
        #
        #         xoppy_data_harmonics = calculated_data.get_content("xoppy_data_harmonics")
        #
        #         titles = self.getTitles()
        #         xtitles = self.getXTitles()
        #         ytitles = self.getYTitles()
        #
        #         progress_bar_step = (100-progressBarValue)/len(titles)
        #
        #         for index in range(0, len(titles)):
        #             x_index, y_index = self.getVariablesToPlot()[index]
        #             log_x, log_y = self.getLogPlot()[index]
        #
        #             if not self.plot_canvas[index] is None:
        #                 self.plot_canvas[index].clear()
        #
        #             try:
        #                 for h_index in range(0, len(xoppy_data_harmonics)):
        #
        #                     self.plot_histo(xoppy_data_harmonics[h_index][1][:, x_index],
        #                                     xoppy_data_harmonics[h_index][1][:, y_index],
        #                                     progressBarValue + ((index+1)*progress_bar_step),
        #                                     tabs_canvas_index=index,
        #                                     plot_canvas_index=index,
        #                                     title=titles[index],
        #                                     xtitle=xtitles[index],
        #                                     ytitle=ytitles[index],
        #                                     log_x=log_x,
        #                                     log_y=log_y,
        #                                     harmonic=xoppy_data_harmonics[h_index][0],
        #                                     control=True)
        #
        #                 self.plot_canvas[index].addCurve(numpy.zeros(1),
        #                                                  numpy.array([max(xoppy_data_harmonics[h_index][1][:, y_index])]),
        #                                                  "Click on curve to highlight it",
        #                                                  xlabel=xtitles[index], ylabel=ytitles[index],
        #                                                  symbol='', color='white')
        #
        #                 self.plot_canvas[index].setActiveCurve("Click on curve to highlight it")
        #                 self.plot_canvas[index].getLegendsDockWidget().setFixedHeight(150)
        #                 self.plot_canvas[index].getLegendsDockWidget().setVisible(True)
        #
        #                 self.tabs.setCurrentIndex(index)
        #             except Exception as e:
        #                 self.view_type_combo.setEnabled(True)
        #
        #                 raise Exception("Data not plottable: bad content\n" + str(e))
        #
        #
        #         self.view_type_combo.setEnabled(True)
        #     else:
        #         raise Exception("Empty Data")

    # def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="",
    #                log_x=False, log_y=False, harmonic=1, color='blue', control=True):
    #     h_title = "Harmonic " + str(harmonic)
    #
    #     hex_r = hex(min(255, 128 + harmonic*10))[2:].upper()
    #     hex_g = hex(min(255, 20 + harmonic*15))[2:].upper()
    #     hex_b = hex(min(255, harmonic*10))[2:].upper()
    #     if len(hex_r) == 1: hex_r = "0" + hex_r
    #     if len(hex_g) == 1: hex_g = "0" + hex_g
    #     if len(hex_b) == 1: hex_b = "0" + hex_b
    #
    #     super().plot_histo(x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, h_title, xtitle, ytitle,
    #                        log_x, log_y, color="#" + hex_r + hex_g + hex_b, replace=False, control=control)
    #
    #     self.plot_canvas[plot_canvas_index].setGraphTitle(title)
    #     self.plot_canvas[plot_canvas_index].setDefaultPlotLines(True)
    #     self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)

    def get_data_exchange_widget_name(self):
        return "YAUP"

    def getTitles(self):
        return ["B field", "Trajectory", "Flux", "Spectral power","Cumulated spectral power"]

    def getXTitles(self):
        return ["s []", "s []", "Energy (eV)", "Energy (eV)", "Energy (eV)"]

    def getYTitles(self):
        return ["B [T]", "x []", "Flux (photons/s/0.1%bw)","Spectral power [W/eV]","Cumulated power W",]


    def getVariablesToPlot(self):
        return [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]

    def getLogPlot(self):
        return[(False, False), (False, False), (False, False), (False, False), (False, False)]

    def xoppy_calc_yaup(self):

        for file in ["bfield.inp","bfield.out","yaup.inp","yaup.out", "u2txt.inp"]:
            try:
                os.remove(os.path.join(locations.home_bin_run(),file))
            except:
                pass

        if self.BFIELD_FLAG == 0:
            pass
        elif self.BFIELD_FLAG == 1:
            with open("bfield.inp", "wt") as f:
                f.write("%g\n" % (self.PERIOD_BFIELD))
                f.write("%d\n" % (self.NPER_BFIELD))
                f.write("%d\n" % (self.NPTS_BFIELD))
                f.write("%d\n" % (1 + self.IMAGNET))
                if self.ITYPE == 0:
                    f.write("%g\n" % (self.K))
                elif self.ITYPE == 1:
                    f.write("%g\n" % (self.GAP))
                    f.write("%g\n" % (self.GAPTAP))
                f.write("%s\n" % (self.FILE))

            if platform.system() == "Windows":
                command = "\"" + os.path.join(locations.home_bin(),'bfield.exe') + "\""
            else:
                command = "'" + os.path.join(locations.home_bin(), 'bfield') + "'"

            command += " < bfield.inp > bfield.out"

            print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
            print("\n--------------------------------------------------------\n")
            os.system(command)
            print("Output file: %s"%("bfield.out"))
            print("\n--------------------------------------------------------\n")

            with open("u2txt.inp", "wt") as f:
                f.write("1\n")
                f.write("%s\n" % (self.FILE))
                f.write("bfield.dat\n")

            if platform.system() == "Windows":
                command = "\"" + os.path.join(locations.home_bin(),'u2txt.exe') + "\""
            else:
                command = "'" + os.path.join(locations.home_bin(), 'u2txt') + "'"

            command += " < u2txt.inp"

            print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
            print("\n--------------------------------------------------------\n")
            os.system(command)
            print("Output file should be: %s"%("bfield.dat"))
            print("\n--------------------------------------------------------\n")


        elif self.BFIELD_FLAG == 2:
            pass


        with open("yaup.inp", "wt") as f:
            f.write("TS called from xoppy\n")



        # if platform.system() == "Windows":
        #     command = "\"" + os.path.join(locations.home_bin(),'tc.exe') + "\""
        # else:
        #     command = "'" + os.path.join(locations.home_bin(), 'tc') + "'"
        #
        #
        # print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        # print("\n--------------------------------------------------------\n")
        # os.system(command)
        # print("Output file: %s"%("tc.out"))
        # print("\n--------------------------------------------------------\n")

        # #
        # # parse result files to exchange object
        # #
        #
        #
        # with open("tc.out","r") as f:
        #     lines = f.readlines()
        #
        # # print output file
        # # for line in lines:
        # #     print(line, end="")
        #
        #
        # # remove returns
        # lines = [line[:-1] for line in lines]
        # harmonics_data = []
        #
        # # separate numerical data from text
        # floatlist = []
        # harmoniclist = []
        # txtlist = []
        # for line in lines:
        #     try:
        #         tmp = line.strip()
        #
        #         if tmp.startswith("Harmonic"):
        #             harmonic_number = int(tmp.split("Harmonic")[1].strip())
        #
        #             if harmonic_number != self.HARMONIC_FROM:
        #                 harmonics_data[-1][1] = harmoniclist
        #                 harmoniclist = []
        #
        #             harmonics_data.append([harmonic_number, None])
        #
        #         tmp = float(line.strip()[0])
        #
        #         floatlist.append(line)
        #         harmoniclist.append(line)
        #     except:
        #         txtlist.append(line)
        #
        # harmonics_data[-1][1] = harmoniclist
        #
        # data = numpy.loadtxt(floatlist)
        #
        # for index in range(0, len(harmonics_data)):
        #     # print (harmonics_data[index][0], harmonics_data[index][1])
        #     harmonics_data[index][1] = numpy.loadtxt(harmonics_data[index][1])
        #
        # #send exchange
        # calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        #
        # try:
        #     calculated_data.add_content("xoppy_data", data)
        #     calculated_data.add_content("xoppy_data_harmonics", harmonics_data)
        #     calculated_data.add_content("plot_x_col", 1)
        #     calculated_data.add_content("plot_y_col", 2)
        # except:
        #     pass
        # try:
        #     calculated_data.add_content("labels",["Energy (eV) without emittance", "Energy (eV) with emittance",
        #                               "Brilliance (ph/s/mrad^2/mm^2/0.1%bw)","Ky","Total Power (W)","Power density (W/mr^2)"])
        # except:
        #     pass
        # try:
        #     calculated_data.add_content("info",txtlist)
        # except:
        #     pass

        calculated_data = None
        return calculated_data

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data.get_light_source().get_magnetic_structure(), synedid):
                light_source = data.get_light_source()

                self.ENERGY = light_source.get_electron_beam().energy()
                self.ENERGY_SPREAD = light_source.get_electron_beam()._energy_spread
                self.CURRENT = 1000.0 * light_source._electron_beam.current()

                x, xp, y, yp = light_source.get_electron_beam().get_sigmas_all()

                self.SIGX = 1e3 * x
                self.SIGY = 1e3 * y
                self.SIGX1 = 1e3 * xp
                self.SIGY1 = 1e3 * yp
                self.PERIOD = 100.0 * light_source.get_magnetic_structure().period_length()
                self.NP = light_source.get_magnetic_structure().number_of_periods()

                self.EMIN = light_source.get_magnetic_structure().resonance_energy(gamma=light_source.get_electron_beam().gamma())
                self.EMAX = 5 * self.EMIN

                self.set_enabled(False)

            else:
                self.set_enabled(True)
                # raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)
            # raise ValueError("Syned data not correct")






    #
    # def receive_syned_data(self, data):
    #
    #     if isinstance(data, synedb.Beamline):
    #         if not data._light_source is None and isinstance(data.get_light_source().get_magnetic_structure(), synedid):
    #             light_source = data.get_light_source()
    #
    #             self.ENERGY = light_source.get_electron_beam().energy()
    #             self.ENERGY_SPREAD = light_source.get_electron_beam()._energy_spread
    #             self.CURRENT = 1000.0 * light_source._electron_beam.current()
    #
    #             x, xp, y, yp = light_source.get_electron_beam().get_sigmas_all()
    #
    #             self.SIGX = 1e3 * x
    #             self.SIGY = 1e3 * y
    #             self.SIGX1 = 1e3 * xp
    #             self.SIGY1 = 1e3 * yp
    #             self.PERIOD = 100.0 * light_source.get_magnetic_structure().period_length()
    #             self.NP = light_source.get_magnetic_structure().number_of_periods()
    #
    #             self.EMIN = light_source.get_magnetic_structure().resonance_energy(gamma=light_source.get_electron_beam().gamma())
    #             self.EMAX = 5 * self.EMIN
    #
    #             self.set_enabled(False)
    #
    #         else:
    #             self.set_enabled(True)
    #             # raise ValueError("Syned data not correct")
    #     else:
    #         self.set_enabled(True)
    #         # raise ValueError("Syned data not correct")
    #
    #
    # def compute(self):
    #     pass
    #     # fileName = xoppy_calc_yaup(TITLE=self.TITLE,PERIOD=self.PERIOD,NPER=self.NPER,NPTS=self.NPTS,EMIN=self.EMIN,EMAX=self.EMAX,NENERGY=self.NENERGY,ENERGY=self.ENERGY,CUR=self.CUR,SIGX=self.SIGX,SIGY=self.SIGY,SIGX1=self.SIGX1,SIGY1=self.SIGY1,D=self.D,XPC=self.XPC,YPC=self.YPC,XPS=self.XPS,YPS=self.YPS,NXP=self.NXP,NYP=self.NYP,MODE=self.MODE,NSIG=self.NSIG,TRAJECTORY=self.TRAJECTORY,XSYM=self.XSYM,HANNING=self.HANNING,BFILE=self.BFILE,TFILE=self.TFILE)
    #     # #send specfile
    #     #
    #     # if fileName == None:
    #     #     print("Nothing to send")
    #     # else:
    #     #     self.send("xoppy_specfile",fileName)
    #     #     sf = specfile.Specfile(fileName)
    #     #     if sf.scanno() == 1:
    #     #         #load spec file with one scan, # is comment
    #     #         print("Loading file:  ",fileName)
    #     #         out = np.loadtxt(fileName)
    #     #         print("data shape: ",out.shape)
    #     #         #get labels
    #     #         txt = open(fileName).readlines()
    #     #         tmp = [ line.find("#L") for line in txt]
    #     #         itmp = np.where(np.array(tmp) != (-1))
    #     #         labels = txt[itmp[0]].replace("#L ","").split("  ")
    #     #         print("data labels: ",labels)
    #     #         self.send("xoppy_data",out)
    #     #     else:
    #     #         print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return


    def get_help_name(self):
        return 'yaup'

    def help1(self):

        home_doc = locations.home_doc()

        filename1 = os.path.join(home_doc, self.get_help_name() + '.txt')

        TextWindow(file=filename1,parent=self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWyaup()
    w.show()
    app.exec()
    w.saveSettings()
