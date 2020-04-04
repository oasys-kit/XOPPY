import sys
import os

import numpy
import h5py

from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from oasys.util.oasys_util import TTYGrabber
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util.xoppy_xraylib_util import reflectivity_fresnel
from oasys.widgets.gui import ConfirmDialog

import scipy.constants as codata
import xraylib
from srxraylib.util.h5_simple_writer import H5SimpleWriter

class OWpower3Dcomponent(XoppyWidget):
    name = "Power3Dcomponent"
    id = "orange.widgets.datapower3D"
    description = "Power (vs Energy and spatial coordinates) Absorbed and Transmitted or Reflected by Optical Elements"
    icon = "icons/xoppy_power3d.png"
    priority = 2
    category = ""
    keywords = ["xoppy", "Undulator Radiation", "power3Dcomponent"]

    inputs = [{"name": "ExchangeData",
               "type": DataExchangeObject,
               "handler": "acceptExchangeData" } ]

    INPUT_BEAM_FROM = Setting(0)
    INPUT_BEAM_FILE = Setting("undulator_radiation.h5")

    EL1_FOR = Setting("Be")
    EL1_FLAG = Setting(0)  # 0=Filter 1=Mirror 2 = Aperture 3 magnifier
    EL1_THI = Setting(0.5)
    EL1_ANG = Setting(3.0)
    EL1_DEF = Setting(1) # deflection 0=H 1=V
    EL1_ROU = Setting(0.0)
    EL1_DEN = Setting("?")
    EL1_HGAP = Setting(1000.0)
    EL1_VGAP = Setting(1000.0)
    EL1_HMAG = Setting(1.0)
    EL1_VMAG = Setting(1.0)
    EL1_HROT = Setting(0.0)
    EL1_VROT = Setting(0.0)

    PLOT_SETS = Setting(1)
    FILE_DUMP = Setting(0)
    FILE_NAME = Setting("power3Dcomponent.h5")

    def build_gui(self):

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical",width=self.CONTROL_AREA_WIDTH-10)

        idx = -1
        box11 = gui.widgetBox(box, "Input beam")

        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box11)
        gui.comboBox(box1, self, "INPUT_BEAM_FROM",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['Oasys wire','h5 file (from undulator_radiation)'],
                    valueType=int, orientation="horizontal", callback=self.visibility_input_file, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 12 ***********   File Browser ******************
        idx += 1
        box1 = gui.widgetBox(box11)
        self.file_box_id = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal")
        self.file_id = oasysgui.lineEdit(self.file_box_id, self, "INPUT_BEAM_FILE", "File hdf5",
                                    labelWidth=100, valueType=str, orientation="horizontal")
        gui.button(self.file_box_id, self, "...", callback=self.select_input_file, width=25)


        #
        box11 = gui.widgetBox(box, "Optical element")
        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box11)
        gui.comboBox(box1, self, "EL1_FLAG",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['Filter', 'Mirror','Aperture','Magnifier','Screen Rotation'],
                    valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box11)
        gui.separator(box1, height=7)
        oasysgui.lineEdit(box1, self, "EL1_FOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        list_w = ["EL1_THI", "EL1_ANG", "EL1_DEF", "EL1_ROU", "EL1_DEN",
                  "EL1_HGAP", "EL1_VGAP", "EL1_HMAG", "EL1_VMAG",
                  "EL1_HROT", "EL1_VROT"]

        for el in list_w:
            idx += 1
            box1 = gui.widgetBox(box11)
            if el == "EL1_DEF":
                gui.comboBox(box1, self, el,
                             label=self.unitLabels()[idx], addSpace=False,
                             items=['Horizontal',
                                    'Vertical'],
                             valueType=int, orientation="horizontal", labelWidth=250)
            elif el == "EL1_DEN":
                oasysgui.lineEdit(box1, self, el,
                                  label=self.unitLabels()[idx], addSpace=False,
                                  valueType=str, orientation="horizontal", labelWidth=250)
            else:
                oasysgui.lineEdit(box1, self, el,
                                  label=self.unitLabels()[idx], addSpace=False,
                                  valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)


        box = gui.widgetBox(box, "Presentation")
        #widget index 41
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "PLOT_SETS",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['Input Beam',
                           'Element transmittance and absorbance',
                           'Absorbed by element',
                           'Transmitted/reflected by element'],
                    valueType=int, orientation="horizontal", labelWidth=100, callback=self.replot_results)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 42
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "FILE_DUMP",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes (hdf5)','Yes (x,y,absorption)', 'Yes (absorption matrix)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)
        oasysgui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        self.visibility_input_file()

    def set_EL_FLAG(self):
        self.initializeTabs()

    def unitLabels(self):
        labels = []
        labels.append('input beam from:')
        labels.append('input beam file:')
        labels.append('optical element is:')
        labels.append('formula: ')
        labels.append('Filter thick[mm]')
        labels.append('Mirror angle[mrad]')
        labels.append('Mirror deflection')
        labels.append('Roughness[A]')
        labels.append('Density [g/cm^3]')
        labels.append('H Size/Gap [mm]')
        labels.append('V Size/Gap [mm]')
        labels.append('H Magnification')
        labels.append('V Magnification')
        labels.append('Rotation angle around V axis [deg]')
        labels.append('Rotation angle around H axis [deg]')

        labels.append("Plot")
        labels.append("Write output file")
        labels.append("File name")

        return labels

    def unitFlags(self):
        flags =  []
        flags.append('True')  # input from
        flags.append('self.INPUT_BEAM_FROM  ==  1')  # input file
        flags.append('True')                   # kind
        flags.append('self.EL1_FLAG  <=  1')   # formula
        flags.append('self.EL1_FLAG  ==  0')   # thickness
        flags.append('self.EL1_FLAG  ==  1')   # angle
        flags.append('self.EL1_FLAG  ==  1')   # mirror deflection
        flags.append('self.EL1_FLAG  ==  1')   # roughness
        flags.append('self.EL1_FLAG  <=  1')   # density
        flags.append('self.EL1_FLAG  <=  2')   # gap
        flags.append('self.EL1_FLAG  <=  2')   # gap
        flags.append('self.EL1_FLAG  ==  3')   # magnification
        flags.append('self.EL1_FLAG  ==  3')   # magnification
        flags.append('self.EL1_FLAG  in (0, 4)')   # rotation
        flags.append('self.EL1_FLAG  in (0, 4)')   # rotation
        flags.append("True")
        flags.append("True")
        flags.append('self.FILE_DUMP >= 1')
        return flags

    def get_help_name(self):
        return 'power3dcomponent'

    def acceptExchangeData(self, exchangeData):
        try:
            if not exchangeData is None:
                if exchangeData.get_program_name() not in ["XOPPY", "UNDULATOR_RADIATION", "POWER3DCOMPONENT"]:
                        raise Exception("Xoppy Input beam not recognized")

                self.input_beam = exchangeData
                self.output_beam = None
                self.process_showers()
                self.compute()
        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

    def select_input_file(self):
        self.file_id.setText(oasysgui.selectFileFromDialog(self, self.INPUT_BEAM_FILE,
                                    "Open hdf File from Undulator Radiation",
                                    file_extension_filter="hdf5 Files (*.h5 *.hdf5)"))

    def visibility_input_file(self):
        self.file_box_id.setVisible(self.INPUT_BEAM_FROM == 1)

    def load_input_file(self):

        e, h, v, p, code = self.extract_data_from_h5file(self.INPUT_BEAM_FILE, "XOPPY_RADIATION")

        received_data = DataExchangeObject("XOPPY", "POWER3DCOMPONENT")
        received_data.add_content("xoppy_data", [p, e, h, v])
        received_data.add_content("xoppy_code", code)
        self.input_beam = received_data

        print("Input beam read from file %s \n\n"%self.INPUT_BEAM_FILE)

    # copied from undulator radiation ... TODO: put it in util?
    def extract_data_from_h5file(self, file_h5, subtitle):

        hf = h5py.File(file_h5, 'r')

        if not subtitle in hf:
            raise Exception("XOPPY_RADIATION not found in h5 file %s"%file_h5)

        try:
            p = hf[subtitle + "/Radiation/stack_data"][:]
            e = hf[subtitle + "/Radiation/axis0"][:]
            h = hf[subtitle + "/Radiation/axis1"][:]
            v = hf[subtitle + "/Radiation/axis2"][:]
        except:
            raise Exception("Error reading h5 file %s \n"%file_h5 + "\n" + str(e))

        code = "unknown"

        try:
            if hf[subtitle + "/parameters/METHOD"].value == 0:
                code = 'US'
            elif hf[subtitle + "/parameters/METHOD"].value == 1:
                code = 'URGENT'
            elif hf[subtitle + "/parameters/METHOD"].value == 2:
                code = 'SRW'
            elif hf[subtitle + "/parameters/METHOD"].value == 3:
                code = 'pySRU'
        except:
            pass

        hf.close()

        return e, h, v, p, code

    def check_fields(self):

        self.EL1_FOR = congruence.checkEmptyString(self.EL1_FOR, "1st oe formula")

        if self.EL1_FLAG == 0: # filter
            self.EL1_THI = congruence.checkStrictlyPositiveNumber(self.EL1_THI, "1st oe filter thickness")
            self.EL1_HROT = congruence.checkNumber(self.EL1_HROT, "1st oe rotation H")
            self.EL1_VROT = congruence.checkNumber(self.EL1_VROT, "1st oe rotation V")
        elif self.EL1_FLAG == 1: # mirror
            self.EL1_ANG = congruence.checkStrictlyPositiveNumber(self.EL1_ANG, "1st oe mirror angle")
            self.EL1_ROU = congruence.checkPositiveNumber(self.EL1_ROU, "1st oe mirror roughness")
            self.EL1_HROT = congruence.checkNumber(self.EL1_HROT, "1st oe rotation H")
            self.EL1_VROT = congruence.checkNumber(self.EL1_VROT, "1st oe rotation V")
            self.EL1_HGAP = congruence.checkStrictlyPositiveNumber(self.EL1_HGAP, "1st oe H gap")
            self.EL1_VGAP = congruence.checkPositiveNumber(self.EL1_VGAP, "1st oe V Gap")
        elif self.EL1_FLAG == 2: # aperture
            self.EL1_HGAP = congruence.checkStrictlyPositiveNumber(self.EL1_HGAP, "1st oe H gap")
            self.EL1_VGAP = congruence.checkPositiveNumber(self.EL1_VGAP, "1st oe V Gap")
        elif self.EL1_FLAG == 3: # magnifier
            self.EL1_HMAG = congruence.checkStrictlyPositiveNumber(self.EL1_HMAG, "1st oe H magnification")
            self.EL1_VMAG = congruence.checkPositiveNumber(self.EL1_VMAG, "1st oe V magnification")
        elif self.EL1_FLAG == 4: # rotation
            self.EL1_HROT = congruence.checkNumber(self.EL1_HROT, "1st oe rotation H")
            self.EL1_VROT = congruence.checkNumber(self.EL1_VROT, "1st oe rotation V")

    def do_xoppy_calculation(self):
        return self.xoppy_calc_power3Dcomponent()

    # TODO THIS TO SEND DATA

    def extract_data_from_xoppy_output(self, calculation_output):

        transmittance, absorbance, E, H, V = calculation_output
        p0, e0, h0, v0 = self.input_beam.get_content("xoppy_data")
        p = p0.copy()
        e = e0.copy()
        h = h0.copy()
        v = v0.copy()

        # coordinates to send: the same as incident beam (perpendicular to the optical axis)
        # except for the magnifier
        if self.EL1_FLAG ==  3: # magnifier  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            h *= self.EL1_HMAG
            v *= self.EL1_VMAG

        p_transmitted = p * transmittance / (h[0] / h0[0]) / (v[0] / v0[0])

        data_to_send = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        data_to_send.add_content("xoppy_data", [p_transmitted, e, h, v])
        data_to_send.add_content("xoppy_transmittivity", calculation_output)
        data_to_send.add_content("xoppy_code", "power3Dcomponent")

        self.output_beam = data_to_send

        return data_to_send


    # def extract_data_from_xoppy_output(self, calculation_output):
    #     return calculation_output

    def get_data_exchange_widget_name(self):
        return "POWER3DCOMPONENT"

    def getTitles(self):
        mylist = []
        if self.EL1_FLAG == 1:
            txt1 = "Reflectance "
            txt2 = "Reflected "
        else:
            txt1 = "Transmittance "
            txt2 = "Transmitted  "

        if self.PLOT_SETS == 0: # local
            for ii in ['Input Spectral Power Density vs E,X,Y',
                       'Input Power Density vs X,Y',
                       'Input Spectral Power vs E',]:
                mylist.append(ii)
        elif self.PLOT_SETS == 1: # input
            for ii in [txt1 + ' vs X,Y,E',
                       txt1 + ' vs E',
                       'Absorbance vs X,Y,E',
                       'Absorbance vs E', ]:
                mylist.append(ii)
        elif self.PLOT_SETS == 2:  # absorption
            for ii in ['Absorbed Spectral Power Density vs E,X,Y',
                       'Absorbed Power Density vs X,Y',
                       'Absorbed Spectral Power vs E']:
                mylist.append(ii)
        elif self.PLOT_SETS == 3: # transmittance/
            for ii in [
                    txt2 + 'Spectral Power Density vs E,X,Y',
                    txt2 + 'Power Density vs X,Y',
                    txt2 + 'Spectral Power vs E']:
                mylist.append(ii)

        return mylist


    def replot_results(self):
        if self.output_beam is None:
            pass
        else:
            self.plot_results(self.output_beam, progressBarValue=80)

    def plot_results(self, calculated_data, progressBarValue=80):
        current_index = self.tabs.currentIndex()
        if not self.view_type == 0:
            if calculated_data is None:
                raise Exception("Empty data")

            self.initializeTabs() # added by srio to avoid overlapping graphs

            self.view_type_combo.setEnabled(False)

            p0, e0, h0, v0 = self.input_beam.get_content("xoppy_data")
            p = p0.copy()
            e = e0.copy()
            h = h0.copy()
            v = v0.copy()
            p_spectral_power = p * codata.e * 1e3

            transmittance, absorbance, E, H, V = calculated_data.get_content("xoppy_transmittivity")

            if self.EL1_FLAG == 3:  # magnifier  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                h *= self.EL1_HMAG
                v *= self.EL1_VMAG

            if self.PLOT_SETS == 0:  # source
                # plot result s E,X,Y
                self.plot_data3D(p_spectral_power, e0, h0, v0, 0, 0,
                                 xtitle='H [mm]',
                                 ytitle='V [mm]',
                                 title='Input beam Spectral power density[W/eV/mm^2]',
                                 color_limits_uniform=False)
                self.tabs.setCurrentIndex(0)

                # plot result vs X,Y
                power_density = numpy.trapz(p_spectral_power, e0, axis=0)
                power_density_integral = integral_2d(power_density, h0, v0)
                self.plot_data2D(power_density, h0, v0, 1, 0,
                                 xtitle='H [mm]',
                                 ytitle='V [mm]',
                                 title='Input beam Power density [W/mm^2]. Integral: %6.3f W'%power_density_integral,)

                # plot result vs E
                spectral_density = numpy.trapz(numpy.trapz(p_spectral_power, v0, axis=2), h0, axis=1)
                spectral_density_integral = numpy.trapz(spectral_density, e0)
                self.plot_data1D(e, spectral_density, 2, 0,
                                 xtitle='Photon Energy [eV]',
                                 ytitle= 'Spectral power [W/eV]',
                                 title='Input beam Spectral power. Integral: %6.3f W'%spectral_density_integral,)

            if self.PLOT_SETS == 1:  # transmittance & absorbance
                # plot transmittance stack
                self.plot_data3D(transmittance, e, h, v, 0, 0,
                                 xtitle='H [mm] (normal to beam)',
                                 ytitle='V [mm] (normal to beam)',
                                 color_limits_uniform=True)
                self.tabs.setCurrentIndex(0)

                # plot transmittance spectrum
                if self.EL1_FLAG == 1:
                    ytitle = "Reflectance"
                else:
                    ytitle = "Transmittance"
                self.plot_data1D(e, numpy.trapz(numpy.trapz(transmittance, v, axis=2), h, axis=1) /
                                 (h[-1] - h[0]) / (v[-1] - v[0]), 1, 0,
                                 xtitle='Photon Energy [eV]',
                                 ytitle=ytitle,
                                 title='Integrated '+ytitle,)
                # self.tabs.setCurrentIndex(1)

                # plot absorbance stack
                self.plot_data3D(absorbance, E, H, V, 2, 0,
                                 xtitle='H [mm] (o.e. coordinates)',
                                 ytitle='V [mm] (o.e. coordinates)',
                                 color_limits_uniform=True)

                # plot absorbance spectrum
                self.plot_data1D(E, numpy.trapz(numpy.trapz(absorbance, V, axis=2), H, axis=1) / (H[-1] - H[0]) / (V[-1] - V[0]), 3, 0,
                                 xtitle='Photon Energy [eV]',
                                 ytitle='Absorbance',
                                 title='Integrated Absorbance',)

            if self.PLOT_SETS == 2:  # absorption by element
                p_absorbed = p_spectral_power * absorbance / (H[0] / h0[0]) / (V[0] / v0[0])
                # plot result vs E,X,Y
                self.plot_data3D(p_absorbed, E, H, V, 0, 0,
                                 xtitle='H [mm] (o.e. coordinates)',
                                 ytitle='V [mm] (o.e. coordinates)',
                                 title='Absorbed Spectral Power Density[W/eV/mm^2]',
                                 color_limits_uniform=False)
                self.tabs.setCurrentIndex(0)

                # plot result vs X,Y
                power_density = numpy.trapz(p_absorbed, E, axis=0)
                power_density_integral = integral_2d(power_density, H, V)
                self.plot_data2D(power_density, H, V, 1, 0,
                                 xtitle='H [mm] (o.e. coordinates)',
                                 ytitle='V [mm] (o.e. coordinates)',
                                 title='Absorbed Power Density [W/mm^2]. Integral: %6.3f W'%power_density_integral, )

                # plot result vs E
                spectral_density = numpy.trapz(numpy.trapz(p_absorbed, V, axis=2), H, axis=1)
                spectral_density_integral = numpy.trapz(spectral_density, E)
                self.plot_data1D(e, spectral_density, 2, 0,
                                 xtitle='Photon Energy [eV]',
                                 ytitle='Spectral power [W/eV]',
                                 title='Absorbed Spectral Power. Integral: %6.3f W'%spectral_density_integral, )

            if self.PLOT_SETS == 3:  # transmitted/reflected by element
                p_transmitted = p_spectral_power * transmittance / (h[0] / h0[0]) / (v[0] / v0[0])
                if self.EL1_FLAG == 1:
                    tr_ref_txt = "Reflected"
                else:
                    tr_ref_txt = "Transmitted"

                # plot result s E,X,Y
                self.plot_data3D(p_transmitted, e, h, v, 0, 0,
                                 xtitle='H [mm] (normal to beam)',
                                 ytitle='V [mm] (normal to beam)',
                                 title=tr_ref_txt+' Spectral Power Density[W/eV/mm^2]',
                                 color_limits_uniform=False)
                self.tabs.setCurrentIndex(0)

                # self.plot_data2D(p_transmitted.sum(axis=0) * energy_step, H, V, 1, 0,
                power_density = numpy.trapz(p_transmitted, E, axis=0)
                power_density_integral = integral_2d(power_density, h, v)
                self.plot_data2D(power_density, h, v, 1, 0,
                                 xtitle='H [mm] (normal to beam)',
                                 ytitle='V [mm] (normal to beam)',
                                 title=tr_ref_txt+' Power Density [W/mm^2]. Integral: %6.3f W'%power_density_integral, )

                # plot result vs E
                spectral_density = numpy.trapz(numpy.trapz(p_transmitted, v, axis=2), h, axis=1)
                spectral_density_integral = numpy.trapz(spectral_density, e)
                self.plot_data1D(e, spectral_density, 2, 0,
                                 xtitle='Photon Energy [eV]',
                                 ytitle='Spectral power [W/eV]',
                                 title=tr_ref_txt+' Spectral Power. Integral: %6.3f W'%spectral_density_integral, )

            self.view_type_combo.setEnabled(True)

            try:
                self.tabs.setCurrentIndex(current_index)
            except:
                pass

    # TODO: integrate this in ow_xoppy_widget
    def plot_data3D(self, data3D, dataE, dataX, dataY, tabs_canvas_index, plot_canvas_index,
                    title="", xtitle="", ytitle="", color_limits_uniform=False):

        from silx.gui.plot.StackView import StackViewMainWindow # TODO (re)move

        for i in range(1+self.tab[tabs_canvas_index].layout().count()):
            self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(i))

        #self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(0))


        xmin = numpy.min(dataX)
        xmax = numpy.max(dataX)
        ymin = numpy.min(dataY)
        ymax = numpy.max(dataY)


        stepX = dataX[1]-dataX[0]
        stepY = dataY[1]-dataY[0]
        if len(dataE) > 1: stepE = dataE[1]-dataE[0]
        else: stepE = 1.0

        if stepE == 0.0: stepE = 1.0
        if stepX == 0.0: stepX = 1.0
        if stepY == 0.0: stepY = 1.0

        dim0_calib = (dataE[0],stepE)
        dim1_calib = (ymin, stepY)
        dim2_calib = (xmin, stepX)


        data_to_plot = numpy.swapaxes(data3D,1,2)

        if color_limits_uniform:
            colormap = {"name":"temperature", "normalization":"linear", "autoscale":False, "vmin":data3D.min(), "vmax":data3D.max(), "colors":256}

        else:
            colormap = {"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256}

        self.plot_canvas[plot_canvas_index] = StackViewMainWindow()

        self.plot_canvas[plot_canvas_index].setGraphTitle(title)
        self.plot_canvas[plot_canvas_index].setLabels(["Photon Energy [eV]",ytitle,xtitle])
        self.plot_canvas[plot_canvas_index].setColormap(colormap=colormap)
        self.plot_canvas[plot_canvas_index].setTitleCallback(lambda idx: "Energy: %6.3f eV"%dataE[idx])

        self.plot_canvas[plot_canvas_index].setStack(numpy.array(data_to_plot),
                                                     calibrations=[dim0_calib, dim1_calib, dim2_calib] )
        self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])




    def xoppy_calc_power3Dcomponent(self):

        #
        # important: the transmittivity calculated here is referred on axes perp to the beam
        # therefore they do not include geometrical corrections for correct integral
        #

        substance = self.EL1_FOR
        thick     = self.EL1_THI
        angle     = self.EL1_ANG
        defection = self.EL1_DEF
        dens      = self.EL1_DEN
        roughness = self.EL1_ROU
        flags     = self.EL1_FLAG
        hgap = self.EL1_HGAP
        vgap = self.EL1_VGAP
        hmag = self.EL1_HMAG
        vmag = self.EL1_VMAG
        hrot = self.EL1_HROT
        vrot = self.EL1_VROT


        if self.INPUT_BEAM_FROM == 1:
            self.load_input_file()

        p0, e0, h0, v0 = self.input_beam.get_content("xoppy_data")

        p = p0.copy()
        e = e0.copy()
        h = h0.copy()
        v = v0.copy()

        transmittance = numpy.ones_like(p)
        E =  e.copy()
        H =  h.copy()
        V =  v.copy()

        # initialize results

        #
        # get undefined densities
        #
        if flags <= 1:
            try:  # apply written value
                rho = float(dens)
            except:   # in case of ?
                grabber = TTYGrabber()
                grabber.start()
                rho = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(substance))
                grabber.stop()
                for row in grabber.ttyData:
                    self.writeStdOut(row)
                print("Density for %s: %g g/cm3"%(substance,rho))
            dens = rho


        txt = ""

        if flags == 0:
            txt += '      *****   oe  [Filter] *************\n'
            txt += '      Material: %s\n'%(substance)
            txt += '      Density [g/cm^3]: %f \n'%(dens)
            txt += '      thickness [mm] : %f \n'%(thick)
            txt += '      H gap [mm]: %f \n'%(hgap)
            txt += '      V gap [mm]: %f \n'%(vgap)
            txt += '      H rotation angle [deg]: %f \n'%(hrot)
            txt += '      V rotation angle [deg]: %f \n'%(vrot)
        elif flags == 1:
            txt += '      *****   oe  [Mirror] *************\n'
            txt += '      Material: %s\n'%(substance)
            txt += '      Density [g/cm^3]: %f \n'%(dens)
            txt += '      grazing angle [mrad]: %f \n'%(angle)
            txt += '      roughness [A]: %f \n'%(roughness)
        elif flags == 2:
            txt += '      *****   oe  [Aperture] *************\n'
            txt += '      H gap [mm]: %f \n'%(hgap)
            txt += '      V gap [mm]: %f \n'%(vgap)
        elif flags == 3:
            txt += '      *****   oe  [Magnifier] *************\n'
            txt += '      H magnification: %f \n'%(hmag)
            txt += '      V magnification: %f \n'%(vmag)
        elif flags == 4:
            txt += '      *****   oe  [Screen rotated] *************\n'
            txt += '      H rotation angle [deg]: %f \n'%(hrot)
            txt += '      V rotation angle [deg]: %f \n'%(vrot)


        if flags == 0: # filter
            grabber = TTYGrabber()
            grabber.start()
            for j,energy in enumerate(e):
                tmp = xraylib.CS_Total_CP(substance,energy/1000.0)
                transmittance[j,:,:] = numpy.exp(-tmp*dens*(thick/10.0))

            grabber.stop()
            for row in grabber.ttyData:
                self.writeStdOut(row)

            # rotation
            H = h / numpy.cos(hrot * numpy.pi / 180)
            V = v / numpy.cos(vrot * numpy.pi / 180)

            # aperture
            h_indices_bad = numpy.where(numpy.abs(H) > 0.5*hgap)
            if len(h_indices_bad) > 0:
                transmittance[:, h_indices_bad, :] = 0.0
            v_indices_bad = numpy.where(numpy.abs(V) > 0.5*vgap)
            if len(v_indices_bad) > 0:
                transmittance[:, :, v_indices_bad] = 0.0

            absorbance = 1.0 - transmittance

        elif flags == 1: # mirror
            tmp = numpy.zeros(e.size)

            for j,energy in enumerate(e):
                tmp[j] = xraylib.Refractive_Index_Re(substance,energy/1000.0,dens)

            if tmp[0] == 0.0:
                raise Exception("Probably the substrance %s is wrong"%substance)

            delta = 1.0 - tmp
            beta = numpy.zeros(e.size)

            for j,energy in enumerate(e):
                beta[j] = xraylib.Refractive_Index_Im(substance,energy/1000.0,dens)

            try:
                (rs,rp,runp) = reflectivity_fresnel(refraction_index_beta=beta,refraction_index_delta=delta,\
                                            grazing_angle_mrad=angle,roughness_rms_A=roughness,\
                                            photon_energy_ev=e)
            except:
                raise Exception("Failed to run reflectivity_fresnel")

            for j,energy in enumerate(e):
                transmittance[j,:,:] = rs[j]

            # rotation
            if defection == 0: # horizontally deflecting
                H = h / numpy.sin(self.EL1_ANG * 1e-3)
            elif defection == 1: # vertically deflecting
                V = v / numpy.sin(self.EL1_ANG * 1e-3)

            # size
            absorbance = 1.0 - transmittance

            h_indices_bad = numpy.where(numpy.abs(H) > 0.5*hgap)
            if len(h_indices_bad) > 0:
                transmittance[:, h_indices_bad, :] = 0.0
                absorbance[:, h_indices_bad, :] = 0.0
            v_indices_bad = numpy.where(numpy.abs(V) > 0.5*vgap)
            if len(v_indices_bad) > 0:
                transmittance[:, :, v_indices_bad] = 0.0
                absorbance[:, :, v_indices_bad] = 0.0

        elif flags == 2:  # aperture
            h_indices_bad = numpy.where(numpy.abs(H) > 0.5*hgap)
            if len(h_indices_bad) > 0:
                transmittance[:, h_indices_bad, :] = 0.0
            v_indices_bad = numpy.where(numpy.abs(V) > 0.5*vgap)
            if len(v_indices_bad) > 0:
                transmittance[:, :, v_indices_bad] = 0.0

            absorbance = 1.0 - transmittance

        elif flags == 3:  # magnifier
            H = h * hmag
            V = v * vmag

            absorbance = 1.0 - transmittance

        elif flags == 4:  # rotation screen
            # transmittance[:, :, :] = numpy.cos(hrot * numpy.pi / 180) * numpy.cos(vrot * numpy.pi / 180)
            H = h / numpy.cos(hrot * numpy.pi / 180)
            V = v / numpy.cos(vrot * numpy.pi / 180)

            absorbance = 1.0 - transmittance

        txt += self.info_total_power(p, e, v, h, transmittance, absorbance)

        print(txt)

        calculated_data = (transmittance, absorbance, E, H, V)

        if self.FILE_DUMP == 0:
            pass
        elif self.FILE_DUMP == 1:
            self.xoppy_write_h5file(calculated_data)
        elif self.FILE_DUMP == 2:
            self.xoppy_write_txt(calculated_data, method="3columns")
        elif self.FILE_DUMP == 3:
            self.xoppy_write_txt(calculated_data, method="matrix")

        return calculated_data

    def info_total_power(self, p, e, v, h, transmittance, absorbance):
        txt = ""
        txt += "\n\n\n"
        power_input = integral_3d(p, e, h, v, method=0) * codata.e * 1e3
        txt += '      Input beam power: %f W\n'%(power_input)

        power_transmitted = integral_3d(p * transmittance, e, h, v, method=0) * codata.e * 1e3
        power_absorbed = integral_3d(p * absorbance, e, h, v, method=0) * codata.e * 1e3

        power_lost = power_input - ( power_transmitted +  power_absorbed)
        if numpy.abs( power_lost ) > 1e-9:
            txt += '      Beam power not considered (removed by o.e. acceptance): %6.3f W (accepted: %6.3f W)\n' % \
                   (power_lost, power_input - power_lost)

        txt += '      Beam power absorbed by optical element: %6.3f W\n' % power_absorbed

        if self.EL1_FLAG == 1:
            txt += '      Beam power reflected after optical element: %6.3f W\n' % power_transmitted
        else:
            txt += '      Beam power transmitted after optical element: %6.3f W\n' % power_transmitted

        return txt

    def xoppy_write_txt(self, calculated_data, method="3columns"):

        p0, e0, h0, v0 = self.input_beam.get_content("xoppy_data")
        p = p0.copy()
        p_spectral_power = p * codata.e * 1e3
        transmittance, absorbance, E, H, V = calculated_data

        if (os.path.splitext(self.FILE_NAME))[-1] not in [".txt",".dat",".TXT",".DAT"]:
            filename_alternative = (os.path.splitext(self.FILE_NAME))[0] + ".txt"
            tmp = ConfirmDialog.confirmed(self,
                                      message="Invalid file extension in output file: \n%s\nIt must be: .txt, .dat, .TXT, .DAT\nChange to: %s ?"%(self.FILE_NAME,filename_alternative),
                                      title="Invalid file extension")
            if tmp == False: return
            self.FILE_NAME = filename_alternative

        absorbed3d = p_spectral_power * absorbance / (H[0] / h0[0]) / (V[0] / v0[0])
        absorbed2d = numpy.trapz(absorbed3d, E, axis=0)

        f = open(self.FILE_NAME, 'w')
        if method == "3columns":
            for i in range(H.size):
                for j in range(V.size):
                    f.write("%g  %g  %g\n" % (H[i]*1e-3, V[i]*1e-3, absorbed2d[i,j]*1e-6))
        elif method == "matrix":
            f.write("%10.5g" % 0)
            for i in range(H.size):
                f.write(", %10.5g" % (H[i] * 1e-3))
            f.write("\n")

            for j in range(V.size):
                    f.write("%10.5g" % (V[j] * 1e-3))
                    for i in range(H.size):
                        f.write(", %10.5g" % (absorbed2d[i,j] * 1e-6))
                    f.write("\n")
        else:
            raise Exception("File type not understood.")
        f.close()

        print("File written to disk: %s" % self.FILE_NAME)

    def xoppy_write_h5file(self,calculated_data):

        p0, e0, h0, v0 = self.input_beam.get_content("xoppy_data")
        p = p0.copy()
        e = e0.copy()
        h = h0.copy()
        v = v0.copy()
        code = self.input_beam.get_content("xoppy_code")
        p_spectral_power = p * codata.e * 1e3
        transmittance, absorbance, E, H, V = calculated_data

        if (os.path.splitext(self.FILE_NAME))[-1] not in [".h5",".H5",".hdf5",".HDF5"]:
            filename_alternative = (os.path.splitext(self.FILE_NAME))[0] + ".h5"
            tmp = ConfirmDialog.confirmed(self,
                                      message="Invalid file extension in output file: \n%s\nIt must be: .h5, .H5, .hdf5, .HDF5\nChange to: %s ?"%(self.FILE_NAME,filename_alternative),
                                      title="Invalid file extension")
            if tmp == False: return
            self.FILE_NAME = filename_alternative

        try:
            h5w = H5SimpleWriter.initialize_file(self.FILE_NAME, creator="power3Dcomponent.py")
            txt = "\n\n\n"
            txt += self.info_total_power(p, e, v, h, transmittance, absorbance)
            h5w.add_key("info", txt, entry_name=None)
        except:
            print("ERROR writing h5 file (info)")


        try:
            #
            # source
            #
            entry_name = "source"

            h5w.create_entry(entry_name, nx_default=None)

            h5w.add_stack(e, h, v, p, stack_name="Radiation stack", entry_name=entry_name,
                          title_0="Photon energy [eV]",
                          title_1="X [mm] (normal to beam)",
                          title_2="Y [mm] (normal to beam)")

            h5w.add_image(numpy.trapz(p_spectral_power, E, axis=0) , H, V,
                          image_name="Power Density", entry_name=entry_name,
                          title_x="X [mm] (normal to beam)",
                          title_y="Y [mm] (normal to beam)")

            h5w.add_dataset(E, numpy.trapz(numpy.trapz(p_spectral_power, v, axis=2), h, axis=1),
                            entry_name=entry_name, dataset_name="Spectral power",
                            title_x="Photon Energy [eV]",
                            title_y="Spectral density [W/eV]")

        except:
            print("ERROR writing h5 file (source)")

        try:
            #
            # optical element
            #
            entry_name = "optical_element"

            h5w.create_entry(entry_name, nx_default=None)

            h5w.add_stack(E, H, V, transmittance, stack_name="Transmittance stack", entry_name=entry_name,
                          title_0="Photon energy [eV]",
                          title_1="X [mm] (o.e. coordinates)",
                          title_2="Y [mm] (o.e. coordinates)")

            absorbed = p_spectral_power * absorbance / (H[0] / h0[0]) / (V[0] / v0[0])
            h5w.add_image(numpy.trapz(absorbed, E, axis=0), H, V,
                          image_name="Absorbed Power Density on Element", entry_name=entry_name,
                          title_x="X [mm] (o.e. coordinates)",
                          title_y="Y [mm] (o.e. coordinates)")

            h5w.add_dataset(E, numpy.trapz(numpy.trapz(absorbed, v, axis=2), h, axis=1),
                            entry_name=entry_name, dataset_name="Absorbed Spectral Power",
                            title_x="Photon Energy [eV]",
                            title_y="Spectral density [W/eV]")

            #
            # transmitted
            #

            # coordinates to send: the same as incident beam (perpendicular to the optical axis)
            # except for the magnifier
            if self.EL1_FLAG == 3:  # magnifier <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                h *= self.EL1_HMAG
                v *= self.EL1_VMAG

            transmitted = p_spectral_power * transmittance / (h[0] / h0[0]) / (v[0] / v0[0])
            h5w.add_image(numpy.trapz(transmitted, E, axis=0), h, v,
                          image_name="Transmitted Power Density on Element", entry_name=entry_name,
                          title_x="X [mm] (normal to beam)",
                          title_y="Y [mm] (normal to beam)")

            h5w.add_dataset(E, numpy.trapz(numpy.trapz(transmitted, v, axis=2), h, axis=1),
                            entry_name=entry_name, dataset_name="Transmitted Spectral Power",
                            title_x="Photon Energy [eV]",
                            title_y="Spectral density [W/eV]")
        except:
            print("ERROR writing h5 file (optical element)")

        try:
            h5_entry_name = "XOPPY_RADIATION"

            h5w.create_entry(h5_entry_name,nx_default=None)
            h5w.add_stack(e, h, v, transmitted,stack_name="Radiation",entry_name=h5_entry_name,
                title_0="Photon energy [eV]",
                title_1="X gap [mm]",
                title_2="Y gap [mm]")
        except:
            print("ERROR writing h5 file (adding XOPPY_RADIATION)")



        print("File written to disk: %s" % self.FILE_NAME)

def integral_2d(data2D,h=None,v=None, method=0):
    if h is None:
        h = numpy.arange(data2D.shape[0])
    if v is None:
        v = numpy.arange(data2D.shape[1])

    if method == 0:
        totPower2 = numpy.trapz(data2D, v, axis=1)
        totPower2 = numpy.trapz(totPower2, h, axis=0)
    else:
        totPower2 = data2D.sum() * (h[1] - h[0]) * (v[1] - v[0])

    return totPower2


def integral_3d(data3D, e=None, h=None, v=None, method=0):
    if e is None:
        e = numpy.arange(data3D.shape[0])
    if h is None:
        h = numpy.arange(data3D.shape[1])
    if v is None:
        v = numpy.arange(data3D.shape[2])

    if method == 0:

        totPower2 = numpy.trapz(data3D, v, axis=2)
        totPower2 = numpy.trapz(totPower2, h, axis=1)
        totPower2 = numpy.trapz(totPower2, e, axis=0)
    else:
        totPower2 = data3D.sum() * (e[1] - e[0]) * (h[1] - h[0]) * (v[1] - v[0])

    return totPower2

if __name__ == "__main__":

    # # create unulator_radiation xoppy exchange data
    # from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_radiation
    # from oasys.widgets.exchange import DataExchangeObject
    #
    # e, h, v, p, code = xoppy_calc_undulator_radiation(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
    #                                    ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
    #                                    ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
    #                                    PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,
    #                                    SETRESONANCE=0,HARMONICNUMBER=1,
    #                                    GAPH=0.001,GAPV=0.001,\
    #                                    HSLITPOINTS=41,VSLITPOINTS=41,METHOD=2,
    #                                    PHOTONENERGYMIN=7000,PHOTONENERGYMAX=8100,PHOTONENERGYPOINTS=20,
    #                                    USEEMITTANCES=1)
    #
    # received_data = DataExchangeObject("XOPPY", "Power3Dcomponent")
    # received_data.add_content("xoppy_data", [p, e, h, v])
    # received_data.add_content("xoppy_code", code)


    #
    app = QApplication(sys.argv)
    w = OWpower3Dcomponent()

    # w.acceptExchangeData(received_data)

    w.show()
    app.exec()

    w.saveSettings()
