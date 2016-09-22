import sys,os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

class OWxtc(XoppyWidget):
    name = "Undulator Tuning Curves"
    id = "orange.widgets.dataxtc"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xtc.png"
    priority = 2
    category = ""
    keywords = ["xoppy", "xtc"]

    #19 variables (minus one: TITLE removed)
    ENERGY = Setting(7.0)
    CURRENT = Setting(100.0)
    ENERGY_SPREAD = Setting(0.00096)
    SIGX = Setting(0.274)
    SIGY = Setting(0.011)
    SIGX1 = Setting(0.0113)
    SIGY1 = Setting(0.0036)
    PERIOD = Setting(3.23)
    NP = Setting(70)
    EMIN = Setting(2950.0)
    EMAX = Setting(13500.0)
    N = Setting(40)
    HARMONIC_FROM = Setting(1)
    HARMONIC_TO = Setting(15)
    HARMONIC_STEP = Setting(2)
    HELICAL = Setting(0)
    METHOD = Setting(1)
    NEKS = Setting(100)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, "XTC Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY_SPREAD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "N",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HARMONIC_FROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HARMONIC_TO",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HARMONIC_STEP",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 21
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "HELICAL",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Planar undulator', 'Helical undulator'],
                     valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)



        #widget index 22
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                     items=['Finite-N', 'Infinite N with convolution'],
                     valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NEKS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

    def unitLabels(self):
         return ['Electron energy (GeV)','Current (mA)','Energy Spread (DE/E)',
                 'Sigma X (mm)','Sigma Y (mm)',"Sigma X' (mrad)","Sigma Y' (mrad)",
                 'Period length (cm)','Number of periods',
                 'E1 minimum energy (eV)','E1 maximum energy (eV)',
                 'Number of energy-points','Minimum harmonic number','Maximum harmonic number','Harmonic step size',
                 'Mode','Method','Intrinsic NEKS']


    def unitFlags(self):
         return ['True' for i in range(19)]


    def get_help_name(self):
        return 'xtc'

    def check_fields(self):
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Electron Energy")
        self.CURRENT = congruence.checkStrictlyPositiveNumber(self.CURRENT, "Current")
        self.ENERGY_SPREAD = congruence.checkStrictlyPositiveNumber(self.ENERGY_SPREAD, "Energy Spread")
        self.SIGX  = congruence.checkPositiveNumber(self.SIGX , "Sigma X")
        self.SIGY  = congruence.checkPositiveNumber(self.SIGY , "Sigma Y")
        self.SIGX1 = congruence.checkPositiveNumber(self.SIGX1, "Sigma X'")
        self.SIGY1 = congruence.checkPositiveNumber(self.SIGY1, "Sigma Y'")
        self.PERIOD = congruence.checkStrictlyPositiveNumber(self.PERIOD, "Period length")
        self.NP = congruence.checkStrictlyPositiveNumber(self.NP, "Number of periods")
        self.EMIN = congruence.checkPositiveNumber(self.EMIN, "E1 minimum energy")
        self.EMAX = congruence.checkStrictlyPositiveNumber(self.EMAX, "E1 maximum energy")
        congruence.checkLessThan(self.EMIN, self.EMAX, "E1 minimum energy", "E1 maximum energy")
        self.N = congruence.checkStrictlyPositiveNumber(self.N, "Number of Energy Points")
        self.HARMONIC_FROM = congruence.checkStrictlyPositiveNumber(self.HARMONIC_FROM, "Minimum harmonic number")
        self.HARMONIC_TO = congruence.checkStrictlyPositiveNumber(self.HARMONIC_TO, "Maximum harmonic number")
        congruence.checkLessThan(self.HARMONIC_FROM, self.HARMONIC_TO, "Minimum harmonic number", "Maximum harmonic number")
        self.HARMONIC_STEP = congruence.checkStrictlyPositiveNumber(self.HARMONIC_STEP, "Harmonic step size")
        self.NEKS  = congruence.checkPositiveNumber(self.NEKS , "Intrinsic NEKS")

    def do_xoppy_calculation(self):
        return self.xoppy_calc_xtc()

    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):


        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        self.plot_canvas[plot_canvas_index].setDefaultPlotLines(False)
        self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)

    def get_data_exchange_widget_name(self):
        return "XTC"

    def getTitles(self):
        return ["Brilliance","Ky","Total Power","Power density"]

    def getXTitles(self):
        return ["Energy (eV)","Energy (eV)","Energy (eV)","Energy (eV)"]

    def getYTitles(self):
        return ["Brilliance (ph/s/mrad^2/mm^2/0.1%bw)","Ky","Total Power (W)","Power density (W/mr^2)"]

    def getVariablesToPlot(self):
        return [(1, 2), (1, 3), (1, 4), (1, 5)]

    def getLogPlot(self):
        return[(False, False), (False, False), (False, False), (False, False)]

    def xoppy_calc_xtc(self):

        for file in ["tc.inp","tc.out"]:
            try:
                os.remove(os.path.join(locations.home_bin_run(),file))
            except:
                pass

        with open("tc.inp", "wt") as f:
            f.write("TS called from xoppy\n")
            f.write("%10.3f %10.2f %10.6f %s\n"%(self.ENERGY,self.CURRENT,self.ENERGY_SPREAD,"Ring-Energy(GeV) Current(mA) Beam-Energy-Spread"))
            f.write("%10.4f %10.4f %10.4f %10.4f %s\n"%(self.SIGX,self.SIGY,self.SIGX1,self.SIGY1,"Sx(mm) Sy(mm) Sx1(mrad) Sy1(mrad)"))
            f.write("%10.3f %d %s\n"%(self.PERIOD,self.NP,"Period(cm) N"))
            f.write("%10.1f %10.1f %d %s\n"%(self.EMIN,self.EMAX,self.N,"Emin Emax Ne"))
            f.write("%d %d %d %s\n"%(self.HARMONIC_FROM,self.HARMONIC_TO,self.HARMONIC_STEP,"Hmin Hmax Hstep"))
            f.write("%d %d %d %d %s\n"%(self.HELICAL,self.METHOD,1,self.NEKS,"Helical Method Print_K Neks"))
            f.write("foreground\n")

        command = os.path.join(locations.home_bin(), 'tc')
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("Output file: %s"%("tc.out"))
        print("\n--------------------------------------------------------\n")

        #
        # parse result files to exchange object
        #


        with open("tc.out","r") as f:
            lines = f.readlines()

        # print output file
        for line in lines:
            print(line, end="")


        # remove returns
        lines = [line[:-1] for line in lines]

        # separate numerical data from text
        floatlist = []
        txtlist = []
        for line in lines:
            try:
                tmp = float(line.strip()[0])
                floatlist.append(line)
            except:
                txtlist.append(line)

        data = numpy.loadtxt(floatlist).T

        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", data.T)
            calculated_data.add_content("plot_x_col", 1)
            calculated_data.add_content("plot_y_col", 2)
        except:
            pass
        try:
            calculated_data.add_content("labels",["Energy (eV) without emittance", "Energy (eV) with emittance",
                                      "Brilliance (ph/s/mrad^2/mm^2/0.1%bw)","Ky","Total Power (W)","Power density (W/mr^2)"])
        except:
            pass
        try:
            calculated_data.add_content("info",txtlist)
        except:
            pass

        return calculated_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtc()
    w.show()
    app.exec()
    w.saveSettings()
