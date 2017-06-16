import sys
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from collections import OrderedDict
from orangecontrib.xoppy.util import srundplug
import scipy.constants as codata
import os

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

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
    DISTANCE = Setting(30.0)
    GAPH = Setting(0.001)
    GAPV = Setting(0.001)
    PHOTONENERGYMIN = Setting(3000.0)
    PHOTONENERGYMAX = Setting(55000.0)
    PHOTONENERGYPOINTS = Setting(500)
    METHOD = Setting(0)

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
        self.id_KV = oasysgui.lineEdit(box1, self, "KV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAPV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYPOINTS",
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
         return ["Use emittances","Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]", "Electron Beam Size H [m]", "Electron Beam Size V [m]", "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]", "Period ID [m]", "Number of periods", "Kv [undulator K value vertical field]", "Distance to slit [m]", "Slit gap H [m]", "Slit gap V [m]", "photon Energy Min [eV]", "photon Energy Max [eV]", "photon Energy Points", "calculation code"]

    def unitFlags(self):
         return ["True", "True", "self.USEEMITTANCES == 1 and self.METHOD != 1", "True", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True"]

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
        self.DISTANCE = congruence.checkPositiveNumber(self.DISTANCE, "Distance to slit")
        self.GAPH = congruence.checkPositiveNumber(self.GAPH, "Slit gap H")
        self.GAPV = congruence.checkPositiveNumber(self.GAPV, "Slit gap V")
        self.PHOTONENERGYMIN = congruence.checkPositiveNumber(self.PHOTONENERGYMIN, "photon Energy Min")
        self.PHOTONENERGYMAX = congruence.checkStrictlyPositiveNumber(self.PHOTONENERGYMAX, "photon Energy Max")
        congruence.checkLessThan(self.PHOTONENERGYMIN, self.PHOTONENERGYMAX, "photon Energy Min", "photon Energy Max")
        self.PHOTONENERGYPOINTS = congruence.checkStrictlyPositiveNumber(self.PHOTONENERGYPOINTS, "photon Energy Points")

        if self.METHOD == 1: # URGENT
            congruence.checkLessThan(self.PHOTONENERGYPOINTS,4701,"Number of energy points","4701")

        # if sys.platform == 'linux' and self.METHOD == 2:
        #     raise Exception("SRW calculation code not supported under Linux")

    def do_xoppy_calculation(self):
        return xoppy_calc_undulator_spectrum(ELECTRONENERGY=self.ELECTRONENERGY,
                                             ELECTRONENERGYSPREAD=self.ELECTRONENERGYSPREAD,
                                             ELECTRONCURRENT=self.ELECTRONCURRENT,
                                             ELECTRONBEAMSIZEH=self.ELECTRONBEAMSIZEH,
                                             ELECTRONBEAMSIZEV=self.ELECTRONBEAMSIZEV,
                                             ELECTRONBEAMDIVERGENCEH=self.ELECTRONBEAMDIVERGENCEH,
                                             ELECTRONBEAMDIVERGENCEV=self.ELECTRONBEAMDIVERGENCEV,
                                             PERIODID=self.PERIODID,
                                             NPERIODS=self.NPERIODS,
                                             KV=self.KV,
                                             DISTANCE=self.DISTANCE,
                                             GAPH=self.GAPH,
                                             GAPV=self.GAPV,
                                             PHOTONENERGYMIN=self.PHOTONENERGYMIN,
                                             PHOTONENERGYMAX=self.PHOTONENERGYMAX,
                                             PHOTONENERGYPOINTS=self.PHOTONENERGYPOINTS,
                                             METHOD=self.METHOD,
                                             USEEMITTANCES=self.USEEMITTANCES)

    def extract_data_from_xoppy_output(self, calculation_output):
        e, f, sp = calculation_output

        data = numpy.zeros((len(e), 3))
        data[:, 0] = numpy.array(e)
        data[:, 1] = numpy.array(f)
        data[:, 2] = numpy.array(sp)

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", data)

        return calculated_data

    def get_data_exchange_widget_name(self):
        return "UNDULATOR_FLUX"

    def getTitles(self):
        return ['Undulator Flux', 'Spectral Power']

    def getXTitles(self):
        return ["Energy [eV]", "Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Phot/sec/0.1%bw]", "Spectral Power [W/eV]"]

    def getLogPlot(self):
        return [(False, False), (False, False)]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2)]

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
                self.KV = light_source._magnetic_structure._K_vertical

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
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def xoppy_calc_undulator_spectrum(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                              ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                              ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                              PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                              PHOTONENERGYMIN=3000.0,PHOTONENERGYMAX=55000.0,PHOTONENERGYPOINTS=500,METHOD=0,
                              USEEMITTANCES=1):
    print("Inside xoppy_calc_undulator_spectrum. ")

    bl = OrderedDict()
    bl['ElectronBeamDivergenceH'] = ELECTRONBEAMDIVERGENCEH
    bl['ElectronBeamDivergenceV'] = ELECTRONBEAMDIVERGENCEV
    bl['ElectronBeamSizeH'] = ELECTRONBEAMSIZEH
    bl['ElectronBeamSizeV'] = ELECTRONBEAMSIZEV
    bl['ElectronCurrent'] = ELECTRONCURRENT
    bl['ElectronEnergy'] = ELECTRONENERGY
    bl['ElectronEnergySpread'] = ELECTRONENERGYSPREAD
    bl['Kv'] = KV
    bl['NPeriods'] = NPERIODS
    bl['PeriodID'] = PERIODID
    bl['distance'] = DISTANCE
    bl['gapH'] = GAPH
    bl['gapV'] = GAPV

    if USEEMITTANCES:
        zero_emittance = False
    else:
        zero_emittance = True

    #TODO remove file and export e,f arrays
    outFile = "undulator_spectrum.spec"

    codata_mee = codata.m_e * codata.c**2 / codata.e # electron mass in eV
    gamma = bl['ElectronEnergy'] * 1e9 / codata_mee

    m2ev = codata.c * codata.h / codata.e      # lambda(m)  = m2eV / energy(eV)
    resonance_wavelength = (1 + bl['Kv']**2 / 2.0) / 2 / gamma**2 * bl["PeriodID"]
    resonance_energy = m2ev / resonance_wavelength
    print ("Gamma: %f \n"%(gamma))
    print ("Resonance wavelength [A]: %g \n"%(1e10*resonance_wavelength))
    print ("Resonance energy [eV]: %g \n"%(resonance_energy))


    if METHOD == 0:
        print("Undulator flux calculation using US. Please wait...")
        e, f = srundplug.calc1d_us(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False,zero_emittance=zero_emittance)
        print("Done")
        print("\nCheck calculation output at: %s"%(os.path.join(os.getcwd(),"us.out")))
    if METHOD == 1:
        print("Undulator flux calculation using URGENT. Please wait...")
        e, f = srundplug.calc1d_urgent(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False,zero_emittance=zero_emittance)
        print("Done")
        print("\nCheck calculation output at: %s"%(os.path.join(os.getcwd(),"urgent.out")))
    if METHOD == 2:
        # get the maximum harmonic number
        h_max = int(1.1*PHOTONENERGYMAX/resonance_energy)

        print ("Number of harmonics considered: %d \n"%(h_max))
        print("Undulator flux calculation using SRW. Please wait...")
        e, f = srundplug.calc1d_srw(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False,zero_emittance=zero_emittance,
              srw_max_harmonic_number=h_max)
        print("Done")

    if zero_emittance:
        print("\nNo emittance calculation")

    print("\nPower from integral of spectrum: %8.3f W"%(f.sum()*1e3*codata.e*(e[1]-e[0])))

    return e, f, f*codata.e * 1e3



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_spectrum()
    w.show()
    app.exec()
    w.saveSettings()
