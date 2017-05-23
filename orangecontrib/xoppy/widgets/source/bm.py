import sys
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from oasys.widgets import gui as oasysgui, congruence
from orangewidget.settings import Setting
from srxraylib.sources import srfunc
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from oasys.widgets.exchange import DataExchangeObject

# TODO show flux(psi) and 2D plot

class OWbm(XoppyWidget):
    name = "BM"
    id = "orange.widgets.databm"
    description = "Bending Magnet Spectrum"
    icon = "icons/xoppy_bm.png"
    priority = 13
    category = ""
    keywords = ["xoppy", "bm"]

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
        box1 = gui.widgetBox(box) 
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
        oasysgui.lineEdit(box1, self, "MACHINE_R_M",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "BFIELD_T",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "BEAM_ENERGY_GEV",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "CURRENT_A",
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
         return ['Type of calculation','Machine name','B from:','Machine Radius [m]','Magnetic Field [T]','Beam energy [GeV]','Beam Current [A]','Horizontal div Theta [mrad]','Psi (vertical div) for energy spectra','Min Photon Energy [eV]','Max Photon Energy [eV]','Number of energy points','Separation between energy points','Max Psi[mrad] for angular plots','Psi min [mrad]','Psi max [mrad]','Number of Psi points','Dump file']

    def unitFlags(self):
         return ['True','True','True','self.RB_CHOICE  ==  0','self.RB_CHOICE  ==  1','True','True','True','True','True','True','True','True','True','self.VER_DIV  >=  2','self.VER_DIV  ==  2','self.VER_DIV  ==  2','True']

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
        if self.TYPE_CALC != 3: super().plot_results(calculated_data, progressBarValue)
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
                                     xtitle="Angle [mrad]",
                                     ytitle="Photon energy [eV]",
                                     title="Flux [photons/s/0.1%bw/mrad]")

                    self.plot_data2D(fm*srfunc.codata_ec*1e3,
                                     a,
                                     energy_ev,
                                     1, 1,
                                     xtitle="Angle [mrad]",
                                     ytitle="Photon energy [eV]",
                                     title="Spectral power [W/eV/mrad]")

                    self.tabs.setCurrentIndex(1)
                except Exception as e:
                    self.view_type_combo.setEnabled(True)

                    raise Exception("Data not plottable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")

    def do_xoppy_calculation(self):
        return xoppy_calc_bm(TYPE_CALC=self.TYPE_CALC,
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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


def xoppy_calc_bm(MACHINE_NAME="ESRF bending magnet",RB_CHOICE=0,MACHINE_R_M=25.0,BFIELD_T=0.8,\
                  BEAM_ENERGY_GEV=6.04,CURRENT_A=0.1,HOR_DIV_MRAD=1.0,VER_DIV=0,\
                  PHOT_ENERGY_MIN=100.0,PHOT_ENERGY_MAX=100000.0,NPOINTS=500,LOG_CHOICE=1,\
                  PSI_MRAD_PLOT=1.0,PSI_MIN=-1.0,PSI_MAX=1.0,PSI_NPOINTS=500,TYPE_CALC=0,FILE_DUMP=0):
    print("Inside xoppy_calc_bm. ")

    # electron energy in GeV
    gamma = BEAM_ENERGY_GEV*1e3 / srfunc.codata_mee

    r_m = MACHINE_R_M      # magnetic radius in m
    if RB_CHOICE == 1:
        r_m = srfunc.codata_me * srfunc.codata_c / srfunc.codata_ec / BFIELD_T * numpy.sqrt(gamma * gamma - 1)

    # calculate critical energy in eV
    ec_m = 4.0*numpy.pi*r_m/3.0/numpy.power(gamma,3) # wavelength in m
    ec_ev = srfunc.m2ev / ec_m

    fm = None
    a = None
    energy_ev = None

    if TYPE_CALC == 0:
        if LOG_CHOICE == 0:
            energy_ev = numpy.linspace(PHOT_ENERGY_MIN,PHOT_ENERGY_MAX,NPOINTS) # photon energy grid
        else:
            energy_ev = numpy.logspace(numpy.log10(PHOT_ENERGY_MIN),numpy.log10(PHOT_ENERGY_MAX),NPOINTS) # photon energy grid

        a5 = srfunc.sync_ene(VER_DIV, energy_ev, ec_ev=ec_ev, polarization=0, \
                             e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, \
                             psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a5par = srfunc.sync_ene(VER_DIV, energy_ev, ec_ev=ec_ev, polarization=1, \
                                e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, \
                                psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a5per = srfunc.sync_ene(VER_DIV, energy_ev, ec_ev=ec_ev, polarization=2, \
                                e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, \
                                psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        if VER_DIV == 0:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw]','Power[Watts/eV]']
            title='integrated in Psi,'
        if VER_DIV == 1:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw/mrad(Psi)]','Power[Watts/eV/mrad(Psi)]']
            title='at Psi=0,'
        if VER_DIV == 2:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw]','Power[Watts/eV]']
            title='in Psi=[%e,%e]'%(PSI_MIN,PSI_MAX)
        if VER_DIV == 3:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw/mrad(Psi)]','Power[Watts/eV/mrad(Psi)]']
            title='at Psi=%e mrad'%(PSI_MIN)

        a6=numpy.zeros((7,len(energy_ev)))
        a1 = energy_ev
        a6[0,:] = (a1)
        a6[1,:] = srfunc.m2ev * 1e10 / (a1)
        a6[2,:] = (a1)/ec_ev # E/Ec
        a6[3,:] = numpy.array(a5par)/numpy.array(a5)
        a6[4,:] = numpy.array(a5per)/numpy.array(a5)
        a6[5,:] = numpy.array(a5)
        a6[6,:] = numpy.array(a5)*1e3 * srfunc.codata_ec

    if TYPE_CALC == 1:  # angular distributions over over all energies
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        a6 = numpy.zeros((6,NPOINTS))
        a6[0,:] = angle_mrad # angle in mrad
        a6[1,:] = angle_mrad*gamma/1e3 # Psi[rad]*Gamma
        a6[2,:] = srfunc.sync_f(angle_mrad * gamma / 1e3)
        a6[3,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=1)
        a6[4,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=2)
        a6[5,:] = srfunc.sync_ang(0, angle_mrad, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, e_gev=BEAM_ENERGY_GEV, r_m=r_m)

        coltitles=['Psi[mrad]','Psi[rad]*Gamma','F','F s-pol','F p-pol','Power[Watts/mrad(Psi)]']

    if TYPE_CALC == 2:  # angular distributions at a single energy
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        a6 = numpy.zeros((7,NPOINTS))
        a6[0,:] = angle_mrad # angle in mrad
        a6[1,:] = angle_mrad*gamma/1e3 # Psi[rad]*Gamma
        a6[2,:] = srfunc.sync_f(angle_mrad * gamma / 1e3)
        a6[3,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=1)
        a6[4,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=2)
        tmp = srfunc.sync_ang(1, angle_mrad, energy=PHOT_ENERGY_MIN, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, e_gev=BEAM_ENERGY_GEV, ec_ev=ec_ev)
        tmp.shape = -1
        a6[5,:] = tmp
        a6[6,:] = a6[5,:] * srfunc.codata_ec * 1e3

        coltitles=['Psi[mrad]','Psi[rad]*Gamma','F','F s-pol','F p-pol','Flux[Ph/sec/0.1%bw/mrad(Psi)]','Power[Watts/eV/mrad(Psi)]']

    if TYPE_CALC == 3:  # angular,energy distributions flux
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        if LOG_CHOICE == 0:
            energy_ev = numpy.linspace(PHOT_ENERGY_MIN,PHOT_ENERGY_MAX,NPOINTS) # photon energy grid
        else:
            energy_ev = numpy.logspace(numpy.log10(PHOT_ENERGY_MIN),numpy.log10(PHOT_ENERGY_MAX),NPOINTS) # photon energy grid

        # fm[angle,energy]
        fm = srfunc.sync_ene(4, energy_ev, ec_ev=ec_ev, e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, \
                                      hdiv_mrad=HOR_DIV_MRAD, psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a = numpy.linspace(PSI_MIN,PSI_MAX,PSI_NPOINTS)

        a6 = numpy.zeros((4,len(a)*len(energy_ev)))
        ij = -1
        for i in range(len(a)):
            for j in range(len(energy_ev)):
                ij += 1
                a6[0,ij] = a[i]
                a6[1,ij] = energy_ev[j]
                a6[2,ij] = fm[i,j] * srfunc.codata_ec * 1e3
                a6[3,ij] = fm[i,j]

        coltitles=['Psi [mrad]','Photon Energy [eV]','Power [Watts/eV/mrad(Psi)]','Flux [Ph/sec/0.1%bw/mrad(Psi)]']

    # write spec file
    ncol = len(coltitles)
    npoints = len(a6[0,:])

    if FILE_DUMP == 1:
        outFile = "bm.spec"
        f = open(outFile,"w")
        f.write("#F "+outFile+"\n")
        f.write("\n")
        f.write("#S 1 bm results\n")
        f.write("#N %d\n"%(ncol))
        f.write("#L")
        for i in range(ncol):
            f.write("  "+coltitles[i])
        f.write("\n")

        for i in range(npoints):
                f.write((" %e "*ncol+"\n")%(tuple(a6[:,i].tolist())))
        f.close()
        print("File written to disk: " + outFile)

    if TYPE_CALC == 0:
        if LOG_CHOICE == 0:
            print("\nPower from integral of spectrum: %15.3f W"%(a5.sum() * 1e3*srfunc.codata_ec * (energy_ev[1]-energy_ev[0])))

    return a6.T, fm, a, energy_ev



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWbm()
    w.show()
    app.exec()
    w.saveSettings()
