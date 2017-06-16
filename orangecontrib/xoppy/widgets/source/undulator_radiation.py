import sys
import numpy

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


import scipy.constants as codata
codata_mee = codata.codata.physical_constants["electron mass energy equivalent in MeV"][0]

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

        self.PHOTONENERGYMIN = congruence.checkNumber(self.PHOTONENERGYMIN, "Photon Energy Min")
        self.PHOTONENERGYMAX = congruence.checkNumber(self.PHOTONENERGYMAX, "Photon Energy Max")
        self.PHOTONENERGYPOINTS = congruence.checkStrictlyPositiveNumber(self.PHOTONENERGYPOINTS, "Number of Photon Energy Points")

        self.PERIODID = congruence.checkStrictlyPositiveNumber(self.PERIODID, "Period ID")
        self.NPERIODS = congruence.checkStrictlyPositiveNumber(self.NPERIODS, "Number of Periods")
        self.KV = congruence.checkPositiveNumber(self.KV, "Kv")
        self.DISTANCE = congruence.checkStrictlyPositiveNumber(self.DISTANCE, "Distance to slit")

        self.HARMONICNUMBER = congruence.checkStrictlyPositiveNumber(self.HARMONICNUMBER, "Harminic number")

        self.GAPH = congruence.checkPositiveNumber(self.GAPH, "Slit gap H")
        self.GAPV = congruence.checkPositiveNumber(self.GAPV, "Slit gap V")
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
                    self.plot_data2D(p.sum(axis=0)*(e[1]-e[0])*codata.e*1e3, h, v, 1, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Code '+code+'; Power density [W/mm^2]',)

                    # self.tabs.setCurrentIndex(1)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))


                try:
                    print("Result arrays (shapes): ",e.shape,h.shape,v.shape,p.shape)
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0]), 2, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Flux [photons/s/0.1%bw/mm^2]',
                                     title='Code '+code+'; Flux',)

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
        return ['Undulator Flux','Undulator Power Density','Undulator Spectrum']


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

def xoppy_calc_undulator_radiation(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                       ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                       ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                       PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,
                                       SETRESONANCE=0,HARMONICNUMBER=1,
                                       GAPH=0.003,GAPV=0.003,\
                                       HSLITPOINTS=41,VSLITPOINTS=41,METHOD=0,
                                       PHOTONENERGYMIN=-0.00000001,PHOTONENERGYMAX=1.0,PHOTONENERGYPOINTS=1,
                                       USEEMITTANCES=1):
    print("Inside xoppy_calc_undulator_radiation. ")

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

    gamma = ELECTRONENERGY / (codata_mee * 1e-3)


    resonance_wavelength = (1 + bl['Kv']**2 / 2.0) / 2 / gamma**2 * bl["PeriodID"]
    m2ev = codata.c * codata.h / codata.e      # lambda(m)  = m2eV / energy(eV)
    resonance_energy = m2ev / resonance_wavelength

    resonance_central_cone = 1.0/gamma*numpy.sqrt( (1+0.5*KV**2)/(2*NPERIODS*HARMONICNUMBER) )

    ring_order = 1

    resonance_ring = 1.0/gamma*numpy.sqrt( ring_order / HARMONICNUMBER * (1+0.5*KV**2) )

    # autoset energy
    if SETRESONANCE == 0:
        photonEnergyMin = PHOTONENERGYMIN
        photonEnergyMax = PHOTONENERGYMAX
        photonEnergyPoints = PHOTONENERGYPOINTS
    else:
        # referred to resonance
        photonEnergyMin = resonance_energy
        photonEnergyMax = resonance_energy + 1
        photonEnergyPoints = 1

    # autoset slit

    if SETRESONANCE == 0:
        pass
    elif SETRESONANCE == 1:
        MAXANGLE = 3 * 0.69 * resonance_central_cone
        bl['gapH'] = 2 * MAXANGLE * DISTANCE
        bl['gapV'] = 2 * MAXANGLE * DISTANCE
    elif SETRESONANCE == 2:
        MAXANGLE = 2.1 * resonance_ring
        bl['gapH'] = 2 * MAXANGLE * DISTANCE
        bl['gapV'] = 2 * MAXANGLE * DISTANCE


    #TODO SPEC file can be removed
    outFile = "undulator_radiation.spec"

    # Memorandum:
    # e = array with energy in eV
    # h = array with horizontal positions in mm
    # v = array with vertical positions in mm
    # p = array with photon flux in photons/s/0.1%bw/mm^2 with shape (Ne,Nh.Nv)
    if METHOD == 0:
        code = "US"
        print("Undulator radiation calculation using US. Please wait...")
        e,h,v,p = srundplug.calc3d_us(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,
                                    photonEnergyPoints=photonEnergyPoints,zero_emittance=zero_emittance)
    if METHOD == 1:
        code = "URGENT"
        print("Undulator radiation calculation using URGENT. Please wait...")
        e,h,v,p = srundplug.calc3d_urgent(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,
                                    photonEnergyPoints=photonEnergyPoints,zero_emittance=zero_emittance)
    if METHOD == 2:
        code = "SRW"
        print("Undulator radiation calculation using SRW. Please wait...")
        e,h,v,p = srundplug.calc3d_srw(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,
                                    photonEnergyPoints=photonEnergyPoints,zero_emittance=zero_emittance)
    if METHOD == 3:
        # todo too slow
        code = "pySRU"
        print("Undulator radiation calculation using SRW. Please wait...")
        e,h,v,p = srundplug.calc3d_pysru(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS,
                                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,
                                    photonEnergyPoints=photonEnergyPoints,zero_emittance=zero_emittance)


    print ("Gamma: %f \n"%(gamma))
    print ("Resonance wavelength (1st harmonic): %g A\n"%(1e10*resonance_wavelength))
    print ("Resonance energy (1st harmonic): %g eV\n"%(resonance_energy))
    if HARMONICNUMBER != 1:
        print ("Resonance wavelength (%d harmonic): %g A\n"%(HARMONICNUMBER,1e10*resonance_wavelength/HARMONICNUMBER))
        print ("Resonance energy (%d harmonic): %g eV\n"%(HARMONICNUMBER,HARMONICNUMBER*resonance_energy))
    print ("Resonance central cone (%d harmonic): %g urad\n"%(HARMONICNUMBER,1e6*resonance_central_cone))


    print ("Resonance first ring (%d harmonic): %g urad\n"%(HARMONICNUMBER,1e6*resonance_ring))

    print("Calculated %d photon energy points from %f to %f."%(photonEnergyPoints,photonEnergyMin,photonEnergyMax))

    if zero_emittance:
        print("No emittance.")

    print("Done")

    return e, h, v, p, code




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWundulator_radiation()
    w.show()
    app.exec()
    w.saveSettings()
