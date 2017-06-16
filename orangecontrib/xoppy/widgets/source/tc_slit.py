import sys
import numpy
from collections import OrderedDict
import scipy.constants as codata

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util import srundplug

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

class OWtc_slit(XoppyWidget):
    name = "TC-SLIT"
    id = "orange.widgets.data_tc_slit"
    description = "Undulator Tuning Curves (Flux on a slit)"
    icon = "icons/xoppy_xtc.png"
    priority = 8
    category = ""
    keywords = ["xoppy", "tc_slit"]

    USEEMITTANCES=Setting(1)
    ELECTRONENERGY = Setting(6.037)
    ELECTRONENERGYSPREAD = Setting(0.001)
    ELECTRONCURRENT = Setting(0.2)
    ELECTRONBEAMSIZEH = Setting(4.99e-05)
    ELECTRONBEAMSIZEV = Setting(3.45e-06)
    ELECTRONBEAMDIVERGENCEH = Setting(0.000107)
    ELECTRONBEAMDIVERGENCEV = Setting(1.16e-06)
    PERIODID = Setting(0.042)
    NPERIODS = Setting(38)
    DISTANCE = Setting(26.0)
    GAPH = Setting(0.00258)
    GAPV = Setting(0.00195)
    KMIN = Setting(0.01)
    KMAX = Setting(2.56)
    KPOINTS = Setting(10)
    HMAX = Setting(1)
    METHOD = Setting(2)

    inputs = WidgetDecorator.syned_input_data()

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1
        #
        #
        #

        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "USEEMITTANCES",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)




        #widget index 0
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONENERGY = oasysgui.lineEdit(box1, self, "ELECTRONENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 1
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONENERGYSPREAD = oasysgui.lineEdit(box1, self, "ELECTRONENERGYSPREAD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 2
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONCURRENT = oasysgui.lineEdit(box1, self, "ELECTRONCURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMSIZEH = oasysgui.lineEdit(box1, self, "ELECTRONBEAMSIZEH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMSIZEV = oasysgui.lineEdit(box1, self, "ELECTRONBEAMSIZEV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMDIVERGENCEH = oasysgui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMDIVERGENCEV = oasysgui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_PERIODID = oasysgui.lineEdit(box1, self, "PERIODID",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_NPERIODS = oasysgui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "KMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KMAX = oasysgui.lineEdit(box1, self, "KMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "KPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "HMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['US', 'URGENT', 'SRW'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)




    def unitLabels(self):
         return ["Use emittances","Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]",
                 "Electron Beam Size H [m]", "Electron Beam Size V [m]",
                 "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]",
                 "Period ID [m]", "Number of periods",
                 "Distance to slit [m]", "Slit gap H [m]", "Slit gap V [m]",
                 "K Min", "K Max", "Number of K Points", "higher harmonic", "calculation code"]

    def unitFlags(self):
         return ["True", "True", "self.USEEMITTANCES == 1 and self.METHOD != 1", "True",
                 "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1",
                 "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1",
                 "True", "True",
                 "True", "True", "True",
                 "True", "True", "True", "True", "True"]


    def get_help_name(self):
        return 'tc_slit'

    def check_fields(self):
        self.ELECTRONENERGY = congruence.checkStrictlyPositiveNumber(self.ELECTRONENERGY, "Electron Energy")
        if not self.METHOD == 1: self.ELECTRONENERGYSPREAD = congruence.checkPositiveNumber(self.ELECTRONENERGYSPREAD, "Electron Energy Spread")
        self.ELECTRONCURRENT = congruence.checkStrictlyPositiveNumber(self.ELECTRONCURRENT, "Electron Current")
        self.ELECTRONBEAMSIZEH = congruence.checkPositiveNumber(self.ELECTRONBEAMSIZEH, "Electron Beam Size H")
        self.ELECTRONBEAMSIZEV = congruence.checkPositiveNumber(self.ELECTRONBEAMSIZEV, "Electron Beam Size V")
        self.ELECTRONBEAMDIVERGENCEH = congruence.checkPositiveNumber(self.ELECTRONBEAMDIVERGENCEH, "Electron Beam Divergence H")
        self.ELECTRONBEAMDIVERGENCEV = congruence.checkPositiveNumber(self.ELECTRONBEAMDIVERGENCEV, "Electron Beam Divergence V")
        self.PERIODID = congruence.checkStrictlyPositiveNumber(self.PERIODID, "Period ID")
        self.NPERIODS = congruence.checkStrictlyPositiveNumber(self.NPERIODS, "Number of Periods")
        self.DISTANCE = congruence.checkPositiveNumber(self.DISTANCE, "Distance to slit")
        self.GAPH = congruence.checkPositiveNumber(self.GAPH, "Slit gap H")
        self.GAPV = congruence.checkPositiveNumber(self.GAPV, "Slit gap V")
        self.KMIN = congruence.checkPositiveNumber(self.KMIN, "K Min")
        self.KMAX = congruence.checkStrictlyPositiveNumber(self.KMAX, "K Max")
        congruence.checkLessThan(self.KMIN, self.KMAX, "K Min", "K Max")
        self.KPOINTS = congruence.checkStrictlyPositiveNumber(self.KPOINTS, "Number of K Points")
        self.HMAX = congruence.checkStrictlyPositiveNumber(self.HMAX, "Higher harmonic")

    def do_xoppy_calculation(self):
        return self.xoppy_calc_tc_slit()


    def extract_data_from_xoppy_output(self, calculation_output):


        K_scan,harmonics,P_scan,energy_values_at_flux_peak,flux_values = calculation_output

        harmonics_data = []

        for ih,harmonic_number in enumerate(harmonics):
            harmonics_data.append([harmonic_number,None])

            data = numpy.zeros((K_scan.size, 5))
            data[:, 0] = numpy.array(energy_values_at_flux_peak[:,ih])
            data[:, 1] = numpy.array(flux_values[:,ih])
            data[:, 2] = numpy.array(flux_values[:,ih])*codata.e*1e3
            data[:, 3] = numpy.array(K_scan)
            data[:, 4] = numpy.array(P_scan)

            harmonics_data[ih][1] = data

        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data_harmonics", harmonics_data)
            calculated_data.add_content("plot_x_col", 1)
            calculated_data.add_content("plot_y_col", 2)
        except:
            pass
        try:
            calculated_data.add_content("labels",["Photon energy [eV]","Flux [photons/s/0.1%bw]","Ky","Power [W]"])
        except:
            pass


        return calculated_data

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="",
                   log_x=False, log_y=False, harmonic=1, color='blue',control=True):
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
        self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)


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
                        # self.plot_canvas[index].setActiveCurve("Click on curve to highlight it")
                        # self.plot_canvas[index].showLegends()

                        self.tabs.setCurrentIndex(index)
                    except Exception as e:
                        self.view_type_combo.setEnabled(True)

                        raise Exception("Data not plottable: bad content\n" + str(e))


                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")

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
        self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)

    def get_data_exchange_widget_name(self):
        return "TC_SLIT"

    def getTitles(self):
        return ["Flux on slit","Spectral power on slit","Ky","Total power on slit"]

    def getXTitles(self):
        return ["Energy (eV)","Energy (eV)","Energy (eV)","Kv"]

    def getYTitles(self):
        return ["Flux (photons/s/0.1%bw)","Spectral power (W/eV)","Ky","Total power (W)"]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2), (0, 3), (2, 3)]

    def getLogPlot(self):
        return[(False, False), (False, False), (False, False), (False, False)]

    def xoppy_calc_tc_slit(self):


        print("Inside xoppy_calc_undulator_spectrum. ")

        bl = OrderedDict()
        bl['ElectronBeamDivergenceH'] = self.ELECTRONBEAMDIVERGENCEH
        bl['ElectronBeamDivergenceV'] = self.ELECTRONBEAMDIVERGENCEV
        bl['ElectronBeamSizeH']       = self.ELECTRONBEAMSIZEH
        bl['ElectronBeamSizeV']       = self.ELECTRONBEAMSIZEV
        bl['ElectronCurrent']         = self.ELECTRONCURRENT
        bl['ElectronEnergy']          = self.ELECTRONENERGY
        bl['ElectronEnergySpread']    = self.ELECTRONENERGYSPREAD
        bl['NPeriods']                = self.NPERIODS
        bl['PeriodID']                = self.PERIODID
        bl['distance']                = self.DISTANCE
        bl['gapH']                    = self.GAPH
        bl['gapV']                    = self.GAPV

        if self.USEEMITTANCES:
            zero_emittance = False
        else:
            zero_emittance = True

        if self.METHOD == 0:
            code = "us"
        if self.METHOD == 1:
            code = "urgent"
        if self.METHOD == 2:
            code = "srw"

        harmonics = []
        for i in range(self.HMAX+1):
            if i % 2 != 0: harmonics.append(i)

        K_scan,harmonics,power_array, energy_values_at_flux_peak,flux_values = srundplug.tuning_curves_on_slit(bl,
                    Kmin=self.KMIN,Kmax=self.KMAX,Kpoints=self.KPOINTS,harmonics=harmonics,
                    zero_emittance=zero_emittance,do_plot_peaks=False,code=code)

        if zero_emittance:
            print("\nNo emittance calculation")

        print("Done")

        return K_scan,harmonics,power_array,energy_values_at_flux_peak,flux_values

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data._light_source._magnetic_structure, synedid.InsertionDevice):
                light_source = data._light_source

                self.ELECTRONENERGY = light_source._electron_beam._energy_in_GeV
                self.ELECTRONENERGYSPREAD = light_source._electron_beam._energy_spread
                self.ELECTRONCURRENT = light_source._electron_beam._current

                x, xp, y, yp = light_source._electron_beam.get_sigmas_all()

                self.ELECTRONBEAMSIZEH = x
                self.ELECTRONBEAMSIZEV = y
                self.ELECTRONBEAMDIVERGENCEH = xp
                self.ELECTRONBEAMDIVERGENCEV = yp
                self.PERIODID = light_source._magnetic_structure._period_length
                self.NPERIODS = light_source._magnetic_structure._number_of_periods
                self.KMAX = light_source._magnetic_structure._K_vertical

                self.set_enabled(False)

            else:
                self.set_enabled(True)
                # raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)
            # raise ValueError("Syned data not correct")

    def set_enabled(self,value):
        if value == True:
                self.id_ELECTRONENERGY.setEnabled(True)
                self.id_ELECTRONENERGYSPREAD.setEnabled(True)
                self.id_ELECTRONBEAMSIZEH.setEnabled(True)
                self.id_ELECTRONBEAMSIZEV.setEnabled(True)
                self.id_ELECTRONBEAMDIVERGENCEH.setEnabled(True)
                self.id_ELECTRONBEAMDIVERGENCEV.setEnabled(True)
                self.id_ELECTRONCURRENT.setEnabled(True)
                self.id_PERIODID.setEnabled(True)
                self.id_NPERIODS.setEnabled(True)
                self.id_KMAX.setEnabled(True)
        else:
                self.id_ELECTRONENERGY.setEnabled(False)
                self.id_ELECTRONENERGYSPREAD.setEnabled(False)
                self.id_ELECTRONBEAMSIZEH.setEnabled(False)
                self.id_ELECTRONBEAMSIZEV.setEnabled(False)
                self.id_ELECTRONBEAMDIVERGENCEH.setEnabled(False)
                self.id_ELECTRONBEAMDIVERGENCEV.setEnabled(False)
                self.id_ELECTRONCURRENT.setEnabled(False)
                self.id_PERIODID.setEnabled(False)
                self.id_NPERIODS.setEnabled(False)
                self.id_KMAX.setEnabled(False)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWtc_slit()
    w.show()
    app.exec()
    w.saveSettings()
