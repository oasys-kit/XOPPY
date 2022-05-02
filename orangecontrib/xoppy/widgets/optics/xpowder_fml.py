import sys,os
import numpy
import platform
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from xoppylib.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from xoppylib.xoppy_run_binaries import xoppy_calc_powder_fml

class OWxpowder_fml(XoppyWidget):
    name = "POWDER_FML"
    id = "orange.widgets.dataxpowder_fml"
    description = "X-ray Powder Diffraction Pattern"
    icon = "icons/xoppy_xpowder_fml.png"
    priority = 23
    category = ""
    keywords = ["xoppy", "xpowder_fml"]


    FILE = Setting(os.path.join(locations.home_data(), "cif" + os.sep + "icsd_31142_sepiolite_BraunerPreisinger.cif"))
    TITLE = Setting("powder pattern using crysFML")
    LAMBDA = Setting(1.54056)
    JOB = Setting(0)
    U = Setting(0.0002)
    V = Setting(-0.0002)
    W = Setting(0.012)
    X = Setting(0.0019)
    LS = Setting(1900.0)
    THMIN = Setting(1.0)
    STEP = Setting(0.05)
    THMAX = Setting(135.0)

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box)

        file_box = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file = oasysgui.lineEdit(file_box, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.button(file_box, self, "...", callback=self.selectFile)

        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "LAMBDA",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "JOB",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['X rays', 'Neutrons'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "U",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "V",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "W",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "X",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "LS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "STEP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

    def unitLabels(self):
         return ['CIF File: ','Title:','Lambda [A]: ','Radiation:','U: ','V: ','W: ','X: ','Ls:','TwoTheta from [deg]','TwoTheta step: ','TwoTheta to','None']

    def unitFlags(self):
         return ['1','1','1','1','1','1','1','1','1','1','1','1','1']

    def selectFile(self):
        self.le_file.setText(oasysgui.selectFileFromDialog(self, self.FILE, "Open CIF File", file_extension_filter="*.cif"))

    def get_help_name(self):
        return 'powder_fml'

    def check_fields(self):
        congruence.checkFile(self.FILE)
        self.LAMBDA = congruence.checkStrictlyPositiveNumber(self.LAMBDA, "Lambda")
        self.U = congruence.checkNumber(self.U, "U")
        self.V = congruence.checkNumber(self.V, "V")
        self.W = congruence.checkNumber(self.W, "W")
        self.X = congruence.checkNumber(self.X, "X")
        self.LS = congruence.checkNumber(self.LS, "LS")
        self.THMIN = congruence.checkPositiveAngle(self.THMIN, "TwoTheta from")
        self.THMAX = congruence.checkPositiveAngle(self.THMAX, "TwoTheta to")
        self.STEP = congruence.checkStrictlyPositiveAngle(self.STEP, "TwoTheta step")
        congruence.checkGreaterThan(self.THMAX, self.THMIN, "TwoTheta to", "TwoTheta from")

    def do_xoppy_calculation(self):
        files = xoppy_calc_powder_fml(
            FILE   = self.FILE  ,
            TITLE  = self.TITLE ,
            LAMBDA = self.LAMBDA,
            JOB    = self.JOB   ,
            U      = self.U     ,
            V      = self.V     ,
            W      = self.W     ,
            X      = self.X     ,
            LS     = self.LS    ,
            THMIN  = self.THMIN ,
            STEP   = self.STEP  ,
            THMAX  = self.THMAX ,
            )

        dict_parameters = {
            "FILE"   : self.FILE  ,
            "TITLE"  : self.TITLE ,
            "LAMBDA" : self.LAMBDA,
            "JOB"    : self.JOB   ,
            "U"      : self.U     ,
            "V"      : self.V     ,
            "W"      : self.W     ,
            "X"      : self.X     ,
            "LS"     : self.LS    ,
            "THMIN"  : self.THMIN ,
            "STEP"   : self.STEP  ,
            "THMAX"  : self.THMAX ,
        }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)

        return files

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:powder_fml)
#
from xoppylib.xoppy_run_binaries import xoppy_calc_powder_fml

out_files =  xoppy_calc_powder_fml(
            FILE   = "{FILE}",
            TITLE  = "{TITLE}",
            LAMBDA = {LAMBDA},
            JOB    = {JOB},
            U      = {U},
            V      = {V},
            W      = {W},
            X      = {X},
            LS     = {LS},
            THMIN  = {THMIN},
            STEP   = {STEP},
            THMAX  = {THMAX},
        )

#
# example plot
#
import numpy
from srxraylib.plot.gol import plot

data = numpy.loadtxt(out_files[2], skiprows=3)

plot(data[:,0],data[:,-1],
    xtitle="TwoTheta[Deg]",ytitle="Intensity[a.u.]",title="Powder diffraction crystal_fml",
    xlog=False,ylog=False,show=True)

#
# end script
#
"""

    def get_data_exchange_widget_name(self):
        return "XPOWDER_FML"

    def getTitles(self):
        return ["Diffraction Pattern"]

    def getXTitles(self):
        return ["TwoTheta[Deg]"]

    def getYTitles(self):
        return ["Intensity[a.u.]"]

    def extract_data_from_xoppy_output(self, calculation_output):

        # files = ["xpowder_fml.par", "xpowder_fml.ref", "xpowder_fml.out"]
        files = calculation_output

        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", numpy.loadtxt(files[2], skiprows=3))
            calculated_data.add_content("plot_x_col",0)
            calculated_data.add_content("plot_y_col",-1)
        except:
            pass
        try:
            calculated_data.add_content("labels",["TwoTheta[Deg]","Intensity[a.u.]"])
        except:
            pass
        try:
            with open(files[0]) as f:
                info = f.readlines()
            info = [line[:-1] for line in info]  # remove "\n"
            calculated_data.add_content("info",info)
        except:
            pass


        return calculated_data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxpowder_fml()
    w.show()
    app.exec()
    w.saveSettings()
