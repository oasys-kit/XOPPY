import sys
import numpy
from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence


from oasys.widgets.exchange import DataExchangeObject
# from orangecontrib.xoppy.util.xoppy_exchange import RadiationDataExchangeObject #as DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util.xoppy_xraylib_util import reflectivity_fresnel

import scipy.constants as codata
import xraylib

from srxraylib.util.h5_simple_writer import H5SimpleWriter

from oasys.widgets.gui import ConfirmDialog

class OWpower3D(XoppyWidget):
    name = "POWER3D"
    id = "orange.widgets.datapower3D"
    description = "Power (vs Energy and spatial coordinates) Absorbed and Transmitted by Optical Elements"
    icon = "icons/obsolete_power3d.png"
    priority = 3
    category = ""
    keywords = ["xoppy", "power3D"]

    inputs = [{"name": "ExchangeData",
               "type": DataExchangeObject,
               "handler": "acceptExchangeData" } ]
    # [("ExchangeData", DataExchangeObject, "acceptExchangeData")]
    # inputs = [("xoppy_data", DataExchangeObject, "acceptExchangeData")]



    NELEMENTS = Setting(1)

    MAX_OE = 5

    EL1_FOR = Setting("Be")
    EL1_FLAG = Setting(4)  # 0=Filter 1=Mirror 2 = Aperture 3 magnifier
    EL1_THI = Setting(0.5)
    EL1_ANG = Setting(3.0)
    EL1_ROU = Setting(0.0)
    EL1_DEN = Setting("?")
    EL1_HGAP = Setting(0.1)
    EL1_VGAP = Setting(0.1)
    EL1_HMAG = Setting(1.0)
    EL1_VMAG = Setting(1.0)
    EL1_HROT = Setting(0.0)
    EL1_VROT = Setting(0.0)

    EL2_FOR = Setting("Rh")
    EL2_FLAG = Setting(3)
    EL2_THI = Setting(0.5)
    EL2_ANG = Setting(3.0)
    EL2_ROU = Setting(0.0)
    EL2_DEN = Setting("?")
    EL2_HGAP = Setting(100.0)
    EL2_VGAP = Setting(100.0)
    EL2_HMAG = Setting(2.0)
    EL2_VMAG = Setting(2.0)
    EL2_HROT = Setting(0.0)
    EL2_VROT = Setting(0.0)

    EL3_FOR = Setting("Al")
    EL3_FLAG = Setting(0)
    EL3_THI = Setting(0.5)
    EL3_ANG = Setting(3.0)
    EL3_ROU = Setting(0.0)
    EL3_DEN = Setting("?")
    EL3_HGAP = Setting(100.0)
    EL3_VGAP = Setting(100.0)
    EL3_HMAG = Setting(2.0)
    EL3_VMAG = Setting(2.0)
    EL3_HROT = Setting(0.0)
    EL3_VROT = Setting(0.0)

    EL4_FOR = Setting("B")
    EL4_FLAG = Setting(0)
    EL4_THI = Setting(0.5)
    EL4_ANG = Setting(3.0)
    EL4_ROU = Setting(0.0)
    EL4_DEN = Setting("?")
    EL4_HGAP = Setting(100.0)
    EL4_VGAP = Setting(100.0)
    EL4_HMAG = Setting(1.0)
    EL4_VMAG = Setting(1.0)
    EL4_HROT = Setting(0.0)
    EL4_VROT = Setting(0.0)

    EL5_FOR = Setting("Pt")
    EL5_FLAG = Setting(1)
    EL5_THI = Setting(0.5)
    EL5_ANG = Setting(3.0)
    EL5_ROU = Setting(0.0)
    EL5_DEN = Setting("?")
    EL5_HGAP = Setting(100.0)
    EL5_VGAP = Setting(100.0)
    EL5_HMAG = Setting(1.0)
    EL5_VMAG = Setting(1.0)
    EL5_HROT = Setting(0.0)
    EL5_VROT = Setting(0.0)

    PLOT_SETS = Setting(1)
    FILE_DUMP = 0

    def build_gui(self):

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        idx = -1 


        #widget index 10
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "NELEMENTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['0','1', '2', '3', '4', '5'],
                    valueType=int, orientation="horizontal", callback=self.set_NELEMENTS, labelWidth=330)
        self.show_at(self.unitFlags()[idx], box1)





        #############################LOOP OVER OE###########################

        for oe_n in range(1,1+self.MAX_OE):
            box11 = gui.widgetBox(box)
            #widget index 12
            idx += 1
            box1 = gui.widgetBox(box11)
            gui.comboBox(box1, self, "EL%d_FLAG"%oe_n,
                        label=self.unitLabels()[idx], addSpace=False,
                        items=['Filter', 'Mirror','Aperture','Magnifier','Screen Rotation'],
                        valueType=int, orientation="horizontal", callback=self.set_EL_FLAG, labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)

            #widget index 11
            idx += 1
            box1 = gui.widgetBox(box11)
            gui.separator(box1, height=7)
            oasysgui.lineEdit(box1, self, "EL%d_FOR"%oe_n,
                         label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
            self.show_at(self.unitFlags()[idx], box1)


            list_w = ["EL%d_THI"%oe_n,"EL%d_ANG"%oe_n,"EL%d_ROU"%oe_n,"EL%d_DEN"%oe_n,
                      "EL%d_HGAP"%oe_n,"EL%d_VGAP"%oe_n,"EL%d_HMAG"%oe_n,"EL%d_VMAG"%oe_n,"EL%d_HROT"%oe_n,"EL%d_VROT"%oe_n]

            for el in list_w:
                idx += 1
                box1 = gui.widgetBox(box11)
                oasysgui.lineEdit(box1, self, el,
                                  label=self.unitLabels()[idx], addSpace=False,
                                  valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
                self.show_at(self.unitFlags()[idx], box1)


        #widget index 41
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "PLOT_SETS",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=['Input beam',
                           'Beam transmitted after last element',
                           'Absorption by ALL elements',
                           'Absorption by LAST element'],
                    valueType=int, orientation="horizontal", labelWidth=250, callback=self.replot_results)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 42
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "FILE_DUMP",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes (power3D.h5)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        tmp = ConfirmDialog.confirmed(self,
                                      message="POWER3D is an obsolete application.\nReplaced by power3Dcomponent.\nPlease move convert your workspaces as it will disappear soon.",
                                      title="Obsolete application")

    def set_NELEMENTS(self):
        self.initializeTabs()

    def set_EL_FLAG(self):
        self.initializeTabs()

    def unitLabels(self):
        labels =  ['Number of elements:']
        ordinals = [
            '1st',
            '2nd',
            '3rd',
            '4th',
            '5th']
        for i in range(self.MAX_OE):
            labels.append('%s oe is: '%ordinals[i])
            labels.append('formula: ')
            labels.append('Filter thick[mm]')
            labels.append('Mirror angle[mrad]')
            labels.append('Roughness[A]')
            labels.append('Density [g/cm^3]')
            labels.append('H Gap [mm]')
            labels.append('V Gap [mm]')
            labels.append('H Magnification')
            labels.append('V Magnification')
            labels.append('Rotation angle around V axis [deg]')
            labels.append('Rotation angle around H axis [deg]')

        labels.append("Plot")
        labels.append("Dump hdf5 file")

        return labels




    def unitFlags(self):
        flags =  ['True']

        for i in range(self.MAX_OE):

            flags.append('self.NELEMENTS  >=  1+%d'%i)                                     # kind
            flags.append('self.EL%d_FLAG  <=  1  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # formula
            flags.append('self.EL%d_FLAG  ==  0  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # thickness
            flags.append('self.EL%d_FLAG  ==  1  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # angle
            flags.append('self.EL%d_FLAG  ==  1  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # roughness
            flags.append('self.EL%d_FLAG  <=  1  and  self.NELEMENTS  >=  1+%i'%(i+1,i))   # density
            flags.append('self.EL%d_FLAG  ==  2  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # gap
            flags.append('self.EL%d_FLAG  ==  2  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # gap
            flags.append('self.EL%d_FLAG  ==  3  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # magnification
            flags.append('self.EL%d_FLAG  ==  3  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # magnification
            flags.append('self.EL%d_FLAG  ==  4  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # rotation
            flags.append('self.EL%d_FLAG  ==  4  and  self.NELEMENTS  >=  1+%d'%(i+1,i))   # rotation

        flags.append("True")
        flags.append("True")
        return flags


    def get_help_name(self):
        return 'power3d'

    def acceptExchangeData(self, exchangeData):
        try:
            if not exchangeData is None:
                if exchangeData.get_program_name() == "XOPPY":
                    if exchangeData.get_widget_name() =="UNDULATOR_RADIATION" :
                        pass
                    elif exchangeData.get_widget_name() =="POWER3D" :
                        pass
                    else:
                        raise Exception("Xoppy Input beam not recognized")

                    self.input_beam = exchangeData
                    self.output_beam = None
                    self.process_showers()


                    self.compute()


        except Exception as exception:
            QMessageBox.critical(self, "Error",
                                       str(exception),
                QMessageBox.Ok)




    def check_fields(self):


        if self.NELEMENTS >= 1:
            self.EL1_FOR = congruence.checkEmptyString(self.EL1_FOR, "1st oe formula")

            if self.EL1_FLAG == 0: # filter
                self.EL1_THI = congruence.checkStrictlyPositiveNumber(self.EL1_THI, "1st oe filter thickness")
            elif self.EL1_FLAG == 1: # mirror
                self.EL1_ANG = congruence.checkStrictlyPositiveNumber(self.EL1_ANG, "1st oe mirror angle")
                self.EL1_ROU = congruence.checkPositiveNumber(self.EL1_ROU, "1st oe mirror roughness")
            elif self.EL1_FLAG == 2: # aperture
                self.EL1_HGAP = congruence.checkStrictlyPositiveNumber(self.EL1_HGAP, "1st oe H gap")
                self.EL1_VGAP = congruence.checkPositiveNumber(self.EL1_VGAP, "1st oe V Gap")
            elif self.EL1_FLAG == 3: # magnifier
                self.EL1_HMAG = congruence.checkStrictlyPositiveNumber(self.EL1_HMAG, "1st oe H magnification")
                self.EL1_VMAG = congruence.checkPositiveNumber(self.EL1_VMAG, "1st oe V magnification")
            elif self.EL1_FLAG == 4: # rotation
                self.EL1_HROT = congruence.checkNumber(self.EL1_HROT, "1st oe rotation H")
                self.EL1_VROT = congruence.checkNumber(self.EL1_VROT, "1st oe rotation V")

            if not self.EL1_DEN.strip() == "?":
                self.EL1_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL1_DEN, "1st oe density")), "1st oe density"))

        if self.NELEMENTS >= 2:
            self.EL2_FOR = congruence.checkEmptyString(self.EL2_FOR, "2nd oe formula")

            if self.EL2_FLAG == 0: # filter
                self.EL2_THI = congruence.checkStrictlyPositiveNumber(self.EL2_THI, "2nd oe filter thickness")
            elif self.EL2_FLAG == 1: # mirror
                self.EL2_ANG = congruence.checkStrictlyPositiveNumber(self.EL2_ANG, "2nd oe mirror angle")
                self.EL2_ROU = congruence.checkPositiveNumber(self.EL2_ROU, "2nd oe mirror roughness")
            elif self.EL2_FLAG == 2: # aperture
                self.EL2_HGAP = congruence.checkStrictlyPositiveNumber(self.EL2_HGAP, "2nd oe H gap")
                self.EL2_VGAP = congruence.checkPositiveNumber(self.EL2_VGAP, "2nd oe V Gap")
            elif self.EL2_FLAG == 3: # magnifier
                self.EL2_HMAG = congruence.checkStrictlyPositiveNumber(self.EL2_HMAG, "2nd oe H magnification")
                self.EL2_VMAG = congruence.checkPositiveNumber(self.EL2_VMAG, "2nd oe V magnification")
            elif self.EL2_FLAG == 4: # rotation
                self.EL2_HROT = congruence.checkNumber(self.EL2_HROT, "2nd oe rotation H")
                self.EL2_VROT = congruence.checkNumber(self.EL2_VROT, "2nd oe rotation V")

            if not self.EL2_DEN.strip() == "?":
                self.EL2_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL2_DEN, "2nd oe density")), "2nd oe density"))

        if self.NELEMENTS >= 3:
            self.EL3_FOR = congruence.checkEmptyString(self.EL3_FOR, "3rd oe formula")

            if self.EL3_FLAG == 0: # filter
                self.EL3_THI = congruence.checkStrictlyPositiveNumber(self.EL3_THI, "3rd oe filter thickness")
            elif self.EL3_FLAG == 1: # mirror
                self.EL3_ANG = congruence.checkStrictlyPositiveNumber(self.EL3_ANG, "3rd oe mirror angle")
                self.EL3_ROU = congruence.checkPositiveNumber(self.EL3_ROU, "3rd oe mirror roughness")
            elif self.EL3_FLAG == 2: # aperture
                self.EL3_HGAP = congruence.checkStrictlyPositiveNumber(self.EL3_HGAP, "3rd oe H gap")
                self.EL3_VGAP = congruence.checkPositiveNumber(self.EL3_VGAP, "3rd oe V Gap")
            elif self.EL3_FLAG == 3: # magnifier
                self.EL3_HMAG = congruence.checkStrictlyPositiveNumber(self.EL3_HMAG, "3rd oe H magnification")
                self.EL3_VMAG = congruence.checkPositiveNumber(self.EL3_VMAG, "3rd oe V magnification")
            elif self.EL3_FLAG == 4: # rotation
                self.EL3_HROT = congruence.checkNumber(self.EL3_HROT, "3rd oe rotation H")
                self.EL3_VROT = congruence.checkNumber(self.EL3_VROT, "3rd oe rotation V")

            if not self.EL3_DEN.strip() == "?":
                self.EL3_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL3_DEN, "3rd oe density")), "3rd oe density"))

        if self.NELEMENTS >= 4:
            self.EL4_FOR = congruence.checkEmptyString(self.EL4_FOR, "4th oe formula")

            if self.EL4_FLAG == 0: # filter
                self.EL4_THI = congruence.checkStrictlyPositiveNumber(self.EL4_THI, "4th oe filter thickness")
            elif self.EL4_FLAG == 1: # mirror
                self.EL4_ANG = congruence.checkStrictlyPositiveNumber(self.EL4_ANG, "4th oe mirror angle")
                self.EL4_ROU = congruence.checkPositiveNumber(self.EL4_ROU, "4th oe mirror roughness")
            elif self.EL4_FLAG == 2: # aperture
                self.EL4_HGAP = congruence.checkStrictlyPositiveNumber(self.EL4_HGAP, "4th oe H gap")
                self.EL4_VGAP = congruence.checkPositiveNumber(self.EL4_VGAP, "4th oe V Gap")
            elif self.EL4_FLAG == 3: # magnifier
                self.EL4_HMAG = congruence.checkStrictlyPositiveNumber(self.EL4_HMAG, "4th oe H magnification")
                self.EL4_VMAG = congruence.checkPositiveNumber(self.EL4_VMAG, "4th oe V magnification")
            elif self.EL4_FLAG == 4: # rotation
                self.EL4_HROT = congruence.checkNumber(self.EL4_HROT, "4th oe rotation H")
                self.EL4_VROT = congruence.checkNumber(self.EL4_VROT, "4th oe rotation V")
            if not self.EL4_DEN.strip() == "?":

                self.EL4_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL4_DEN, "4th oe density")), "4th oe density"))

        if self.NELEMENTS >= 5:
            self.EL5_FOR = congruence.checkEmptyString(self.EL5_FOR, "5th oe formula")

            if self.EL5_FLAG == 0: # filter
                self.EL5_THI = congruence.checkStrictlyPositiveNumber(self.EL5_THI, "5th oe filter thickness")
            elif self.EL5_FLAG == 1: # mirror
                self.EL5_ANG = congruence.checkStrictlyPositiveNumber(self.EL5_ANG, "5th oe mirror angle")
                self.EL5_ROU = congruence.checkPositiveNumber(self.EL5_ROU, "5th oe mirror roughness")
            elif self.EL5_FLAG == 2: # aperture
                self.EL5_HGAP = congruence.checkStrictlyPositiveNumber(self.EL5_HGAP, "5th oe H gap")
                self.EL5_VGAP = congruence.checkPositiveNumber(self.EL5_VGAP, "5th oe V Gap")
            elif self.EL5_FLAG == 3: # magnifier
                self.EL5_HMAG = congruence.checkStrictlyPositiveNumber(self.EL5_HMAG, "5th oe H magnification")
                self.EL5_VMAG = congruence.checkPositiveNumber(self.EL5_VMAG, "5th oe V magnification")
            elif self.EL5_FLAG == 4: # rotation
                self.EL5_HROT = congruence.checkNumber(self.EL5_HROT, "5th oe rotation H")
                self.EL5_VROT = congruence.checkNumber(self.EL5_VROT, "5th oe rotation V")

            if not self.EL5_DEN.strip() == "?":
                self.EL5_DEN = str(congruence.checkStrictlyPositiveNumber(float(congruence.checkNumber(self.EL5_DEN, "5th oe density")), "5th oe density"))

    def do_xoppy_calculation(self):

        return self.xoppy_calc_power3D()


    # TODO THIS TO SEND DATA

    def extract_data_from_xoppy_output(self, calculation_output):

        transmittance,E,H,V = calculation_output

        [p, e, h, v] = self.input_beam.get_content("xoppy_data")

        data_to_send = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        data_to_send.add_content("xoppy_data", [p*transmittance.prod(axis=0), E[-1], H[-1], V[-1]])
        data_to_send.add_content("xoppy_transmittivity", calculation_output)
        data_to_send.add_content("xoppy_code", "power3")

        self.output_beam = data_to_send

        return data_to_send


    # def extract_data_from_xoppy_output(self, calculation_output):
    #     return calculation_output

    def get_data_exchange_widget_name(self):
        return "POWER3D"

    def getKind(self, oe_n):
        if oe_n == 1:
            return self.EL1_FLAG
        elif oe_n == 2:
            return self.EL2_FLAG
        elif oe_n == 3:
            return self.EL3_FLAG
        elif oe_n == 4:
            return self.EL4_FLAG
        elif oe_n == 5:
            return self.EL5_FLAG

    def getTitles(self):
        return ['Transmittance vs X,Y,E','Transmittance vs E',
                'Spectral Power Density vs E,X,Y','Power Density vs X,Y','Spectral Power vs E']


    def replot_results(self):
        if self.output_beam is None:
            pass
        else:
            self.plot_results(self.output_beam, progressBarValue=80)

    def plot_results(self, calculated_data, progressBarValue=80):
        current_index = self.tabs.currentIndex()
        if not self.view_type == 0:
            if not calculated_data is None:

                self.initializeTabs() # added by srio to avoid overlapping graphs

                self.view_type_combo.setEnabled(False)

                p,e,h,v = self.input_beam.get_content("xoppy_data")
                code = self.input_beam.get_content("xoppy_code")

                p_spectral_power = p * codata.e * 1e3
                p_to_plot = p_spectral_power

                transmittivity,E,H,V = calculated_data.get_content("xoppy_transmittivity")


                transmittivity_total = transmittivity.prod(axis=0)

                if self.PLOT_SETS == 0: # source
                    p_to_plot = p_spectral_power
                    pre_title = "Input beam"
                elif self.PLOT_SETS == 1:
                    p_to_plot = p_spectral_power * transmittivity_total
                    pre_title = "Beam transmitted after LAST element"
                elif self.PLOT_SETS == 2: # wrong with rotation
                    p_to_plot = p_spectral_power * ( numpy.ones_like(transmittivity_total) - transmittivity_total)
                    pre_title = "Absorption by ALL elements"
                elif self.PLOT_SETS == 3:  # wrong with slit, rotation
                    transmittivity_before_last_element = transmittivity_total / transmittivity[-1,:,:,:]
                    p_to_plot = p_spectral_power * (transmittivity_before_last_element - transmittivity_total)
                    pre_title = "Absorption by the LAST element"

                # plot transmittance stack
                try:
                    self.plot_data3D(transmittivity_total, e, H[-1], V[-1], 0, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title='Code '+code+'; Flux [photons/s/0.1%bw/mm^2]',)

                    self.tabs.setCurrentIndex(0)
                except Exception as ex:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(ex))


                # plot transmittance spectrum
                try:
                    self.plot_data1D(e,transmittivity_total.sum(axis=2).sum(axis=1)/h.size/v.size, 1, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Tramsmittance',
                                     title='Transmittance',)

                    # self.tabs.setCurrentIndex(2)
                except Exception as ex:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(ex))



                # plot result s E,X,Y
                try:
                    self.plot_data3D(p_to_plot, e, H[-1], V[-1], 2, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title=pre_title+' Spectral power density[W/eV/mm^2]',)

                    self.tabs.setCurrentIndex(0)
                except Exception as ex:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(ex))

                # plot result vs X,Y
                try:
                    if len(e) > 1:
                        energy_step = e[1]-e[0]
                    else:
                        energy_step = 1.0

                    self.plot_data2D(p_to_plot.sum(axis=0)*energy_step, H[-1], V[-1], 3, 0,
                                     xtitle='H [mm]',
                                     ytitle='V [mm]',
                                     title=pre_title+' Power density [W/mm^2]',)

                    # self.tabs.setCurrentIndex(1)
                except Exception as ex:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(ex))

                # plot result vs E
                try:
                    self.plot_data1D(e,p_to_plot.sum(axis=2).sum(axis=1)*(H[-1][1]-H[-1][0])*(V[-1][1]-V[-1][0]), 4, 0,
                                     xtitle='Photon Energy [eV]',
                                     ytitle= 'Spectral power [W/eV]',
                                     title=pre_title+' Spectral power',)

                    # self.tabs.setCurrentIndex(2)
                except Exception as ex:
                    self.view_type_combo.setEnabled(True)
                    raise Exception("Data not plottable: bad content\n" + str(ex))

                self.view_type_combo.setEnabled(True)

                try:
                    self.tabs.setCurrentIndex(current_index)
                except:
                    pass

            else:
                raise Exception("Empty Data")


    def xoppy_calc_power3D(self):

        #
        # prepare input for xpower_calc
        # Note that the input for xpower_calc accepts any number of elements.
        #

        substance = [self.EL1_FOR,self.EL2_FOR,self.EL3_FOR,self.EL4_FOR,self.EL5_FOR]
        thick     = numpy.array( (self.EL1_THI,self.EL2_THI,self.EL3_THI,self.EL4_THI,self.EL5_THI))
        angle     = numpy.array( (self.EL1_ANG,self.EL2_ANG,self.EL3_ANG,self.EL4_ANG,self.EL5_ANG))
        dens      = [self.EL1_DEN,self.EL2_DEN,self.EL3_DEN,self.EL4_DEN,self.EL5_DEN]
        roughness = numpy.array( (self.EL1_ROU,self.EL2_ROU,self.EL3_ROU,self.EL4_ROU,self.EL5_ROU))
        flags     = numpy.array( (self.EL1_FLAG,self.EL2_FLAG,self.EL3_FLAG,self.EL4_FLAG,self.EL5_FLAG))
        hgap = numpy.array( (self.EL1_HGAP,self.EL2_HGAP,self.EL3_HGAP,self.EL4_HGAP,self.EL5_HGAP))
        vgap = numpy.array( (self.EL1_VGAP,self.EL2_VGAP,self.EL3_VGAP,self.EL4_VGAP,self.EL5_VGAP))
        hmag = numpy.array( (self.EL1_HMAG,self.EL2_HMAG,self.EL3_HMAG,self.EL4_HMAG,self.EL5_HMAG))
        vmag = numpy.array( (self.EL1_VMAG,self.EL2_VMAG,self.EL3_VMAG,self.EL4_VMAG,self.EL5_VMAG))
        hrot = numpy.array( (self.EL1_HROT,self.EL2_HROT,self.EL3_HROT,self.EL4_HROT,self.EL5_HROT))
        vrot = numpy.array( (self.EL1_VROT,self.EL2_VROT,self.EL3_VROT,self.EL4_VROT,self.EL5_VROT))

        substance = substance[0:self.NELEMENTS+1]
        thick = thick[0:self.NELEMENTS+1]
        angle = angle[0:self.NELEMENTS+1]
        dens = dens[0:self.NELEMENTS+1]
        roughness = roughness[0:self.NELEMENTS+1]
        flags = flags[0:self.NELEMENTS+1]

        p,e,h,v = self.input_beam.get_content("xoppy_data")

        nelem_including_source = self.NELEMENTS + 1
        energies = e


        # note that element of zero index corresponds to source!!!
        transmittance = numpy.zeros((nelem_including_source,p.shape[0],p.shape[1],p.shape[2]))
        E =  numpy.zeros((nelem_including_source,p.shape[0]))
        H =  numpy.zeros((nelem_including_source,p.shape[1]))
        V =  numpy.zeros((nelem_including_source,p.shape[2]))

        # initialize results

        for i in range(nelem_including_source):
            transmittance[i] = numpy.ones_like(p)  # initialize all transmissions to one
            E[i] = e  # same energy array for all elements
        H[0] = h
        V[0] = v

        #
        # get undefined densities
        #
        for i in range(self.NELEMENTS):
            try:  # apply written value
                rho = float(dens[i])
            except:   # in case of ?
                rho = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(substance[i]))
                print("Density for %s: %g g/cm3"%(substance[i],rho))
            dens[i] = rho


        txt = ""
        for i in range(self.NELEMENTS):
            if flags[i] == 0:
                txt += '      *****   oe '+str(i+1)+'  [Filter] *************\n'
                txt += '      Material: %s\n'%(substance[i])
                txt += '      Density [g/cm^3]: %f \n'%(dens[i])
                txt += '      thickness [mm] : %f \n'%(thick[i])
            elif flags[i] == 1:
                txt += '      *****   oe '+str(i+1)+'  [Mirror] *************\n'
                txt += '      Material: %s\n'%(substance[i])
                txt += '      Density [g/cm^3]: %f \n'%(dens[i])
                txt += '      grazing angle [mrad]: %f \n'%(angle[i])
                txt += '      roughness [A]: %f \n'%(roughness[i])
            elif flags[i] == 2:
                txt += '      *****   oe '+str(i+1)+'  [Aperture] *************\n'
                txt += '      H gap [mm]: %f \n'%(hgap[i])
                txt += '      V gap [mm]: %f \n'%(vgap[i])
            elif flags[i] == 3:
                txt += '      *****   oe '+str(i+1)+'  [Magnifier] *************\n'
                txt += '      H magnification: %f \n'%(hmag[i])
                txt += '      V magnification: %f \n'%(vmag[i])
            elif flags[i] == 4:
                txt += '      *****   oe '+str(i+1)+'  [Screen rotated] *************\n'
                txt += '      H angle [deg]: %f \n'%(hrot[i])
                txt += '      V angle [deg]: %f \n'%(vrot[i])

        for i in range(self.NELEMENTS):
            if flags[i] == 0: # filter

                for j,energy in enumerate(energies):

                    tmp = xraylib.CS_Total_CP(substance[i],energy/1000.0)

                    # pay attention to the element index...
                    transmittance[i+1,j,:,:] = numpy.exp(-tmp*dens[i]*(thick[i]/10.0))
                    H[i + 1] = H[i]
                    V[i + 1] = V[i]


            elif flags[i] == 1: # mirror
                tmp = numpy.zeros(energies.size)
                for j,energy in enumerate(energies):
                    tmp[j] = xraylib.Refractive_Index_Re(substance[i],energy/1000.0,dens[i])
                delta = 1.0 - tmp

                beta = numpy.zeros(energies.size)
                for j,energy in enumerate(energies):
                    beta[j] = xraylib.Refractive_Index_Im(substance[i],energy/1000.0,dens[i])

                (rs,rp,runp) = reflectivity_fresnel(refraction_index_beta=beta,refraction_index_delta=delta,\
                                            grazing_angle_mrad=angle[i],roughness_rms_A=roughness[i],\
                                            photon_energy_ev=energies)

                for j,energy in enumerate(energies):
                    transmittance[i+1,j,:,:] = rs[j]
                H[i + 1] = H[i]
                V[i + 1] = V[i]

            elif flags[i] == 2:  # aperture

                transmittance[i + 1, :, :, :] = 1.0
                h_indices_bad = numpy.where(numpy.abs(H[i]) > 0.5*hgap[i])
                if len(h_indices_bad) > 0:
                    transmittance[i + 1, :, h_indices_bad, :] = 0.0

                v_indices_bad = numpy.where(numpy.abs(V[i]) > 0.5*vgap[i])
                if len(v_indices_bad) > 0:
                    transmittance[i + 1, :, :, v_indices_bad] = 0.0
                H[i + 1] = H[i]
                V[i + 1] = V[i]

            elif flags[i] == 3:  # magnifier
                transmittance[i + 1, :, :, :] = 1.0 / (hmag[i] * vmag[i])
                H[i + 1] = H[i] * hmag[i]
                V[i + 1] = V[i] * vmag[i]

            elif flags[i] == 4:  # rotation screen
                transmittance[i + 1, :, :, :] = numpy.cos(hrot[i] * numpy.pi / 180) * numpy.cos(vrot[i] * numpy.pi / 180)
                H[i + 1] = H[i] / numpy.cos(hrot[i] * numpy.pi / 180)
                V[i + 1] = V[i] / numpy.cos(vrot[i] * numpy.pi / 180)


        txt += "\n\n\n"
        integration_constante = (e[1] - e[0]) * (h[1] - h[0]) * (v[1] - v[0]) * codata.e * 1e3
        p_cumulated = p.copy()
        power_cumulated = p_cumulated.sum()*integration_constante
        txt += '      Input beam power: %f W\n'%(power_cumulated)

        for i in range(self.NELEMENTS):
            integration_constante = (E[i+1][1] - E[i+1][0]) * (H[i+1][1] - H[i+1][0]) * (V[i+1][1] - V[i+1][0]) * codata.e * 1e3
            p_cumulated *= transmittance[i+1]
            power_transmitted = (p_cumulated).sum()*integration_constante
            txt += '      Beam power after optical element %d: %6.3f W (absorbed: %6.3f W)\n'%\
                   (i+1,power_transmitted,power_cumulated-power_transmitted)
            power_cumulated = power_transmitted
        print(txt)

        calculated_data = (transmittance,E,H,V)

        if self.FILE_DUMP:
            self.xoppy_write_h5file(calculated_data)

        return  calculated_data

    def xoppy_write_h5file(self,calculated_data):

        p, e, h, v = self.input_beam.get_content("xoppy_data")
        code = self.input_beam.get_content("xoppy_code")

        p_spectral_power = p * codata.e * 1e3

        transmittivity, E, H, V = calculated_data


        h5_file = "power3D.h5"
        try:

            h5w = H5SimpleWriter.initialize_file(h5_file, creator="power3D.py")
            p_cumulated = p.copy()
            txt = "\n\n\n"
            integration_constante = (e[1] - e[0]) * (h[1] - h[0]) * (v[1] - v[0]) * codata.e * 1e3
            p_cumulated = p.copy()
            power_cumulated = p_cumulated.sum() * integration_constante
            txt += '      Input beam power: %f W\n' % (power_cumulated)

            for i in range(self.NELEMENTS):
                integration_constante = (E[i + 1][1] - E[i + 1][0]) * (H[i + 1][1] - H[i + 1][0]) * (
                            V[i + 1][1] - V[i + 1][0]) * codata.e * 1e3
                p_cumulated *= transmittivity[i + 1]
                power_transmitted = (p_cumulated).sum() * integration_constante
                txt += '      Beam power after optical element %d: %6.3f W (absorbed: %6.3f W)\n' % \
                       (i + 1, power_transmitted, power_cumulated - power_transmitted)
                power_cumulated = power_transmitted
            print(txt)

            h5w.add_key("info", txt, entry_name=None)

            #
            # source
            #
            entry_name = "source"

            h5w.create_entry(entry_name, nx_default=None)


            h5w.add_stack(e, h, v, p, stack_name="Radiation stack", entry_name=entry_name,
                          title_0="Photon energy [eV]",
                          title_1="X gap [mm]",
                          title_2="Y gap [mm]")

            h5w.add_image(p_spectral_power.sum(axis=0) * (E[i][1] - E[i][0]), H[i], V[i],
                          image_name="Power Density", entry_name=entry_name,
                          title_x="X [mm]", title_y="Y [mm]")

            h5w.add_dataset(E[0], p_spectral_power.sum(axis=2).sum(axis=1) * (h[1] - h[0]) * (v[1] - v[0]) ,
                            entry_name=entry_name, dataset_name="Spectral power",
                            title_x="Photon Energy [eV]", title_y="Spectral density [W/eV]")


            for i in range(self.NELEMENTS):
                entry_name = "optical_element_%d"%(i+1)

                h5w.create_entry(entry_name, nx_default="Absorbed Power Density")

                h5w.add_stack(E[i], H[i], V[i], transmittivity[i],
                              stack_name="Transmittivity_stack", entry_name=entry_name,
                              title_0="Photon energy [eV]",
                              title_1="X gap [mm]",
                              title_2="Y gap [mm]")

                transmittivity_total = (transmittivity[0:(i+2),:,:,:]).prod(axis=0)
                p_to_plot = p_spectral_power * transmittivity_total
                h5w.add_image(p_to_plot.sum(axis=0)*(E[i][1]-E[i][0]),H[i],V[i],image_name="Transmitted Power Density",entry_name=entry_name,
                              title_x="X [mm]",title_y="Y [mm]")

                h5w.add_dataset(E[i], p_to_plot.sum(axis=2).sum(axis=1) * (H[i][1] - H[i][0]) * (V[i][1] - V[i][0]) ,
                                entry_name=entry_name, dataset_name="Spectral power",
                                title_x="Photon Energy [eV]", title_y="Spectral density [W/eV]")

                transmittivity_before_last_element = (transmittivity[0:(i+1),:,:,:]).prod(axis=0)
                p_to_plot = p_spectral_power * (transmittivity_before_last_element - transmittivity_total)
                h5w.add_image(p_to_plot.sum(axis=0)*(E[i][1]-E[i][0]),H[i],V[i],image_name="Absorbed Power Density",entry_name=entry_name,
                              title_x="X [mm]",title_y="Y [mm]")



            print("File written to disk: %s" % h5_file)
        except:
            print("ERROR writing h5 file")


if __name__ == "__main__":

    # create unulator_radiation xoppy exchange data
    from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_radiation
    from oasys.widgets.exchange import DataExchangeObject

    e, h, v, p, code = xoppy_calc_undulator_radiation(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                       ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                       ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                       PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,
                                       SETRESONANCE=0,HARMONICNUMBER=1,
                                       GAPH=0.001,GAPV=0.001,\
                                       HSLITPOINTS=41,VSLITPOINTS=41,METHOD=2,
                                       PHOTONENERGYMIN=7000,PHOTONENERGYMAX=8100,PHOTONENERGYPOINTS=20,
                                       USEEMITTANCES=1)

    received_data = DataExchangeObject("XOPPY", "POWER3D")
    received_data.add_content("xoppy_data", [p, e, h, v])
    received_data.add_content("xoppy_code", code)


    #
    app = QApplication(sys.argv)
    w = OWpower3D()

    w.acceptExchangeData(received_data)

    w.show()
    app.exec()

    w.saveSettings()
