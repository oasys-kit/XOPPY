import sys
import numpy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from xoppylib.sources.xoppy_bm_wiggler import xoppy_calc_wiggler_radiation, create_magnetic_field_for_bending_magnet

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

try:
    from silx.gui.dialog.DataFileDialog import DataFileDialog
except:
    print("Fail to import silx.gui.dialog.DataFileDialog: need silx >= 0.7")

import scipy.constants as codata
import os
import h5py
from oasys.widgets.gui import ConfirmDialog

class OWwiggler_radiation(XoppyWidget, WidgetDecorator):
    name = "Wiggler Radiation"
    id = "wiggler_radiation"
    description = "Wiggler Radiation"
    icon = "icons/xoppy_wiggler_radiation.png"
    priority = 12
    category = ""
    keywords = ["xoppy", "wiggler_radiation"]

    # overwrite from
    outputs = [{"name": "xoppy_data",
                "type": DataExchangeObject,
                "doc": ""}]

    ELECTRONENERGY = Setting(3.0)
    ELECTRONCURRENT = Setting(0.1)
    PERIODID = Setting(0.120)
    NPERIODS = Setting(37.0)
    KV = Setting(22.416)
    DISTANCE = Setting(30.0)
    HSLITPOINTS = Setting(500)
    VSLITPOINTS = Setting(500)
    PHOTONENERGYMIN = Setting(100.0)
    PHOTONENERGYMAX = Setting(100100.0)
    PHOTONENERGYPOINTS = Setting(101)
    H5_FILE_DUMP = Setting(0)
    NTRAJPOINTS = Setting(1001)
    FIELD = Setting(0)
    FILE = Setting("")
    POLARIZATION = Setting(0)

    h5_file = Setting("wiggler_radiation.h5",)
    h5_entry_name = Setting("XOPPY_RADIATION",)
    h5_initialize = Setting(True,)
    h5_parameters = Setting(None,)

    SHIFT_X_FLAG = Setting(0)
    SHIFT_X_VALUE = Setting(0.0)
    SHIFT_BETAX_FLAG = Setting(0)
    SHIFT_BETAX_VALUE = Setting(0.0)
    CONVOLUTION = Setting(1)
    PASSEPARTOUT = Setting(3.0)

    bm_magnetic_radius = Setting(10.0)
    bm_magnetic_field = Setting(1.001)
    bm_divergence = Setting(1.0e-3)

    inputs = WidgetDecorator.syned_input_data()

    filename = ""

    # IS_DEVELOP = False

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        tab_1 = oasysgui.createTabPage(tabs_setting, self.name + " Input Parameters")
        tab_2 = oasysgui.createTabPage(tabs_setting, "Advanced Settings")

        box0 = oasysgui.widgetBox(tab_1, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-15)
        
        idx = -1 

        #
        #
        #

        box = oasysgui.widgetBox(box0, "Electron beam", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 15)

        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ELECTRONENERGY = oasysgui.lineEdit(box1, self, "ELECTRONENERGY",
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



        box = oasysgui.widgetBox(box0, "Wiggler", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 15)

        #widget index 0
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_FIELD = self.id_FIELD = gui.comboBox(box1, self, "FIELD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Sinusoidal', 'B from file', 'Bending magnet (cte B)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
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
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        self.id_KV = oasysgui.lineEdit(box1, self, "KV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        file_box = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal", height=25)
        self.le_file = oasysgui.lineEdit(file_box, self, "FILE",
                                         label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        gui.button(file_box, self, "...", callback=self.selectFile)


        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "bm_magnetic_radius", label=self.unitLabels()[idx], labelWidth=250,
                          callback=self.calculateMagneticField, tooltip=self.unitLabels()[idx], valueType=float,
                          orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "bm_magnetic_field", label=self.unitLabels()[idx], labelWidth=250,
                          callback=self.calculateMagneticRadius, tooltip=self.unitLabels()[idx], valueType=float,
                          orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "bm_divergence", label=self.unitLabels()[idx], labelWidth=250,
                          tooltip=self.unitLabels()[idx], valueType=float,
                          orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)




        box = oasysgui.widgetBox(box0, "Scan", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 15)
        #widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DISTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "HSLITPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "VSLITPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index <><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index <><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index <><>
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PHOTONENERGYPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)




        box = oasysgui.widgetBox(box0, "Output", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 15)
        #widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "H5_FILE_DUMP",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['None', 'Write h5 file: wiggler_radiation.h5','Read from file...'],
                    valueType=int, orientation="horizontal", labelWidth=250, callback=self.read_or_write_file)
        self.show_at(self.unitFlags()[idx], box1)



        #
        # advanced
        #
        box0 = oasysgui.widgetBox(tab_2, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 15)

        box = oasysgui.widgetBox(box0, "Electron trajectory", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 15)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "NTRAJPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "SHIFT_BETAX_FLAG", label=self.unitLabels()[idx], items=["No shift", "Half excursion", "Minimum", "Maximum", "Value at zero", "User value"], labelWidth=260, valueType=float, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "SHIFT_BETAX_VALUE", label=self.unitLabels()[idx], labelWidth=260, valueType=float, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "SHIFT_X_FLAG", label=self.unitLabels()[idx], items=["No shift", "Half excursion", "Minimum", "Maximum", "Value at zero", "User value"], labelWidth=260, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "SHIFT_X_VALUE", label=self.unitLabels()[idx], labelWidth=260, valueType=float, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)


        box = oasysgui.widgetBox(box0, "Photon divergence", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 15)
        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "CONVOLUTION", label=self.unitLabels()[idx], items=["No", "Yes [default]"], labelWidth=260, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "PASSEPARTOUT", label=self.unitLabels()[idx], labelWidth=260, valueType=float, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)


        box = oasysgui.widgetBox(box0, "Photon Polarization", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 15)
        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "POLARIZATION", label=self.unitLabels()[idx], items=["Total", "Parellel", "Perpendicular"], labelWidth=260, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)


    def unitLabels(self):
        return [
                "Electron Energy [GeV]",
                "Electron Current [A]",
                "Magnetic field: ",
                "Period ID [m]",
                "Number of periods",
                "Kv [K value vertical field]",
                'File/Url with Magnetic Field',
                'BM Magnetic radius [m]',
                'BM Magnetic field [T]',
                'BM divergence [rad]',
                "Distance to slit [m]",
                "Number of slit mesh points in H",
                "Number of slit mesh points in V",
                "Photon Energy Min [eV]",
                "Photon Energy Max [eV]",
                "Number of Photon Energy Points",
                "hdf5 file",
                'Number of traj points per period',
                "Shift Transversal Velocity",
                "Value",
                "Shift Transversal Coordinate",
                "Value",
                "Convolution electron x' with photon div",
                "Passepartout in sigma' units at Emin",
                "Polarization",
        ]

    # TODO check energy spread flag: set to False (not used at all)!!
    def unitFlags(self):
        flags = ["True"] * len(self.unitLabels())
        flags[3] = "self.FIELD == 0"
        flags[4] = "self.FIELD == 0"
        flags[5] = "self.FIELD == 0"
        flags[6] = "self.FIELD == 1"
        flags[7] = "self.FIELD == 2"
        flags[8] = "self.FIELD == 2"
        flags[9] = "self.FIELD == 2"
        flags[19] = "self.SHIFT_BETAX_FLAG == 5"
        flags[21] = "self.SHIFT_X_FLAG == 5"
        return flags

    def get_help_name(self):
        return 'wiggler_radiation'

    def selectFile(self):
        self.le_file.setText(oasysgui.selectFileFromDialog(self, self.FILE, "Open File with B map"))

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
                    QMessageBox.critical(self, "Error", str("Failed to load hdf5 /XOPPY_RADIATION"), QMessageBox.Ok)
                    calculation_output = None


            if calculation_output is None:
                QMessageBox.critical(self, "Error", str("Bad data from file."), QMessageBox.Ok)
            else:
                self.calculated_data = self.extract_data_from_xoppy_output(calculation_output)
                try:
                    self.set_fields_from_h5file(self.filename, "/XOPPY_RADIATION")
                except:
                    QMessageBox.critical(self, "Error", "Failed to set fields hdf5 /XOPPY_RADIATION/parameters \n", QMessageBox.Ok)


                # self.add_specific_content_to_calculated_data(self.calculated_data)
                #
                self.setStatusMessage("Plotting Results")

                self.plot_results(self.calculated_data, progressBarValue=60)

                self.setStatusMessage("")

                # p, e, h, v = self.calculated_data.get_content("xoppy_data")
                # traj = self.calculated_data.get_content("xoppy_data")
                # data_to_send = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
                # data_to_send.add_content("xoppy_data", [p, e, h, v, traj])
                self.send("xoppy_data", self.calculated_data)


            self.set_enabled(True)

    def extract_data_from_h5file(self,file_h5,subtitle):

        hf = h5py.File(file_h5,'r')

        try:
            p = hf[subtitle+"/Radiation/stack_data"][:]
            e = hf[subtitle+"/Radiation/axis0"][:]
            h = hf[subtitle+"/Radiation/axis1"][:]
            v = hf[subtitle+"/Radiation/axis2"][:]
            traj = hf[subtitle + "/trajectory/traj"][:]
        except:
            QMessageBox.critical(self, "Error", "Failed to load hdf5 data\n",
                                 QMessageBox.Ok)


        hf.close()

        return e, h, v, p, traj

    def set_fields_from_h5file(self,file_h5,subtitle):


        hf = h5py.File(file_h5,'r')


        self.ELECTRONENERGY          = hf[subtitle + "/parameters/ELECTRONENERGY"].value
        self.ELECTRONCURRENT         = hf[subtitle + "/parameters/ELECTRONCURRENT"].value
        self.PERIODID                = hf[subtitle + "/parameters/PERIODID"].value
        self.NPERIODS                = hf[subtitle + "/parameters/NPERIODS"].value
        self.KV                      = hf[subtitle + "/parameters/KV"].value
        self.DISTANCE                = hf[subtitle + "/parameters/DISTANCE"].value
        self.HSLITPOINTS             = hf[subtitle + "/parameters/HSLITPOINTS"].value
        self.VSLITPOINTS             = hf[subtitle + "/parameters/VSLITPOINTS"].value
        self.PHOTONENERGYMIN         = hf[subtitle + "/parameters/PHOTONENERGYMIN"].value
        self.PHOTONENERGYMAX         = hf[subtitle + "/parameters/PHOTONENERGYMAX"].value
        self.PHOTONENERGYPOINTS      = hf[subtitle + "/parameters/PHOTONENERGYPOINTS"].value

        self.FIELD = hf[subtitle + "/parameters/FIELD"].value
        self.FILE = hf[subtitle + "/parameters/FILE"].value
        self.POLARIZATION = hf[subtitle + "/parameters/POLARIZATION"].value
        self.CONVOLUTION = hf[subtitle + "/parameters/CONVOLUTION"].value
        self.PASSEPARTOUT = hf[subtitle + "/parameters/PASSEPARTOUT"].value

        self.SHIFT_X_FLAG = hf[subtitle + "/parameters/SHIFT_X_FLAG"].value
        self.SHIFT_BETAX_FLAG = hf[subtitle + "/parameters/SHIFT_BETAX_FLAG"].value
        self.SHIFT_X_VALUE = hf[subtitle + "/parameters/SHIFT_X_VALUE"].value
        self.SHIFT_BETAX_VALUE = hf[subtitle + "/parameters/SHIFT_BETAX_VALUE"].value


        hf.close()




    def check_fields(self):
        self.ELECTRONENERGY = congruence.checkStrictlyPositiveNumber(self.ELECTRONENERGY, "Electron Energy")
        self.ELECTRONCURRENT = congruence.checkStrictlyPositiveNumber(self.ELECTRONCURRENT, "Electron Current")

        self.PERIODID = congruence.checkStrictlyPositiveNumber(self.PERIODID, "Period ID")
        self.NPERIODS = congruence.checkStrictlyPositiveNumber(self.NPERIODS, "Number of Periods")
        self.KV = congruence.checkPositiveNumber(self.KV, "Kv")
        self.DISTANCE = congruence.checkStrictlyPositiveNumber(self.DISTANCE, "Distance to slit")

        self.PHOTONENERGYMIN = congruence.checkNumber(self.PHOTONENERGYMIN, "Photon Energy Min")
        self.PHOTONENERGYMAX = congruence.checkNumber(self.PHOTONENERGYMAX, "Photon Energy Max")
        congruence.checkGreaterOrEqualThan(self.PHOTONENERGYPOINTS, 2, "Number of Photon Energy Points", " 2")

        self.HSLITPOINTS = congruence.checkStrictlyPositiveNumber(self.HSLITPOINTS, "Number of slit mesh points in H")
        self.VSLITPOINTS = congruence.checkStrictlyPositiveNumber(self.VSLITPOINTS, "Number of slit mesh points in V")

        self.NTRAJPOINTS = congruence.checkStrictlyPositiveNumber(self.NTRAJPOINTS, "Number Trajectory points")

        self.PASSEPARTOUT = congruence.checkStrictlyPositiveNumber(self.PASSEPARTOUT, "Passepartout in units of sigma' at Emin")

    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:

                self.initializeTabs() # added by srio to avoid overlapping graphs

                self.view_type_combo.setEnabled(False)

                p, e, h, v = calculated_data.get_content("xoppy_data")
                traj = calculated_data.get_content("xoppy_trajectory")
                # code = calculated_data.get_content("xoppy_code")

                try:
                    self.plot_data3D(p, e, h, v, 0, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Flux [photons/s/0.1%bw/mm^2]',)

                    self.tabs.setCurrentIndex(0)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    if len(e) > 1:
                        energy_step = e[1]-e[0]
                    else:
                        energy_step = 1.0

                    self.plot_data2D(p.sum(axis=0)*energy_step*codata.e*1e3, h, v, 1, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Power density [W/mm^2]',)
                except Exception as exception:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise exception

                # except Exception as exception:
                #     QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)
                #
                #     if self.IS_DEVELOP: raise exception

                    return False

                try:
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0]), 2, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Flux [photons/s/0.1%bw]',
                                     title='Flux',)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    self.plot_data1D(e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*codata.e*1e3, 3, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Spectral power [W/eV]',
                                     title='Spectral power',)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    self.plot_data1D(traj[1,:],traj[0,:], 4, 0,
                                     xtitle="s [m]",
                                     ytitle="X [m]",
                                     title="Transversal Trajectory X(s)",)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise Exception("Data not plottable: bad content\n" + str(e))

                try:
                    self.plot_data1D(traj[1,:],traj[3,:], 5, 0,
                                     xtitle="s [m]",
                                     ytitle="betaX [c units]",
                                     title="Transversal velocity betaX(s)",)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise Exception("Data not plottable: bad content\n" + str(e))


                try:
                    self.plot_data1D(traj[1,:],traj[7,:], 6, 0,
                                     xtitle="s [m]",
                                     ytitle="Bz [T]",
                                     title="Magnetic field Bz(s)",)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)
                    QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)
                    if self.IS_DEVELOP: raise Exception("Data not plottable: bad content\n" + str(e))


                self.view_type_combo.setEnabled(True)
            else:
                QMessageBox.critical(self, "Error", "Empty data", QMessageBox.Ok)
                if self.IS_DEVELOP: raise Exception("Empty Data")


    def do_xoppy_calculation(self):

        if self.H5_FILE_DUMP == 0:
            h5_file = ""
        else:
            h5_file = "wiggler_radiation.h5"

        if self.FIELD == 0:
            FILE = ""
            FIELD = 0
        elif self.FIELD == 1:
            FILE = self.FILE
            FIELD = 1
        elif self.FIELD == 2:
            FILE = "bending_magnet_field.dat"
            create_magnetic_field_for_bending_magnet(do_plot=False, filename=FILE,
                            B0=self.bm_magnetic_field, divergence=self.bm_divergence, radius=self.bm_magnetic_radius,
                            npoints=self.NTRAJPOINTS)
            FIELD = 1



        if self.H5_FILE_DUMP == 0:
            h5_file = ""
        else:
            h5_file = "wiggler_radiation.h5"

        dict_parameters = {
                "ELECTRONENERGY"         : self.ELECTRONENERGY,
                "ELECTRONCURRENT"        : self.ELECTRONCURRENT,
                "PERIODID"               : self.PERIODID,
                "NPERIODS"               : self.NPERIODS,
                "KV"                     : self.KV,
                "DISTANCE"               : self.DISTANCE,
                "HSLITPOINTS"            : self.HSLITPOINTS,
                "VSLITPOINTS"            : self.VSLITPOINTS,
                "PHOTONENERGYMIN"        : self.PHOTONENERGYMIN,
                "PHOTONENERGYMAX"        : self.PHOTONENERGYMAX,
                "PHOTONENERGYPOINTS"     : self.PHOTONENERGYPOINTS,
                "FIELD"                  : FIELD,
                "FILE"                   : FILE,
                "POLARIZATION"           : self.POLARIZATION,
                "SHIFT_X_FLAG"           : self.SHIFT_X_FLAG,
                "SHIFT_X_VALUE"          : self.SHIFT_X_VALUE,
                "SHIFT_BETAX_FLAG"       : self.SHIFT_BETAX_FLAG,
                "SHIFT_BETAX_VALUE"      : self.SHIFT_BETAX_VALUE,
                "CONVOLUTION"            : self.CONVOLUTION,
                "PASSEPARTOUT"            : self.PASSEPARTOUT,
        }


        # write python script
        script = self.script_template().format_map(dict_parameters)
        self.xoppy_script.set_code(script)

        e, h, v, p, traj = xoppy_calc_wiggler_radiation(
                ELECTRONENERGY           = self.ELECTRONENERGY,
                ELECTRONCURRENT          = self.ELECTRONCURRENT,
                PERIODID                 = self.PERIODID,
                NPERIODS                 = self.NPERIODS,
                KV                       = self.KV,
                DISTANCE                 = self.DISTANCE,
                HSLITPOINTS              = self.HSLITPOINTS,
                VSLITPOINTS              = self.VSLITPOINTS,
                PHOTONENERGYMIN          = self.PHOTONENERGYMIN,
                PHOTONENERGYMAX          = self.PHOTONENERGYMAX,
                PHOTONENERGYPOINTS       = self.PHOTONENERGYPOINTS,
                FIELD                    = FIELD,
                FILE                     = FILE,
                POLARIZATION             = self.POLARIZATION,
                SHIFT_X_FLAG             = self.SHIFT_X_FLAG,
                SHIFT_X_VALUE            = self.SHIFT_X_VALUE,
                SHIFT_BETAX_FLAG         = self.SHIFT_BETAX_FLAG,
                SHIFT_BETAX_VALUE        = self.SHIFT_BETAX_VALUE,
                CONVOLUTION              = self.CONVOLUTION,
                PASSEPARTOUT             = self.PASSEPARTOUT,
                h5_file                  = h5_file,
                h5_entry_name            = "XOPPY_RADIATION",
                h5_initialize            = True,
                h5_parameters            = dict_parameters,
        )

        return e, h, v, p, traj, script


    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:wiggler_radiation)
#

from xoppylib.sources.xoppy_bm_wiggler import xoppy_calc_wiggler_radiation

h5_parameters = dict()
h5_parameters["ELECTRONENERGY"]          = {ELECTRONENERGY}
h5_parameters["ELECTRONCURRENT"]         = {ELECTRONCURRENT}
h5_parameters["PERIODID"]                = {PERIODID}
h5_parameters["NPERIODS"]                = {NPERIODS}
h5_parameters["KV"]                      = {KV}
h5_parameters["FIELD"]                   = {FIELD}   # 0= sinusoidal, 1=from file
h5_parameters["FILE"]                    = '{FILE}'
h5_parameters["POLARIZATION"]            = {POLARIZATION}  # 0=total, 1=s, 2=p
h5_parameters["DISTANCE"]                = {DISTANCE}
h5_parameters["HSLITPOINTS"]             = {HSLITPOINTS}
h5_parameters["VSLITPOINTS"]             = {VSLITPOINTS}
h5_parameters["PHOTONENERGYMIN"]         = {PHOTONENERGYMIN}
h5_parameters["PHOTONENERGYMAX"]         = {PHOTONENERGYMAX}
h5_parameters["PHOTONENERGYPOINTS"]      = {PHOTONENERGYPOINTS}
h5_parameters["SHIFT_X_FLAG"]            = {SHIFT_X_FLAG}
h5_parameters["SHIFT_X_VALUE"]           = {SHIFT_X_VALUE}
h5_parameters["SHIFT_BETAX_FLAG"]        = {SHIFT_BETAX_FLAG}
h5_parameters["SHIFT_BETAX_VALUE"]       = {SHIFT_BETAX_VALUE}
h5_parameters["CONVOLUTION"]             = {CONVOLUTION}
h5_parameters["PASSEPARTOUT"]            = {PASSEPARTOUT}

energy, horizontal, vertical, flux3D, traj = xoppy_calc_wiggler_radiation(
        ELECTRONENERGY           = h5_parameters["ELECTRONENERGY"]         ,
        ELECTRONCURRENT          = h5_parameters["ELECTRONCURRENT"]        ,
        PERIODID                 = h5_parameters["PERIODID"]               ,
        NPERIODS                 = h5_parameters["NPERIODS"]               ,
        KV                       = h5_parameters["KV"]                     ,
        FIELD                    = h5_parameters["FIELD"]                  ,
        FILE                     = h5_parameters["FILE"]                   ,
        POLARIZATION             = h5_parameters["POLARIZATION"]           ,
        DISTANCE                 = h5_parameters["DISTANCE"]               ,
        HSLITPOINTS              = h5_parameters["HSLITPOINTS"]            ,
        VSLITPOINTS              = h5_parameters["VSLITPOINTS"]            ,
        PHOTONENERGYMIN          = h5_parameters["PHOTONENERGYMIN"]        ,
        PHOTONENERGYMAX          = h5_parameters["PHOTONENERGYMAX"]        ,
        PHOTONENERGYPOINTS       = h5_parameters["PHOTONENERGYPOINTS"]     ,
        SHIFT_X_FLAG             = h5_parameters["SHIFT_X_FLAG"]           ,
        SHIFT_X_VALUE            = h5_parameters["SHIFT_X_VALUE"]          ,
        SHIFT_BETAX_FLAG         = h5_parameters["SHIFT_BETAX_FLAG"]       ,
        SHIFT_BETAX_VALUE        = h5_parameters["SHIFT_BETAX_VALUE"]      ,
        CONVOLUTION              = h5_parameters["CONVOLUTION"]            ,
        PASSEPARTOUT             = h5_parameters["PASSEPARTOUT"]            ,
        h5_file                  = "wiggler_radiation.h5"                  ,
        h5_entry_name            = "XOPPY_RADIATION"                       ,
        h5_initialize            = True                                    ,
        h5_parameters            = h5_parameters                           ,
        )

# example plot
from srxraylib.plot.gol import plot_image
plot_image(flux3D[0],horizontal,vertical,title="Flux [photons/s] per 0.1 bw per mm2 at %9.3f eV"%({PHOTONENERGYMIN}),xtitle="H [mm]",ytitle="V [mm]")
#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):
        e, h, v, p, traj, script = calculation_output

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        calculated_data.add_content("xoppy_data", [p, e, h, v])
        calculated_data.add_content("xoppy_trajectory", traj)
        calculated_data.add_content("xoppy_code", "srfunc")
        calculated_data.add_content("xoppy_script", script)
        return calculated_data

    def get_data_exchange_widget_name(self):
        return "WIGGLER_RADIATION"

    def getTitles(self):
        return ['Wiggler Flux vs E,X,Y',
                'Wiggler Power Density vs X,Y',
                'Wiggler Flux vs E',
                'Wiggler Spectral Power vs E',
                'e- trajectory',
                'e- velocity',
                'Bz']


    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data._light_source._magnetic_structure, synedid.InsertionDevice):
                light_source = data._light_source

                self.ELECTRONENERGY = light_source._electron_beam._energy_in_GeV
                self.ELECTRONCURRENT = light_source._electron_beam._current

                self.FIELD = 0
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
                self.id_ELECTRONCURRENT.setEnabled(True)
                self.id_PERIODID.setEnabled(True)
                self.id_NPERIODS.setEnabled(True)
                self.id_KV.setEnabled(True)
                self.id_FIELD.setEnabled(True)
        else:
                self.id_ELECTRONENERGY.setEnabled(False)
                self.id_ELECTRONCURRENT.setEnabled(False)
                self.id_PERIODID.setEnabled(False)
                self.id_NPERIODS.setEnabled(False)
                self.id_KV.setEnabled(False)
                self.id_FIELD.setEnabled(False)

    def calculateMagneticField(self):
        self.bm_magnetic_field = numpy.round((1e9/codata.c)*self.ELECTRONENERGY/self.bm_magnetic_radius, 3)

    def calculateMagneticRadius(self):
        self.bm_magnetic_radius = numpy.round(numpy.abs((1e9/codata.c)*self.ELECTRONENERGY/self.bm_magnetic_field), 3)

if __name__ == "__main__":

    from PyQt5.QtWidgets import QApplication

    bl = None

    LOAD_REMOTE_BEAMLINE = True

    if LOAD_REMOTE_BEAMLINE:
        try:
            from syned.util.json_tools import load_from_json_file, load_from_json_url
            from syned.storage_ring.light_source import LightSource
            from syned.beamline.beamline import Beamline

            # remote_file_name = "http://ftp.esrf.eu/pub/scisoft/syned/lightsources/ESRF_ID21_EBS_ppu42_17.json"
            remote_file_name = "http://ftp.esrf.eu/pub/scisoft/syned/lightsources/ESRF_ID17_LowBeta_HPW150_2.json"
            tmp = load_from_json_url(remote_file_name)
            if  isinstance(tmp,LightSource):
                bl = Beamline(tmp)
        except:
            pass



    app = QApplication(sys.argv)
    w = OWwiggler_radiation()
    w.IS_DEVELOP = True



    if bl is not None:
        w.receive_syned_data(bl)

    w.show()
    app.exec()
    w.saveSettings()
