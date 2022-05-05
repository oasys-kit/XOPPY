import sys
import numpy
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject



from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from xoppylib.sources.xoppy_undulators import xoppy_calc_undulator_spectrum

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid


class OWundulator_spectrum(XoppyWidget, WidgetDecorator):
    name = "Undulator Spectrum"
    id = "orange.widgets.dataundulator_spectrum"
    description = "Undulator Spectrum"
    icon = "icons/xoppy_undulator_spectrum.png"
    priority = 1
    category = ""
    keywords = ["xoppy", "undulator_spectrum"]

    USEEMITTANCES=Setting(1)
    ELECTRONENERGY = Setting(6.04)
    ELECTRONENERGYSPREAD = Setting(0.001)
    ELECTRONCURRENT = Setting(0.2)
    ELECTRONBEAMSIZEH = Setting(0.000395)
    ELECTRONBEAMSIZEV = Setting(9.9e-06)
    ELECTRONBEAMDIVERGENCEH = Setting(1.05e-05)
    ELECTRONBEAMDIVERGENCEV = Setting(3.9e-06)
    PERIODID = Setting(0.018)
    NPERIODS = Setting(222)
    KV = Setting(1.68)
    KH = Setting(0.0)
    KPHASE = Setting(0.0)
    DISTANCE = Setting(30.0)
    GAPH = Setting(0.001)
    GAPV = Setting(0.001)
    GAPH_CENTER = Setting(0.0)
    GAPV_CENTER = Setting(0.0)
    PHOTONENERGYMIN = Setting(3000.0)
    PHOTONENERGYMAX = Setting(55000.0)
    PHOTONENERGYPOINTS = Setting(500)
    METHOD = Setting(2)

    inputs = WidgetDecorator.syned_input_data()

    def __init__(self):
        super().__init__(show_script_tab=True)

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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 1
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONENERGYSPREAD = oasysgui.lineEdit(box1, self, "ELECTRONENERGYSPREAD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 2
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONCURRENT = oasysgui.lineEdit(box1, self, "ELECTRONCURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMSIZEH = oasysgui.lineEdit(box1, self, "ELECTRONBEAMSIZEH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMSIZEV = oasysgui.lineEdit(box1, self, "ELECTRONBEAMSIZEV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMDIVERGENCEH = oasysgui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_ELECTRONBEAMDIVERGENCEV = oasysgui.lineEdit(box1, self, "ELECTRONBEAMDIVERGENCEV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_PERIODID = oasysgui.lineEdit(box1, self, "PERIODID",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_NPERIODS = oasysgui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KV = oasysgui.lineEdit(box1, self, "KV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9B
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KH = oasysgui.lineEdit(box1, self, "KH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9C
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KPHASE = oasysgui.lineEdit(box1, self, "KPHASE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)




        #widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11B
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPH_CENTER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 12B
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPV_CENTER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
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
         return ["Use emittances","Electron Energy [GeV]", "Electron Energy Spread",
                 "Electron Current [A]", "Electron Beam Size H [m]", "Electron Beam Size V [m]",
                 "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]", "Period ID [m]",
                 "Number of periods", "Kv [K value vertical field]", "Kh [K value horizontal field]",
                 "Kphase [phase diff Kh - Kv in rad]","Distance to slit [m]","Slit gap H [m]",
                 "Slit gap V [m]", "Slit center H [m]", "Slit center V [m]",
                 "photon Energy Min [eV]","photon Energy Max [eV]",
                 "photon Energy Points", "calculation code"]

    def unitFlags(self):
         return ["True", "True", "self.USEEMITTANCES == 1 and self.METHOD != 1",
                 "True", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1",
                 "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "True",
                 "True", "True", "self.METHOD != 0",
                 "self.METHOD != 0","True", "True",
                 "True", "True", "True",
                 "True", "True",
                 "True", "True"]

    def get_help_name(self):
        return 'undulator_spectrum'

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
        self.KV = congruence.checkPositiveNumber(self.KV, "Kv")
        self.KH = congruence.checkPositiveNumber(self.KH, "Kh")
        self.KPHASE = congruence.checkNumber(self.KPHASE, "KPHASE")
        self.DISTANCE = congruence.checkPositiveNumber(self.DISTANCE, "Distance to slit")
        self.GAPH = congruence.checkPositiveNumber(self.GAPH, "Slit gap H")
        self.GAPV = congruence.checkPositiveNumber(self.GAPV, "Slit gap V")
        self.GAPH_CENTER = congruence.checkPositiveNumber(self.GAPH_CENTER, "Slit center H")
        self.GAPV_CENTER = congruence.checkPositiveNumber(self.GAPV_CENTER, "Slit center V")
        self.PHOTONENERGYMIN = congruence.checkPositiveNumber(self.PHOTONENERGYMIN, "photon Energy Min")
        self.PHOTONENERGYMAX = congruence.checkStrictlyPositiveNumber(self.PHOTONENERGYMAX, "photon Energy Max")
        congruence.checkLessThan(self.PHOTONENERGYMIN, self.PHOTONENERGYMAX, "photon Energy Min", "photon Energy Max")
        self.PHOTONENERGYPOINTS = congruence.checkStrictlyPositiveNumber(self.PHOTONENERGYPOINTS, "photon Energy Points")

        if self.METHOD == 1: # URGENT
            congruence.checkLessThan(self.PHOTONENERGYPOINTS,4701,"Number of energy points","4701")

        # if sys.platform == 'linux' and self.METHOD == 2:
        #     raise Exception("SRW calculation code not supported under Linux")

    def do_xoppy_calculation(self):
        energy, flux, spectral_power, cumulated_power = xoppy_calc_undulator_spectrum(ELECTRONENERGY=self.ELECTRONENERGY,
                                             ELECTRONENERGYSPREAD=self.ELECTRONENERGYSPREAD,
                                             ELECTRONCURRENT=self.ELECTRONCURRENT,
                                             ELECTRONBEAMSIZEH=self.ELECTRONBEAMSIZEH,
                                             ELECTRONBEAMSIZEV=self.ELECTRONBEAMSIZEV,
                                             ELECTRONBEAMDIVERGENCEH=self.ELECTRONBEAMDIVERGENCEH,
                                             ELECTRONBEAMDIVERGENCEV=self.ELECTRONBEAMDIVERGENCEV,
                                             PERIODID=self.PERIODID,
                                             NPERIODS=self.NPERIODS,
                                             KV=self.KV,
                                             KH=self.KH,
                                             KPHASE=self.KPHASE,
                                             DISTANCE=self.DISTANCE,
                                             GAPH=self.GAPH,
                                             GAPV=self.GAPV,
                                             GAPH_CENTER=self.GAPH_CENTER,
                                             GAPV_CENTER=self.GAPV_CENTER,
                                             PHOTONENERGYMIN=self.PHOTONENERGYMIN,
                                             PHOTONENERGYMAX=self.PHOTONENERGYMAX,
                                             PHOTONENERGYPOINTS=self.PHOTONENERGYPOINTS,
                                             METHOD=self.METHOD,
                                             USEEMITTANCES=self.USEEMITTANCES)

        # write python script in standard output
        dict_parameters = {
            "ELECTRONENERGY" : self.ELECTRONENERGY,
            "ELECTRONENERGYSPREAD" : self.ELECTRONENERGYSPREAD,
            "ELECTRONCURRENT" : self.ELECTRONCURRENT,
            "ELECTRONBEAMSIZEH" : self.ELECTRONBEAMSIZEH,
            "ELECTRONBEAMSIZEV" : self.ELECTRONBEAMSIZEV,
            "ELECTRONBEAMDIVERGENCEH" : self.ELECTRONBEAMDIVERGENCEH,
            "ELECTRONBEAMDIVERGENCEV" : self.ELECTRONBEAMDIVERGENCEV,
            "PERIODID" : self.PERIODID,
            "NPERIODS" : self.NPERIODS,
            "KV" : self.KV,
            "KH": self.KH,
            "KPHASE": self.KPHASE,
            "DISTANCE" : self.DISTANCE,
            "GAPH" : self.GAPH,
            "GAPV" : self.GAPV,
            "GAPH_CENTER": self.GAPH_CENTER,
            "GAPV_CENTER": self.GAPV_CENTER,
            "PHOTONENERGYMIN" : self.PHOTONENERGYMIN,
            "PHOTONENERGYMAX" : self.PHOTONENERGYMAX,
            "PHOTONENERGYPOINTS" : self.PHOTONENERGYPOINTS,
            "METHOD" : self.METHOD,
            "USEEMITTANCES" : self.USEEMITTANCES,
        }


        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)

        return energy, flux, spectral_power, cumulated_power, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:undulator_spectrum)
#
from xoppylib.sources.xoppy_undulators import xoppy_calc_undulator_spectrum
energy, flux, spectral_power, cumulated_power = xoppy_calc_undulator_spectrum(
    ELECTRONENERGY={ELECTRONENERGY},
    ELECTRONENERGYSPREAD={ELECTRONENERGYSPREAD},
    ELECTRONCURRENT={ELECTRONCURRENT},
    ELECTRONBEAMSIZEH={ELECTRONBEAMSIZEH},
    ELECTRONBEAMSIZEV={ELECTRONBEAMSIZEV},
    ELECTRONBEAMDIVERGENCEH={ELECTRONBEAMDIVERGENCEH},
    ELECTRONBEAMDIVERGENCEV={ELECTRONBEAMDIVERGENCEV},
    PERIODID={PERIODID},
    NPERIODS={NPERIODS},
    KV={KV},
    KH={KH},
    KPHASE={KPHASE},
    DISTANCE={DISTANCE},
    GAPH={GAPH},
    GAPV={GAPV},
    GAPH_CENTER={GAPH_CENTER},
    GAPV_CENTER={GAPV_CENTER},
    PHOTONENERGYMIN={PHOTONENERGYMIN},
    PHOTONENERGYMAX={PHOTONENERGYMAX},
    PHOTONENERGYPOINTS={PHOTONENERGYPOINTS},
    METHOD={METHOD},
    USEEMITTANCES={USEEMITTANCES})

#
# example plot
#
from srxraylib.plot.gol import plot

plot(energy,flux,
    xtitle="Photon energy [eV]",ytitle="Flux [photons/s/o.1%bw]",title="Undulator Flux",
    xlog=False,ylog=False,show=False)
plot(energy,spectral_power,
    xtitle="Photon energy [eV]",ytitle="Power [W/eV]",title="Undulator Spectral Power",
    xlog=False,ylog=False,show=False)
plot(energy,cumulated_power,
    xtitle="Photon energy [eV]",ytitle="Cumulated Power [W]",title="Undulator Cumulated Power",
    xlog=False,ylog=False,show=True)
#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):
        e, f, sp, csp, script = calculation_output

        data = numpy.zeros((len(e), 4))
        data[:, 0] = numpy.array(e)
        data[:, 1] = numpy.array(f)
        data[:, 2] = numpy.array(sp)
        data[:, 3] = numpy.array(csp)

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", data)
        calculated_data.add_content("xoppy_script", script)


        return calculated_data

    def get_data_exchange_widget_name(self):
        return "UNDULATOR_FLUX"

    def getTitles(self):
        return ['Undulator Flux', 'Spectral Power', 'Cumulated Power']

    def getXTitles(self):
        return ["Energy [eV]", "Energy [eV]", "Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Phot/sec/0.1%bw]", "Spectral Power [W/eV]", "Cumulated Power [W]"]

    def getLogPlot(self):
        return [(False, False), (False, False), (False, False)]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2), (0, 3)]

    def getDefaultPlotTabIndex(self):
        return 0

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
                self.NPERIODS = int(light_source._magnetic_structure._number_of_periods)
                self.KV = light_source._magnetic_structure._K_vertical
                self.KH = light_source._magnetic_structure._K_horizontal
                # TODO  self.KPHASE = light_source._magnetic_structure....

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
                self.id_KV.setEnabled(True)
                self.id_KH.setEnabled(True)
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
                self.id_KV.setEnabled(False)
                self.id_KH.setEnabled(False)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_spectrum()
    w.show()
    app.exec()
    w.saveSettings()
