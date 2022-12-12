import sys, os
import numpy
from PyQt5.QtWidgets import QApplication

import platform

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from xoppylib.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice as synedid
from xoppylib.xoppy_run_binaries import xoppy_calc_xtcap

class OWtcap(XoppyWidget):
    name = "Aperture Flux TC"
    id = "orange.widgets.datatcap"
    description = "On-axis Aperture Flux Undulator Tuning Curves"
    icon = "icons/xoppy_xtc.png"
    priority = 8
    category = ""
    keywords = ["xoppy", "tcap"]

    #25 variables (minus one: TITLE removed)
    ENERGY = Setting(6.0)
    CURRENT = Setting(200.0)
    ENERGY_SPREAD = Setting(0.00138)
    SIGX = Setting(0.0148)
    SIGY = Setting(0.0037)
    SIGX1 = Setting(0.0029)
    SIGY1 = Setting(0.0015)
    PERIOD = Setting(2.8)
    NP = Setting(84)
    EMIN = Setting(3217.0)
    EMAX = Setting(11975.0)
    N = Setting(50)
    DISTANCE = Setting(30.0)
    XPS = Setting(1.0)
    YPS = Setting(1.0)
    XPC = Setting(0.0)
    YPC = Setting(0.0)
    HARMONIC_FROM = Setting(1)
    HARMONIC_TO = Setting(7)
    HARMONIC_STEP = Setting(2)
    HRED = Setting(0)
    HELICAL = Setting(0)
    NEKS = Setting(100)
    METHOD = Setting(0)
    BSL = Setting(0)

    inputs = WidgetDecorator.syned_input_data()

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        self.IMAGE_WIDTH = 850

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        tab_1 = oasysgui.createTabPage(tabs_setting, self.name + " Input Parameters")
        tab_2 = oasysgui.createTabPage(tabs_setting, "Undulator Setting")

        box = oasysgui.widgetBox(tab_1, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-15)

        idx = -1
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ENERGY = oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_CURRENT = oasysgui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ENERGY_SPREAD = oasysgui.lineEdit(box1, self, "ENERGY_SPREAD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
      
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGX = oasysgui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGY = oasysgui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGX1 = oasysgui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGY1 = oasysgui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
  
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_PERIOD = oasysgui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_NP = oasysgui.lineEdit(box1, self, "NP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
       
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float,  orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 17
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        box = oasysgui.widgetBox(tab_2, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-15)

        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HARMONIC_FROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HARMONIC_TO",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HARMONIC_STEP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "HRED",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['No', 'Yes'],
                     valueType=int, orientation="horizontal", labelWidth=350)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 22
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "HELICAL",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Planar undulator', 'Helical undulator'],
                     valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NEKS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 24
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Infinite N +convolution (Dejus)','Infinite N +convolution (Dejus)','Infinite N +convolution(Walker)','Finite-N'],
                     valueType=int, orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1)
       
        #widget index 25
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "BSL",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['No', 'Yes'],
                     valueType=int, orientation="horizontal", labelWidth=350)
        self.show_at(self.unitFlags()[idx], box1)

    def unitLabels(self):
         return ['Electron energy (GeV)','Current (mA)','Energy Spread (dE/E)',
                 'Sigma X (mm)','Sigma Y (mm)',"Sigma X' (mrad)","Sigma Y' (mrad)",
                 'Period length (cm)','Number of periods',
                 'E1 minimum energy (eV)','E1 maximum energy (eV)','Number of energy-points',                 
                 'Distance to Aperture [m]', 'Aperture Width H [mm]', 'Aperture Height V [mm]',
                 'Aperture Center H [mm]', 'Aperture Center V [mm]',
                 'Minimum harmonic number','Maximum harmonic number','Harmonic step size','Apply Harmonic Reduction',
                 'Mode','Neks OR % Helicity','Method','Baseline Subraction']


    def unitFlags(self):
         return ['True' for i in range(26)]


    def get_help_name(self):
        return 'tcap'

    def check_fields(self):
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Electron Energy")
        self.CURRENT = congruence.checkStrictlyPositiveNumber(self.CURRENT, "Current")
        self.ENERGY_SPREAD = congruence.checkStrictlyPositiveNumber(self.ENERGY_SPREAD, "Energy Spread")
        self.SIGX  = congruence.checkPositiveNumber(self.SIGX , "Sigma X")
        self.SIGY  = congruence.checkPositiveNumber(self.SIGY , "Sigma Y")
        self.SIGX1 = congruence.checkPositiveNumber(self.SIGX1, "Sigma X'")
        self.SIGY1 = congruence.checkPositiveNumber(self.SIGY1, "Sigma Y'")
        self.PERIOD = congruence.checkStrictlyPositiveNumber(self.PERIOD, "Period length")
        self.NP = congruence.checkStrictlyPositiveNumber(self.NP, "Number of periods")
        self.EMIN = congruence.checkPositiveNumber(self.EMIN, "E1 minimum energy")
        self.EMAX = congruence.checkStrictlyPositiveNumber(self.EMAX, "E1 maximum energy")
        congruence.checkLessThan(self.EMIN, self.EMAX, "E1 minimum energy", "E1 maximum energy")
        self.N = congruence.checkStrictlyPositiveNumber(self.N, "Number of Energy Points")
        self.DISTANCE = congruence.checkPositiveNumber(self.DISTANCE, "Distance to slit")
        self.XPS = congruence.checkPositiveNumber(self.XPS, "Aperture Width H")
        self.YPS = congruence.checkPositiveNumber(self.YPS, "Aperture Height V")
        self.XPC = congruence.checkPositiveNumber(self.XPC, "Aperture Center H")
        self.YPC = congruence.checkPositiveNumber(self.YPC, "Aperture Center V")
        self.HARMONIC_FROM = congruence.checkStrictlyPositiveNumber(self.HARMONIC_FROM, "Minimum harmonic number")
        self.HARMONIC_TO = congruence.checkStrictlyPositiveNumber(self.HARMONIC_TO, "Maximum harmonic number")
        congruence.checkLessThan(self.HARMONIC_FROM, self.HARMONIC_TO, "Minimum harmonic number", "Maximum harmonic number")
        self.HARMONIC_STEP = congruence.checkStrictlyPositiveNumber(self.HARMONIC_STEP, "Harmonic step size")
        self.NEKS = congruence.checkStrictlyPositiveNumber(self.NEKS, "Neks OR % Helicity")

    def do_xoppy_calculation(self):
        data, harmonics_data = xoppy_calc_xtcap(
            ENERGY        = self.ENERGY       ,
            CURRENT       = self.CURRENT      ,
            ENERGY_SPREAD = self.ENERGY_SPREAD,
            SIGX          = self.SIGX         ,
            SIGY          = self.SIGY         ,
            SIGX1         = self.SIGX1        ,
            SIGY1         = self.SIGY1        ,
            PERIOD        = self.PERIOD       ,
            NP            = self.NP           ,
            EMIN          = self.EMIN         ,
            EMAX          = self.EMAX         ,
            N             = self.N            ,
            DISTANCE      = self.DISTANCE     ,
            XPS           = self.XPS          ,
            YPS           = self.YPS          ,
            XPC           = self.XPC          ,
            YPC           = self.YPC          ,
            HARMONIC_FROM = self.HARMONIC_FROM,
            HARMONIC_TO   = self.HARMONIC_TO  ,
            HARMONIC_STEP = self.HARMONIC_STEP,
            HRED          = self.HRED         ,
            HELICAL       = self.HELICAL      ,
            NEKS          = self.NEKS         ,
            METHOD        = self.METHOD       ,
            BSL           = self.BSL          ,
        )

        dict_parameters = {
            "ENERGY"        : self.ENERGY       ,
            "CURRENT"       : self.CURRENT      ,
            "ENERGY_SPREAD" : self.ENERGY_SPREAD,
            "SIGX"          : self.SIGX         ,
            "SIGY"          : self.SIGY         ,
            "SIGX1"         : self.SIGX1        ,
            "SIGY1"         : self.SIGY1        ,
            "PERIOD"        : self.PERIOD       ,
            "NP"            : self.NP           ,
            "EMIN"          : self.EMIN         ,
            "EMAX"          : self.EMAX         ,
            "N"             : self.N            ,
            "DISTANCE"      : self.DISTANCE     ,
            "XPS"           : self.XPS          ,
            "YPS"           : self.YPS          ,
            "XPC"           : self.XPC          ,
            "YPC"           : self.YPC          ,
            "HARMONIC_FROM" : self.HARMONIC_FROM,
            "HARMONIC_TO"   : self.HARMONIC_TO  ,
            "HARMONIC_STEP" : self.HARMONIC_STEP,
            "HRED"          : self.HRED         ,
            "HELICAL"       : self.HELICAL      ,
            "NEKS"          : self.NEKS         ,
            "METHOD"        : self.METHOD       ,
            "BSL"           : self.BSL          ,
        }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)

        return data, harmonics_data, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:XTCAP)
#
from xoppylib.xoppy_run_binaries import xoppy_calc_xtcap

data, harmonics_data =  xoppy_calc_xtcap(
            ENERGY        = {ENERGY},
            CURRENT       = {CURRENT},
            ENERGY_SPREAD = {ENERGY_SPREAD},
            SIGX          = {SIGX},
            SIGY          = {SIGY},
            SIGX1         = {SIGX1},
            SIGY1         = {SIGY1},
            PERIOD        = {PERIOD},
            NP            = {NP},
            EMIN          = {EMIN},
            EMAX          = {EMAX},
            N             = {N},
            DISTANCE      = {DISTANCE},
            XPS           = {XPS},
            YPS           = {YPS},
            XPC           = {XPC},
            YPC           = {YPC},
            HARMONIC_FROM = {HARMONIC_FROM},
            HARMONIC_TO   = {HARMONIC_TO},
            HARMONIC_STEP = {HARMONIC_STEP},
            HRED          = {HRED},
            HELICAL       = {HELICAL},
            NEKS          = {NEKS},
            METHOD        = {METHOD},
            BSL           = {BSL},
        )

#
# example plot
#
import numpy
from srxraylib.plot.gol import plot
# 

# 
print("Number of harmonics calculated: ",len(harmonics_data))

plot((harmonics_data[0][1])[:,0],
     (harmonics_data[0][1])[:,1],
     title="harmonic number = %d" % (harmonics_data[0][0]), xtitle="Energy[eV]", ytitle="Flux" )

#
# end script
#
"""
    def extract_data_from_xoppy_output(self, calculation_output):
        data, harmonics_data, script = calculation_output
        # send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        try:
            calculated_data.add_content("xoppy_data", data)
            calculated_data.add_content("xoppy_data_harmonics", harmonics_data)
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", 1)
        except:
            pass

        try:
            calculated_data.add_content("labels", ["Energy(eV)", "Flux(ph/s/0.1%bw)", "FWHM(eV)", "Ky",
                                                   "Ptot(W)", "Pd(W/mm^2)", "IntP(W)"])

        except:
            pass
        try:
            calculated_data.add_content("info", txtlist)
        except:
            pass

        return calculated_data


    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:
                self.view_type_combo.setEnabled(False)


                xoppy_data_harmonics = calculated_data.get_content("xoppy_data_harmonics")

                titles = self.getTitles()
                xtitles = self.getXTitles()
                ytitles = self.getYTitles()

                progress_bar_step = (100-progressBarValue)/len(titles)

                for index in range(0, len(titles)):
                    x_index, y_index = self.getVariablesToPlot()[index]
                    log_x, log_y = self.getLogPlot()[index]

                    if not self.plot_canvas[index] is None:
                        self.plot_canvas[index].clear()

                    try:
                        for h_index in range(0, len(xoppy_data_harmonics)):

                            self.plot_histo(xoppy_data_harmonics[h_index][1][:, x_index],
                                            xoppy_data_harmonics[h_index][1][:, y_index],
                                            progressBarValue + ((index+1)*progress_bar_step),
                                            tabs_canvas_index=index,
                                            plot_canvas_index=index,
                                            title=titles[index],
                                            xtitle=xtitles[index],
                                            ytitle=ytitles[index],
                                            log_x=log_x,
                                            log_y=log_y,
                                            harmonic=xoppy_data_harmonics[h_index][0],
                                            control=True)

                        self.plot_canvas[index].addCurve(numpy.zeros(1),
                                                         numpy.array([max(xoppy_data_harmonics[h_index][1][:, y_index])]),
                                                         "Click on curve to highlight it",
                                                         xlabel=xtitles[index], ylabel=ytitles[index],
                                                         symbol='', color='white')

                        self.plot_canvas[index].setActiveCurve("Click on curve to highlight it")
                        self.plot_canvas[index].getLegendsDockWidget().setFixedHeight(150)
                        self.plot_canvas[index].getLegendsDockWidget().setVisible(True)

                        self.tabs.setCurrentIndex(index)
                    except Exception as e:
                        self.view_type_combo.setEnabled(True)

                        raise Exception("Data not plottable: bad content\n" + str(e))


                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")

            try:
                self.tabs.setCurrentIndex(0)
            except:
                pass

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="",
                   log_x=False, log_y=False, harmonic=1, color='blue', control=True):
        h_title = "Harmonic " + str(harmonic)

        hex_r = hex(min(255, 128 + harmonic*10))[2:].upper()
        hex_g = hex(min(255, 20 + harmonic*15))[2:].upper()
        hex_b = hex(min(255, harmonic*10))[2:].upper()
        if len(hex_r) == 1: hex_r = "0" + hex_r
        if len(hex_g) == 1: hex_g = "0" + hex_g
        if len(hex_b) == 1: hex_b = "0" + hex_b

        super().plot_histo(x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, h_title, xtitle, ytitle,
                           log_x, log_y, color="#" + hex_r + hex_g + hex_b, replace=False, control=control)

        self.plot_canvas[plot_canvas_index].setGraphTitle(title)
        self.plot_canvas[plot_canvas_index].setDefaultPlotLines(True)


    def get_data_exchange_widget_name(self):
        return "XTCAP"

    def getTitles(self):
        return ["Flux peak","Ky","Total Power","Power density peak","Integrated Power on aperture"]

    def getXTitles(self):
        return ["Energy (eV)","Energy (eV)","Energy (eV)","Energy (eV)","Energy (eV)"]

    def getYTitles(self):
        return ["Flux (ph/s/0.1%bw)","Ky","Total Power (W)","Power density (W/mm^2)","Integrated Power on Aperture (W)"]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 3), (0, 4), (0, 5), (0, 6)]

    def getLogPlot(self):
        return[(False, True), (False, False), (False, False), (False, False),(False, False)]

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data.get_light_source() is None and isinstance(data.get_light_source().get_magnetic_structure(), synedid):
                light_source = data.get_light_source()

                self.ENERGY = light_source.get_electron_beam().energy()
                self.ENERGY_SPREAD = light_source.get_electron_beam()._energy_spread
                self.CURRENT = 1000.0 * light_source.get_electron_beam().current()

                x, xp, y, yp = light_source.get_electron_beam().get_sigmas_all()

                self.SIGX = 1e3 * x
                self.SIGY = 1e3 * y
                self.SIGX1 = 1e3 * xp
                self.SIGY1 = 1e3 * yp
                self.PERIOD = 100.0 * light_source._magnetic_structure._period_length
                self.NP = light_source._magnetic_structure._number_of_periods

                self.EMIN = light_source.get_magnetic_structure().resonance_energy(gamma=light_source.get_electron_beam().gamma())
                self.EMAX = 5 * self.EMIN

                self.set_enabled(False)

            else:
                self.set_enabled(True)
                # raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)
            # raise ValueError("Syned data not correct")



    def set_enabled(self,value):
        if value == True:
                self.id_ENERGY.setEnabled(True)
                self.id_ENERGY_SPREAD.setEnabled(True)
                self.id_SIGX.setEnabled(True)
                self.id_SIGX1.setEnabled(True)
                self.id_SIGY.setEnabled(True)
                self.id_SIGY1.setEnabled(True)
                self.id_CURRENT.setEnabled(True)
                self.id_PERIOD.setEnabled(True)
                self.id_NP.setEnabled(True)
        else:
                self.id_ENERGY.setEnabled(False)
                self.id_ENERGY_SPREAD.setEnabled(False)
                self.id_SIGX.setEnabled(False)
                self.id_SIGX1.setEnabled(False)
                self.id_SIGY.setEnabled(False)
                self.id_SIGY1.setEnabled(False)
                self.id_CURRENT.setEnabled(False)
                self.id_PERIOD.setEnabled(False)
                self.id_NP.setEnabled(False)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWtcap()
    w.show()
    app.exec()
    w.saveSettings()
