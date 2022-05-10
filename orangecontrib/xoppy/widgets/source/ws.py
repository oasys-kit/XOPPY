from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget


import numpy
import scipy.constants as codata

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

from xoppylib.xoppy_run_binaries import xoppy_calc_ws

class OWws(XoppyWidget,WidgetDecorator):
    name = "WS"
    id = "orange.widgets.dataws"
    description = "Wiggler Spectrum on a Screen"
    icon = "icons/xoppy_ws.png"
    priority = 11
    category = ""
    keywords = ["xoppy", "ws"]

    ENERGY = Setting(7.0)
    CUR = Setting(100.0)
    PERIOD = Setting(8.5)
    N = Setting(28)
    KX = Setting(0.0)
    KY = Setting(8.74)
    EMIN = Setting(1000.0)
    EMAX = Setting(200000.0)
    NEE = Setting(500)
    D = Setting(30.0)
    XPC = Setting(0.0)
    YPC = Setting(0.0)
    XPS = Setting(2.0)
    YPS = Setting(2.0)
    NXP = Setting(10)
    NYP = Setting(10)

    inputs = WidgetDecorator.syned_input_data()

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 


        #widget index 1
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ENERGY = oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_CUR = oasysgui.lineEdit(box1, self, "CUR",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_PERIOD = oasysgui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_N = oasysgui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        # COMMENTED AS IT IS NOT IMPLEMENTED!!
        #widget index 5 
        # idx += 1
        # box1 = gui.widgetBox(box)
        # oasysgui.lineEdit(box1, self, "KX",
        #              label=self.unitLabels()[idx], addSpace=False,
        #             valueType=float, orientation="horizontal", labelWidth=250)
        # self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_KY = oasysgui.lineEdit(box1, self, "KY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NEE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "D",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NXP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NYP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         # return ['Beam energy (GeV)','Beam current (mA)','Period (cm)','Number of periods','Kx','Ky','Min energy (eV)','Max energy (eV)','Number of energy steps','Distance (m)','X-pos. (mm)','Y-pos. (mm)','X slit [mm or mrad]','Y slit [mm or mrad]','Integration points X','Integration points Y']
         return ['Beam energy (GeV)','Beam current (mA)','Period (cm)','Number of periods','Ky','Min energy (eV)','Max energy (eV)','Number of energy steps','Distance (m)','X-pos. (mm)','Y-pos. (mm)','X slit [mm or mrad]','Y slit [mm or mrad]','Integration points X','Integration points Y']

    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','True','True','True','True']

    def get_help_name(self):
        return 'ws'

    def check_fields(self):
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Beam Energy")
        self.CUR = congruence.checkStrictlyPositiveNumber(self.CUR, "Beam Current")
        self.PERIOD = congruence.checkStrictlyPositiveNumber(self.PERIOD, "Period")
        self.N = congruence.checkStrictlyPositiveNumber(self.N, "Number of Periods")
        self.KX = congruence.checkNumber(self.KX, "Kx")
        self.KY = congruence.checkNumber(self.KY, "Ky")
        self.EMIN = congruence.checkPositiveNumber(self.EMIN, "Min Energy")
        self.EMAX = congruence.checkStrictlyPositiveNumber(self.EMAX, "Max Energy")
        congruence.checkLessThan(self.EMIN, self.EMAX, "Min Energy", "Max Energy")
        self.NEE = congruence.checkStrictlyPositiveNumber(self.NEE, "Number of energy steps")
        self.D = congruence.checkPositiveNumber(self.D, "Distance")
        self.XPC = congruence.checkNumber(self.XPC, "X-pos")
        self.YPC = congruence.checkNumber(self.YPC, "Y-pos")
        self.XPS = congruence.checkNumber(self.XPS, "X slit")
        self.YPS = congruence.checkNumber(self.YPS, "Y Slit")
        self.NXP = congruence.checkStrictlyPositiveNumber(self.NXP, "Integration points X")
        self.NYP = congruence.checkStrictlyPositiveNumber(self.NYP, "Integration points Y")

    def do_xoppy_calculation(self):
        outFile = xoppy_calc_ws(
            ENERGY = self.ENERGY,
            CUR    = self.CUR,
            PERIOD = self.PERIOD,
            N      = self.N,
            KX     = self.KX,
            KY     = self.KY,
            EMIN   = self.EMIN,
            EMAX   = self.EMAX,
            NEE    = self.NEE,
            D      = self.D,
            XPC    = self.XPC,
            YPC    = self.YPC,
            XPS    = self.XPS,
            YPS    = self.YPS,
            NXP    = self.NXP,
            NYP    = self.NYP,
        )

        dict_parameters = {
            "ENERGY" : self.ENERGY,
            "CUR"    : self.CUR,
            "PERIOD" : self.PERIOD,
            "N"      : self.N,
            "KX"     : self.KX,
            "KY"     : self.KY,
            "EMIN"   : self.EMIN,
            "EMAX"   : self.EMAX,
            "NEE"    : self.NEE,
            "D"      : self.D,
            "XPC"    : self.XPC,
            "YPC"    : self.YPC,
            "XPS"    : self.XPS,
            "YPS"    : self.YPS,
            "NXP"    : self.NXP,
            "NYP"    : self.NYP,
        }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)

        return outFile, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:WS)
#
import numpy
from xoppylib.xoppy_run_binaries import xoppy_calc_ws

out_file =  xoppy_calc_ws(
        ENERGY = {ENERGY},
        CUR    = {CUR},
        PERIOD = {PERIOD},
        N      = {N},
        KX     = {KX},
        KY     = {KY},
        EMIN   = {EMIN},
        EMAX   = {EMAX},
        NEE    = {NEE},
        D      = {D},
        XPC    = {XPC},
        YPC    = {YPC},
        XPS    = {XPS},
        YPS    = {YPS},
        NXP    = {NXP},
        NYP    = {NYP},
        )

# data to pass to power
data = numpy.loadtxt(out_file)
energy = data[:,0]
flux = data[:,1]
spectral_power = data[:,2]
cumulated_power = data[:,3]

#
# example plot
#
from srxraylib.plot.gol import plot
plot(energy,flux,
    xtitle="Photon energy [eV]",ytitle="Flux [photons/s/0.1%bw]",title="WS Flux",
    xlog=True,ylog=True,show=False)
plot(energy,spectral_power,
    xtitle="Photon energy [eV]",ytitle="Power [W/eV]",title="WS Spectral Power",
    xlog=True,ylog=True,show=False)
plot(energy,cumulated_power,
    xtitle="Photon energy [eV]",ytitle="Cumulated Power [W]",title="WS Cumulated Power",
    xlog=False,ylog=False,show=True)
    
#
# end script
#
"""
    def extract_data_from_xoppy_output(self, calculation_output):

        spec_file_name, script = calculation_output
        out = numpy.loadtxt(spec_file_name)
        if len(out) == 0: raise Exception("Calculation gave no results (empty data)")

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_specfile", spec_file_name)
        calculated_data.add_content("xoppy_data", out)
        calculated_data.add_content("xoppy_script", script)

        return calculated_data

    def get_data_exchange_widget_name(self):
        return "WS"

    def getTitles(self):
        return ['Flux','Spectral power','Cumulated power']

    def getXTitles(self):
        return ["Energy [eV]","Energy [eV]","Energy [eV]"]

    def getYTitles(self):
        return ["Flux [Photons/sec/0.1%bw]","Spectral Power [W/eV]","Cumulated Power [W]"]

    def getVariablesToPlot(self):
        return [(0, 1),(0, 2),(0, 3)]

    def getLogPlot(self):
        return [(True, True),(True, True),(False, False)]

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data._light_source._magnetic_structure, synedid.InsertionDevice):
                light_source = data._light_source

                self.N = int(light_source._magnetic_structure._number_of_periods)
                self.ENERGY = light_source._electron_beam._energy_in_GeV
                self.CUR = 1e3*light_source._electron_beam._current
                self.PERIOD = 1e2*light_source._magnetic_structure._period_length
                self.KY = light_source._magnetic_structure._K_vertical

                self.set_enabled(False)

            else:
                self.set_enabled(True)
        else:
            self.set_enabled(True)

    def set_enabled(self,value):
        if value == True:
                self.id_N.setEnabled(True)
                self.id_ENERGY.setEnabled(True)
                self.id_CUR.setEnabled(True)
                self.id_PERIOD.setEnabled(True)
                self.id_KY.setEnabled(True)
        else:
                self.id_N.setEnabled(False)
                self.id_ENERGY.setEnabled(False)
                self.id_CUR.setEnabled(False)
                self.id_PERIOD.setEnabled(False)
                self.id_KY.setEnabled(False)

if __name__ == "__main__":
    import os, sys
    os.environ['LD_LIBRARY_PATH'] = ''
    app = QApplication(sys.argv)
    w = OWws()
    w.show()
    app.exec()
    w.saveSettings()
