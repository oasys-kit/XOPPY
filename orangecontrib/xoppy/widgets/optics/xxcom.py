import platform
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from xoppylib.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from xoppylib.xoppy_run_binaries import xoppy_calc_xcom

class OWxxcom(XoppyWidget):
    name = "XCOM"
    id = "orange.widgets.dataxxcom"
    description = "X-ray Matter Cross Sections"
    icon = "icons/xoppy_xxcom.png"
    priority = 21
    category = ""
    keywords = ["xoppy", "xxcom"]

    NAME = Setting("Pyrex Glass")
    SUBSTANCE = Setting(3)
    DESCRIPTION = Setting("SiO2:B2O3:Na2O:Al2O3:K2O")
    FRACTION = Setting("0.807:0.129:0.038:0.022:0.004")
    GRID = Setting(1)
    GRIDINPUT = Setting(0)
    GRIDDATA = Setting("0.0804:0.2790:0.6616:1.3685:2.7541")
    ELEMENTOUTPUT = Setting(0)

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NAME",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=80)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SUBSTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Element (Atomic number)', 'Element (Symbol)', 'Compound (Formula)', 'Mixture (F1:F2:F3...)'],
                    valueType=int, orientation="horizontal", callback=self.set_SUBSTANCE)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTION",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=80)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FRACTION",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=80)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Standard', 'Standard+points', 'Points only'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRIDINPUT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['From Keyboard', 'From file'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDDATA",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ELEMENTOUTPUT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Cross section [b/atom]', 'Cross section [b/atom] & Attenuation coeff [cm2/g]', 'Partial interaction coeff & Attenuation coeff [cm2/g]'],
                    valueType=int, orientation="horizontal", callback=self.set_ELEMENTOUTPUT)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def set_SUBSTANCE(self):
        self.initializeTabs()

    def set_ELEMENTOUTPUT(self):
        self.initializeTabs()

    def unitLabels(self):
         return ['Name','Substance:','Description:','fraction','grid','grid points','grid points [MeV]/file name','Output quantity']

    def unitFlags(self):
         return ['True','True','True','self.SUBSTANCE  ==  3','True','self.GRID  !=  0','(self.GRID  !=  0)','self.SUBSTANCE  <=  1']
    
    def get_help_name(self):
        return 'xcom'

    def check_fields(self):
        self.DESCRIPTION = congruence.checkEmptyString(self.DESCRIPTION, "Description")

        if self.SUBSTANCE == 3:
            self.FRACTION = congruence.checkEmptyString(self.FRACTION, "fraction")

        if self.GRID != 0:
            if self.GRIDINPUT == 0:
                self.GRIDDATA = congruence.checkEmptyString(self.GRIDDATA, "grid points")
            else:
                congruence.checkFile(self.GRIDDATA)

    def do_xoppy_calculation(self):
        out_file = xoppy_calc_xcom(
            NAME          = self.NAME,
            SUBSTANCE     = self.SUBSTANCE,
            DESCRIPTION   = self.DESCRIPTION,
            FRACTION      = self.FRACTION,
            GRID          = self.GRID,
            GRIDINPUT     = self.GRIDINPUT,
            GRIDDATA      = self.GRIDDATA,
            ELEMENTOUTPUT = self.ELEMENTOUTPUT,
        )

        dict_parameters = {
            "NAME"          : self.NAME,
            "SUBSTANCE"     : self.SUBSTANCE,
            "DESCRIPTION"   : self.DESCRIPTION,
            "FRACTION"      : self.FRACTION,
            "GRID"          : self.GRID,
            "GRIDINPUT"     : self.GRIDINPUT,
            "GRIDDATA"      : self.GRIDDATA,
            "ELEMENTOUTPUT" : self.ELEMENTOUTPUT,
        }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)
        return out_file

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:xcom)
#
from xoppylib.xoppy_run_binaries import xoppy_calc_xcom

out_file =  xoppy_calc_xcom(
            NAME          = "{NAME}",
            SUBSTANCE     = {SUBSTANCE},
            DESCRIPTION   = "{DESCRIPTION}",
            FRACTION      = "{FRACTION}",
            GRID          = {GRID},
            GRIDINPUT     = {GRIDINPUT},
            GRIDDATA      = "{GRIDDATA}",
            ELEMENTOUTPUT = {ELEMENTOUTPUT},
        )

#
# example plot
#
import numpy
from srxraylib.plot.gol import plot

data = numpy.loadtxt(out_file)
energy_in_MeV = data[:,0]
total = data[:,6]

plot(energy_in_MeV,total,
    xtitle="Photon energy [MeV]",ytitle="Tot atten with coh scat ",title="XCOM attenuation",
    xlog=True,ylog=True,show=True)


#
# end script
#
"""

    def get_data_exchange_widget_name(self):
        return "XCOM"

    def getTitles(self):
        return ["Coherent scat",
                "Incoherent scat",
                "Photoel abs",
                "Pair prod in nucl field]",
                "Pair prod in elec field]",
                "Tot atten with coh scat]",
                "Tot atten w/o coh scat"]

    def getXTitles(self):
        return ["Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]"]

    def getYTitles(self):
        if (1+self.SUBSTANCE) <= 2:
            if (1+self.ELEMENTOUTPUT) == 1:
                return ["Coherent scat [b/atom]",
                        "Incoherent scat [b/atom]",
                        "Photoel abs [b/atom]",
                        "Pair prod in nucl field [b/atom]",
                        "Pair prod in elec field [b/atom]",
                        "Tot atten with coh scat [b/atom]",
                        "Tot atten w/o coh scat [b/atom]"]
            elif (1+self.ELEMENTOUTPUT) == 2:
                return ["Coherent scat [b/atom]",
                        "Incoherent scat [b/atom]",
                        "Photoel abs [b/atom]",
                        "Pair prod in nucl field [b/atom]",
                        "Pair prod in elec field [b/atom]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]
            elif (1+self.ELEMENTOUTPUT) == 3:
                return ["Coherent scat [cm2/g]",
                        "Incoherent scat [cm2/g]",
                        "Photoel abs [cm2/g]",
                        "Pair prod in nucl field [cm2/g]",
                        "Pair prod in elec field [cm2/g]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]
            else:
                return ["Coherent scat [cm2/g]",
                        "Incoherent scat [cm2/g]",
                        "Photoel abs [cm2/g]",
                        "Pair prod in nucl field [cm2/g]",
                        "Pair prod in elec field [cm2/g]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]
        else:
                return ["Coherent scat [cm2/g]",
                        "Incoherent scat [cm2/g]",
                        "Photoel abs [cm2/g]",
                        "Pair prod in nucl field [cm2/g]",
                        "Pair prod in elec field [cm2/g]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]

    def getLogPlot(self):
        return [(True, True), (True, True), (True, True), (True, True), (True, True), (True, True), (True, True)]


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = OWxxcom()
    w.show()
    app.exec()
    w.saveSettings()
