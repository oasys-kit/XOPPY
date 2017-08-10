import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_radiation

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid



import scipy.constants as codata


class OWundulator_radiation(XoppyWidget, WidgetDecorator):
    name = "Undulator Radiation"
    id = "orange.widgets.dataundulator_radiation"
    description = "Undulator Radiation"
    icon = "icons/xoppy_undulator_radiation.png"
    priority = 5
    category = ""
    keywords = ["xoppy", "undulator_radiation"]

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
    SETRESONANCE = Setting(0)
    HARMONICNUMBER = Setting(1)

    GAPH = Setting(0.003)
    GAPV = Setting(0.003)
    HSLITPOINTS = Setting(41)
    VSLITPOINTS = Setting(41)

    PHOTONENERGYMIN = Setting(6000.0)
    PHOTONENERGYMAX = Setting(8500.0)
    PHOTONENERGYPOINTS = Setting(20)


    METHOD = Setting(1)

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



        # widget <><><>
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "SETRESONANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['User defined', 'Set to resonance/central cone','Set to resonance/up to first ring'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget <><><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "HARMONICNUMBER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
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

        #widget index <><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index <><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index <><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['US', 'URGENT', 'SRW','pySRU'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
        return ["Use emittances","Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]",
                "Electron Beam Size H [m]", "Electron Beam Size V [m]","Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]",
                "Period ID [m]", "Number of periods","Kv [undulator K value vertical field]",
                "Distance to slit [m]",
                "Set photon energy and slit","Harmonic number",
                "Slit gap H [m]", "Slit gap V [m]",
                "Number of slit mesh points in H", "Number of slit mesh points in V",
                "Photon Energy Min [eV]","Photon Energy Max [eV]","Number of Photon Energy Points",
                "calculation code"]

    # TODO check energy spread flag: set to False (not used at all)!!
    def unitFlags(self):
        return ["True", "True", "False", "True",
                "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1","self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1",
                "True", "True", "True",
                "True",
                "True", "self.SETRESONANCE > 0",
                "self.SETRESONANCE == 0", "self.SETRESONANCE == 0",
                "True", "True",
                "self.SETRESONANCE == 0", "self.SETRESONANCE == 0","self.SETRESONANCE == 0",
                "True"]

    def get_help_name(self):
        return 'undulator_radiation'

    def check_fields(self):
        self.ELECTRONENERGY = congruence.checkStrictlyPositiveNumber(self.ELECTRONENERGY, "Electron Energy")
        if not self.METHOD == 1: self.ELECTRONENERGYSPREAD = congruence.checkPositiveNumber(self.ELECTRONENERGYSPREAD, "Electron Energy Spread")
        self.ELECTRONCURRENT = congruence.checkStrictlyPositiveNumber(self.ELECTRONCURRENT, "Electron Current")
        self.ELECTRONBEAMSIZEH = congruence.checkPositiveNumber(self.ELECTRONBEAMSIZEH, "Electron Beam Size H")
        self.ELECTRONBEAMSIZEV = congruence.checkPositiveNumber(self.ELECTRONBEAMSIZEV, "Electron Beam Size V")
        self.ELECTRONBEAMDIVERGENCEH = congruence.checkNumber(self.ELECTRONBEAMDIVERGENCEH, "Electron Beam Divergence H")
        self.ELECTRONBEAMDIVERGENCEV = congruence.checkNumber(self.ELECTRONBEAMDIVERGENCEV, "Electron Beam Divergence V")

        self.PERIODID = congruence.checkStrictlyPositiveNumber(self.PERIODID, "Period ID")
        self.NPERIODS = congruence.checkStrictlyPositiveNumber(self.NPERIODS, "Number of Periods")
        self.KV = congruence.checkPositiveNumber(self.KV, "Kv")
        self.DISTANCE = congruence.checkStrictlyPositiveNumber(self.DISTANCE, "Distance to slit")

        if self.SETRESONANCE == 0:
            self.GAPH = congruence.checkPositiveNumber(self.GAPH, "Slit gap H")
            self.GAPV = congruence.checkPositiveNumber(self.GAPV, "Slit gap V")
            self.PHOTONENERGYMIN = congruence.checkNumber(self.PHOTONENERGYMIN, "Photon Energy Min")
            self.PHOTONENERGYMAX = congruence.checkNumber(self.PHOTONENERGYMAX, "Photon Energy Max")
            congruence.checkGreaterOrEqualThan(self.PHOTONENERGYPOINTS, 2, "Number of Photon Energy Points", " 2")
        else:
            self.HARMONICNUMBER = congruence.checkStrictlyPositiveNumber(self.HARMONICNUMBER, "Harmonic number")

        self.HSLITPOINTS = congruence.checkStrictlyPositiveNumber(self.HSLITPOINTS, "Number of slit mesh points in H")
        self.VSLITPOINTS = congruence.checkStrictlyPositiveNumber(self.VSLITPOINTS, "Number of slit mesh points in V")

        if  self.METHOD == 1: # URGENT
            congruence.checkLessOrEqualThan(self.HSLITPOINTS, 51, "Number of slit mesh points for URGENT "," 51")
            congruence.checkLessOrEqualThan(self.VSLITPOINTS, 51, "Number of slit mesh points for URGENT "," 51")

    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:

                self.initializeTabs() # added by srio to avoid overlapping graphs

                self.view_type_combo.setEnabled(False)

                p,e,h,v = calculated_data.get_content("xoppy_data")
                code = calculated_data.get_content("xoppy_code")


                try:
                    self.plot_data3D(p, e, h, v, 0, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Code '+code+'; Flux [photons/s/0.1%bw/mm^2]',)

                    self.tabs.setCurrentIndex(0)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    if len(e) > 1:
                        energy_step = e[1]-e[0]
                    else:
                        energy_step = 1.0

                    self.plot_data2D(p.sum(axis=0)*energy_step*codata.e*1e3, h, v, 1, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Code '+code+'; Power density [W/mm^2]',)

                    # self.tabs.setCurrentIndex(1)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))


                try:
                    print("\nResult arrays (shapes): ",e.shape,h.shape,v.shape,p.shape)
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0]), 2, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Flux [photons/s/0.1%bw]',
                                     title='Code '+code+'; Flux',)

                    # self.tabs.setCurrentIndex(2)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    print("\nResult arrays (shapes): ",e.shape,h.shape,v.shape,p.shape)
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*codata.e*1e3, 3, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Spectral power [W/eV]',
                                     title='Code '+code+'; Spectral power',)

                    # self.tabs.setCurrentIndex(2)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))


                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")





    def do_xoppy_calculation(self):
        return xoppy_calc_undulator_radiation(ELECTRONENERGY=self.ELECTRONENERGY,
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
                    SETRESONANCE=self.SETRESONANCE,
                    HARMONICNUMBER=self.HARMONICNUMBER,
                    GAPH=self.GAPH,
                    GAPV=self.GAPV,
                    HSLITPOINTS=self.HSLITPOINTS,
                    VSLITPOINTS=self.VSLITPOINTS,
                    METHOD=self.METHOD,
                    PHOTONENERGYMIN=self.PHOTONENERGYMIN,
                    PHOTONENERGYMAX=self.PHOTONENERGYMAX,
                    PHOTONENERGYPOINTS=self.PHOTONENERGYPOINTS,
                    USEEMITTANCES=self.USEEMITTANCES)

    def extract_data_from_xoppy_output(self, calculation_output):
        e, h, v, p, code = calculation_output

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        calculated_data.add_content("xoppy_data", [p, e, h, v])
        calculated_data.add_content("xoppy_code", code)

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "UNDULATOR_RADIATION"

    def getTitles(self):
        return ['Undulator Flux vs E,X,Y','Undulator Power Density vs X,Y','Undulator Flux vs E','Undulator Spectral Power vs E']


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




if __name__ == "__main__":



    bl = None
    try:
        from syned.util.json_tools import load_from_json_file, load_from_json_url
        from syned.storage_ring.light_source import LightSource
        from syned.beamline.beamline import Beamline

        remote_file_name = "http://ftp.esrf.eu/pub/scisoft/syned/lightsources/ESRF_ID21_EBS_ppu42_17.json"
        remote_file_name = "http://ftp.esrf.eu/pub/scisoft/syned/lightsources/ESRF_ID21_LowBeta_ppu42_17.json"
        tmp = load_from_json_url(remote_file_name)
        if  isinstance(tmp,LightSource):
            bl = Beamline(tmp)
    except:
        pass



    app = QApplication(sys.argv)
    w = OWundulator_radiation()

    if bl is not None:
        w.receive_syned_data(bl)

    w.show()
    app.exec()
    w.saveSettings()
