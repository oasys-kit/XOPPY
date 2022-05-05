import sys
import numpy
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from xoppylib.sources.xoppy_bm_wiggler import xoppy_calc_wigg

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
import syned.storage_ring.magnetic_structures.insertion_device as synedid

class OWxwiggler(XoppyWidget,WidgetDecorator):
    name = "WIGGLER"
    id = "orange.widgets.dataxwiggler"
    description = "Wiggler Spectrum (Full Emission)"
    icon = "icons/xoppy_xwiggler.png"
    priority = 9
    category = ""
    keywords = ["xoppy", "xwiggler"]

    FIELD = Setting(0)
    NPERIODS = Setting(12)
    ULAMBDA = Setting(0.125)
    K = Setting(14.0)
    ENERGY = Setting(6.04)
    PHOT_ENERGY_MIN = Setting(100.0)
    PHOT_ENERGY_MAX = Setting(100100.0)
    NPOINTS = Setting(100)
    NTRAJPOINTS = Setting(101)
    CURRENT = Setting(200.0)
    FILE = Setting("?")

    inputs = WidgetDecorator.syned_input_data()

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_FIELD = gui.comboBox(box1, self, "FIELD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Sinusoidal', 'B from file', 'B from harmonics'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_NPERIODS = oasysgui.lineEdit(box1, self, "NPERIODS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ULAMBDA = oasysgui.lineEdit(box1, self, "ULAMBDA",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_K = oasysgui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_ENERGY = oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHOT_ENERGY_MIN",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHOT_ENERGY_MAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "NTRAJPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.id_CURRENT = oasysgui.lineEdit(box1, self, "CURRENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 

        box1 = gui.widgetBox(box)

        file_box = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file = oasysgui.lineEdit(file_box, self, "FILE",
                                         label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.button(file_box, self, "...", callback=self.selectFile)

    def unitLabels(self):
         return ['Magnetic field: ','Number of periods','Wiggler period [m]','K value','Beam energy [GeV]',
                 'Min Photon Energy [eV]','Max Photon Energy [eV]','Number of energy points',
                 'Number of traj points per period','Electron Beam Current [mA]','File/Url with Magnetic Field']

    def unitFlags(self):
         return ['True','True','self.FIELD  !=  1','self.FIELD  ==  0','True',
                 'True','True','True',
                 'self.FIELD  !=  1','True','self.FIELD  !=  0']

    def selectFile(self):
        self.le_file.setText(oasysgui.selectFileFromDialog(self, self.FILE, "Open B File"))

    def get_help_name(self):
        return 'wiggler'

    def check_fields(self):
        self.NPERIODS = congruence.checkStrictlyPositiveNumber(self.NPERIODS, "Number of Periods")
        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Beam Energy")
        self.PHOT_ENERGY_MIN = congruence.checkPositiveNumber(self.PHOT_ENERGY_MIN, "Min Photon Energy")
        self.PHOT_ENERGY_MAX = congruence.checkStrictlyPositiveNumber(self.PHOT_ENERGY_MAX, "Max Photon Energy")
        congruence.checkLessThan(self.PHOT_ENERGY_MIN, self.PHOT_ENERGY_MAX, "Min Photon Energy", "Max Photon Energy")
        self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.NPOINTS, "Number of Energy Points")
        self.CURRENT = congruence.checkStrictlyPositiveNumber(self.CURRENT, "Electron Beam Current")

        if self.FIELD == 0:
            self.ULAMBDA = congruence.checkStrictlyPositiveNumber(self.ULAMBDA, "Wiggler period")
            self.K = congruence.checkStrictlyPositiveNumber(self.K, "K")
            self.NTRAJPOINTS = congruence.checkStrictlyPositiveNumber(self.NTRAJPOINTS, "Number of traj points per period")
        elif self.FIELD == 1:
            self.ULAMBDA = congruence.checkStrictlyPositiveNumber(self.ULAMBDA, "Wiggler period")
            self.NTRAJPOINTS = congruence.checkStrictlyPositiveNumber(self.NTRAJPOINTS, "Number of traj points per period")
            congruence.checkUrl(self.FILE)
        elif self.FIELD == 2:
            congruence.checkUrl(self.FILE)


    def do_xoppy_calculation(self):
        e, f0, p0, cumulated_power, traj, traj_info =  xoppy_calc_wigg(
            FIELD=self.FIELD,
            NPERIODS=self.NPERIODS,
            ULAMBDA=self.ULAMBDA,
            K=self.K,
            ENERGY=self.ENERGY,
            PHOT_ENERGY_MIN=self.PHOT_ENERGY_MIN,
            PHOT_ENERGY_MAX=self.PHOT_ENERGY_MAX,
            NPOINTS=self.NPOINTS,
            NTRAJPOINTS=self.NTRAJPOINTS,
            CURRENT=self.CURRENT,
            FILE=self.FILE)

        # write python script in standard output
        dict_parameters = {
            "FIELD"           : self.FIELD,
            "NPERIODS"        : self.NPERIODS,
            "ULAMBDA"         : self.ULAMBDA,
            "K"               : self.K,
            "ENERGY"          : self.ENERGY,
            "PHOT_ENERGY_MIN" : self.PHOT_ENERGY_MIN,
            "PHOT_ENERGY_MAX" : self.PHOT_ENERGY_MAX,
            "NPOINTS"         : self.NPOINTS,
            "NTRAJPOINTS"     : self.NTRAJPOINTS,
            "CURRENT"         : self.CURRENT,
            "FILE"            : self.FILE,
            }

        script = self.script_template().format_map(dict_parameters)

        self.xoppy_script.set_code(script)




        return e, f0, p0 , cumulated_power, traj, traj_info, script

    def script_template(self):
        return """
#
# script to make the calculations (created by XOPPY:wiggler)
#
from xoppylib.sources.xoppy_bm_wiggler import xoppy_calc_wigg
energy, flux, spectral_power, cumulated_power, traj, traj_info =  xoppy_calc_wigg(
    FIELD={FIELD},
    NPERIODS={NPERIODS},
    ULAMBDA={ULAMBDA},
    K={K},
    ENERGY={ENERGY},
    PHOT_ENERGY_MIN={PHOT_ENERGY_MIN},
    PHOT_ENERGY_MAX={PHOT_ENERGY_MAX},
    NPOINTS={NPOINTS},
    NTRAJPOINTS={NTRAJPOINTS},
    CURRENT={CURRENT},
    FILE="{FILE}")

#
# example plot
#
from srxraylib.plot.gol import plot
plot(energy,flux,
    xtitle="Photon energy [eV]",ytitle="Flux [photons/s/o.1%bw]",title="Wiggler Flux",
    xlog=True,ylog=True,show=False)
plot(energy,spectral_power,
    xtitle="Photon energy [eV]",ytitle="Power [W/eV]",title="Wiggler Spectral Power",
    xlog=True,ylog=True,show=False)
plot(energy,cumulated_power,
    xtitle="Photon energy [eV]",ytitle="Cumulated Power [W]",title="Wiggler Cumulated Power",
    xlog=False,ylog=False,show=True)
#
# end script
#
"""



    def extract_data_from_xoppy_output(self, calculation_output):
        e, f, sp, cumulated_power, traj, traj_info, script = calculation_output

        data = numpy.zeros((len(e), 4))
        data[:,0] = numpy.array(e)
        data[:,1] = numpy.array(f)
        data[:,2] = numpy.array(sp)
        data[:,3] = numpy.array(cumulated_power)

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", data)
        calculated_data.add_content("xoppy_traj", traj.T)
        calculated_data.add_content("xoppy_script", script)

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "XWIGGLER"

    def getTitles(self):
        return ['Flux', 'Spectral Power', 'Cumulated Power', 'e trajectory', 'e velocity', 'B field']

    def getXTitles(self):
        return ["Energy [eV]", "Energy [eV]", "Energy [eV]", "s [m]", "s [m]", "s [m]"]

    def getYTitles(self):
        return ["Flux [Phot/sec/0.1%bw]", "Spectral Power [W/eV]", "Cumulated Power [W]", "x [m]", "beta_x [m]", "B [T]"]

    def getLogPlot(self):
        return [(True, True), (True, True), (False, False), (False, False), (False, False), (False, False)]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2), (0,3), (1,0), (1,3), (1,7)]

    def getTagToPlot(self):
        return ["xoppy_data", "xoppy_data", "xoppy_data", "xoppy_traj", "xoppy_traj", "xoppy_traj"]


    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data._light_source._magnetic_structure, synedid.InsertionDevice):
                light_source = data._light_source

                self.NPERIODS = int(light_source._magnetic_structure._number_of_periods)
                self.ENERGY = light_source._electron_beam._energy_in_GeV
                self.CURRENT = 1e3*light_source._electron_beam._current
                self.ULAMBDA = light_source._magnetic_structure._period_length
                self.K = light_source._magnetic_structure._K_vertical
                self.FIELD = 0

                self.set_enabled(False)

            else:
                self.set_enabled(True)
        else:
            self.set_enabled(True)

    def set_enabled(self,value):
        if value == True:
                self.id_NPERIODS.setEnabled(True)
                self.id_ENERGY.setEnabled(True)
                self.id_CURRENT.setEnabled(True)
                self.id_ULAMBDA.setEnabled(True)
                self.id_K.setEnabled(True)
                self.id_FIELD.setEnabled(True)
        else:
                self.id_NPERIODS.setEnabled(False)
                self.id_ENERGY.setEnabled(False)
                self.id_CURRENT.setEnabled(False)
                self.id_ULAMBDA.setEnabled(False)
                self.id_K.setEnabled(False)
                self.id_FIELD.setEnabled(False)

    # extended this method here to also plot data from trajectories
    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:
                current_index = self.tabs.currentIndex()

                self.view_type_combo.setEnabled(False)



                titles = self.getTitles()
                xtitles = self.getXTitles()
                ytitles = self.getYTitles()
                tags = self.getTagToPlot()

                progress_bar_step = (100-progressBarValue)/len(titles)

                for index in range(0, len(titles)):

                    xoppy_data = calculated_data.get_content(tags[index])

                    x_index, y_index = self.getVariablesToPlot()[index]
                    log_x, log_y = self.getLogPlot()[index]

                    try:
                        self.plot_histo(xoppy_data[:, x_index],
                                        xoppy_data[:, y_index],
                                        progressBarValue + ((index+1)*progress_bar_step),
                                        tabs_canvas_index=index,
                                        plot_canvas_index=index,
                                        title=titles[index],
                                        xtitle=xtitles[index],
                                        ytitle=ytitles[index],
                                        log_x=log_x,
                                        log_y=log_y)

                        # self.tabs.setCurrentIndex(index)
                    except Exception as e:
                        self.view_type_combo.setEnabled(True)

                        raise Exception("Data not plottable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)

                try:
                    self.tabs.setCurrentIndex(current_index)
                except:
                    if self.getDefaultPlotTabIndex() == -1:
                        self.tabs.setCurrentIndex(len(titles) - 1)
                    else:
                        self.tabs.setCurrentIndex(self.getDefaultPlotTabIndex())


            else:
                raise Exception("Empty Data")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxwiggler()

    # # external:
    # w.FIELD = 1
    # w.NPERIODS = 1
    # w.ENERGY = 6.0
    # w.PHOT_ENERGY_MIN = 100.0
    # w.PHOT_ENERGY_MAX = 100100.0
    # w.NPOINTS = 100
    # w.NTRAJPOINTS = 101
    # w.CURRENT = 200.0
    # w.FILE = "http://ftp.esrf.fr/pub/scisoft/syned/resources/SW_3P.txt"

    w.show()
    app.exec()
    w.saveSettings()


    # e, f0, p0, cumulated_power = xoppy_calc_wigg(
    #     FIELD=1,
    #     NPERIODS=1,
    #     ULAMBDA=1.0,
    #     K=1.0,
    #     ENERGY=6.0,
    #     PHOT_ENERGY_MIN=100.0,
    #     PHOT_ENERGY_MAX=100100.0,
    #     NPOINTS=200,
    #     NTRAJPOINTS=101,
    #     CURRENT=200.0,
    #     FILE="http://ftp.esrf.fr/pub/scisoft/syned/resources/SW_3P.txt")



