import sys
import numpy
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject


from xoppylib.crystals.tools import bragg_calc, bragg_calc2, crystal_fh
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import xraylib
from dabax.dabax_xraylib import DabaxXraylib

class OWxfh(XoppyWidget):
    name = "Fh"
    id = "orange.widgets.dataxfh"
    description = "Crystal Structure Factors"
    icon = "icons/xoppy_xfh.png"
    priority = 17
    category = ""
    keywords = ["xoppy", "xfh"]

    ILATTICE = Setting(32)
    HMILLER = Setting(1)
    KMILLER = Setting(1)
    LMILLER = Setting(1)
    plot_variable = Setting(0)
    I_PLOT = Setting(2)
    TEMPER = Setting(1.0)
    ENERGY = Setting(8000.0)
    ENERGY_END = Setting(18000.0)
    NPOINTS = Setting(20)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME = Setting("Fh.dat")

    # new crystals  #todo: add to menus?
    material_constants_library_flag = Setting(2) # 0=xraylib, 1=dabax, 2=xraylib completed by dabax
    dx = None # DABAX object

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ILATTICE",
                    label=self.unitLabels()[idx], addSpace=False,
                    items=self.get_crystal_list(),
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HMILLER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "KMILLER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "LMILLER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "plot_variable",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=self.plotOptionList()[2:],
                    valueType=int, orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TEMPER",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY_END",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        # widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["No", "Yes"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)


        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal:','h miller index','k miller index','l miller index',
                 'Plot:','Temperature factor [see help]:',
                 'From Energy [eV]','To energy [eV]','Number of points',
                 'Dump to file','File name']

    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True',
                  "True","self.DUMP_TO_FILE == 1"]

    def plotOptionList(self):
        return ["Photon energy [eV]",
                  "Wavelength [A]",
                  "Bragg angle [deg]",
                  "Re(f_0)",
                  "Im(f_0)  ",
                  "Re(FH)",
                  "Im(FH)",
                  "Re(FH_BAR)",
                  "Im(FH_BAR)",
                  "Re(psi_0)",
                  "Im(psi_0)  ",
                  "Re(psi_H)",
                  "Im(psi_H)",
                  "Re(psi_BAR)",
                  "Im(psi_BAR)",
                  "Re(F(h,k,l))",
                  "Im(F(h,k,l))",
                  "delta (1-Re(refrac))",
                  "Re(refrac index)",
                  "Im(refrac index)",
                  "absorption coeff",
                  "s-pol Darwin half-width [microrad]",
                  "p-pol Darwin half-width [microrad]",
                  "Sin(Bragg angle)/Lambda",
                  "psi_over_f"]


    def get_help_name(self):
        return 'fh'

    def check_fields(self):
        self.HMILLER = congruence.checkNumber(self.HMILLER, "h miller index")
        self.KMILLER = congruence.checkNumber(self.KMILLER, "k miller index")
        self.LMILLER = congruence.checkNumber(self.LMILLER, "l miller index")

        self.TEMPER = congruence.checkNumber(self.TEMPER, "Temperature factor")

        self.ENERGY = congruence.checkPositiveNumber(self.ENERGY, "Energy from")
        self.ENERGY_END = congruence.checkStrictlyPositiveNumber(self.ENERGY_END, "Energy to")
        congruence.checkLessThan(self.ENERGY, self.ENERGY_END, "Energy from", "Energy to")
        self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.NPOINTS, "Number of Points")

    def get_crystal_list(self):
        crystal_list_xrl = list(xraylib.Crystal_GetCrystalsList())

        if self.material_constants_library_flag == 0:
            return crystal_list_xrl

        if self.dx is None:
            self.dx = DabaxXraylib()
        crystal_list_dabax = self.dx.Crystal_GetCrystalsList()

        if self.material_constants_library_flag == 1:
            return crystal_list_dabax

        crystal_list_combined = crystal_list_xrl
        for crystal in crystal_list_dabax:
            if crystal not in crystal_list_combined:
                crystal_list_combined.append(crystal)

        if self.material_constants_library_flag == 2:
            return crystal_list_combined

    def do_xoppy_calculation(self):
        self.I_PLOT = self.plot_variable + 2
        return self.xoppy_calc_xfh()

    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def get_data_exchange_widget_name(self):
        return "XFH"

    def getTitles(self):
        return ["Calculation Result"]

    def getXTitles(self):
        return ["Photon energy [eV]"]

    def getYTitles(self):
        return [self.plotOptionList()[self.I_PLOT]]

    def getVariablesToPlot(self):
        return [(0, self.I_PLOT)]

    def getLogPlot(self):
        return[(False, False)]

    def xoppy_calc_xfh(self):
        #TODO: remove I_ABSORP
        ILATTICE = self.ILATTICE
        HMILLER = self.HMILLER
        KMILLER = self.KMILLER
        LMILLER = self.LMILLER
        I_PLOT = self.I_PLOT
        TEMPER = self.TEMPER
        ENERGY = self.ENERGY
        ENERGY_END = self.ENERGY_END
        NPOINTS = self.NPOINTS

        descriptor = self.get_crystal_list()[self.ILATTICE]

        if self.material_constants_library_flag == 0:
            material_constants_library = xraylib
        elif self.material_constants_library_flag == 1:
            material_constants_library = self.dx
        elif self.material_constants_library_flag == 2:
            if descriptor in xraylib.Crystal_GetCrystalsList():
                material_constants_library = xraylib
            elif descriptor in self.dx.Crystal_GetCrystalsList():
                material_constants_library = self.dx
            else:
                raise Exception("Descriptor not found in material constants database")

        # descriptor = material_constants_library.Crystal_GetCrystalsList()[ILATTICE]
        print("Using crystal descriptor: ",descriptor)

        bragg_dictionary = bragg_calc2(descriptor=descriptor,
                                        hh=HMILLER,
                                        kk=KMILLER,
                                        ll=LMILLER,
                                        temper=TEMPER,
                                        emin=ENERGY,
                                        emax=ENERGY_END,
                                        estep=50.0,
                                        fileout=None,
                                        material_constants_library=material_constants_library)

        energy = numpy.linspace(ENERGY,ENERGY_END,NPOINTS)
        out = numpy.zeros((25,NPOINTS))
        info = ""
        for i,ienergy in enumerate(energy):
            dic2 = crystal_fh(bragg_dictionary,ienergy)
            print("Energy=%g eV FH=(%g,%g)"%(ienergy,dic2["STRUCT"].real,dic2["STRUCT"].imag))

            out[0,i]  = ienergy
            out[1,i]  = dic2["WAVELENGTH"]*1e10
            out[2,i]  = dic2["THETA"]*180/numpy.pi
            out[3,i]  = dic2["F_0"].real
            out[4,i]  = dic2["F_0"].imag
            out[5,i]  = dic2["FH"].real
            out[6,i]  = dic2["FH"].imag
            out[7,i]  = dic2["FH_BAR"].real
            out[8,i]  = dic2["FH_BAR"].imag
            out[9,i]  = dic2["psi_0"].real
            out[10,i] = dic2["psi_0"].imag
            out[11,i] = dic2["psi_h"].real
            out[12,i] = dic2["psi_h"].imag
            out[13,i] = dic2["psi_hbar"].real
            out[14,i] = dic2["psi_hbar"].imag
            out[15,i] = dic2["STRUCT"].real
            out[16,i] = dic2["STRUCT"].imag
            out[17,i] = dic2["DELTA_REF"]
            out[18,i] = dic2["REFRAC"].real
            out[19,i] = dic2["REFRAC"].imag
            out[20,i] = dic2["ABSORP"]
            out[21,i] = 1e6 * dic2["ssr"]  # in microrads
            out[22,i] = 1e6 * dic2["spr"]  # in microrads
            out[23,i] = dic2["RATIO"]
            out[24,i] = dic2["psi_over_f"]
            info += "#\n#\n#\n"
            info += dic2["info"]


        if self.DUMP_TO_FILE:
            with open(self.FILE_NAME, "w") as file:
                try:
                    file.write("#F %s\n"%self.FILE_NAME)
                    file.write("\n#S 1 xoppy CrossSec results\n")
                    file.write("#N %d\n"%(out.shape[0]))
                    tmp = "#L"
                    for item in self.plotOptionList():
                        tmp += "  %s"%(item)
                    tmp += "\n"
                    file.write(tmp)
                    for j in range(out.shape[1]):
                        file.write(("%19.12e  "*out.shape[0]+"\n")%tuple(out[i,j] for i in range(out.shape[0])))
                    file.close()
                    print("File written to disk: %s \n"%self.FILE_NAME)
                except:
                    raise Exception("CrossSec: The data could not be dumped onto the specified file!\n")

        #
        # write python script
        #
        if isinstance(material_constants_library, DabaxXraylib):
            material_constants_library_txt = "DabaxXraylib()"
        else:
            material_constants_library_txt = "xraylib"


        dict_parameters = {
            'descriptor':  descriptor,
            'ILATTICE'   : ILATTICE,
            'HMILLER'    : HMILLER,
            'KMILLER'    : KMILLER,
            'LMILLER'    : LMILLER,
            'I_PLOT'     : self.I_PLOT,
            'TEMPER'     : TEMPER,
            'ENERGY'     : ENERGY,
            'ENERGY_END' : ENERGY_END,
            'NPOINTS'    : NPOINTS,
            'material_constants_library_txt': material_constants_library_txt,
            'xtitle' : self.plotOptionList()[0],
            'ytitle' : self.plotOptionList()[self.I_PLOT],
            }


        self.xoppy_script.set_code(self.script_template().format_map(dict_parameters))


        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", out.T)
            calculated_data.add_content("plot_x_col",0)
            calculated_data.add_content("plot_y_col", I_PLOT)
        except:
            pass
        try:
            calculated_data.add_content("labels",self.plotOptionList())
        except:
            pass
        try:
            calculated_data.add_content("info",info)
        except:
            pass


        return calculated_data

    def script_template(self):
        return """
#
# script to calculate crystal diffraction profiles (created by XOPPY:crystal)
#

import numpy
from xoppylib.crystals.tools import bragg_calc2, crystal_fh
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

#
# run bragg_calc2 (preprocessor)
#    
bragg_dictionary = bragg_calc2(
    descriptor = "{descriptor}",
    hh         = {HMILLER}, 
    kk         = {KMILLER}, 
    ll         = {LMILLER}, 
    temper     = {TEMPER}, 
    emin       = {ENERGY},
    emax       = {ENERGY_END},
    estep      = 50,
    ANISO_SEL  = 0,
    fileout    = None,
    do_not_prototype = 0,  # 0=use site groups (recommended), 1=use all individual sites
    verbose = False,
    material_constants_library = {material_constants_library_txt},
    )

#
# run loop
#
energy = numpy.linspace({ENERGY},{ENERGY_END},{NPOINTS})
out = numpy.zeros((25,{NPOINTS}))
info = ""
for i,ienergy in enumerate(energy):
    dic2 = crystal_fh(bragg_dictionary,ienergy)
    print("Energy=%g eV FH=(%g,%g)"%(ienergy,dic2["STRUCT"].real,dic2["STRUCT"].imag))

    out[0,i]  = ienergy
    out[1,i]  = dic2["WAVELENGTH"]*1e10
    out[2,i]  = dic2["THETA"]*180/numpy.pi
    out[3,i]  = dic2["F_0"].real
    out[4,i]  = dic2["F_0"].imag
    out[5,i]  = dic2["FH"].real
    out[6,i]  = dic2["FH"].imag
    out[7,i]  = dic2["FH_BAR"].real
    out[8,i]  = dic2["FH_BAR"].imag
    out[9,i]  = dic2["psi_0"].real
    out[10,i] = dic2["psi_0"].imag
    out[11,i] = dic2["psi_h"].real
    out[12,i] = dic2["psi_h"].imag
    out[13,i] = dic2["psi_hbar"].real
    out[14,i] = dic2["psi_hbar"].imag
    out[15,i] = dic2["STRUCT"].real
    out[16,i] = dic2["STRUCT"].imag
    out[17,i] = dic2["DELTA_REF"]
    out[18,i] = dic2["REFRAC"].real
    out[19,i] = dic2["REFRAC"].imag
    out[20,i] = dic2["ABSORP"]
    out[21,i] = 1e6 * dic2["ssr"]  # in microrads
    out[22,i] = 1e6 * dic2["spr"]  # in microrads
    out[23,i] = dic2["RATIO"]
    out[24,i] = dic2["psi_over_f"]
    info += "#"
    info += dic2["info"]
            
#                       
# example plot
#
from srxraylib.plot.gol import plot
plot(out[0,:], out[{I_PLOT},:], xtitle="{xtitle}", ytitle="{ytitle}")

#
# end script
#
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxfh()
    w.show()
    app.exec()
    w.saveSettings()