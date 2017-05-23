import sys
import numpy
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.util.xoppy_xraylib_util import f1f2_calc,f1f2_calc_mix
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

import xraylib


class OWxf1f2(XoppyWidget):
    name = "F1F2"
    id = "orange.widgets.dataxf1f2"
    description = "X-ray Matter Scattering Functions and Reflectivity"
    icon = "icons/xoppy_xf1f2.png"
    priority = 15
    category = ""
    keywords = ["xoppy", "xf1f2"]

    # DATASETS = Setting(1)
    MAT_FLAG = Setting(0)
    DESCRIPTOR = Setting("Si")
    DENSITY = Setting(1.0)
    CALCULATE = Setting(1)
    GRID = Setting(0)
    GRIDSTART = Setting(5000.0)
    GRIDEND = Setting(25000.0)
    GRIDN = Setting(100)
    THETAGRID = Setting(0)
    ROUGH = Setting(0.0)
    THETA1 = Setting(2.0)
    THETA2 = Setting(5.0)
    THETAN = Setting(50)
    DUMP_TO_FILE = Setting(0)  # No
    FILE_NAME = Setting("f1f2.dat")

    xtitle = None
    ytitle = None

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Element(formula)', 'Mixture(formula)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DENSITY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CALCULATE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['f1', 'f2', 'delta', 'beta *see help*', 'mu [cm^-1] *see help*', 'mu [cm^2/g] *see help*', 'Cross Section[barn] *see help*', 'reflectivity-s', 'reflectivity-p', 'reflectivity-unpol', 'delta/beta **see help**'],
                    valueType=int, orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Standard', 'User defined', 'Single Value'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "THETAGRID",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Single value', 'User Defined'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ROUGH",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THETA1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETA2",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETAN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        # widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["No", "Yes"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)



        gui.rubber(self.controlArea)



    def unitLabels(self):
         return ['material',                        #   True',
                 'formula',                         #   self.MAT_FLAG  <=  1',
                 'density',                         #   self.MAT_FLAG  ==  1  &  (s
                 'Calculate',                       #   True',
                 'Energy [eV] grid:',               #   True',
                 'Starting Energy [eV]: ',          #   self.GRID  !=  0',
                 'To: ',                            #   self.GRID  ==  1',
                 'Number of points',                #   self.GRID  ==  1',
                 'Grazing angle',                   #   self.CALCULATE  ==  0 or (s
                 'Roughness rms [A]',               #   self.CALCULATE  ==  0 or (s
                 'Starting Graz angle [mrad]',      #   self.CALCULATE  ==  0 or (s
                 'To [mrad]',                       #   (self.CALCULATE  ==  0 or (
                 'Number of angular points',        #   (self.CALCULATE  ==  0 or (
                 'Dump to file',
                 'File name']


    def unitFlags(self):
         return ['True',
                 'self.MAT_FLAG  <=  1',
                 'self.MAT_FLAG  ==  1  or (self.MAT_FLAG  ==  1 and  (self.CALCULATE  ==  2 or self.CALCULATE  ==  3 or self.CALCULATE  ==  4 or self.CALCULATE  ==  7 or self.CALCULATE  ==  8 or self.CALCULATE  ==  9 or self.CALCULATE  ==  10 ))  ',
                 'True',
                 'True',
                 'self.GRID  !=  0',
                 'self.GRID  ==  1',
                 'self.GRID  ==  1',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 '(self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9)  &  self.THETAGRID  ==  1',
                 '(self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9)  &  self.THETAGRID  ==  1',
                 'True',
                 'self.DUMP_TO_FILE == 1']

    def get_help_name(self):
        return 'f1f2'

    def check_fields(self):
        self.DESCRIPTOR = congruence.checkEmptyString(self.DESCRIPTOR, "formula")
        if self.MAT_FLAG == 1:
            self.DENSITY = congruence.checkStrictlyPositiveNumber(self.DENSITY, "density")

        if self.GRID > 0:
            self.GRIDSTART = congruence.checkPositiveNumber(self.GRIDSTART, "Starting Energy")

            if self.GRID == 1:
                self.GRIDEND = congruence.checkStrictlyPositiveNumber(self.GRIDEND, "Energy to")
                congruence.checkLessThan(self.GRIDSTART, self.GRIDEND, "Starting Energy", "Energy to")
                self.GRIDN = congruence.checkStrictlyPositiveNumber(self.GRIDN, "Number of points")

        if self.CALCULATE >= 7 and self.CALCULATE <= 9:
            self.ROUGH = congruence.checkPositiveNumber(self.ROUGH, "Roughness")
            self.THETA1 = congruence.checkPositiveNumber(self.THETA1, "Starting Graz angle")

            if self.THETAGRID == 1:
                self.THETA2 = congruence.checkStrictlyPositiveNumber(self.THETA2, "Graz angle to")
                congruence.checkLessThan(self.THETA1, self.THETA2, "Starting Graz angle", "Graz angle to")
                self.THETAN = congruence.checkStrictlyPositiveNumber(self.THETAN, "Number of angular points")
        else:
            self.THETAGRID = 0

    def do_xoppy_calculation(self):
        return self.xoppy_calc_xf1f2()

    def extract_data_from_xoppy_output(self, calculation_output):
        try:
            calculation_output.get_content("data2D")
        except:
            try:
                tmp = calculation_output.get_content("xoppy_data")
                labels = calculation_output.get_content("labels")

                self.xtitle = labels[0]
                self.ytitle = labels[1]

                if tmp.shape == (1, 2): # single value calculation
                    message = calculation_output.get_content("info")
                    QMessageBox.information(self,
                                            "Calculation Result",
                                            "Calculation Result:\n %s"%message,
                                            QMessageBox.Ok)

            except:
                QMessageBox.information(self,
                                        "Calculation Result",
                                        "Calculation Result:\n"+calculation_output.get_content("info"),
                                        QMessageBox.Ok)

                self.xtitle = None
                self.ytitle = None

        return calculation_output

    def plot_results(self, calculated_data, progressBarValue=80):
        self.initializeTabs()

        try:
            calculated_data.get_content("xoppy_data")

            self.tab[0].layout().removeItem(self.tab[0].layout().itemAt(0))
            self.plot_canvas[0] = None

            super().plot_results(calculated_data, progressBarValue)
        except:
            try:
                data2D = calculated_data.get_content("data2D")
                dataX = calculated_data.get_content("dataX")
                dataY = calculated_data.get_content("dataY")

                self.plot_data2D(data2D, dataX, dataY, 0, 0,
                                 xtitle='Energy [eV]',
                                 ytitle='Theta [mrad]',
                                 title='Reflectivity')
            except:
                try:
                    self.plot_info(calculated_data.get_content("info") + "\n", progressBarValue, 0, 0)
                except:
                    pass


    def get_data_exchange_widget_name(self):
        return "XF1F2"

    def getTitles(self):
        return ["Calculation Result"]

    def getXTitles(self):
        if self.xtitle is None:
            return [""]
        else:
            return [self.xtitle]

    def getYTitles(self):
        if self.ytitle is None:
            return [""]
        else:
            return [self.ytitle]

    def getVariablesToPlot(self):
        return [(0, 1)]

    def getLogPlot(self):
        return[(True, True)]

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):
        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        # place a big dot if there is only a single value
        if ((x.size == 1) and (y.size == 1)):
            self.plot_canvas[plot_canvas_index].setDefaultPlotLines(False)
            self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)


    def xoppy_calc_xf1f2(self):

        MAT_FLAG   = self.MAT_FLAG
        DESCRIPTOR = self.DESCRIPTOR
        density    = self.DENSITY
        CALCULATE  = self.CALCULATE
        GRID       = self.GRID
        GRIDSTART  = self.GRIDSTART
        GRIDEND    = self.GRIDEND
        GRIDN      = self.GRIDN
        THETAGRID  = self.THETAGRID
        ROUGH      = self.ROUGH
        THETA1     = self.THETA1
        THETA2     = self.THETA2
        THETAN     = self.THETAN

        if MAT_FLAG == 0: # element
            descriptor = DESCRIPTOR
            density = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(DESCRIPTOR))
        elif MAT_FLAG == 1: # formula
            descriptor = DESCRIPTOR

        if GRID == 0: # standard energy grid
            energy = numpy.arange(0,500)
            elefactor = numpy.log10(10000.0 / 30.0) / 300.0
            energy = 10.0 * 10**(energy * elefactor)
        elif GRID == 1: # user energy grid
            if GRIDN == 1:
                energy = numpy.array([GRIDSTART])
            else:
                energy = numpy.linspace(GRIDSTART,GRIDEND,GRIDN)
        elif GRID == 2: # single energy point
            energy = numpy.array([GRIDSTART])

        if THETAGRID == 0:
            theta = numpy.array([THETA1])
        else:
            theta = numpy.linspace(THETA1,THETA2,THETAN)


        CALCULATE_items=['f1', 'f2', 'delta', 'beta', 'mu [cm^-1]', 'mu [cm^2/g]', 'Cross Section [barn]', 'reflectivity-s', 'reflectivity-p', 'reflectivity-unpol', 'delta/beta ']

        out = numpy.zeros((energy.size,theta.size))
        for i,itheta in enumerate(theta):
            if MAT_FLAG == 0: # element
                tmp = f1f2_calc(descriptor,energy,1e-3*itheta,F=1+CALCULATE,rough=ROUGH,density=density)
                out[:,i] = tmp
            else:
                tmp = f1f2_calc_mix(descriptor,energy,1e-3*itheta,F=1+CALCULATE,rough=ROUGH,density=density)
                out[:,i] = tmp

        if ((energy.size == 1) and (theta.size == 1)):
            info = "** Single value calculation E=%g eV, theta=%g mrad, Result(F=%d)=%g "%(energy[0],theta[0],1+CALCULATE,out[0,0])
            labels = ["Energy [eV]",CALCULATE_items[CALCULATE]]
            tmp = numpy.vstack((energy,out[:,0]))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",energy.shape,out.shape,tmp.shape)
            out_dict = {"application":"xoppy","name":"xf12","info":info, "data":tmp,"labels":labels}
        elif theta.size == 1:
            tmp = numpy.vstack((energy,out[:,0]))
            labels = ["Energy [eV]",CALCULATE_items[CALCULATE]]
            out_dict = {"application":"xoppy","name":"xf12","data":tmp,"labels":labels}
        elif energy.size == 1:
            tmp = numpy.vstack((theta,out[0,:]))
            labels = ["Theta [mrad]",CALCULATE_items[CALCULATE]]
            out_dict = {"application":"xoppy","name":"xf12","data":tmp,"labels":labels}
        else:
            labels = [r"energy[eV]",r"theta [mrad]"]
            out_dict = {"application":"xoppy","name":"xf12","data2D":out,"dataX":energy,"dataY":theta,"labels":labels}

        #
        #
        #
        if "info" in out_dict.keys():
            print(out_dict["info"])

        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", out_dict["data"].T)
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", -1)
        except:
            pass

        try:
            calculated_data.add_content("labels", out_dict["labels"])
        except:
            pass

        try:
            calculated_data.add_content("info", out_dict["info"])
        except:
            pass

        try:
            calculated_data.add_content("data2D", out_dict["data2D"])
            calculated_data.add_content("dataX", out_dict["dataX"])
            calculated_data.add_content("dataY", out_dict["dataY"])
        except:
            pass


        if self.DUMP_TO_FILE:
            with open(self.FILE_NAME, "w") as file:
                try:
                    file.write("#F %s\n"%self.FILE_NAME)
                    file.write("\n#S 1 xoppy f1f2 results\n")

                    print("data shape",out_dict["data"].shape)
                    print("labels: ",out_dict["labels"])
                    file.write("#N 2\n")
                    file.write("#L  %s  %s\n"%(out_dict["labels"][0],out_dict["labels"][1]))
                    out = out_dict["data"]
                    for j in range(out.shape[1]):
                        file.write(("%19.12e  "*out.shape[0]+"\n")%tuple(out[i,j] for i in range(out.shape[0])))
                    file.close()
                    print("File written to disk: %s \n"%self.FILE_NAME)
                except:
                    raise Exception("CrossSec: The data could not be dumped onto the specified file!\n")




        return calculated_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxf1f2()
    w.show()
    app.exec()
    w.saveSettings()
