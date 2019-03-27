import sys
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from oasys.widgets import gui as oasysgui, congruence
from orangewidget.settings import Setting

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util.xoppy_bm_wiggler import xoppy_calc_bm

from oasys.widgets.exchange import DataExchangeObject

# TODO show flux(psi) and 2D plot
from syned.widget.widget_decorator import WidgetDecorator

from syned.storage_ring.magnetic_structures.bending_magnet import BendingMagnet
import syned.beamline.beamline as synedb


import scipy.constants as codata

class OWbm(XoppyWidget, WidgetDecorator):
    name = "BM"
    id = "orange.widgets.databm"
    description = "Bending Magnet Spectrum"
    icon = "icons/xoppy_bm.png"
    priority = 13
    category = ""
    keywords = ["xoppy", "bm"]

    inputs = WidgetDecorator.syned_input_data()

    TYPE_CALC = Setting(0)
    MACHINE_NAME = Setting("ESRF bending magnet")
    RB_CHOICE = Setting(0)
    MACHINE_R_M = Setting(25.0)
    BFIELD_T = Setting(0.8)
    BEAM_ENERGY_GEV = Setting(6.0)
    CURRENT_A = Setting(0.2)
    HOR_DIV_MRAD = Setting(1.0)
    VER_DIV = Setting(0)
    PHOT_ENERGY_MIN = Setting(100.0)
    PHOT_ENERGY_MAX = Setting(100000.0)
    NPOINTS = Setting(500)
    LOG_CHOICE = Setting(1)
    PSI_MRAD_PLOT = Setting(1.0)
    PSI_MIN = Setting(-1.0)
    PSI_MAX = Setting(1.0)
    PSI_NPOINTS = Setting(500)
    FILE_DUMP = Setting(0)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TYPE_CALC",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Energy or Power spectra', 'Angular distribution (all wavelengths)', 'Angular distribution (one wavelength)', '2D flux and power (angular,energy) distribution'],
                    valueType=int, orientation="horizontal", callback=self.set_TYPE_CALC)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        self.id_MACHINE_NAME = box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "MACHINE_NAME",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "RB_CHOICE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Magnetic Radius', 'Magnetic Field'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_MACHINE_R_M = oasysgui.lineEdit(box1, self, "MACHINE_R_M",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_BFIELD_T = oasysgui.lineEdit(box1, self, "BFIELD_T",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_BEAM_ENERGY_GEV = oasysgui.lineEdit(box1, self, "BEAM_ENERGY_GEV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_CURRENT_A = oasysgui.lineEdit(box1, self, "CURRENT_A",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HOR_DIV_MRAD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "VER_DIV",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Full (integrated in Psi)', 'At Psi=0', 'In [PsiMin,PsiMax]', 'At Psi=Psi_Min'],
                     valueType=int, orientation="horizontal", callback=self.set_VER_DIV, labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHOT_ENERGY_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHOT_ENERGY_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "LOG_CHOICE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Lin', 'Log'],
                    valueType=int, orientation="horizontal", labelWidth=350)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PSI_MRAD_PLOT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PSI_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PSI_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PSI_NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        #widget index 17
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "FILE_DUMP",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['No', 'YES (bm.spec)'],
                     valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

    def unitLabels(self):
         return ['Type of calculation','Machine name',
                 'B from:','Machine Radius [m]','Magnetic Field [T]',
                 'Beam energy [GeV]','Beam Current [A]',
                 'Horizontal div Theta [mrad]','Psi (vertical div) for energy spectra',
                 'Min Photon Energy [eV]','Max Photon Energy [eV]','Number of points','Separation between energy points',
                 'Max Psi[mrad] for angular plots','Psi min [mrad]','Psi max [mrad]','Number of Psi points',
                 'Dump file']

    def unitFlags(self):
         return ['True','True',
                 'True','self.RB_CHOICE  ==  0','self.RB_CHOICE  ==  1',
                 'True','True',
                 'True','self.TYPE_CALC == 0',
                 'True','True','True','self.TYPE_CALC == 0',
                 'True','self.VER_DIV  >=  2','self.VER_DIV  ==  2','self.VER_DIV  ==  2',
                 'True']

    def set_TYPE_CALC(self):

        self.initializeTabs()
        if self.TYPE_CALC == 3:
                self.VER_DIV = 2


    def set_VER_DIV(self):
        if self.TYPE_CALC == 0: self.initializeTabs()


    def get_help_name(self):
        return 'bm'

    def check_fields(self):
        if self.RB_CHOICE == 0:
            self.MACHINE_R_M = congruence.checkStrictlyPositiveNumber(self.MACHINE_R_M, "Magnetic Radius")
        else:
            self.BFIELD_T = congruence.checkStrictlyPositiveNumber(self.BFIELD_T, "Magnetic Field")

        self.BEAM_ENERGY_GEV = congruence.checkStrictlyPositiveNumber(self.BEAM_ENERGY_GEV, "Beam Energy")
        self.CURRENT_A = congruence.checkStrictlyPositiveNumber(self.CURRENT_A, "Beam Current")
        self.HOR_DIV_MRAD = congruence.checkPositiveNumber(self.HOR_DIV_MRAD, "Horizontal div Theta")

        self.PHOT_ENERGY_MIN = congruence.checkPositiveNumber(self.PHOT_ENERGY_MIN, "Min Photon Energy")
        self.PHOT_ENERGY_MAX = congruence.checkStrictlyPositiveNumber(self.PHOT_ENERGY_MAX, "Max Photon Energy")
        congruence.checkLessThan(self.PHOT_ENERGY_MIN, self.PHOT_ENERGY_MAX, "Min Photon Energy", "Max Photon Energy")
        self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.NPOINTS, "Number of Energy Points")

        self.PSI_MRAD_PLOT = congruence.checkNumber(self.PSI_MRAD_PLOT, "Max Psi for angular plots")

        if self.VER_DIV == 2:
            self.PSI_MIN = congruence.checkNumber(self.PSI_MIN, "Min Photon Energy")
            self.PSI_MAX = congruence.checkNumber(self.PSI_MAX, "Max Photon  Max")
            congruence.checkLessThan(self.PSI_MIN, self.PSI_MAX, "Psi Min", "Psi Max")
        elif self.VER_DIV == 3:
            self.PSI_MIN = congruence.checkNumber(self.PSI_MIN, "Min Photon Energy")

    def plot_results(self, calculated_data, progressBarValue=80):
        if self.TYPE_CALC != 3:
            super().plot_results(calculated_data, progressBarValue)
            self.tabs.setCurrentIndex(len(self.getTitles())-1)
        elif not self.view_type == 0:
            if not calculated_data is None:
                self.view_type_combo.setEnabled(False)

                data = calculated_data.get_content("xoppy_data_3D")

                fm = data[0]
                a = data[1]
                energy_ev = data[2]

                try:
                    self.plot_data2D(fm,
                                     a,
                                     energy_ev,
                                     0, 0,
                                     xtitle="Psi [mrad]",
                                     ytitle="Photon energy [eV]",
                                     title="Flux [photons/s/0.1%bw]")

                    self.plot_data2D(fm*codata.e*1e3,
                                     a,
                                     energy_ev,
                                     1, 1,
                                     xtitle="Psi [mrad]",
                                     ytitle="Photon energy [eV]",
                                     title="Spectral power [W/eV]")
                except Exception as e:
                    self.view_type_combo.setEnabled(True)

                    raise Exception("Data not plottable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")


    def do_xoppy_calculation(self):
        a6_T, fm, a, energy_ev =  xoppy_calc_bm(TYPE_CALC=self.TYPE_CALC,
                             MACHINE_NAME=self.MACHINE_NAME,
                             RB_CHOICE=self.RB_CHOICE,
                             MACHINE_R_M=self.MACHINE_R_M,
                             BFIELD_T=self.BFIELD_T,
                             BEAM_ENERGY_GEV=self.BEAM_ENERGY_GEV,
                             CURRENT_A=self.CURRENT_A,
                             HOR_DIV_MRAD=self.HOR_DIV_MRAD,
                             VER_DIV=self.VER_DIV,
                             PHOT_ENERGY_MIN=self.PHOT_ENERGY_MIN,
                             PHOT_ENERGY_MAX=self.PHOT_ENERGY_MAX,
                             NPOINTS=self.NPOINTS,
                             LOG_CHOICE=self.LOG_CHOICE,
                             PSI_MRAD_PLOT=self.PSI_MRAD_PLOT,
                             PSI_MIN=self.PSI_MIN,
                             PSI_MAX=self.PSI_MAX,
                             PSI_NPOINTS=self.PSI_NPOINTS,
                             FILE_DUMP=self.FILE_DUMP)

        # write python script in standard output
        dict_parameters = {
            "TYPE_CALC"       : self.TYPE_CALC,
            "MACHINE_NAME"    : self.MACHINE_NAME,
            "RB_CHOICE"       : self.RB_CHOICE,
            "MACHINE_R_M"     : self.MACHINE_R_M,
            "BFIELD_T"        : self.BFIELD_T,
            "BEAM_ENERGY_GEV" : self.BEAM_ENERGY_GEV,
            "CURRENT_A"       : self.CURRENT_A,
            "HOR_DIV_MRAD"    : self.HOR_DIV_MRAD,
            "VER_DIV"         : self.VER_DIV,
            "PHOT_ENERGY_MIN" : self.PHOT_ENERGY_MIN,
            "PHOT_ENERGY_MAX" : self.PHOT_ENERGY_MAX,
            "NPOINTS"         : self.NPOINTS,
            "LOG_CHOICE"      : self.LOG_CHOICE,
            "PSI_MRAD_PLOT"   : self.PSI_MRAD_PLOT,
            "PSI_MIN"         : self.PSI_MIN,
            "PSI_MAX"         : self.PSI_MAX,
            "PSI_NPOINTS"     : self.PSI_NPOINTS,
            "FILE_DUMP"       : self.FILE_DUMP,
            }
        print(self.script_template().format_map(dict_parameters))

        return a6_T, fm, a, energy_ev



    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:bm)
#
from orangecontrib.xoppy.util.xoppy_bm_wiggler import xoppy_calc_bm

# TYPE_CALC: 
# 0: 'Energy or Power spectra'
# 1: 'Angular distribution (all wavelengths)'
# 2: 'Angular distribution (one wavelength)'
# 3: '2D flux and power (angular,energy) distribution'
#
a6_T, fm, a, energy_ev =  xoppy_calc_bm(
    TYPE_CALC={TYPE_CALC},
    MACHINE_NAME="{MACHINE_NAME}",
    RB_CHOICE={RB_CHOICE},
    MACHINE_R_M={MACHINE_R_M},
    BFIELD_T={BFIELD_T},
    BEAM_ENERGY_GEV={BEAM_ENERGY_GEV},
    CURRENT_A={CURRENT_A},
    HOR_DIV_MRAD={HOR_DIV_MRAD},
    VER_DIV={VER_DIV},
    PHOT_ENERGY_MIN={PHOT_ENERGY_MIN},
    PHOT_ENERGY_MAX={PHOT_ENERGY_MAX},
    NPOINTS={NPOINTS},
    LOG_CHOICE={LOG_CHOICE},
    PSI_MRAD_PLOT={PSI_MRAD_PLOT},
    PSI_MIN={PSI_MIN},
    PSI_MAX={PSI_MAX},
    PSI_NPOINTS={PSI_NPOINTS},
    FILE_DUMP=True) # writes output to bm.spec
#
# end script
#
"""
    def add_specific_content_to_calculated_data(self, calculated_data):
        calculated_data.add_content("is_log_plot", self.LOG_CHOICE)
        calculated_data.add_content("calculation_type", self.TYPE_CALC)
        calculated_data.add_content("psi", self.VER_DIV)

    def get_data_exchange_widget_name(self):
        return "BM"

    def extract_data_from_xoppy_output(self, calculation_output):
        data, fm, a, energy_ev = calculation_output
        
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data",  data)
        calculated_data.add_content("xoppy_data_3D",  [fm, a, energy_ev])

        return calculated_data

    def getTitles(self):
        if self.TYPE_CALC == 0:
            return ['E/Ec', 'Flux s-pol/Flux total', 'Flux p-pol/Flux total', 'Flux', 'Spectral Power']
        elif self.TYPE_CALC == 1:
            return ["Psi[rad]*Gamma", "F", "F s-pol", "F p-pol", "Spectral Power"]
        elif self.TYPE_CALC == 2:
            return ["Psi[rad]*Gamma", "F", "F s-pol", "F p-pol", "Flux", "Spectral Power"]
        elif self.TYPE_CALC == 3:
            return ["2D Flux (angle,energy)", "2D Spectral Power (angle,energy)"]

    def getXTitles(self):
        if self.TYPE_CALC == 0:
            return ["Energy [eV]", "Energy [eV]", "Energy [eV]", "Energy [eV]", "Energy [eV]"]
        elif self.TYPE_CALC == 1:
            return ["Psi [mrad]", "Psi [mrad]", "Psi [mrad]", "Psi [mrad]", "Psi [mrad]"]
        elif self.TYPE_CALC == 2:
            return ["Psi [mrad]", "Psi [mrad]", "Psi [mrad]", "Psi [mrad]", "Psi [mrad]", "Psi [mrad]"]
        elif self.TYPE_CALC == 3:
            return []

    def getYTitles(self):
        if self.TYPE_CALC == 0:
            if self.VER_DIV == 0:
                return ['E/Ec', 'Flux_spol/Flux_total', 'Flux_ppol/Flux_total', 'Flux [Phot/sec/0.1%bw]', 'Power [Watts/eV]']
            elif self.VER_DIV == 1:
                return ['E/Ec', 'Flux_spol/Flux_total', 'Flux_ppol/Flux_total', 'Flux [Phot/sec/0.1%bw/mrad(Psi)]', 'Power[Watts/eV/mrad(Psi)]']
            elif self.VER_DIV == 2:
                return ['E/Ec', 'Flux_spol/Flux_total', 'Flux_ppol/Flux_total', 'Flux [Phot/sec/0.1%bw]', 'Power [Watts/eV]']
            elif self.VER_DIV == 3:
                return ['E/Ec', 'Flux_spol/Flux_total', 'Flux_ppol/Flux_total', 'Flux [Phot/sec/0.1%bw/mrad(Psi)]', 'Power [Watts/eV/mrad(Psi)]']
        elif self.TYPE_CALC == 1:
           return ["Psi[rad]*Gamma", "F", "F s-pol", "F p-pol", "Power [Watts/mrad(Psi)]"]
        elif self.TYPE_CALC == 2:
           return ["Psi[rad]*Gamma", "F", "F s-pol", "F p-pol", "Flux [Phot/sec/0.1%bw/mrad(Psi)]", "Power [Watts/mrad(Psi)]"]
        elif self.TYPE_CALC == 3:
           return []

    def getVariablesToPlot(self):
        if self.TYPE_CALC == 0:
            return [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
        elif self.TYPE_CALC == 1:
            return [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
        elif self.TYPE_CALC == 2:
            return [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
        elif self.TYPE_CALC == 3:
            return []

    def getLogPlot(self):
        if self.TYPE_CALC == 0:
            return [(True, False), (True, False), (True, False), (True, True), (True, True)]
        elif self.TYPE_CALC == 1:
            return [(False, False), (False, False), (False, False), (False, False), (False, False)]
        elif self.TYPE_CALC == 2:
            return [(False, False), (False, False), (False, False), (False, False), (False, False), (False, False)]
        elif self.TYPE_CALC == 3:
            return []

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data is None:
                if not data._light_source is None and isinstance(data._light_source._magnetic_structure, BendingMagnet):
                    light_source = data._light_source

                    self.MACHINE_NAME = light_source._name
                    self.BEAM_ENERGY_GEV = light_source._electron_beam._energy_in_GeV
                    self.CURRENT_A = light_source._electron_beam._current
                    self.BFIELD_T = light_source._magnetic_structure._magnetic_field
                    self.MACHINE_R_M = light_source._magnetic_structure._radius

                    self.set_enabled(False)
                else:
                    self.set_enabled(True)
                    raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)

    def set_enabled(self,value):
        if value == True:
                self.id_MACHINE_NAME.setEnabled(True)
                self.id_BEAM_ENERGY_GEV.setEnabled(True)
                self.id_CURRENT_A.setEnabled(True)
                self.id_BFIELD_T.setEnabled(True)
                self.id_MACHINE_R_M.setEnabled(True)
        else:
                self.id_MACHINE_NAME.setEnabled(False)
                self.id_BEAM_ENERGY_GEV.setEnabled(False)
                self.id_CURRENT_A.setEnabled(False)
                self.id_BFIELD_T.setEnabled(False)
                self.id_MACHINE_R_M.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWbm()
    w.show()
    app.exec()
    w.saveSettings()
