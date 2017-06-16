import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject
from collections import OrderedDict

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util import srundplug

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

class OWundulator_power_density(XoppyWidget, WidgetDecorator):
    name = "Undulator Power Density"
    id = "orange.widgets.dataundulator_power_density"
    description = "Undulator Power Density"
    icon = "icons/xoppy_undulator_power_density.png"
    priority = 3
    category = ""
    keywords = ["xoppy", "undulator_power_density"]

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
    GAPH = Setting(0.003)
    GAPV = Setting(0.003)
    HSLITPOINTS = Setting(41)
    VSLITPOINTS = Setting(41)
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
        oasysgui.lineEdit(box1, self, "HSLITPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "VSLITPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['US', 'URGENT', 'SRW'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ["Use emittances","Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]", "Electron Beam Size H [m]", "Electron Beam Size V [m]", "Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]", "Period ID [m]", "Number of periods", "Kv [undulator K value vertical field]", "Distance to slit [m]", "Slit gap H [m]", "Slit gap V [m]", "Number of slit mesh points in H", "Number of slit mesh points in V", "calculation code"]

    def unitFlags(self):
         return ["True","True", "self.USEEMITTANCES == 1 and self.METHOD != 1", "True", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1", "True", "True", "True", "True", "True", "True", "True", "True", "True"]

    def get_help_name(self):
        return 'undulator_power_density'

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
        self.HSLITPOINTS = congruence.checkStrictlyPositiveNumber(self.HSLITPOINTS, "Number of slit mesh points in H")
        self.VSLITPOINTS = congruence.checkStrictlyPositiveNumber(self.VSLITPOINTS, "Number of slit mesh points in V")

        if  self.METHOD == 1: # URGENT
            congruence.checkLessOrEqualThan(self.HSLITPOINTS, 51, "Number of slit mesh points for URGENT "," 51")
            congruence.checkLessOrEqualThan(self.VSLITPOINTS, 51, "Number of slit mesh points for URGENT "," 51")


        # if sys.platform == 'linux' and self.METHOD == 2:
        #     raise Exception("SRW calculation code not supported under Linux")

    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:

                self.initializeTabs() # added by srio to avoid overlapping graphs

                self.view_type_combo.setEnabled(False)

                data = calculated_data.get_content("xoppy_data")
                code = calculated_data.get_content("xoppy_code")

                h = data[0]
                v = data[1]
                p = data[2]

                try:

                    print("Result arrays (shapes): ", h.shape, v.shape, p.shape )

                    self.plot_data2D(p, h, v, 0, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Code '+code+'; Power density [W/mm^2]')

                except Exception as e:
                    self.view_type_combo.setEnabled(True)

                    raise Exception("Data not plottable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")

    def do_xoppy_calculation(self):
        return  xoppy_calc_undulator_power_density(ELECTRONENERGY=self.ELECTRONENERGY,
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
                                                   HSLITPOINTS=self.HSLITPOINTS,
                                                   VSLITPOINTS=self.VSLITPOINTS,
                                                   METHOD=self.METHOD,
                                                   USEEMITTANCES=self.USEEMITTANCES)

    def extract_data_from_xoppy_output(self, calculation_output):
        h, v, p, code = calculation_output

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        calculated_data.add_content("xoppy_data", [h, v, p])
        calculated_data.add_content("xoppy_code",  code)

        return calculated_data

    def get_data_exchange_widget_name(self):
        return "UNDULATOR_POWER_DENSITY"

    def getTitles(self):
        return ['Undulator Power Density']

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

def xoppy_calc_undulator_power_density(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                       ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                       ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                       PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                                       HSLITPOINTS=101,VSLITPOINTS=51,METHOD=0,USEEMITTANCES=1):
    print("Inside xoppy_calc_undulator_power_density. ")

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

    #TODO remove SPEC file
    outFile = "undulator_power_density.spec"

    if METHOD == 0:
        code = "US"
        print("Undulator power_density calculation using US. Please wait...")
        h,v,p = srundplug.calc2d_us(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                    zero_emittance=zero_emittance)
        print("Done")
    if METHOD == 1:
        code = "URGENT"
        print("Undulator power_density calculation using URGENT. Please wait...")
        h,v,p = srundplug.calc2d_urgent(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                        zero_emittance=zero_emittance)
        print("Done")
    if METHOD == 2:
        code = "SRW"
        print("Undulator power_density calculation using SRW. Please wait...")
        h,v,p = srundplug.calc2d_srw(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                     zero_emittance=zero_emittance)
        print("Done")

    if zero_emittance:
        print("No emittance calculation")

    return h, v, p, code


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_power_density()
    w.show()
    app.exec()
    w.saveSettings()