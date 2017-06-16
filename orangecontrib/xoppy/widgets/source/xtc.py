import sys,os
import numpy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

class OWxtc(XoppyWidget):
    name = "TC"
    id = "orange.widgets.dataxtc"
    description = "Undulator Tuning Curves"
    icon = "icons/xoppy_xtc.png"
    priority = 7
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

    inputs = WidgetDecorator.syned_input_data()

    def build_gui(self):

        self.IMAGE_WIDTH = 850

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ENERGY = oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_CURRENT = oasysgui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ENERGY_SPREAD = oasysgui.lineEdit(box1, self, "ENERGY_SPREAD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGX = oasysgui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGY = oasysgui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGX1 = oasysgui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_SIGY1 = oasysgui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_PERIOD = oasysgui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_NP = oasysgui.lineEdit(box1, self, "NP",
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
        return 'tc'

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

    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:
                self.view_type_combo.setEnabled(False)


                xoppy_data_harmonics = calculated_data.get_content("xoppy_data_harmonics")

                titles = self.getTitles()
                xtitles = self.getXTitles()
                ytitles = self.getYTitles()

                progress_bar_step = (100-progressBarValue)/len(titles)

                for index in range(0, len(titles)):
                    x_index, y_index = self.getVariablesToPlot()[index]
                    log_x, log_y = self.getLogPlot()[index]

                    if not self.plot_canvas[index] is None:
                        self.plot_canvas[index].clear()

                    try:
                        for h_index in range(0, len(xoppy_data_harmonics)):

                            self.plot_histo(xoppy_data_harmonics[h_index][1][:, x_index],
                                            xoppy_data_harmonics[h_index][1][:, y_index],
                                            progressBarValue + ((index+1)*progress_bar_step),
                                            tabs_canvas_index=index,
                                            plot_canvas_index=index,
                                            title=titles[index],
                                            xtitle=xtitles[index],
                                            ytitle=ytitles[index],
                                            log_x=log_x,
                                            log_y=log_y,
                                            harmonic=xoppy_data_harmonics[h_index][0],
                                            control=True)

                        self.plot_canvas[index].addCurve(numpy.zeros(1),
                                                         numpy.array([max(xoppy_data_harmonics[h_index][1][:, y_index])]),
                                                         "Click on curve to highlight it",
                                                         xlabel=xtitles[index], ylabel=ytitles[index],
                                                         symbol='', color='white')

                        self.plot_canvas[index].setActiveCurve("Click on curve to highlight it")
                        self.plot_canvas[index].getLegendsDockWidget().setFixedHeight(150)
                        self.plot_canvas[index].getLegendsDockWidget().setVisible(True)

                        self.tabs.setCurrentIndex(index)
                    except Exception as e:
                        self.view_type_combo.setEnabled(True)

                        raise Exception("Data not plottable: bad content\n" + str(e))


                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="",
                   log_x=False, log_y=False, harmonic=1, color='blue', control=True):
        h_title = "Harmonic " + str(harmonic)

        hex_r = hex(min(255, 128 + harmonic*10))[2:].upper()
        hex_g = hex(min(255, 20 + harmonic*15))[2:].upper()
        hex_b = hex(min(255, harmonic*10))[2:].upper()
        if len(hex_r) == 1: hex_r = "0" + hex_r
        if len(hex_g) == 1: hex_g = "0" + hex_g
        if len(hex_b) == 1: hex_b = "0" + hex_b

        super().plot_histo(x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, h_title, xtitle, ytitle,
                           log_x, log_y, color="#" + hex_r + hex_g + hex_b, replace=False, control=control)

        self.plot_canvas[plot_canvas_index].setGraphTitle(title)
        self.plot_canvas[plot_canvas_index].setDefaultPlotLines(True)
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
        return[(False, True), (False, False), (False, False), (False, False)]

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

        command = "'" + os.path.join(locations.home_bin(), 'tc') + "'"
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
        # for line in lines:
        #     print(line, end="")


        # remove returns
        lines = [line[:-1] for line in lines]
        harmonics_data = []

        # separate numerical data from text
        floatlist = []
        harmoniclist = []
        txtlist = []
        for line in lines:
            try:
                tmp = line.strip()

                if tmp.startswith("Harmonic"):
                    harmonic_number = int(tmp.split("Harmonic")[1].strip())

                    if harmonic_number != self.HARMONIC_FROM:
                        harmonics_data[-1][1] = harmoniclist
                        harmoniclist = []

                    harmonics_data.append([harmonic_number, None])

                tmp = float(line.strip()[0])

                floatlist.append(line)
                harmoniclist.append(line)
            except:
                txtlist.append(line)

        harmonics_data[-1][1] = harmoniclist

        data = numpy.loadtxt(floatlist)

        for index in range(0, len(harmonics_data)):
            # print (harmonics_data[index][0], harmonics_data[index][1])
            harmonics_data[index][1] = numpy.loadtxt(harmonics_data[index][1])

        #send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", data)
            calculated_data.add_content("xoppy_data_harmonics", harmonics_data)
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

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data._light_source._magnetic_structure, synedid.InsertionDevice):
                light_source = data._light_source

                self.ENERGY = light_source._electron_beam._energy_in_GeV
                self.ENERGY_SPREAD = light_source._electron_beam._energy_spread
                self.CURRENT = 1000.0 * light_source._electron_beam._current

                x, xp, y, yp = light_source._electron_beam.get_sigmas_all()

                self.SIGX = 1e3 * x
                self.SIGY = 1e3 * y
                self.SIGX1 = 1e3 * xp
                self.SIGY1 = 1e3 * yp
                self.PERIOD = 100.0 * light_source._magnetic_structure._period_length
                self.NP = light_source._magnetic_structure._number_of_periods

                self.set_enabled(False)

            else:
                self.set_enabled(True)
                # raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)
            # raise ValueError("Syned data not correct")



    def set_enabled(self,value):
        if value == True:
                self.id_ENERGY.setEnabled(True)
                self.id_ENERGY_SPREAD.setEnabled(True)
                self.id_SIGX.setEnabled(True)
                self.id_SIGX1.setEnabled(True)
                self.id_SIGY.setEnabled(True)
                self.id_SIGY1.setEnabled(True)
                self.id_CURRENT.setEnabled(True)
                self.id_PERIOD.setEnabled(True)
                self.id_NP.setEnabled(True)
        else:
                self.id_ENERGY.setEnabled(False)
                self.id_ENERGY_SPREAD.setEnabled(False)
                self.id_SIGX.setEnabled(False)
                self.id_SIGX1.setEnabled(False)
                self.id_SIGY.setEnabled(False)
                self.id_SIGY1.setEnabled(False)
                self.id_CURRENT.setEnabled(False)
                self.id_PERIOD.setEnabled(False)
                self.id_NP.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtc()
    w.show()
    app.exec()
    w.saveSettings()
