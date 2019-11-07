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

try:
    from silx.gui.dialog.DataFileDialog import DataFileDialog
except:
    print("Fail to import silx.gui.dialog.DataFileDialog: need silx >= 0.7")

import scipy.constants as codata
import os
import h5py
from oasys.widgets.gui import ConfirmDialog

class OWundulator_radiation(XoppyWidget, WidgetDecorator):
    name = "Undulator Radiation"
    id = "orange.widgets.dataundulator_radiation"
    description = "Undulator Radiation"
    icon = "icons/xoppy_undulator_radiation.png"
    priority = 5
    category = ""
    keywords = ["xoppy", "undulator_radiation"]

    # overwrite from
    outputs = [{"name": "xoppy_data",
                "type": DataExchangeObject,
                "doc": ""}]

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
    H5_FILE_DUMP = Setting(0)

    inputs = WidgetDecorator.syned_input_data()

    filename = ""

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        tab_1 = oasysgui.createTabPage(tabs_setting, self.name + " Input Parameters")
        tab_2 = oasysgui.createTabPage(tabs_setting, "Calculation Setting")

        box = oasysgui.widgetBox(tab_1, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-15)
        
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

        #widget index 9B
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KH = oasysgui.lineEdit(box1, self, "KH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9C
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KPHASE = oasysgui.lineEdit(box1, self, "KPHASE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        box = oasysgui.widgetBox(tab_2, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-15)

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


        #widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "H5_FILE_DUMP",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['None', 'Write h5 file: undulator_radiation.h5','Read from file...'],
                    valueType=int, orientation="horizontal", labelWidth=250, callback=self.read_or_write_file)
        self.show_at(self.unitFlags()[idx], box1)

    def read_or_write_file(self):

        value = self.H5_FILE_DUMP

        if value == 0:
            return
        elif value == 1: # write
            return
        elif value == 2: # read

            self.H5_FILE_DUMP = 0

            use_silx_file_dialog = False   # silx dialog is freezing the linux system, change to traditional

            if use_silx_file_dialog:
                tmp = ConfirmDialog.confirmed(self,
                        message="Please select in a hdf5 file a data block\n(such as XOPPY_RADIATION)\nthat contains a 'Radiation' entry",
                        title="Confirm Action")
                if tmp == False: return
                dialog = DataFileDialog(self)
                dialog.setFilterMode(DataFileDialog.FilterMode.ExistingGroup)
                result = dialog.exec_()
                if not result:
                    return
                print(dialog.selectedFile())
                print(dialog.selectedUrl())
                print(dialog.selectedDataUrl().data_path())
                calculation_output = self.extract_data_from_h5file(dialog.selectedFile(), dialog.selectedDataUrl().data_path() )
                self.filename = dialog.selectedFile()
            else:
                tmp = ConfirmDialog.confirmed(self,
                        message="Please select a hdf5 file containing a data block\n named XOPPY_RADIATION which includes 'Radiation' entry",
                        title="Confirm Action")
                if tmp == False: return

                self.filename = oasysgui.selectFileFromDialog(self,
                                    previous_file_path=self.filename,
                                    message="Open hdf5 File",
                                    start_directory="",
                                    file_extension_filter="*.*5")
                if self.filename == "":
                    return

                try:
                    calculation_output = self.extract_data_from_h5file(self.filename, "/XOPPY_RADIATION" )
                except:
                    calculation_output = None


            if calculation_output is None:
                raise Exception("Bad data from file.")
            else:
                self.calculated_data = self.extract_data_from_xoppy_output(calculation_output)
                try:
                    self.set_fields_from_h5file(self.filename, "/XOPPY_RADIATION")
                except:
                    pass

                # self.add_specific_content_to_calculated_data(self.calculated_data)
                #
                self.setStatusMessage("Plotting Results")

                self.plot_results(self.calculated_data, progressBarValue=60)

                self.setStatusMessage("")

                self.send("xoppy_data", self.calculated_data)


            self.set_enabled(True)

    def extract_data_from_h5file(self,file_h5,subtitle):

        hf = h5py.File(file_h5,'r')

        try:
            p = hf[subtitle+"/Radiation/stack_data"].value
            e = hf[subtitle+"/Radiation/axis0"].value
            h = hf[subtitle+"/Radiation/axis1"].value
            v = hf[subtitle+"/Radiation/axis2"].value
        except:
            raise Exception("Data not plottable: bad content\n" + str(e))

        code = "unknown"

        try:
            if hf[subtitle+"/parameters/METHOD"].value == 0:
                code = 'US'
            elif hf[subtitle+"/parameters/METHOD"].value == 1:
                code = 'URGENT'
            elif hf[subtitle+"/parameters/METHOD"].value == 2:
                code = 'SRW'
            elif hf[subtitle+"/parameters/METHOD"].value == 3:
                code = 'pySRU'
        except:
            pass

        hf.close()

        return e, h, v, p, code

    def set_fields_from_h5file(self,file_h5,subtitle):

        hf = h5py.File(file_h5,'r')

        self.METHOD                  = hf[subtitle + "/parameters/METHOD"].value
        self.USEEMITTANCES           = hf[subtitle + "/parameters/USEEMITTANCES"].value
        self.ELECTRONENERGY          = hf[subtitle + "/parameters/ELECTRONENERGY"].value
        self.ELECTRONENERGYSPREAD    = hf[subtitle + "/parameters/ELECTRONENERGYSPREAD"].value
        self.ELECTRONCURRENT         = hf[subtitle + "/parameters/ELECTRONCURRENT"].value
        self.ELECTRONBEAMSIZEH       = hf[subtitle + "/parameters/ELECTRONBEAMSIZEH"].value
        self.ELECTRONBEAMSIZEV       = hf[subtitle + "/parameters/ELECTRONBEAMSIZEV"].value
        self.ELECTRONBEAMDIVERGENCEH = hf[subtitle + "/parameters/ELECTRONBEAMDIVERGENCEH"].value
        self.ELECTRONBEAMDIVERGENCEV = hf[subtitle + "/parameters/ELECTRONBEAMDIVERGENCEV"].value
        self.PERIODID                = hf[subtitle + "/parameters/PERIODID"].value
        self.NPERIODS                = hf[subtitle + "/parameters/NPERIODS"].value
        self.KV                      = hf[subtitle + "/parameters/KV"].value
        self.KH                      = hf[subtitle + "/parameters/KH"].value
        self.KPHASE                  = hf[subtitle + "/parameters/KPHASE"].value
        self.DISTANCE                = hf[subtitle + "/parameters/DISTANCE"].value
        self.SETRESONANCE            = hf[subtitle + "/parameters/SETRESONANCE"].value
        self.HARMONICNUMBER          = hf[subtitle + "/parameters/HARMONICNUMBER"].value
        self.GAPH                    = hf[subtitle + "/parameters/GAPH"].value
        self.GAPV                    = hf[subtitle + "/parameters/GAPV"].value
        self.HSLITPOINTS             = hf[subtitle + "/parameters/HSLITPOINTS"].value
        self.VSLITPOINTS             = hf[subtitle + "/parameters/VSLITPOINTS"].value
        self.PHOTONENERGYMIN         = hf[subtitle + "/parameters/PHOTONENERGYMIN"].value
        self.PHOTONENERGYMAX         = hf[subtitle + "/parameters/PHOTONENERGYMAX"].value
        self.PHOTONENERGYPOINTS      = hf[subtitle + "/parameters/PHOTONENERGYPOINTS"].value

        hf.close()


    def unitLabels(self):
        return ["Use emittances","Electron Energy [GeV]", "Electron Energy Spread", "Electron Current [A]",
                "Electron Beam Size H [m]", "Electron Beam Size V [m]","Electron Beam Divergence H [rad]", "Electron Beam Divergence V [rad]",
                "Period ID [m]", "Number of periods","Kv [K value vertical field]",
                "Kh [K value horizontal field]","Kphase [phase diff Kh - Kv in rad]",
                "Distance to slit [m]",
                "Set photon energy and slit","Harmonic number",
                "Slit gap H [m]", "Slit gap V [m]",
                "Number of slit mesh points in H", "Number of slit mesh points in V",
                "Photon Energy Min [eV]","Photon Energy Max [eV]","Number of Photon Energy Points",
                "calculation code","hdf5 file"]

    # TODO check energy spread flag: set to False (not used at all)!!
    def unitFlags(self):
        return ["True", "True", "False", "True",
                "self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1","self.USEEMITTANCES == 1", "self.USEEMITTANCES == 1",
                "True", "True", "True",
                "self.METHOD != 0","self.METHOD != 0",
                "True",
                "True", "self.SETRESONANCE > 0",
                "self.SETRESONANCE == 0", "self.SETRESONANCE == 0",
                "True", "True",
                "self.SETRESONANCE == 0", "self.SETRESONANCE == 0","self.SETRESONANCE == 0",
                "True","True"]

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
        self.KH = congruence.checkPositiveNumber(self.KH, "Kh")
        self.KPHASE = congruence.checkNumber(self.KPHASE, "KPHASE")
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

                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))


                try:
                    print("\nResult arrays (shapes): ",e.shape,h.shape,v.shape,p.shape)
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0]), 2, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Flux [photons/s/0.1%bw]',
                                     title='Code '+code+'; Flux',)

                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    print("\nResult arrays (shapes): ",e.shape,h.shape,v.shape,p.shape)
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*codata.e*1e3, 3, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Spectral power [W/eV]',
                                     title='Code '+code+'; Spectral power',)

                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(e))


                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")


    def do_xoppy_calculation(self):

        if self.H5_FILE_DUMP == 0:
            h5_file = ""
        else:
            h5_file = "undulator_radiation.h5"

        dict_parameters = {
                "ELECTRONENERGY"         : self.ELECTRONENERGY,
                "ELECTRONENERGYSPREAD"   : self.ELECTRONENERGYSPREAD,
                "ELECTRONCURRENT"        : self.ELECTRONCURRENT,
                "ELECTRONBEAMSIZEH"      : self.ELECTRONBEAMSIZEH,
                "ELECTRONBEAMSIZEV"      : self.ELECTRONBEAMSIZEV,
                "ELECTRONBEAMDIVERGENCEH": self.ELECTRONBEAMDIVERGENCEH,
                "ELECTRONBEAMDIVERGENCEV": self.ELECTRONBEAMDIVERGENCEV,
                "PERIODID"               : self.PERIODID,
                "NPERIODS"               : self.NPERIODS,
                "KV"                     : self.KV,
                "KH"                     : self.KH,
                "KPHASE"                 : self.KPHASE,
                "DISTANCE"               : self.DISTANCE,
                "SETRESONANCE"           : self.SETRESONANCE,
                "HARMONICNUMBER"         : self.HARMONICNUMBER,
                "GAPH"                   : self.GAPH,
                "GAPV"                   : self.GAPV,
                "HSLITPOINTS"            : self.HSLITPOINTS,
                "VSLITPOINTS"            : self.VSLITPOINTS,
                "METHOD"                 : self.METHOD,
                "PHOTONENERGYMIN"        : self.PHOTONENERGYMIN,
                "PHOTONENERGYMAX"        : self.PHOTONENERGYMAX,
                "PHOTONENERGYPOINTS"     : self.PHOTONENERGYPOINTS,
                "USEEMITTANCES"          : self.USEEMITTANCES,
        }


        # write python script
        self.xoppy_script.set_code(self.script_template().format_map(dict_parameters))

        return xoppy_calc_undulator_radiation(
                ELECTRONENERGY           = self.ELECTRONENERGY,
                ELECTRONENERGYSPREAD     = self.ELECTRONENERGYSPREAD,
                ELECTRONCURRENT          = self.ELECTRONCURRENT,
                ELECTRONBEAMSIZEH        = self.ELECTRONBEAMSIZEH,
                ELECTRONBEAMSIZEV        = self.ELECTRONBEAMSIZEV,
                ELECTRONBEAMDIVERGENCEH  = self.ELECTRONBEAMDIVERGENCEH,
                ELECTRONBEAMDIVERGENCEV  = self.ELECTRONBEAMDIVERGENCEV,
                PERIODID                 = self.PERIODID,
                NPERIODS                 = self.NPERIODS,
                KV                       = self.KV,
                KH                       = self.KH,
                KPHASE                   = self.KPHASE,
                DISTANCE                 = self.DISTANCE,
                SETRESONANCE             = self.SETRESONANCE,
                HARMONICNUMBER           = self.HARMONICNUMBER,
                GAPH                     = self.GAPH,
                GAPV                     = self.GAPV,
                HSLITPOINTS              = self.HSLITPOINTS,
                VSLITPOINTS              = self.VSLITPOINTS,
                METHOD                   = self.METHOD,
                PHOTONENERGYMIN          = self.PHOTONENERGYMIN,
                PHOTONENERGYMAX          = self.PHOTONENERGYMAX,
                PHOTONENERGYPOINTS       = self.PHOTONENERGYPOINTS,
                USEEMITTANCES            = self.USEEMITTANCES,
                h5_file                  = h5_file,
                h5_entry_name            = "XOPPY_RADIATION",
                h5_initialize            = True,
                h5_parameters            = dict_parameters,
        )


    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:undulator_radiation)
#
from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_radiation

h5_parameters = dict()
h5_parameters["ELECTRONENERGY"]          = {ELECTRONENERGY}
h5_parameters["ELECTRONENERGYSPREAD"]    = {ELECTRONENERGYSPREAD}
h5_parameters["ELECTRONCURRENT"]         = {ELECTRONCURRENT}
h5_parameters["ELECTRONBEAMSIZEH"]       = {ELECTRONBEAMSIZEH}
h5_parameters["ELECTRONBEAMSIZEV"]       = {ELECTRONBEAMSIZEV}
h5_parameters["ELECTRONBEAMDIVERGENCEH"] = {ELECTRONBEAMDIVERGENCEH}
h5_parameters["ELECTRONBEAMDIVERGENCEV"] = {ELECTRONBEAMDIVERGENCEV}
h5_parameters["PERIODID"]                = {PERIODID}
h5_parameters["NPERIODS"]                = {NPERIODS}
h5_parameters["KV"]                      = {KV}
h5_parameters["KH"]                      = {KH}
h5_parameters["KPHASE"]                  = {KPHASE}
h5_parameters["DISTANCE"]                = {DISTANCE}
h5_parameters["SETRESONANCE"]            = {SETRESONANCE}
h5_parameters["HARMONICNUMBER"]          = {HARMONICNUMBER}
h5_parameters["GAPH"]                    = {GAPH}
h5_parameters["GAPV"]                    = {GAPV}
h5_parameters["HSLITPOINTS"]             = {HSLITPOINTS}
h5_parameters["VSLITPOINTS"]             = {VSLITPOINTS}
h5_parameters["METHOD"]                  = {METHOD}
h5_parameters["PHOTONENERGYMIN"]         = {PHOTONENERGYMIN}
h5_parameters["PHOTONENERGYMAX"]         = {PHOTONENERGYMAX}
h5_parameters["PHOTONENERGYPOINTS"]      = {PHOTONENERGYPOINTS}
h5_parameters["USEEMITTANCES"]           = {USEEMITTANCES}

e, h, v, p, code = xoppy_calc_undulator_radiation(
        ELECTRONENERGY           = h5_parameters["ELECTRONENERGY"]         ,
        ELECTRONENERGYSPREAD     = h5_parameters["ELECTRONENERGYSPREAD"]   ,
        ELECTRONCURRENT          = h5_parameters["ELECTRONCURRENT"]        ,
        ELECTRONBEAMSIZEH        = h5_parameters["ELECTRONBEAMSIZEH"]      ,
        ELECTRONBEAMSIZEV        = h5_parameters["ELECTRONBEAMSIZEV"]      ,
        ELECTRONBEAMDIVERGENCEH  = h5_parameters["ELECTRONBEAMDIVERGENCEH"],
        ELECTRONBEAMDIVERGENCEV  = h5_parameters["ELECTRONBEAMDIVERGENCEV"],
        PERIODID                 = h5_parameters["PERIODID"]               ,
        NPERIODS                 = h5_parameters["NPERIODS"]               ,
        KV                       = h5_parameters["KV"]                     ,
        KH                       = h5_parameters["KH"]                     ,
        KPHASE                   = h5_parameters["KPHASE"]                 ,
        DISTANCE                 = h5_parameters["DISTANCE"]               ,
        SETRESONANCE             = h5_parameters["SETRESONANCE"]           ,
        HARMONICNUMBER           = h5_parameters["HARMONICNUMBER"]         ,
        GAPH                     = h5_parameters["GAPH"]                   ,
        GAPV                     = h5_parameters["GAPV"]                   ,
        HSLITPOINTS              = h5_parameters["HSLITPOINTS"]            ,
        VSLITPOINTS              = h5_parameters["VSLITPOINTS"]            ,
        METHOD                   = h5_parameters["METHOD"]                 ,
        PHOTONENERGYMIN          = h5_parameters["PHOTONENERGYMIN"]        ,
        PHOTONENERGYMAX          = h5_parameters["PHOTONENERGYMAX"]        ,
        PHOTONENERGYPOINTS       = h5_parameters["PHOTONENERGYPOINTS"]     ,
        USEEMITTANCES            = h5_parameters["USEEMITTANCES"]          ,
        h5_file                  = "undulator_radiation.h5",
        h5_entry_name            = "XOPPY_RADIATION",
        h5_initialize            = True,
        h5_parameters            = h5_parameters, 
        )

# example plot
from srxraylib.plot.gol import plot_image
plot_image(p[0],h,v,title="Flux [photons/s] per 0.1 bw per mm2 at %9.3f eV"%({PHOTONENERGYMIN}),xtitle="H [mm]",ytitle="V [mm]")
#
# end script
#
"""

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
                self.KH = light_source._magnetic_structure._K_horizontal
                # TODO: self.KPHASE = ... define and import it in SYNED

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



    bl = None

    LOAD_REMOTE_BEAMLINE = False

    if LOAD_REMOTE_BEAMLINE:
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
